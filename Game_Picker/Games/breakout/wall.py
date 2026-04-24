import pygame
import numpy
from game import Game
from ship import Ship
import random
class Wall:
    brick = numpy.zeros((Game.brick_rows, Game.brick_cols))
    BrickType = None
    def init(BrickType):
        Wall.BrickType = BrickType
        Wall.brick = numpy.zeros((Game.brick_rows, Game.brick_cols))
        for i in range(4, 4 + Game.level):
            for j in range (0, Game.brick_cols):
                if random.randint(1, 100) <= 30:
                    ty = random.randint(1, max(Wall.BrickType))
                else:
                    ty = 1
                Wall.brick[i, j] = ty

    def collision(x1, y1, x2, y2, vx, vy):
        j1 = int(x1*Game.windowSize[0]) // Game.brick_width
        i1 = int(y1*Game.windowSize[1]) // Game.brick_height
        j2 = int(x2*Game.windowSize[0]) // Game.brick_width
        i2 = int(y2*Game.windowSize[1]) // Game.brick_height
        if i2 >= 0 and i2 < Game.brick_rows and j2 >= 0 and j2 < Game.brick_cols:
            if Wall.brick[i2, j2]:
                Wall.brick[i2, j2] = Wall.BrickType.effect(Wall.brick[i2, j2], i2, j2)
                Game.ships.append(Ship(3*random.random()))
                if i1 != i2:
                    vy = -vy
                if j1 != j2:
                    vx = -vx
        return (vx, vy)

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
                pygame.draw.rect(Game.screen, c, r)

                label = Wall.BrickType.label(Wall.brick[i, j])
                font = Game.font
                text = font.render(label, True, (255, 255, 255))
                text_rect = text.get_rect(center=(x+w//2, y+h //2))
                Game.screen.blit(text, text_rect)
