from bricktype import BrickType
from wall import Wall
from ship import Ship
from game import Game
from heart import Heart
from ball import Ball
from paddle import Paddle
from rocket import Rocket
import controller
import time
import pygame
import math
import random
import glob

Game.init()
Paddle.init()

for dev in glob.glob("/dev/cu.usbserial*") + glob.glob("/dev/ttyUSB*"):
    print(f"trying {dev}")
    if controller.connect(dev):
        break


running = True
Game.balls = []
Game.rockets = []
Game.ships = [Ship(0), Ship(0.5), Ship(1)]
clock = pygame.time.Clock()
start = False
auto_fire_key = False
auto_fire_ser = False
Wall.init(BrickType)

while running:
    if len(Game.balls) == 0:
        if Game.lifes > 1:
            Game.lifes -= 1
        else:
            Game.reset()
            Wall.init(BrickType)
        Game.balls.append(Ball(400, 0, random.randint(-3, 3), 8))
    if Wall.brick.sum() == 0:
        Game.level += 1
        Game.lifes += 1
        for b in Game.balls:
            b.active = False
        Wall.init(BrickType)

    if auto_fire_ser or auto_fire_key:
        Paddle.fire()

    if Game.heart and Game.heart % Game.heart_rate == 0:
        Paddle.fire_heart()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_UP and Paddle.damage == 0:
                if not start:
                    start = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        Game.balls.append(Ball(400, 300, -1, 2))
    if keys[pygame.K_UP]:
        if start:
            auto_fire_key = True
        else:
            start = True
    else:
        auto_fire_key = False
    if keys[pygame.K_LEFT]:
        if not Game.reverse:
            Paddle.left()
        else:
            Paddle.right()
    if keys[pygame.K_RIGHT]:
        if not Game.reverse:
            Paddle.right()
        else:
            Paddle.left()

    if keys[pygame.K_p]:
        for dev in glob.glob("/dev/cu.usbserial*") + glob.glob("/dev/ttyUSB*"):
            print(f"trying {dev}")
            if controller.connect(dev):
                break
    while True:
        ser_data = controller.readdata()
        if ser_data is None:
            break
        if ser_data[0] == "A" and Paddle.damage == 0:
            if start:
                auto_fire_ser = True
            else:
                start = True
        elif ser_data[0] == "a":
            auto_fire_ser = False
        elif ser_data[0] == "X":
            pos = ser_data[1] * Game.scale_x
            if not Game.reverse:
                Paddle.set(pos)
            else:
                Paddle.set(Game.width - pos)

    pygame.Surface.fill(Game.screen, (150, 150, 150))

    Paddle.draw()
    if start:
        Game.draw()

        tmp = []
        for h in Game.hearts:
            for item in Game.ships + Game.bombs:
                dist = math.hypot(item.x - h.x, item.y - h.y)
                if dist < 32:
                    item.alive = False
                    nh = Heart(item.x, item.y)
                    tmp.append(nh)
        Game.hearts += tmp

        for s in Game.ships + Game.bombs:
            for item in Game.balls + Game.rockets:
                dist = math.hypot(item.x - s.x, item.y - s.y)
                if dist <= 25:
                    s.hit = True
                    item.hit = True
    Wall.draw()
    Game.display.blit(Game.screen, (Game.display_x, Game.display_y))
    pygame.display.flip()
    clock.tick(30)


Game.quit()
