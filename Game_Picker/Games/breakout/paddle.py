from game import Game
import pygame

class Paddle:
    c = (0, 0, 255)
    w, h = 150, 30
    x, y = None, None
    rocket = None
    damage = 0
    shield = 0
    shield_max = 300
    cooldown = 0

    def init():
        from rocket import Rocket
        from heart import Heart
        Paddle.x, Paddle.y = (Game.width - Paddle.w) // 2, Game.height - Paddle.h       
        Paddle.rocket = Rocket
        Paddle.heart = Heart

    def hit():
        if Paddle.damage == 0 and Paddle.shield == 0:
            Paddle.damage = 90
            return True
        return False

    def set_shield():
        Paddle.shield = Paddle.shield_max

    def fire_heart():
        h = Paddle.heart(Paddle.x + Paddle.w // 2, Paddle.y - 20)
        Game.hearts.append(h)

    def fire():
        if Paddle.cooldown == 0 and Paddle.damage == 0 and Game.ammo > 0:
            Paddle.cooldown = 5
            Game.ammo -= 1
            Game.launch.play()
            r = Paddle.rocket(Paddle.x + Paddle.w // 2, Paddle.y - 20, -20)
            Game.rockets.append(r)

    def left():
        Paddle.x -= 10
        if Paddle.x < 0:
            Paddle.x = 0
            
    def right():
        Paddle.x += 10
        if Paddle.x + Paddle.w > Game.width:
            Paddle.x = Game.width - Paddle.w

    def set(x):
        Paddle.x = x
        if Paddle.x < 0:
            Paddle.x = 0
        if Paddle.x + Paddle.w > Game.width:
            Paddle.x = Game.width - Paddle.w

    def draw():
        if Paddle.cooldown > 0:
            Paddle.cooldown -= 1
        if Paddle.damage > 0:
            Paddle.damage -= 1
            if Paddle.damage == 0:
                Paddle.shield = Paddle.shield_max
            return
        t = Paddle.shield / Paddle.shield_max
        c = (Paddle.c[0] * (1-t) + t * 255,
             Paddle.c[1] * (1-t) + t * 255,
             Paddle.c[2] * (1-t) + t * 255)
        if Paddle.shield > 0:
            Paddle.shield -= 1
        pygame.draw.rect(Game.screen, c,
                         (Paddle.x, Paddle.y, Paddle.w, Paddle.h))
