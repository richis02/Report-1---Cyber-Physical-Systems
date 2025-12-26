from dataclasses import dataclass

@dataclass
class SimulationConfig:
    # --- Parametri Generali ---
    duration_ms: int = 2000          
    log_file: str = "simulation.csv" 
    random_seed: int = None          
    
    # --- Parametri Vittima ---
    victim_period_ms: int = 10       
    victim_id: int = 0x10            
    
    # --- Parametri Attaccante ---
    skip_strategy: int = 2           
    recovery_count: int = 2          

CURRENT_CONFIG = SimulationConfig(
    duration_ms = 500,         
    log_file = "file.csv",
    
    victim_period_ms = 10,
    
    skip_strategy = 3,          
    recovery_count = 3          
)