# WeepingCAN Attack Simulator 🚗💻

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## 📌 Overview

This project is a custom **Discrete Event Simulator (DES)** developed in Python to replicate the findings of the research paper **"WeepingCAN: A Stealthy CAN Bus-off Attack"**.

The simulator models the Controller Area Network (CAN) error handling mechanism and implements the specific **WeepingCAN** attack logic. It demonstrates how an attacker can force a victim ECU into a *Bus-off* state while remaining stealthy and avoiding detection by traditional Intrusion Detection Systems (IDS).

> **Course:** Cyber-Physical Systems and IoT Security  
> **Reference Paper:** [WeepingCAN: A Stealthy CAN Bus-off Attack](https://dx.doi.org/10.14722/autosec.2021.23002) (AutoSec 2021).

---

## 🎯 Objectives

The main goal is to demonstrate the feasibility of the WeepingCAN attack using a software-only approach, validating the theoretical models presented in the paper. Key objectives include:

1. **CAN State Machine Modeling:** Simulating the transitions between *Error-Active*, *Error-Passive*, and *Bus-off* states based on TEC/REC counters as defined in the CAN standard.
2. **WeepingCAN Logic Implementation:** Implementing the four critical differences that distinguish WeepingCAN from a traditional Bus-off attack:
   * (i) Disabling retransmission of the attack message.
   * (ii) Injecting recessive bit errors.
   * (iii) Eliminating the need for fabricated preceded messages.
   * (iv) Randomizing bit error injection.
3. **Skipping Strategy Validation:** Demonstrating how skipping attack cycles (k) allows the attacker to recover their TEC and evade detection.

---

## 📂 Project Structure

```text
weeping-can-sim/
│
├── core/                   # Core simulation logic
│   ├── node.py             # Generic CAN Node (TEC/REC state machine)
│   ├── attacker.py         # WeepingAttacker logic (Skipping, Sync)
│   └── can_frame.py        # Physical layer abstraction (Bit manipulation)
│
├── config.py               # Central configuration file (Simulation parameters)
├── main.py                 # Main simulation engine (Time-loop & Queue logic)
├── simulation.py           # Visualization helper (Console bit-collision output)
│
├── README.md               # This file
└── requirements.txt        # Dependencies
```

---

## 🚀 Installation & Usage

### 1. Prerequisites
Ensure you have Python 3 installed. You will need `matplotlib` for generating the graphs.

```bash
pip install matplotlib
```

### 2. Running a Single Simulation
To run a specific scenario (defined in `config.py`), execute:

```bash
python main.py
```

*This will run the simulation, print the physical bit-collision analysis to the console, and generate a plot for the currently configured scenario.*

---

## ⚙️ Configuration

All simulation parameters are managed in `config.py`. You can modify the `CURRENT_CONFIG` object to test different attack strategies without changing the core code.

```python
# config.py example
CURRENT_CONFIG = SimulationConfig(
    duration_ms = 3500,        # Duration of the simulation
    victim_period_ms = 10,     # Victim's transmission period (Tv)

    # Critical Attack Parameters
    skip_strategy = 2,         # k: Number of cycles to skip (2=Aggressive, 5/6=Stealth)
    recovery_count = 2         # m'_T: Messages sent by attacker to recover TEC
)
```

---

## 📊 Results and Theoretical Validation

The simulator successfully validates the stability condition derived in Equation 1 of the paper:

$$
\exists v \in M_\mathcal{V}\;s.t.\;8>\sum_{m'\in M_\mathcal{V}}\frac{v_T}{m'_T}<\sum_{m\in M_\mathcal{A}}\frac{v_T}{m_T}
$$

### Key Findings:
* **Aggressive Attack (Skip 2):** The victim is forced into Bus-off quickly (~1.5s), but the attacker's TEC rises, reducing stealth.
* **Stealth Attack (Skip 6):** The victim accumulates errors slowly. The extended skip interval allows the attacker to transmit sufficient background traffic to keep its TEC near zero, remaining virtually invisible.
