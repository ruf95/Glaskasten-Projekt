from game import Game
from paddle import Paddle
import pygame
import math

class Rocket:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.c = (255,255,255)
        self.alive = True
        self.img = pygame.image.load("breakout/asp-ulm-data/rocket0.png")
        self.die = pygame.image.load("breakout/asp-ulm-data/explosion.png")
        self.hit = False

    def move(self):
        if self.y < 0:
            self.alive = False
            return
        self.y += self.vy

    def draw(self):
        if self.hit:
            img = self.die
            self.alive = False
        else:
            img = self.img
        pos = img.get_rect()
        pos.midtop = (self.x,self.y)
        Game.screen.blit(img,pos)
