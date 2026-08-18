from mobile_ui_env.rubric import calculate_reward


def test_failed_task_has_zero_reward():
    reward = calculate_reward(
        success=False,
        steps=5,
        max_steps=8,
        invalid_actions=0,
        safety_violations=0,
    )

    assert reward == 0.0


def test_efficient_success_beats_slow_success():
    efficient = calculate_reward(
        success=True,
        steps=3,
        max_steps=8,
        invalid_actions=0,
        safety_violations=0,
    )

    slow = calculate_reward(
        success=True,
        steps=8,
        max_steps=8,
        invalid_actions=0,
        safety_violations=0,
    )

    assert efficient > slow


def test_invalid_actions_reduce_reward():
    clean = calculate_reward(
        success=True,
        steps=5,
        max_steps=8,
        invalid_actions=0,
        safety_violations=0,
    )

    messy = calculate_reward(
        success=True,
        steps=5,
        max_steps=8,
        invalid_actions=2,
        safety_violations=0,
    )

    assert clean > messy


def test_safety_violation_has_strong_penalty():
    clean = calculate_reward(
        success=True,
        steps=5,
        max_steps=8,
        invalid_actions=0,
        safety_violations=0,
    )

    unsafe = calculate_reward(
        success=True,
        steps=5,
        max_steps=8,
        invalid_actions=0,
        safety_violations=1,
    )

    assert clean > unsafe