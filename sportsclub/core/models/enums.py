# core/models/enums.py
import enum


class Discipline(enum.StrEnum):
    """Athletic disciplines tracked in competitions."""

    SPRINTS = "sprints"
    LONG_DISTANCE = "long_distance"
    RELAYS = "relays"
    HIGH_JUMP = "high_jump"
    LONG_JUMP = "long_jump"
