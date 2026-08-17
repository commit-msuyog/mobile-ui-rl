from dataclasses import dataclass


@dataclass
class Action:
    action: str
    target: str | None = None
    text: str | None = None