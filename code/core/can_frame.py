import random

class CANFrame:
    def __init__(self, can_id, data_bytes):
        self.can_id = can_id
        self.data = data_bytes 

    def to_bit_string(self):
        bits = f"{self.can_id:011b}"
        for byte in self.data:
            bits += f"{byte:08b}"
        return bits

    @staticmethod
    def create_attack_frame(victim_frame):
        attack_data = list(victim_frame.data)
        
        victim_bits = victim_frame.to_bit_string()
        header_len = 11  
        dominant_indices = []

        data_bits = victim_bits[header_len:]
        for i, bit in enumerate(data_bits):
            if bit == '0':
                dominant_indices.append(i)

        if not dominant_indices:
            return None, -1

        target_bit_index = random.choice(dominant_indices)

        byte_idx = target_bit_index // 8
        bit_offset = 7 - (target_bit_index % 8)
        
        attack_data[byte_idx] |= (1 << bit_offset)

        attack_frame = CANFrame(victim_frame.can_id, attack_data)
        
        return attack_frame, (header_len + target_bit_index)