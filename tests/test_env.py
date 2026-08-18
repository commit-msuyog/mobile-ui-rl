from mobile_ui_env.actions import Action
from mobile_ui_env.env import MobileUIEnvironment


def test_environment_starts_at_home():
    env = MobileUIEnvironment()

    assert env.state.screen == "home"
    assert env.state.notes == []
    assert env.state.step_count == 0


def test_can_open_notes():
    env = MobileUIEnvironment()

    env.step(Action("tap", "notes_button"))

    assert env.state.screen == "notes"


def test_can_create_note():
    env = MobileUIEnvironment()

    goal = {
        "type": "note_created",
        "title": "Buy milk"
    }

    env.step(Action("tap", "notes_button"), goal)
    env.step(Action("tap", "add_note_button"), goal)
    env.step(Action("type", "note_input", "Buy milk"), goal)

    state, reward, done = env.step(
        Action("tap", "save_note_button"),
        goal
    )

    assert "Buy milk" in state.notes
    assert done is True


def test_invalid_action_does_not_crash():
    env = MobileUIEnvironment()

    state, reward, done = env.step(
        Action("tap", "save_note_button")
    )

    assert state.invalid_actions == 1


def test_focus_mode_goal():
    env = MobileUIEnvironment()

    goal = {
        "type": "focus_mode_enabled"
    }

    env.step(Action("tap", "settings_button"), goal)

    state, reward, done = env.step(
        Action("tap", "focus_mode_toggle"),
        goal
    )

    assert state.focus_mode is True
    assert done is True


def test_profile_navigation():
    env = MobileUIEnvironment()

    goal = {
        "type": "username_found"
    }

    state, reward, done = env.step(
        Action("tap", "profile_button"),
        goal
    )

    assert state.screen == "profile"
    assert done is True