from enum import Enum

class Economy(Enum):
    NORMAL = ("NORMAL", "Round win")
    ATK_THRIFTY = ("ATK_THRIFTY", "Thrifty (ATK)")
    DEF_THRIFTY = ("DEF_THRIFTY", "Thrifty (DEF)")

    def __init__(self, code, label):
        self.code = code
        self.label = label

    def __str__(self):
        return self.label