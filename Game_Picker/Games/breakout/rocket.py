from game import Game
from paddle import Paddle
import pygame
import math
class Rocket:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.c = (255, 255, 255)
        self.alive = True
        self.hit = False
        self.explosionDuration = 0.5
    def move(self, dt):
        if self.y*Game.windowSize[1] < 10:
            self.alive = False
            return
        if not self.hit:
            self.y += self.vy * dt
    def draw(self, dt):
        if self.hit:
            img = Game.explosion_image
            if self.explosionDuration <= 0.0:
                self.alive = False
            self.explosionDuration -= dt
        else:
            img = Game.rocket_image
        pos = img.get_rect()
        pos.midtop = (self.x*Game.windowSize[0], self.y*Game.windowSize[1])
        Game.screen.blit(img, pos)
