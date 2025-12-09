from game import Game
from paddle import Paddle
from wall import Wall
import pygame
import math
class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.c = (255, 255, 0)
        self.alive = True
        self.active = False
        self.hit = False
    def move(self, dt):

        new_x = self.x + self.vx*dt
        new_y = self.y + self.vy*dt
        if self.y < Paddle.y-5/Game.windowSize[1] and new_y >= Paddle.y-5/Game.windowSize[1] and Paddle.damage == 0:
            Dy = Paddle.y - self.y
            dx = new_x - self.x 
            dy = new_y - self.y
            Dx = dx / dy * Dy
            px = self.x + Dx
            self.active = True
            if px >= Paddle.x and px <= Paddle.x + Paddle.w:
                Game.bounce.play()
                new_y = Paddle.y + Dy - dy -10/Game.windowSize[1]
                t = (px - Paddle.x) * 2 / Paddle.w - 1
                phi = ((t / 3) - 1) * math.pi / 2
                v = math.hypot(self.vx, self.vy)
                self.vx = v*math.cos(phi)
                self.vy = v*math.sin(phi)

        new_x_pixels = new_x*Game.windowSize[0]
        new_y_pixels = new_y*Game.windowSize[1]
               
        if new_x_pixels < 5:
            new_x_2 = -new_x_pixels + 10
            new_x = new_x_2 /Game.windowSize[0]
            self.vx = -self.vx
        if new_x_pixels > Game.windowSize[0] - 5:
            new_x_2 = 2 * Game.windowSize[0] - new_x_pixels - 10
            new_x = new_x_2 /Game.windowSize[0]
            self.vx = -self.vx
        if new_y_pixels < 5:
            new_y_2 = -new_y_pixels + 10
            new_y = new_y_2 / Game.windowSize[1]
            self.vy = -self.vy
        if new_y_pixels > Game.windowSize[1] - 5:
            self.alive = False 
            return
        if self.active == True:
            self.vx, self.vy = Wall.collision(self.x, self.y, new_x, new_y, self.vx, self.vy)
        self.x = new_x
        self.y = new_y
    def draw(self, dt):
        self.hit = False
        pygame.draw.circle(Game.screen, self.c, (self.x*Game.windowSize[0], self.y*Game.windowSize[1]), 0.005*Game.windowSize[0])
