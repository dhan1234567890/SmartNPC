# Fuzzy Logic Decision NPCs (SmartNPC)

An adaptive Non-Player Character (NPC) decision framework built in Python and Pygame for evaluating AI decision-making architectures.

---

## 🎯 Project Vision & Objective

The objective of this project is to evaluate and compare how different decision-making paradigms influence NPC behavior in a 2D game environment.

Rather than showcasing a single AI implementation, this framework directly compares traditional hard-coded and state-based approaches against **Fuzzy Logic reasoning** to answer the core research question:

> **Does Fuzzy Logic produce smarter, more realistic, and challenging NPC behavior than conventional decision-making approaches?**

---

## 🏗️ AI Architectures to Implement

1. **Version 1 — Rule-Based System**:
   - Baseline hard-coded conditional rules (`If health < 30% retreat; else attack`).
2. **Version 2 — Finite State Machine (FSM)**:
   - Classic game AI industry approach using state transitions (`Idle`, `Patrol`, `Chase`, `Attack`, `Retreat`, `Search`).
3. **Version 3 — Fuzzy Logic Engine**:
   - Continuous reasoning based on multi-variable inputs (Health, Distance, Ammo/Stamina) mapped through membership functions to derive gradual behavioral outputs (Aggression Level, Retreat Urgency, Attack Confidence).

---

## 🎮 Features & Environment

- **Top-Down 2D Warehouse Arena**: Built with Pygame featuring obstacle cartons and goal zones.
- **Player Controls**: Smooth WASD top-down navigation with collision detection and boundary locking.
- **Real-Time AI Visualization Panel**: Live telemetry rendering NPC membership functions and active decision states.
- **Quantitative Comparison Framework**: Automated metrics collection (survival time, engagement distance, win rates, state oscillation counts).

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+** installed on your system.

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dhan1234567890/SmartNPC.git
   cd SmartNPC
   ```

2. **Create and activate a virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the demo**:
   ```bash
   python main.py
   ```

---

## ⌨️ Controls

| Key | Action |
| :--- | :--- |
| **W / A / S / D** | Move Player Triangle |
| **ESC** | Exit Game |

---

## 📁 Directory Structure

```text
SmartNPC/
├── src/
│   ├── __init__.py
│   ├── settings.py       # Screen dimensions, colors, obstacle data
│   ├── player.py         # Player sprite, WASD movement & collision
│   ├── level.py          # Warehouse arena rendering & obstacles
│   └── game.py           # Pygame initialization & 60 FPS main loop
├── .gitignore            # Git exclusion rules
├── main.py               # Application entry point
├── requirements.txt      # Project dependencies (pygame, scikit-fuzzy, etc.)
└── README.md             # Project documentation
```

---

## 📊 Evaluation Metrics

The experimental framework records and compares:
- Average Survival Time
- Damage Dealt / Received
- Attack & Retreat Frequencies
- Average Engagement Distance
- Decision Change Oscillation Rate

---

## 👥 Authors & Collaborators

Developed for the **Artificial Intelligence (SEM-5)** Course Project.
