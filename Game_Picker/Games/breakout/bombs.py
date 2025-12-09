from game import Game
from paddle import Paddle
import pygame
import math
class Bomb:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.c = (255, 255, 255)
        self.alive = True
        self.hit = False
        self.explosionDuration = 0.5
    def move(self, dt):
        if self.y < 0 or self.y > Game.height:
            self.alive = False
            return
        
        if not self.hit:
            new_y = self.y + self.vy*dt
        else:
            return

        if self.y < Paddle.y-10/Game.windowSize[0] and new_y >= Paddle.y-10/Game.windowSize[1] and self.alive:
            if self.x >= Paddle.x and self.x <= Paddle.x + Paddle.w:
                if not self.hit and Paddle.damage == 0 and Paddle.shield == 0:
                    Game.exploding.play()
                self.hit = Paddle.hit()
        self.y = new_y
        ##self.y += self.vy
    def draw(self, dt):
        if self.hit:
            img = Game.explosion_image
            if self.explosionDuration <= 0.0:
                self.alive = False
            
            self.explosionDuration -= dt
        else:
            img = Game.bomb_image
        pos = img.get_rect()
        pos.midtop = (self.x*Game.windowSize[0], self.y*Game.windowSize[1])
        Game.screen.blit(img, pos)
