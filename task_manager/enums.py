from enum import StrEnum

class TaskStatus(StrEnum):
    new = "new"
    in_progress = "in_progress"
    pending = "pending"
    blocked = "blocked"
    done = "done"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]