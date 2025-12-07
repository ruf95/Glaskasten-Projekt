from game import Game
import pygame 

class Paddle:
    c = (0,0,255)
    w, h = 100,30
    x, y = None, None
    damage = 0
    shield = 0

    def init():
        Paddle.x, Paddle.y = (Game.width - Paddle.w) // 2, 570
    
    def left():
        Paddle.x -= 10
        if Paddle.x < 0:
            Paddle.x = 0

    def right():
        Paddle.x += 10
        if Paddle.x + Paddle.w > Game.width:
            Paddle.x = Game.width - Paddle.w

    def draw():
        if Paddle.damage > 0:
            Paddle.damage -= 1
            return
        if Paddle.shield > 0:
            Paddle.shield -= 1
            c = (255,255,255)
        else:
            c = Paddle.c
        pygame.draw.rect(Game.screen, c, (Paddle.x, Paddle.y, Paddle.w, Paddle.h))

    def set(x):
        Paddle.x = x
        if Paddle.x < 0:
            Paddle.x = 0
        if Paddle.x + Paddle.w > Game.width:
            Paddle.x = Game.width - Paddle.w

    def hit():
        if Paddle.damage == 0 and Paddle.shield == 0:
            Paddle.damage = 90
            return True
        return False

    def set_shield():
        Paddle.shield = 300
