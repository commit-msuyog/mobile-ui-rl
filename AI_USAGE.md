# AI Usage

I used AI tools as an assistant to help me plan and build this project. 

## How I used AI

I mainly used AI to help me with:
* Understanding the project requirements.
* Planning how the RL environment should work.
* Discussing the design for states, actions, and rewards.
* Figuring out why I was getting errors and fixing bugs.
* Cleaning up the README file.

## What I actually built and checked

While AI helped me brainstorm, I ran and tested the actual code locally. The parts I made sure worked include:
* Keeping track of the environment state
* Handling and checking actions
* Checking if the goal was met
* Calculating the rewards
* Creating the dataset of tasks
* Writing and running the tests

I also ran the evaluation script locally to make sure the whole environment worked with basic valid actions.

## Fixing code and not just copying

I didn't just blindly copy-paste the AI's suggestions. I ran the code, checked the results, and changed things when they didn't work the way they were supposed to.

**Here is a real example of a bug I fixed:**
While running my tests, I found a problem with how points were given out. If a task failed, it was still getting a small "efficiency" reward just for finishing quickly. A test caught this issue. I went back in, changed the logic so the efficiency reward is *only* given if the task is actually successful, and ran the tests again to make sure it was fixed.

### Current Test Results
```text
13 passed

Current evaluation result:
Tasks: 10
Success rate: 100.00%
Average episode reward: 0.855
Average steps: 2.40
Invalid actions: 0
Safety violations: 0
```

## What I learned

Building this project taught me a lot about how Reinforcement Learning works under the hood. Specifically, I learned:

1. How an RL environment keeps track of states and actions.
2. How the `reset()` and `step()` functions control the flow of an episode.
3. How to design rewards so the agent focuses on actually completing the task.
4. Why we need to track invalid actions and safety rules (like accidental logouts) separately.
5. What "reward hacking" is (like the bug I fixed where the agent got points for failing fast).
6. How to use a simple baseline script to test the environment before you even start training an AI model.

AI was a great learning tool, but I made sure to run, test, and review all the code locally myself.