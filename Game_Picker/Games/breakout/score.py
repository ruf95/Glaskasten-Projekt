from game import Game
from paddle import Paddle
import pygame
import math

class Score:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val
        self.vx = -1
        self.vy = -4
        self.c = (125, 0, 0)
        self.alive = 30

    def move(self):
        if self.x < 0 or self.x > Game.width or self.y < 0 \
                or self.y > Game.height:
            self.alive = False
            return
        self.x += self.vx
        self.y += self.vy
       
    def draw(self):
        if self.alive > 0:
            self.alive -= 1
        label = f"{self.val}"
        text = Game.font.render(label, True, self.c)
        text_rect = text.get_rect(center=(self.x, self.y))
        Game.screen.blit(text, text_rect)
