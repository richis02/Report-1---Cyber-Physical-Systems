class CANNode:
    def __init__(self, name, transmit_period_ms):
        self.name = name
        self.period = transmit_period_ms
        
        self.tec = 0  
        self.state = "ERROR_ACTIVE" 
        
        self.history_tec = []

    def log_status(self):
        self.history_tec.append(self.tec)

    def _update_state_machine(self):
        # Active -> Passive
        if self.tec > 127 and self.state == "ERROR_ACTIVE":
            self.state = "ERROR_PASSIVE"
        
        # Passive -> Bus-off
        if self.tec > 255:
            self.state = "BUS_OFF"
        
        # Recovery 
        if self.tec < 128 and self.state == "ERROR_PASSIVE":
            self.state = "ERROR_ACTIVE"

    def event_transmit_success(self):
        # Successo: TEC -1
        if self.state == "BUS_OFF": return
        if self.tec > 0:
            self.tec -= 1
        self._update_state_machine()

    def event_transmit_error(self):
        # Errore in trasmissione: TEC +8
        if self.state == "BUS_OFF": return
        self.tec += 8
        self._update_state_machine()