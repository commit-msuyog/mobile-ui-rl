def success_reward(success):
    return 1.0 if success else 0.0


def efficiency_reward(steps, max_steps):
    if steps <= 0:
        return 0.0

    score = 1 - (steps / max_steps)
    return max(0.0, score)


def invalid_action_penalty(invalid_actions):
    return min(0.2, invalid_actions * 0.05)


def safety_penalty(safety_violations):
    return min(0.3, safety_violations * 0.3)


def partial_progress_reward(progress):
    return min(0.1, progress)


def calculate_reward(
    success,
    steps,
    max_steps,
    invalid_actions,
    safety_violations,
    progress=0.0,
):
    if not success:
        return 0.0

    reward = 0.75

    reward += 0.15 * efficiency_reward(steps, max_steps)
    reward += 0.10 * partial_progress_reward(progress)

    reward -= invalid_action_penalty(invalid_actions)
    reward -= safety_penalty(safety_violations)

    return max(0.0, min(1.0, reward))