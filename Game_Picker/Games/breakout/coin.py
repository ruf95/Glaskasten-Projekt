from game import Game
from paddle import Paddle
import pygame
import math

class Coin:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.c = (255, 255, 255)
        self.alive = True
    def move(self, dt):
        if self.y < 0 or self.y > Game.height:
            self.alive = False
            return
        
        new_y = self.y + self.vy*dt

        if self.y < Paddle.y-10/Game.windowSize[0] and new_y >= Paddle.y-10/Game.windowSize[1] and self.alive:
            if self.x >= Paddle.x and self.x <= Paddle.x + Paddle.w:
                if Paddle.damage == 0:
                    Game.coins += 1
                    self.alive = False

        self.y = new_y
        ##self.y += self.vy
    def draw(self, dt):
        img = Game.coin_image

        pos = img.get_rect()
        pos.midtop = (self.x*Game.windowSize[0], self.y*Game.windowSize[1])
        Game.screen.blit(img, pos)