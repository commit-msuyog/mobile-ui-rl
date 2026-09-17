# Mobile UI RL Environment

A lightweight, symbolic reinforcement learning environment where an agent completes mobile UI tasks using structured actions (`tap`, `type`, `back`, `finish`).

## Overview

This project implements the core loop behind most RL environments — `Task → State → Action → State Change → Reward → Goal Check` — for a small mock mobile app instead of a real Android device. The mock app has four screens (**Home**, **Notes**, **Settings**, **Profile**), and an agent is given a natural-language task (e.g. *"Create a note titled 'Buy milk'"*) that it must complete using a fixed set of structured actions.

The goal of the project isn't to train a state-of-the-art agent — it's to build a correct, well-tested environment: one where states transition predictably, invalid actions are caught instead of crashing the episode, and rewards are computed consistently. That environment logic is the reusable part; a learned policy could be trained against it later (see [Future Improvements](#future-improvements)).

**What this demonstrates:** environment design for GUI-agent RL — state representation, action validation, goal checking, and reward shaping — without the overhead of a real emulator.

## Key Features

- Symbolic mobile UI environment with deterministic state transitions
- Structured, validated action space (`tap`, `type`, `back`, `finish`)
- Goal-based task completion checking
- Multi-component reward function (success, efficiency, invalid-action penalty, safety penalty)
- Deterministic heuristic baseline for evaluation (no trained model required)
- Separate train/eval task datasets
- Automated test suite (`pytest`)

## How the Environment Works

### State

The environment does not use pixels, screenshots, or accessibility trees. State is a small, deterministic symbolic representation:

- **Current screen** — `home`, `notes`, `settings`, or `profile`
- **App data** — saved notes and the current draft note content
- **System toggles** — focus mode and notification status
- **Episode metrics** — step count, invalid-action count, safety-violation count

This is enough information to drive transitions and check goals without the complexity of rendering a real UI.

### Action

Four structured actions make up the action space:

| Action | Description |
|---|---|
| `tap(target)` | Interacts with a specific UI element |
| `type(target, text)` | Inputs text into a specific field |
| `back()` | Returns to the previous screen |
| `finish()` | Manually ends the episode |

### Transition

On each step, the environment:

1. Checks whether the action is valid given the current screen and state
2. Applies the state update if valid, or flags it as invalid and penalizes it (without crashing)
3. Checks whether the task's goal condition is now met
4. Computes the reward for that step
5. Decides whether the episode continues or ends

### Goal / Termination

An episode ends when one of three conditions is met:

- **Goal reached** — the task's completion condition is satisfied
- **Agent finishes** — the agent calls `finish()`
- **Timeout** — the episode hits the task's `max_steps` limit

## Project Structure

```
mobile-ui-rl/
├── mobile_ui_env/
│   ├── __init__.py
│   ├── env.py          # Core environment: reset/step loop, transitions
│   ├── state.py         # Symbolic state representation
│   ├── actions.py        # Action definitions and validation
│   ├── dataset.py        # Task loading (train/eval split)
│   └── rubric.py         # Reward calculation and goal checking
├── data/
│   └── tasks.json         # Task definitions (train + eval)
├── tests/
│   ├── test_actions.py
│   ├── test_rewards.py
│   └── test_env.py
├── screenshots/            # Reference screenshots (dataset size, eval output)
├── run_eval.py             # Deterministic heuristic baseline runner
├── pyproject.toml
├── README.md
└── AI_USAGE.md
```

## Reward Design

The reward function combines a primary sparse signal with smaller shaping terms, deliberately structured to avoid rewarding the wrong behavior.

| Component | Type | Purpose |
|---|---|---|
| Success | Sparse, primary | Awarded only when the task's exact goal condition is met. Getting "closer" (opening the right screen, partially typing text) earns nothing on its own. |
| Efficiency | Bonus | A small bonus scaled by how few steps a *successful* episode took. |
| Invalid action | Penalty | Applied immediately when the agent attempts an action that isn't valid on the current screen. |
| Safety violation | Stronger penalty | Applied for explicitly unsafe actions (e.g. triggering a logout unintentionally). |

Success is the main signal by design — it's the only component that reflects whether the agent actually did what was asked. Everything else exists to discourage sloppy or harmful behavior along the way, not to replace the success signal.

One design detail worth calling out: the efficiency bonus is only ever added *after* a successful completion. Rewarding efficiency unconditionally would let an agent maximize reward by calling `finish()` immediately on step one without doing any work — the classic reward-hacking failure mode for step-count bonuses. Gating it on success closes that loophole.

## Task Dataset

Tasks live in `data/tasks.json` and are split into training and evaluation sets:

| Split | Task count |
|---|---|
| Train | 25 |
| Eval | 15 |
| **Total** | **40** |

The evaluation tasks are distinct task instances from training, but draw on the same goal types the environment currently supports (note creation, navigation, toggling settings, etc.) — this checks that the environment and heuristic generalize across task instances, not across genuinely new goal types.

## Baseline Evaluation

There is no trained RL policy in this repository. The current baseline (`run_eval.py`) is a **deterministic heuristic**: for each goal type, it maps to a predefined, known-valid action sequence and executes it. It exists to validate that the environment mechanics — state transitions, invalid-action handling, reward computation, goal checking — behave correctly end to end, not to demonstrate learning.

Running it against the evaluation set currently produces a **100% success rate**, since the heuristic always executes a valid path to each goal. This is a correctness check on the environment, not evidence of a trained or generalizing agent — a policy that had to *learn* the right action sequence, rather than have it hardcoded, would be a meaningfully different result.

## Testing

The project uses `pytest`. All **13 tests currently pass**, covering:

- Action creation and screen navigation
- Note-creation workflows
- Invalid-action handling
- Profile navigation and focus-mode toggling
- Reward calculation and safety penalties

## Example Task / Example Interaction

A representative task and the heuristic's action sequence for it:

**Task:** `"Create a note titled 'Buy milk'"`

```
1. tap(notes_icon)          # Home → Notes screen
2. tap(new_note_button)     # Open a blank note
3. type(title_field, "Buy milk")
4. tap(save_button)         # Goal condition met: note exists with this title
```

At step 4, the goal check passes, the episode terminates successfully, and the success + efficiency reward components are applied.

## Real Android / Emulator Mapping

This is a **future extension**, not something currently implemented. The symbolic design was chosen deliberately to keep the environment lightweight and iterate fast on the RL logic, but the interfaces are meant to be swappable:

| Symbolic (current) | Real Android (future) |
|---|---|
| Symbolic state dict | Accessibility tree (UI hierarchy XML), screenshots, OCR |
| `tap` / `type` / `back` / `finish` on symbolic targets | ADB or Appium commands against a real device/emulator |
| Hardcoded four-screen mock app | Arbitrary installed app |

The state and action interfaces are structured so this swap wouldn't require rewriting the reward or goal-checking logic — but the swap itself hasn't been built.

## Limitations

- The environment is fully symbolic — there is no real Android emulator, device, or app behind it.
- No learned RL policy has been trained; the only baseline is a deterministic heuristic.
- Goal verification is simplified (exact-match style checks against structured state), not the kind of fuzzy or vision-based verification a real UI would need.
- The task set is small and hand-crafted, not automatically generated or adversarially tested.

## Future Improvements

- Train a learned RL policy (e.g. against a framework like Verifiers / PRIME-RL) instead of relying on the heuristic baseline
- Action masking to constrain the action space to valid actions per state
- Richer observations (e.g. partial accessibility-tree-style structure) instead of the current flat symbolic state
- Real Android emulator integration (ADB/Appium-backed actions, accessibility-tree or screenshot-based state)
- Stronger evaluation on unseen task/goal types, not just unseen task instances within known goal types

## Installation

```bash
git clone https://github.com/commit-msuyog/mobile-ui-rl.git
cd mobile-ui-rl

python -m venv venv311

# Windows PowerShell
.\venv311\Scripts\Activate.ps1
# Mac/Linux
source venv311/bin/activate

pip install -e .
```

## Usage

**Run the test suite:**

```bash
pytest
```

**Run the evaluation baseline:**

```bash
python run_eval.py
```

## Results

Running the deterministic baseline against the evaluation set currently produces:

- **Success rate:** 100%
- **Invalid actions:** 0
- **Safety violations:** 0

As noted above, this reflects the environment mechanics working correctly with a hardcoded valid solution per goal type — it is not a measure of a learned agent's performance.