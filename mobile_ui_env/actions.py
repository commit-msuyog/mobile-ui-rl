from dataclasses import dataclass


@dataclass
class Action:

    # tap, type, back or finish
    action: str

    # Used by tap/type when needed.
    target: str | None = None

    # Only used by type.
    text: str | None = None