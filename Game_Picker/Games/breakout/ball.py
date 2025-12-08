from wall import Wall
from game import Game
from paddle import Paddle
import pygame
import math

class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.c_normal = (255, 255, 0)
        self.c_hard = (255, 55, 0)
        self.alive = True
        self.active = False

    def move(self):
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        if new_x < 0:
            new_x = -new_x
            self.vx = -self.vx
            Game.bounce.play()
            
        if new_x > Game.width:
            new_x = 2 * Game.width - new_x
            self.vx = -self.vx
            Game.bounce.play()

        if new_y < 0:
            new_y = -new_y
            self.vy = -self.vy
            Game.bounce.play()

        if self.active:
            self.vx, self.vy = Wall.collision(self.x, self.y, new_x, new_y, self.vx, self.vy)

        if Paddle.damage == 0 and self.y < Paddle.y and new_y >= Paddle.y:
            px = self.x + (((new_x - self.x) // (new_y - self.y)) * (Paddle.y - self.y))
            if px >= Paddle.x and px <= Paddle.x + Paddle.w:
                new_y = Paddle.y + (Paddle.y - self.y) - (new_y - self.y)
                t = (px - Paddle.x) * (2/Paddle.w) - 1
                phi = ((t/2)-1) * ((math.pi)/2)
                v = math.hypot(self.vx, self.vy)
                if abs(t) < 0.25:
                    v = min(14, v * 1.1)
                self.vx = v * math.cos(phi)
                self.vy = v * math.sin(phi)
                self.active = True
                Game.bounce.play()
                
        if self.y > Game.height:
            self.alive = False
            return
       

        self.x = new_x
        self.y = new_y
        
    def draw(self):
        if Game.hard:
            Game.hard -= 1
            c = self.c_hard
        else:
            c = self.c_normal
        pygame.draw.circle(Game.screen, c, (self.x, self.y), 5)
