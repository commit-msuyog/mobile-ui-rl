from dataclasses import dataclass, field


@dataclass
class EnvironmentState:
    screen: str = "home"

    notes: list[str] = field(default_factory=list)
    draft_note: str = ""

    focus_mode: bool = False
    notifications: bool = True

    step_count: int = 0
    invalid_actions: int = 0
    safety_violations: int = 0