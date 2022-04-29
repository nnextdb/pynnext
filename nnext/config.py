from enum import Enum

class Ops(Enum):
    OR = 1
    AND = 2
    EQ = 3
    NOT = 4
    IN = 5
    GTE = 6

_or = Ops.OR
_and = Ops.AND
_eq = Ops.EQ
_not = Ops.NOT
_in = Ops.IN
_gte = Ops.GTE