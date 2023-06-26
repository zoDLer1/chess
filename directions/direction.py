from typing import Any


class ViewDirectionDebugManager:

    X_FACTOR = 1
    Y_FACTOR = 3

    DIAGONALS_IDS = {
        -4: '↖',
        -2: '↗',
        4: '↘',
        2: '↙',
        3: '↓',
        -3: '↑',
        1: '→',
        -1: '←',
        0: '·'
    }


    def __init__(self, offset_x, offset_y) -> None:
        self.view = self.DIAGONALS_IDS.get(offset_x * self.X_FACTOR + offset_y * self.Y_FACTOR, 'uncalc')

    def __str__(self) -> str:
        return self.view

    def __repr__(self) -> str:
        return self.view

class Direction:
    def __init__(self, up, left):
        self.up = up
        self.left = left
        self.view = ViewDirectionDebugManager(up, left)

    def get_next(self, column, row):
        return (column + self.up, row + self.left)

    def reverse(self):
        return Direction(-self.up, -self.left)


    @classmethod
    def nw(cls):
        return cls(-1, -1)
    
    @classmethod
    def ne(cls):
        return cls(1, -1)

    @classmethod
    def se(cls):
        return cls(1, 1)

    @classmethod
    def sw(cls):
        return cls(-1, 1)

    @classmethod
    def s(cls):
        return cls(0, 1)

    @classmethod
    def n(cls):
        return cls(0, -1)

    @classmethod
    def e(cls):
        return cls(1, 0)

    @classmethod
    def w(cls):
        return cls(-1, 0)

    @classmethod
    def een(cls):
        return cls(-2, 1)
    
    @classmethod
    def wwn(cls):
        return cls(-2, -1)
    
    @classmethod
    def ees(cls):
        return cls(2, 1)
    
    @classmethod
    def wws(cls):
        return cls(2, -1)
    
    @classmethod
    def sse(cls):
        return cls(1, 2)
    
    @classmethod
    def ssw(cls):
        return cls(-1, 2)
    
    @classmethod
    def nnw(cls):
        return cls(-1, -2)

    @classmethod
    def nne(cls):
        return cls(1, -2)



    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} - ( {self.view} )>'

class DirectionManager:

    def __next__(self, index: int) -> Direction:
        yield self.directions[index]

    def __add__(self, other):
        self.directions += other.directions
        return self

    def __init__(self, *directions):
        self.directions = directions

    def __getitem__(self, index: int) -> Direction:
        return self.directions[index]

    def __str__(self) -> str:
        return str(self.directions)

    @classmethod
    def lines(cls):
        return cls(Direction.n(), Direction.s(), Direction.e(), Direction.w())

    @classmethod
    def diagonals(cls):
        return cls(Direction.nw(), Direction.ne(), Direction.se(), Direction.sw())

    @classmethod
    def circle(cls):
        return cls(Direction.een(), Direction.ees(), Direction.wws(), Direction.wwn(), Direction.ssw(), Direction.sse(), Direction.nne(), Direction.nnw())

    @classmethod
    def star(cls):
        return cls.diagonals() + cls.lines()