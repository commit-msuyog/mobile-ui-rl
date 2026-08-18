from mobile_ui_env.actions import Action
from mobile_ui_env.dataset import load_tasks
from mobile_ui_env.env import MobileUIEnvironment


def actions_for_goal(goal):
    goal_type = goal["type"]

    if goal_type == "note_created":
        return [
            Action("tap", "notes_button"),
            Action("tap", "add_note_button"),
            Action("type", "note_input", goal["title"]),
            Action("tap", "save_note_button"),
        ]

    if goal_type == "focus_mode_enabled":
        return [
            Action("tap", "settings_button"),
            Action("tap", "focus_mode_toggle"),
        ]

    if goal_type == "notifications_disabled":
        return [
            Action("tap", "settings_button"),
            Action("tap", "notifications_toggle"),
        ]

    if goal_type == "screen_open":
        if goal["screen"] == "settings":
            return [Action("tap", "settings_button")]

        if goal["screen"] == "profile":
            return [Action("tap", "profile_button")]

    if goal_type in {"username_found", "email_found"}:
        return [
            Action("tap", "profile_button")
        ]

    return []


def run_task(task):
    env = MobileUIEnvironment()

    actions = actions_for_goal(task["goal"])

    final_state = env.state
    episode_reward = 0.0
    done = False

    for action in actions:
        final_state, reward, done = env.step(
            action,
            task["goal"]
        )

        episode_reward += reward

        if done:
            break

    success = env.is_goal_complete(task["goal"])

    return {
        "task_id": task["task_id"],
        "success": success,
        "reward": episode_reward,
        "steps": final_state.step_count,
        "invalid_actions": final_state.invalid_actions,
        "safety_violations": final_state.safety_violations,
    }


def evaluate(tasks):
    results = []

    for task in tasks:
        results.append(run_task(task))

    return results


def print_results(results):
    total = len(results)

    successes = sum(
        result["success"]
        for result in results
    )

    average_reward = sum(
        result["reward"]
        for result in results
    ) / total

    average_steps = sum(
        result["steps"]
        for result in results
    ) / total

    invalid_actions = sum(
        result["invalid_actions"]
        for result in results
    )

    safety_violations = sum(
        result["safety_violations"]
        for result in results
    )

    print("\nEvaluation Results")
    print("------------------")
    print(f"Tasks: {total}")
    print(f"Success rate: {successes / total:.2%}")
    print(f"Average episode reward: {average_reward:.3f}")
    print(f"Average steps: {average_steps:.2f}")
    print(f"Invalid actions: {invalid_actions}")
    print(f"Safety violations: {safety_violations}")

    print("\nIndividual Tasks")
    print("----------------")

    for result in results:
        print(
            f"{result['task_id']} | "
            f"success={result['success']} | "
            f"reward={result['reward']:.3f} | "
            f"steps={result['steps']}"
        )


if __name__ == "__main__":
    eval_tasks = load_tasks("eval")
    results = evaluate(eval_tasks)
    print_results(results)