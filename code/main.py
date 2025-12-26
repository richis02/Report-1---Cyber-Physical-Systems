import csv
import random
import matplotlib.pyplot as plt
from dataclasses import asdict

from core.node import CANNode
from core.attacker import WeepingAttacker
from core.can_frame import CANFrame
from simulation import visualize_collision
from config import SimulationConfig, CURRENT_CONFIG

def run_simulation(config: SimulationConfig, show_physics=False):
    if config.random_seed is not None:
        random.seed(config.random_seed)
        
    victim = CANNode("Victim", transmit_period_ms=config.victim_period_ms)
    attacker = WeepingAttacker("Attacker", target_period=config.victim_period_ms, 
                               skip_strategy=config.skip_strategy)
    
    random_data = [random.randint(0, 255) for _ in range(8)]
    
    log_file = open(config.log_file, 'w', newline='')
    csv_writer = csv.writer(log_file, delimiter=';')
    csv_writer.writerow(['Time_ms', 'Victim_TEC', 'Attacker_TEC', 'Victim_State', 'Action', 'Bus_Status'])

    tec_history_v = []
    tec_history_a = []
    bus_off_reached = False

    victim_retx_pending = False  
    attacker_msg_queue = 0       

    print(f"--- START SIMULATION (Skip={config.skip_strategy}) ---")

    for time_ms in range(config.duration_ms):
        
        step_action = "IDLE"
        bus_status = "FREE"

        if victim.state == "BUS_OFF":
            if not bus_off_reached:
                print(f"!!! VICTIM WENT BUS-OFF @ {time_ms}ms !!!")
                step_action = "VICTIM_KILLED"
                bus_off_reached = True
            
            if attacker_msg_queue > 0:
                attacker.recover_tec()
                attacker_msg_queue -= 1
            
            csv_writer.writerow([time_ms, victim.tec, attacker.tec, "BUS_OFF", step_action, "SILENCE"])
            tec_history_v.append(victim.tec)
            tec_history_a.append(attacker.tec)
            continue

        is_periodic_time = (time_ms > 0 and time_ms % victim.period == 0)
        victim_wants_to_send = is_periodic_time or victim_retx_pending

        if victim_wants_to_send:
            bus_status = "VICTIM_TX"
            v_frame = CANFrame(config.victim_id, random_data)
            
            is_attack_window = attacker.predict_window(time_ms)

            should_attack = is_attack_window and not victim_retx_pending
            
            attack_decision = "IDLE"
            if should_attack:
                 attack_decision, a_frame, bit_idx = attacker.attempt_attack(v_frame)
            
            if attack_decision == "ATTACKING":
                step_action = "ATTACK_COLLISION"
                
                victim.event_transmit_error()
                attacker.event_transmit_error()
                
                if show_physics:
                    visualize_collision(v_frame, a_frame, bit_idx)

                victim_retx_pending = True     
                attacker_msg_queue += config.recovery_count 
                
            elif attack_decision == "SKIPPING":
                step_action = "SKIPPING_TX"
                
                victim.event_transmit_success()
                victim_retx_pending = False    
                
                attacker_msg_queue += config.recovery_count

            elif attack_decision == "IMPOSSIBLE":
                step_action = "ATTACK_FAIL_DATA"
                victim.event_transmit_success()
                victim_retx_pending = False
                attacker_msg_queue += config.recovery_count

            else:
                if victim_retx_pending:
                    step_action = "VICTIM_RETRANSMIT_SUCCESS"
                else:
                    step_action = "VICTIM_PERIODIC_SUCCESS"
                    
                victim.event_transmit_success()
                victim_retx_pending = False 

            if not victim_retx_pending: 
                attacker.sync_with_bus(v_frame, time_ms)

        else:
            if attacker_msg_queue > 0:
                bus_status = "ATTACKER_BG_TX"
                step_action = "ATTACKER_RECOVERY"
                
                attacker.recover_tec() 
                attacker_msg_queue -= 1 
            else:
                bus_status = "IDLE"

        csv_writer.writerow([time_ms, victim.tec, attacker.tec, victim.state, step_action, bus_status])
        
        tec_history_v.append(victim.tec)
        tec_history_a.append(attacker.tec)

    log_file.close()
    return tec_history_v, tec_history_a

if __name__ == "__main__":

    tec_v, tec_a = run_simulation(CURRENT_CONFIG, show_physics=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(tec_v, label='Victim TEC')
    plt.plot(tec_a, label='Attacker TEC')
    plt.axhline(255, color='r', linestyle='--', label='Bus-Off Threshold')
    
    plt.title(f'WeepingCAN Simulation\n(Skip={CURRENT_CONFIG.skip_strategy}, Recovery={CURRENT_CONFIG.recovery_count})')
    plt.xlabel('Time (ms)')
    plt.ylabel('TEC Value')
    plt.legend()
    plt.grid()
    plt.show()