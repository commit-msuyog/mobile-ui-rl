# Mobile UI RL Environment

A lightweight, symbolic Reinforcement Learning (RL) environment that simulates interacting with a mobile application. 

Designed for rapid prototyping and educational purposes, this project bypasses the heavy overhead of real Android emulators (like Appium or OCR). Instead, it provides a clean, symbolic UI where an agent receives text-based instructions and executes simple structured actions to reach a goal.

---

## Core Concept

The mock application consists of four primary screens: **Home**, **Notes**, **Settings**, and **Profile**. 

An agent navigates and interacts with the app using four distinct actions:
* `tap` (requires a target element)
* `type` (requires a target input and text string)
* `back` (navigates to the previous screen)
* `finish` (ends the episode)

**The Interaction Loop:**
1. **Task Given:** e.g., *"Create a note titled 'Buy milk'"*
2. **Step:** The agent outputs an action.
3. **Environment Update:** The environment validates the action, updates the mock state (current screen, active notes, step count), and evaluates the goal.
4. **Reward:** A reward is calculated and returned alongside the new state.

##  Reward System

The environment is designed to teach an agent to complete tasks quickly, safely, and accurately using a mix of sparse and shaped rewards:

* **Task Success:** The primary reward (scaled between 0 and 1) is sparse. It is only awarded if the specific task goal is achieved.
* **Efficiency Bonus:** If the task is successful, a small bonus is added for completing it in fewer steps. *(Note: Failed tasks receive no efficiency bonus to prevent reward hacking).*
* **Penalties:** Points are deducted for invalid actions (e.g., trying to tap a button that isn't on the current screen) and safety violations (e.g., triggering an unsafe logout action).

## Task Dataset

The project ships with a built-in JSON dataset (`data/tasks.json`) containing **30 tasks** total:
* **20 Training Tasks**
* **10 Evaluation Tasks**

Each task defines a specific instruction, a target goal state, and a maximum step limit (`max_steps`). The environment will automatically terminate the episode if the task is completed, if the agent calls `finish`, or if the step limit is reached.

##  Quick Start

**1. Clone the repository**
```bash
git clone <repository-url>
cd mobile-ui-rl
```

**2. Set up a virtual environment**
```bash
python -m venv venv311

# Mac/Linux:
source venv311/bin/activate
# Windows PowerShell:
.\venv311\Scripts\Activate.ps1
```

**3. Install the project**
```bash
pip install -e .
```

**4. Run test suite**
```bash
pytest
```

**5. Run the evaluation baseline**
```bash
python run_eval.py
```
*Note: The current evaluation script runs a deterministic heuristic baseline. It acts as a sanity check to prove the environment handles states, valid actions, and rewards correctly (currently achieving a 100% success rate).*

##  Project Structure

```text
mobile-ui-rl/
├── mobile_ui_env/       # Core environment logic
│   ├── __init__.py
│   ├── env.py           # reset() and step() logic
│   ├── state.py
│   ├── actions.py
│   ├── dataset.py
│   └── rubric.py        # Reward and penalty calculations
├── data/
│   └── tasks.json       # Train/Eval dataset
├── tests/               # Pytest suite (13/13 passing)
│   ├── test_actions.py
│   ├── test_rewards.py
│   └── test_env.py
├── run_eval.py          # Baseline evaluation script
└── pyproject.toml
```

## 🗺️ Scope & Next Steps

This repository is currently a **24-hour MVP** focused on establishing a clean RL environment loop (State → Action → Reward). It intentionally excludes heavy dependencies like LLM-based action generation, distributed training, or pixel-level screenshot understanding.

**Future Roadmap:**
* Connect the environment logic to an actual Android Emulator using Accessibility Trees and UI hierarchies.
* Integrate with the **Verifiers** framework (`load_environment()`).
* Train a true RL agent to generalize across unseen UI layouts.