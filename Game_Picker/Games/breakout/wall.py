import pygame
import numpy
import random

from ship import Ship
from game import Game

class Wall:
    brick = None
    BrickType = None

    def init(BrickType):
        Wall.BrickType = BrickType
        Wall.brick = numpy.zeros((Game.brick_rows, Game.brick_cols))
        for i in range(4, 8 + Game.level):
            for j in range(0, Game.brick_cols):
                if random.randint(1, 100) <= 20:
                    ty = random.randint(2, max(Wall.BrickType) - 2)
                else:
                    ty = 1
                Wall.brick[i, j] = ty
        Wall.brick[8 + Game.level - 2, Game.brick_cols // 2] = BrickType.HEART

    def collision(x1, y1, x2, y2, vx, vy):
        j1 = int(x1) // Game.brick_width
        j2 = int(x2) // Game.brick_width
        i1 = int(y1) // Game.brick_height
        i2 = int(y2) // Game.brick_height
        if i2 >= 0 and i2 < Game.brick_rows and j2 >= 0 and j2 < Game.brick_cols:
            if Wall.brick[i2, j2]:
                Wall.brick[i2, j2] = Wall.BrickType.effect(Wall.brick[i2, j2])
                Game.ships.append(Ship(0))
                Game.add_score(x2, y2, 5)
                if not Game.hard and i1 == i2:
                    vx = -vx 
                if not Game.hard and j1 == j2:
                    vy = -vy
                Game.bounce.play()
                    
        return vx, vy

    def draw():
        for i in range(0, Wall.brick.shape[0]):
            for j in range(0, Wall.brick.shape[1]):
                if not Wall.brick[i, j]:
                    continue

                w = Game.brick_width
                h = Game.brick_height
                x = j * w
                y = i * h
                r = (x + 1, y + 1, w - 1, h - 1)
                c = Wall.BrickType.color(Wall.brick[i, j])
                brick_surface = pygame.Surface((w-2, h-2), pygame.SRCALPHA)
                brick_surface.fill((c[0], c[1], c[2], 128))
                # pygame.draw.rect(Game.screen, c, r)
                Game.screen.blit(brick_surface, (x+1, y+1))

                label = Wall.BrickType.label(Wall.brick[i, j])
                text = Game.font.render(label, True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + w//2, y + h //2))
                Game.screen.blit(text, text_rect)
