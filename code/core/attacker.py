from .node import CANNode
from .can_frame import CANFrame

class WeepingAttacker(CANNode):
    def __init__(self, name, target_period, skip_strategy):
        super().__init__(name, 0) 
        self.target_period = target_period
        
        self.skip_strategy = skip_strategy  
        self.skip_counter = 0
        
        self.last_seen_time = None
        self.sync_locked = False

    def sync_with_bus(self, frame, current_time):
        if frame.can_id == 0x10:
            if self.last_seen_time is not None:
                delta = current_time - self.last_seen_time
                if abs(delta - self.target_period) <= 1:
                    self.sync_locked = True
            self.last_seen_time = current_time

    def predict_window(self, current_time):
        if not self.sync_locked or self.last_seen_time is None:
            return False
        expected_time = self.last_seen_time + self.target_period
        return abs(current_time - expected_time) <= 1

    def attempt_attack(self, victim_frame):
        if self.state == "BUS_OFF":
            return "BUS_OFF", None, -1

        # Logica Skipping
        if self.skip_counter < self.skip_strategy:
            self.skip_counter += 1
            return "SKIPPING", None, -1
        
        self.skip_counter = 0
        attack_frame, bit_pos = CANFrame.create_attack_frame(victim_frame)
        
        if attack_frame is None:
            return "IMPOSSIBLE", None, -1
            
        return "ATTACKING", attack_frame, bit_pos

    def recover_tec(self):
        if self.state != "BUS_OFF":
            self.event_transmit_success()