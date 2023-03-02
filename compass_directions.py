from enum import Enum

class CompassDirection(Enum):
    N = 0
    NNE = 1
    NE = 2
    ENE = 3
    E = 4
    ESE = 5
    SE = 6
    SSE = 7
    S = 8
    SSW = 9
    SW = 10
    WSW = 11
    W = 12
    WNW = 13
    NW = 14
    NNW = 15

    def prev(self):
        values = list(self.__class__.__members__.values())
        index = values.index(self)
        prev_index = (index - 1) % len(values)
        return values[prev_index]

    def next(self):
        values = list(self.__class__.__members__.values())
        index = values.index(self)
        next_index = (index + 1) % len(values)
        return values[next_index]