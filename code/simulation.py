def visualize_collision(victim_frame, attack_frame, bit_error_index):
    v_bits = victim_frame.to_bit_string()
    a_bits = attack_frame.to_bit_string()
    
    print(f"\nCollision Analysis @ Bit {bit_error_index}")
    print(f"Victim:          {v_bits}")
    
    marker = ""
    for i in range(len(v_bits)):
        if i == bit_error_index:
            marker += "^"
        else:
            marker += " "
            
    print(f"Attacker:        {a_bits}")
    print(f"Collision Point: {marker}")
    print("Result: Attacker detects Bit Error -> Sends Error Flag.\n")