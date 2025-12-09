from game import Game
from paddle import Paddle
import random
from rocket import Rocket
from bombs import Bomb
from coin import Coin
from heart import Heart
import pygame
import math
class Ship:
    def __init__(self, t):
        self.x0 = 1 / 2
        self.y0 = 1 / 3
        self.a = 0.9 / 2
        self.b = 0.9 / 3
        self.t = t
        self.x, self.y = None, None
        self.c = (255, 0, 0)
        self.bombCooldown = random.random()
        self.alive = True
        self.hit = False
        self.move(0)
        self.explosionDuration = 0.5
        self.coinDropped = False
        self.extraLife = random.randint(1, 100) <= 7

    def move(self, dt):
        self.bombCooldown -= dt
        if self.hit:
            return
        if self.bombCooldown <= 0.0:
            self.bombCooldown = 2.0
            Game.bombs.append(Bomb(self.x, self.y, 0.2))
        self.x = self.x0 + self.a * math.cos(self.t)
        self.y = self.y0 + self.b * math.sin(2 * self.t) / 2
        self.t += 0.5*dt
        while self.t > 2 * math.pi:
            self.t -= 2 * math.pi
            
    def draw(self, dt):
        if self.extraLife:
            self.img = Game.invader_image2
        else:
            self.img = Game.invader_image1
    
        if self.hit:
            if not self.coinDropped:
                self.coinDropped = True
                if self.extraLife:
                    Game.hearts.append(Heart(self.x, self.y, 0.15))
                else:
                    Game.coin.append(Coin(self.x, self.y, 0.15))
            img = Game.explosion_image
            if self.explosionDuration <= 0.0:
                self.alive = False
            self.explosionDuration -= dt
        else:
            img = self.img

        pos = img.get_rect()
        pos.center = (self.x*Game.windowSize[0], self.y*Game.windowSize[1])
        Game.screen.blit(img, pos)
