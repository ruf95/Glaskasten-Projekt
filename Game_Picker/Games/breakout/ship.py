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
        self.a = 0.9 * Game.width / 2
        self.b = 0.9 * Game.height / 3
        self.c = (100,0,0)
        self.t = t
        self.alive = 3
        self.x, self.y = None, None
        self.move()
        self.img = [
                pygame.image.load("data/space_invader0.png"),
                pygame.image.load("data/space_invader1.png"),
                pygame.image.load("data/space_invader2.png")
        ]
        self.die = pygame.image.load("data/explosion.png")
        self.hit = False
        
    def move(self):
        self.x = self.x0 + self.a * math.cos(self.t)
        self.y = self.y0 + self.b * math.sin(2 * self.t) / 2
        if random.randint(1, 100) == 1:
            Game.bombs.append(Bomb(self.x, self.y, 10))
        self.t += 0.01
        while self.t > 2 * math.pi:
            self.t -= 2 * math.pi

    def draw(self):
        if self.alive:
            img = self.img[self.alive - 1]
        else:
            img = self.die
        if self.hit:
            self.alive -= 1
            self.hit = False
            if not self.alive:
                img = self.die
            Game.add_score(self.x, self.y, 20)
            Game.exploding.play()
        pos = img.get_rect()
        pos.center = (self.x, self.y)
        Game.screen.blit(img, pos)
