from enum import IntEnum
from ball import Ball
from game import Game
from paddle import Paddle
from ship import Ship

class BrickType(IntEnum):
    NONE = 0
    NORMAL = 1
    BALL = 2
    SHIELD = 3
    TWICE = 4
    BREAK = 5
    HEART = 6
    REVERSE = 7

    def label(self):
        if self == BrickType.BALL:
            return "Ball"
        elif self == BrickType.SHIELD:
            return "Shield"
        elif self == BrickType.TWICE:
            return "Twice"
        elif self == BrickType.REVERSE:
            return "Reverse"
        elif self == BrickType.HEART:
            return "Heart"
        elif self == BrickType.BREAK:
            return "Break"
        else:
            return ""

    def color(self):
        if self == BrickType.BALL:
            return (0, 255, 0)
        elif self == BrickType.SHIELD:
            return (255, 0, 0)
        elif self == BrickType.TWICE:
            return (200, 200, 200)
        elif self == BrickType.HEART:
            return (100, 10, 10)
        elif self == BrickType.REVERSE:
            return (100, 100, 100)
        else:
            return (105, 223, 165)

    def effect(self):
        Game.ships.append(Ship(0))
        if self == BrickType.TWICE:
            return BrickType.NORMAL
        if self == BrickType.REVERSE:
            Game.set_reverse()
            return BrickType.NONE
        elif self == BrickType.SHIELD:
            Paddle.set_shield()
            return BrickType.NONE
        elif self == BrickType.BALL:
            Game.balls.append(Ball(100, 0, -3, 8))
            return BrickType.NONE
        elif self == BrickType.HEART:
            Game.set_heart()
            return BrickType.NONE
        elif self == BrickType.BREAK:
            Game.hard = 30 * 20
            return BrickType.NONE
        else:
            return BrickType.NONE


def main():
    for i in range(0, max(BrickType)):
        bt = BrickType(i)
        print(f"i = {i}, bt = {bt}, bt.label = {bt.label()}")

if __name__ == "__main__":
    main()

