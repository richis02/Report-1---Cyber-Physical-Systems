# WeepingCAN Attack Simulator 🚗💻

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Research_Prototype-orange)

## 📌 Overview

This project is a custom **Discrete Event Simulator (DES)** developed in Python to replicate the findings of the research paper **"WeepingCAN: A Stealthy CAN Bus-off Attack"** (Bloom et al., AutoSec 2021).

The simulator models the Controller Area Network (CAN) error handling mechanism and implements the specific **WeepingCAN** attack logic, demonstrating how an attacker can force a victim ECU into a *Bus-off* state while remaining stealthy and avoiding detection by traditional IDSs.

> **Course:** Cyber-Physical Systems and IoT Security  
> **Reference Paper:** [WeepingCAN: A Stealthy CAN Bus-off Attack]

## 🎯 Objectives

The main goal is to demonstrate the feasibility of the WeepingCAN attack using a software-only approach. Key objectives include:
- **CAN State Machine:** Simulating transitions (Error-Active $\rightarrow$ Error-Passive $\rightarrow$ Bus-off) based on TEC counters.
- **WeepingCAN Logic:** Implementing the critical attack features:
  - Disabling retransmission of the attack message.
  - Recessive bit injection on dominant bits.
  - **Skipping Strategy** for stealthiness.
- **Validation:** Reproducing the experimental results (TEC progression graphs) presented in the original paper (Fig. 3).

## 📂 Project Structure

```text
weeping-can-sim/
│
├── core/                   # Core simulation logic
│   ├── __init__.py
│   ├── node.py             # Generic CAN Node (TEC/REC logic)
│   ├── attacker.py         # WeepingAttacker logic (Skipping, Sync)
│   └── can_frame.py        # Physical layer abstraction (Bit manipulation)
│
├── config.py               # Central configuration file (Simulation parameters)
├── main.py                 # Main simulation engine (Time-loop, Queue logic)
├── reproduce_fig3.py       # Script to generate the comparative grid plot (Skip 2-6)
├── simulation.py           # Helper for visualization (CLI output)
│
├── README.md               # This file
└── requirements.txt        # Dependencies

## 🚀 Installation
