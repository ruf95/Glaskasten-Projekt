from game import Game
from paddle import Paddle
import pygame
import math

class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = -5
        self.vy = -3
        self.img = [
                pygame.image.load("data/heart.png"), 
                pygame.image.load("data/heart2.png"), 
                pygame.image.load("data/heart3.png"), 
                pygame.image.load("data/heart4.png")
        ]
        self.rate = 0
        self.img_index = 0
        self.c = (125, 0, 0)
        self.alive = True

    def move(self):
        if self.x < 0 or self.x > Game.width or self.y < 0 \
                or self.y > Game.height:
            self.alive = False
            return
        if self.vx > -5:
            self.vx -= 1
        else:
            self.vx = 5
        self.x += self.vx
        self.y += self.vy
       
    def draw(self):
        img = self.img[self.img_index]
        self.rate += 1
        if self.rate > 15 and self.img_index < len(self.img) - 1:
            self.rate = 0
            self.img_index += 1
        pos = img.get_rect()
        pos.center = (self.x, self.y)
        Game.screen.blit(img, pos)
