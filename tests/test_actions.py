from mobile_ui_env.actions import Action


def test_tap_action():
    action = Action("tap", "notes_button")

    assert action.action == "tap"
    assert action.target == "notes_button"


def test_type_action():
    action = Action("type", "note_input", "Buy milk")

    assert action.action == "type"
    assert action.target == "note_input"
    assert action.text == "Buy milk"


def test_back_action():
    action = Action("back")

    assert action.action == "back"
    assert action.target is None
    assert action.text is None