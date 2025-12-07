from game import Game
from paddle import Paddle
from wall import Wall
import pygame
import math

class Ball:
    def __init__(self, x, y , vx, vy):
        self.x= x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.c = (255, 255, 0)
        self.alive = True
        self.active = False

    def move(self):
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        if new_x < 5:
            new_x = -new_x + 10
            self.vx = -self.vx
            Game.bounce.play()
        if new_x > (Game.width-5):
            new_x = 2 * Game.width - new_x -10
            self.vx = -self.vx
            Game.bounce.play()

        if new_y < 5:
            new_y = -new_y + 10
            self.vy = -self.vy
            Game.bounce.play()
        if new_y > (Game.height+5):
            self.alive = False

            
        if Paddle.damage == 0:
            if self.y < Paddle.y - 5 and new_y >= Paddle.y - 5 :
                dx = new_x - self.x
                dy = new_y - self.y
                Dy = Paddle.y - self.y
                Dx = (dx//dy) * Dy       
                Game.bounce.play()
               
                px = self.x + Dx
                if px >= Paddle.x and px <= Paddle.x + Paddle.w:
                    self.active = True
                    new_y = Paddle.y + Dy - dy - 10
                    self.vy = -self.vy
                    t = (px - Paddle.x) * 2/Paddle.w - 1
                    phi = (t/3 -1) * math.pi/2
                    v = math.hypot(self.vx, self.vy)
                    self.vx = v * math.cos(phi)
                    self.vy = v * math.sin(phi)
        if self.active == True:
            self.vx, self.vy = Wall.collision(self.x, self.y, new_x, new_y, self.vx, self.vy)
        self.x = new_x
        self.y = new_y
        
        
    def draw(self):
        pygame.draw.circle(Game.screen, self.c, (self.x, self.y), 5)
