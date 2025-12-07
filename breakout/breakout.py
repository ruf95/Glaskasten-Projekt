from game import Game
from ball import Ball
from paddle import Paddle
from rocket import Rocket
from ship import Ship
from wall import Wall
from controller import Controller
from bricktype import BrickType

import time
import pygame
import math


Game.init()
Paddle.init()


running = True
Game.balls = []
Game.rockets = []
Game.ships = [Ship(0), Ship(0.5), Ship(1)]

Controller.connect("/dev/ttyUSB0")

clock = pygame.time.Clock()
while running:
    while True:
        if Wall.brick.sum() == 0:
            Game.level += 1
            Wall.init(BrickType)
            if Game.level != 1:
                Game.current_score += 20
        if len(Game.balls) == 0:
            if Game.lifes > 1:
                Game.lifes -= 1
            else:
                Game.lifes = 3
                Game.level = 1
                Wall.init(BrickType)
            Game.balls.append(Ball(400,0,-2,6))
        ser_data = Controller.readdata()
        if ser_data is None:
            break
        if ser_data[0] == "A" and Paddle.damage == 0:
            Game.rockets.append(Rocket(Paddle.x + Paddle.w // 3, Paddle.y, -10))
            Game.launch.play()
        elif ser_data[0] == "X":
            Paddle.set(ser_data[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                Controller.connect("/dev/ttyUSB0")
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_UP and Paddle.damage == 0:
                Game.rockets.append(Rocket(Paddle.x +  Paddle.w//2, Paddle.y, -10))
                Game.launch.play()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        Game.balls.append(Ball(400,300, -1, 2))
    if keys[pygame.K_LEFT]:
        Paddle.left()
    if keys[pygame.K_RIGHT]:
        Paddle.right()

    
    pygame.Surface.fill(Game.screen, (0,0,0))
    for s in Game.ships + Game.bombs:
        for b in Game.balls+Game.rockets:
            dist = math.hypot(b.x - s.x, b.y - s.y)
            if dist <= 20:
                b.hit = True
                s.hit = True
                Game.current_score += 5
   
    Wall.draw()
    Game.draw()
    Paddle.draw()
    pygame.display.flip()
    clock.tick(30)
#done
Game.quit()
