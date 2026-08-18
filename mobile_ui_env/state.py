from dataclasses import dataclass, field


@dataclass
class EnvironmentState:

    # current app screen.
    screen: str = "home"

    # saved note + note being edited.
    notes: list[str] = field(default_factory=list)
    draft_note: str = ""

    # app settings.
    focus_mode: bool = False
    notifications: bool = True

    # used for limits, penalties and reward.
    step_count: int = 0
    invalid_actions: int = 0
    safety_violations: int = 0