from game import Game
import pygame
class Paddle:
    c = (0, 0, 255)
    x, y = None, None
    damage = 0
    shield = 0
    def init():
        Paddle.h = 0.03
        Paddle.w = 0.08*(0.1*Game.paddle_lvl+1.0)
        Paddle.x = 0.5-0.5*Paddle.w
        Paddle.y = 0.95

    def updateSize():
        Paddle.w = 0.08*(Game.paddle_lvl_change*Game.paddle_lvl+1.0)
   
    def left(dt):
        if Paddle.damage == 0:
            Paddle.x -= 0.25*dt
            if Paddle.x < 0:
                Paddle.x = 0

    def right(dt):
        if Paddle.damage == 0:
            Paddle.x += 0.25*dt
            if Paddle.x + Paddle.w > 1.0:
                Paddle.x = 1.0 - Paddle.w

    def hit():
        if Paddle.damage == 0 and Paddle.shield == 0:
            Paddle.damage = 3
            return True
        return False

    def set_shield():
        Paddle.shield = 5+Game.shield_lvl_change*Game.shield_lvl

    def draw(dt):
        if Paddle.damage > 0:
            Paddle.damage -= dt
            Paddle.damage = max(Paddle.damage, 0.0)
            return
        if Paddle.shield > 0:
            Paddle.shield -= dt
            Paddle.shield = max(Paddle.shield, 0.0)
            c = (255, 255, 255)
        else:
            c = Paddle.c
        pygame.draw.rect(Game.screen, c, (Paddle.x*Game.windowSize[0], Paddle.y*Game.windowSize[1], Paddle.w*Game.windowSize[0], Paddle.h*Game.windowSize[1]))
    def set(x):
        Paddle.x = x 
        if Paddle.x < 0:
            Paddle.x = 0 
        if Paddle.x + Paddle.w > 1.0:
            Paddle.x = 1.0 - Paddle.w
    
