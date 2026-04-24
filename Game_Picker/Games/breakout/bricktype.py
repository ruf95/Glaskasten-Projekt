from enum import IntEnum
from ball import Ball
from game import Game
from paddle import Paddle
class BrickType(IntEnum):
    NONE = 0
    NORMAL = 1
    BALL = 2
    SHIELD = 3
    TWICE = 4

    def label(self):
        if self == BrickType.BALL:
            return f"Ball"
        if self == BrickType.SHIELD:
            return f"Shield"
        if self == BrickType.TWICE:
            return f"Twice"
        return f""

    def color(self):
        if self == BrickType.BALL:
            return(255, 0, 0)
        if self == BrickType.SHIELD:
            return(0, 0, 255)
        if self == BrickType.TWICE:
            return(0, 255, 0)   
        return(233, 100, 0)

    def effect(self, i, j):
        if self == BrickType.TWICE:
            return BrickType.NORMAL
        elif self == BrickType.BALL:
            x = (j + 0.5) * Game.brick_width / Game.windowSize[0]
            y = (i + 0.5) * Game.brick_height / Game.windowSize[1]
            Game.balls.append(Ball(x, y, 0, 0.2))
            return BrickType.NONE
        elif self == BrickType.SHIELD:
            Paddle.set_shield()
            return BrickType.NONE
        else:
            Game.highscore += 10.0*Game.highscore_mult
            return BrickType.NONE
def main():
    for i in range(0, max(BrickType)):
        bt = BrickType(i)
        print(f"i = {i}, bt {bt}, bt.label = {bt.label()}")
    ##print(max(BrickType))
    ##print(BrickType.BALL)
    ##print(BrickType.BALL.label())
    ##foo = BrickType(4)
    ##print(foo)
    ##print(foo.label())

    
if __name__ == "__main__":
    main()
