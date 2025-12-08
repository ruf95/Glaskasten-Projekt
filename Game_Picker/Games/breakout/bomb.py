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
        self.img = pygame.image.load("data/bomb.png") 
        self.hit = False
        self.die = pygame.image.load("data/explosion.png")

#    def move(self):
#        if self.y < 0:
#            self.alive = False
#            return
#        self.y += self.vy        

    def move(self):
        if self.y < 0 or self.y > Game.height:
            self.alive = False
            return
        new_y = self.y + self.vy
        if self.y < Paddle.y-10 and new_y >= Paddle.y-10:
            if self.x >= Paddle.x and self.x <= Paddle.x + Paddle.w:
                self.hit = Paddle.hit()
        self.y = new_y
       
    def draw(self):
        if self.hit:
            img = self.die
            self.alive = False
            Game.exploding.play()
            Game.add_score(self.x, self.y, 5)
        else:
            img = self.img
        pos = img.get_rect()
        pos.center = (self.x, self.y)
        Game.screen.blit(img, pos)
