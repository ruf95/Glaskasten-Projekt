from game import Game
from paddle import Paddle
from rocket import Rocket
from bomb import Bomb
import pygame
import math
import random


class Ship:
    def __init__(self, t):
        self.x0 = Game.width / 2
        self.y0 = Game.height / 3
        self.a = 0.9 * Game.width/2
        self.b = 0.9 * Game.height / 3
        self.t = t
        self.alive = True
        self.x, self.y = None, None
        self.move()
        self.c = (255, 0, 0)
        self.img = pygame.image.load("breakout/asp-ulm-data/space_invader0.png")
        self.die = pygame.image.load("breakout/asp-ulm-data/explosion.png")
        self.hit = False
         
    def move(self):
        self.x = self.x0 + self.a * math.cos(self.t)
        self.y = self.y0 + self.b * math.sin(2*self.t)/2
        self.t += 0.01
        while self.t > 2 * math.pi:
            self.t -= 2*math.pi
        if random.randint(1,100) == 1:
            Game.bombs.append(Bomb(self.x,self.y,10))
       
    def draw(self):
        if self.hit:
            img = self.die
            self.alive = False
            Game.exploding.play()
        else:
            img = self.img
        pos = self.img.get_rect()
        pos.center = (self.x, self.y)
        Game.screen.blit(img, pos)
