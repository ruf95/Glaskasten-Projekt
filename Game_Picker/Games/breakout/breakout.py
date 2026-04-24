from functions import *
from game import Game
from ball import Ball
from paddle import Paddle
from rocket import Rocket
from ship import Ship
from wall import Wall
from controller import Controller
from bricktype import BrickType
import json
import pygame
import pygame_textinput
import time
import math
import controller
import locale
Game.init()
Paddle.init()
# draw stuff
running= True
Game.balls = [Ball(0.5, 0.1, 0.0, 0.2)]
Game.rockets = []
Game.ships = [Ship(0), Ship(2), Ship(4)]

Controller.connect("/dev/ttyUSB0")
clock = pygame.time.Clock()

FPS = 0
last_time = time.perf_counter()
start_time = last_time
last_UI_time = 0.0

in_shop = False
in_menu = True
in_gameover_screen = False
enter_name = True
in_highscore = False
last_shop_time = 0.0
last_menu_time = 0.0
last_highscore_time = 0.0
time_paused = 0.0

fullscreen = True
last_fullscreen_change = 0.0

last_rocket_time = 0.0

game_speed = 1.0

old_window_size = pygame.display.get_window_size()

pygame.mouse.set_visible(False)

paddle_price = [5, 10, 15]
shield_price = [5, 10, 20]
rocket_price = [10, 17, 25]

Game.paddle_lvl_change = 0.15
Game.shield_lvl_change = 3
Game.rocket_lvl_change = 0.5

paddle_priceText = [f"PRICE: {paddle_price[0]}", f"PRICE: {paddle_price[1]}", f"PRICE: {paddle_price[2]}", "MAX LVL"]
shield_priceText = [f"PRICE: {shield_price[0]}", f"PRICE: {shield_price[1]}", f"PRICE: {shield_price[2]}", "MAX LVL"]
rocket_priceText = [f"PRICE: {rocket_price[0]}", f"PRICE: {rocket_price[1]}", f"PRICE: {rocket_price[2]}", "MAX LVL"]

def buyPaddle():
    if Game.paddle_lvl < 3:
        if Game.coins >= paddle_price[Game.paddle_lvl]:
            Game.coins -= paddle_price[Game.paddle_lvl]
            Game.paddle_lvl += 1
def buyShield():
    if Game.shield_lvl < 3:
        if Game.coins >= shield_price[Game.shield_lvl]:
            Game.coins -= shield_price[Game.shield_lvl]
            Game.shield_lvl += 1

def buyRocket():
    if Game.rocket_lvl < 3:
        if Game.coins >= rocket_price[Game.rocket_lvl]:
            Game.coins -= rocket_price[Game.rocket_lvl]
            Game.rocket_lvl += 1

def buyItem(i):
    if i == 0:
        buyPaddle()
    elif i == 1:
        buyShield()
    elif i == 2:
        buyRocket()

item_select = 0
menu_select = 0

player_name = ""
player_text_length = 0

def save_score():
    # [["", 0, ""], ["", 0, ""], ["", 0, ""], ["", 0, ""], ["", 0, ""], ["", 0, ""], ["", 0, ""], ["", 0, ""], ["", 0, ""], ["", 0, ""]]
    with open("scoreboard.json", "r") as f:
        topTen = json.load(f)

    with open("scoreboard.json", "w") as f:
        topTen.append((player_name, int(Game.highscore), time.strftime("%d %b %Y %H:%M:%S")))
        topTen = sorted(topTen, key=lambda x: x[1])
        topTen.pop(0)
        json.dump(topTen, f)

    if player_name != "" and Game.highscore > 5.0:
        with open("highscore.txt", "a") as f:
            f.write(player_name + f" {int(Game.highscore)} " + time.strftime("%d %b %Y %H:%M:%S") + f" {round(current_time - start_time, 1)}" + "\n")

locale.setlocale(locale.LC_TIME, "de_DE")

while running:
    events = pygame.event.get()
    current_time = time.perf_counter()
    dt = current_time - last_time

    dt_1 = min(dt, 0.2)
    dt_2 = dt_1

    dt = min(dt*game_speed, 0.2)

    keys = pygame.key.get_pressed()        

    if in_shop or in_menu or in_highscore:
        start_time += current_time - last_time
        dt = 0.0
        dt_1 = 0.0

    Game.windowSize = pygame.display.get_window_size()

    escape_pressed = False

    windowChange = old_window_size[0] != Game.windowSize[0] or old_window_size[1] != Game.windowSize[1]
    for event in events:
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_e or event.key == pygame.K_LEFT and in_shop) and current_time - last_shop_time > 0.2 and not in_menu and not in_highscore:
            last_shop_time = current_time
            in_shop = not in_shop
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and current_time - last_menu_time > 0.2 and not in_highscore and not enter_name:
            last_menu_time = current_time
            in_menu = not in_menu
            in_shop = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and enter_name:
            escape_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11 or windowChange:
            if current_time - last_fullscreen_change > 0.2 or not fullscreen:
                last_fullscreen_change = current_time
                if windowChange:
                    if old_window_size[0] != Game.windowSize[0]:
                        Game.screen = pygame.display.set_mode((Game.windowSize[0], Game.windowSize[0]*9/16), pygame.RESIZABLE)
                    else:
                        Game.screen = pygame.display.set_mode((Game.windowSize[1]*16/9, Game.windowSize[1]), pygame.RESIZABLE)
                else:
                    if fullscreen:
                        Game.screen = pygame.display.set_mode((Game.width, Game.height), pygame.RESIZABLE)
                        fullscreen = False
                    else:
                        Game.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        fullscreen = True
                
                Game.windowSize = pygame.display.get_window_size()
                old_window_size = Game.windowSize

                Game.font_size = int(0.05 * Game.windowSize[1])
                Game.font = pygame.font.SysFont(None, Game.font_size)

                Game.font_size2 = int(0.065 * Game.windowSize[1])
                Game.font2 = pygame.font.SysFont(None, Game.font_size2)

                Game.textinput_custom = pygame_textinput.TextInputVisualizer(manager=Game.manager, font_object=Game.font2)
                Game.textinput_custom.cursor_width = 4
                Game.textinput_custom.antialias = True
                Game.textinput_custom.font_color = (255, 255, 255)

                Game.invader_image1 = pygame.transform.smoothscale(Game.invader_image1_original, (0.03*Game.windowSize[0], 0.04*Game.windowSize[1]))
                Game.invader_image2 = pygame.transform.smoothscale(Game.invader_image2_original, (0.03*Game.windowSize[0], 0.04*Game.windowSize[1]))
                Game.explosion_image = pygame.transform.smoothscale(Game.explosion_image_original, (0.04*Game.windowSize[0], 0.06*Game.windowSize[1]))
                Game.bomb_image = pygame.transform.smoothscale(Game.bomb_image_original, (0.03*Game.windowSize[0], 0.05*Game.windowSize[1]))
                Game.rocket_image = pygame.transform.smoothscale(Game.rocket_image_original, (0.01*Game.windowSize[0], 0.06*Game.windowSize[1]))
                Game.coin_image = pygame.transform.smoothscale(Game.coin_image_original, (0.03*Game.windowSize[0], 0.04*Game.windowSize[1]))
                Game.heart_image = pygame.transform.smoothscale(Game.heart_image_original, (0.03*Game.windowSize[0], 0.045*Game.windowSize[1]))
                Game.game_over = pygame.transform.smoothscale(Game.game_over_original, (Game.windowSize[0], Game.windowSize[1]))

                Game.brick_width = Game.windowSize[0] // Game.brick_cols
                Game.brick_height = Game.windowSize[1] // Game.brick_rows

    if Wall.brick.sum() == 0:
        #Game.lifes += 3
        Game.level += 1
        Wall.init(BrickType)
        if Game.level > 1:
            Game.highscore_mult *= 1.25
            game_speed += 0.1

    if len(Game.balls) == 0:
        if Game.lifes > 1:
            Game.lifes -= 1
        else:
            Game.gameover_sound.play()
            in_gameover_screen = True
            
            save_score()
            Game.highscore = 0.0
            Game.highscore_mult = 1.0
            Game.lifes = 3
            Game.level = 1
            game_speed = 1.0
            Wall.init(BrickType)
            Game.ships = [Ship(0), Ship(0.5), Ship(1)]
            Game.rockets = []
            Game.bombs = []
            Game.coins = 0
            Game.paddle_lvl = 0
            Game.shield_lvl = 0
            Game.rocket_lvl = 0
            in_menu = True
            enter_name = True
            player_name = ""
        Game.balls = [Ball(0.5, 0.1, 0.0, 0.2)]

    while True:
        ser_data = Controller.readdata()
        if ser_data is None:
            break
        if ser_data[0] == "A" and Paddle.damage == 0 and not in_shop and not in_menu and not in_highscore and current_time - last_rocket_time > 2-Game.rocket_lvl_change*Game.rocket_lvl:
            Game.rockets.append(Rocket(Paddle.x + Paddle.w / 2, Paddle.y, -0.8))
            Game.launch.play()
        elif ser_data[0] == "X":
            Paddle.set(ser_data[1] * 1.5)
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not in_gameover_screen:
            if event.key == pygame.K_p:
                Controller.connect("/dev/ttyUSB0")
            elif event.key == pygame.K_UP and Paddle.damage == 0 and not in_shop and not in_menu and not in_highscore and current_time - last_rocket_time > 2-Game.rocket_lvl_change*Game.rocket_lvl:
                Game.rockets.append(Rocket(Paddle.x + Paddle.w / 2, Paddle.y, -0.8))
                Game.launch.play()
                last_rocket_time = current_time
            elif event.key == pygame.K_a and not in_shop and not in_menu and not in_highscore:
                Game.balls.append(Ball(0.5, 0.1, 0.0, 0.2))
            elif event.key == pygame.K_UP:
                if in_shop:
                    item_select -= 1
                elif in_menu:
                    menu_select -= 1
            elif event.key == pygame.K_DOWN:
                if in_shop:
                    item_select += 1
                elif in_menu:
                    menu_select += 1
            elif event.key == pygame.K_RIGHT and in_shop and not in_menu and not in_highscore and current_time - last_shop_time > 0.05:
                buyItem(item_select)
                Paddle.updateSize()
            elif event.key == pygame.K_RIGHT and in_menu and current_time - last_menu_time > 0.05:
                if menu_select == 2:
                    running = False
                elif menu_select == 1:
                    in_highscore = True
                    in_menu = False
                    last_highscore_time = current_time
                elif menu_select == 0 and player_text_length > 0:
                    if enter_name:
                        player_name = f"{Game.textinput_custom.value}"
                        enter_name = False
                    in_menu = False
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_ESCAPE) and in_highscore and current_time - last_highscore_time > 0.05:
                in_highscore = False
                in_menu = True
                menu_select = 1
                
        elif event.type == pygame.KEYDOWN and in_gameover_screen:
            in_gameover_screen = False

    if keys[pygame.K_LEFT]:
        Paddle.left(dt_1)
    if keys[pygame.K_RIGHT]:
        Paddle.right(dt_1)

    pygame.Surface.fill(Game.screen, (0, 0, 0))
    Wall.draw()
    Paddle.draw(dt_1)
    Game.draw(dt)
    for s in Game.ships + Game.bombs:
        for r in Game.rockets + Game.balls:
            if s.alive and not s.hit and not r.hit:
                dist = math.hypot(r.x - s.x, r.y - s.y)
                if dist <= 0.015:
                    s.hit = True
                    r.hit = True
                    Game.exploding.play()

    if current_time - last_UI_time > 0.2:
        last_UI_time = current_time
        dt_2 = max(dt_2, 0.0001)
        FPS = round(1/dt_2, 2)
    fps_text = Game.font.render(f"FPS: {FPS}", True, (255, 255, 255))
    rect = fps_text.get_rect(topright=(0.995*Game.windowSize[0], 0.005*Game.windowSize[1]))
    Game.screen.blit(fps_text, rect)

    rainbowColor = math.sin(0.5*current_time)
    rainbowColor = HSVtoRGB(rainbowColor, 1.0, 1.0)

    highscore_text = Game.font.render(f"SCORE: {int(Game.highscore)}", True, (rainbowColor))
    rect = highscore_text.get_rect(center=(0.5*Game.windowSize[0], 0.05*Game.windowSize[1]))
    Game.screen.blit(highscore_text, rect)

    highscore_mult_text = Game.font.render(f"MULT: {round(Game.highscore_mult, 2)}x", True, (255, 255, 255))
    rect = highscore_mult_text.get_rect(midtop=(0.5*Game.windowSize[0], 0.08*Game.windowSize[1]))
    Game.screen.blit(highscore_mult_text, rect)

    speed_text = Game.font.render(f"SPEED: {round(game_speed, 2)}x", True, (255, 255, 255))
    rect = speed_text.get_rect(topright=(0.995*Game.windowSize[0], 0.08*Game.windowSize[1]))
    Game.screen.blit(speed_text, rect)

    time_text = Game.font.render(f"TIME: {round(current_time - start_time, 1)}s", True, (255, 255, 255))
    rect = time_text.get_rect(topleft=(0.005*Game.windowSize[0], 0.08*Game.windowSize[1]))
    Game.screen.blit(time_text, rect)


    if in_shop:
        color1 = (100, 20, 0)
        color2 = (0, 0, 0)
        color3 = (50, 50, 55)
        color4 = (212, 175, 55)
        pygame.draw.rect(Game.screen, color1, (0.1*Game.windowSize[0], 0.1*Game.windowSize[1], 0.8*Game.windowSize[0], 0.8*Game.windowSize[1]))
        pygame.draw.rect(Game.screen, color2, (0.11*Game.windowSize[0], 0.12*Game.windowSize[1], 0.78*Game.windowSize[0], 0.76*Game.windowSize[1]))

        shop_text = Game.font2.render(f"$ SHOP $", True, (255, 200, 200))
        rect = shop_text.get_rect(midtop=(0.5*Game.windowSize[0], 0.15*Game.windowSize[1]))
        Game.screen.blit(shop_text, rect)

        shop_text = Game.font2.render(f"COINS: {Game.coins}", True, (255, 200, 200))
        rect = shop_text.get_rect(midtop=(0.65*Game.windowSize[0], 0.15*Game.windowSize[1]))
        Game.screen.blit(shop_text, rect)
            
        item_select = item_select % 3

        if item_select == 0:
            pygame.draw.rect(Game.screen, color4, (0.21*Game.windowSize[0], 0.24*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))
        elif item_select == 1:
            pygame.draw.rect(Game.screen, color4, (0.21*Game.windowSize[0], 0.44*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))
        elif item_select == 2:
            pygame.draw.rect(Game.screen, color4, (0.21*Game.windowSize[0], 0.64*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))


        pygame.draw.rect(Game.screen, color3, (0.2*Game.windowSize[0], 0.25*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))
        pygame.draw.rect(Game.screen, color3, (0.2*Game.windowSize[0], 0.45*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))
        pygame.draw.rect(Game.screen, color3, (0.2*Game.windowSize[0], 0.65*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))

        shop_item_1 = Game.font2.render(f"BIGGER PADDLE Lvl.{Game.paddle_lvl} ", True, (255, 255, 255))
        rect = shop_item_1.get_rect(midleft=(0.25*Game.windowSize[0], 0.3*Game.windowSize[1]))
        Game.screen.blit(shop_item_1, rect)

        shop_item_2 = Game.font2.render(f"SHIELD Lvl.{Game.shield_lvl} ", True, (255, 255, 255))
        rect = shop_item_2.get_rect(midleft=(0.25*Game.windowSize[0], 0.5*Game.windowSize[1]))
        Game.screen.blit(shop_item_2, rect)

        shop_item_3 = Game.font2.render(f"ROCKETS Lvl.{Game.rocket_lvl} ", True, (255, 255, 255))
        rect = shop_item_3.get_rect(midleft=(0.25*Game.windowSize[0], 0.7*Game.windowSize[1]))
        Game.screen.blit(shop_item_3, rect)

        shop_item_1_price = Game.font.render(f"{paddle_priceText[Game.paddle_lvl]} ", True, (255, 255, 255))
        rect = shop_item_1_price.get_rect(center=(0.65*Game.windowSize[0], 0.325*Game.windowSize[1]))
        Game.screen.blit(shop_item_1_price, rect)

        shop_item_2_price = Game.font.render(f"{shield_priceText[Game.shield_lvl]} ", True, (255, 255, 255))
        rect = shop_item_2_price.get_rect(center=(0.65*Game.windowSize[0], 0.525*Game.windowSize[1]))
        Game.screen.blit(shop_item_2_price, rect)

        shop_item_3_price = Game.font.render(f"{rocket_priceText[Game.rocket_lvl]} ", True, (255, 255, 255))
        rect = shop_item_3_price.get_rect(center=(0.65*Game.windowSize[0], 0.725*Game.windowSize[1]))
        Game.screen.blit(shop_item_3_price, rect)

        shop_item_1_info_1 = Game.font.render(f"SIZE: +{Game.paddle_lvl*int(100*Game.paddle_lvl_change)}%", True, (255, 255, 255))
        rect = shop_item_1_info_1.get_rect(midleft=(0.25*Game.windowSize[0], 0.34*Game.windowSize[1]))
        Game.screen.blit(shop_item_1_info_1, rect)

        shop_item_2_info_1 = Game.font.render(f"DURATION: {5+Game.shield_lvl*Game.shield_lvl_change}s", True, (255, 255, 255))
        rect = shop_item_2_info_1.get_rect(midleft=(0.25*Game.windowSize[0], 0.54*Game.windowSize[1]))
        Game.screen.blit(shop_item_2_info_1, rect)

        shop_item_3_info_1 = Game.font.render(f"COOLDOWN: {2-Game.rocket_lvl*Game.rocket_lvl_change}s", True, (255, 255, 255))
        rect = shop_item_3_info_1.get_rect(midleft=(0.25*Game.windowSize[0], 0.74*Game.windowSize[1]))
        Game.screen.blit(shop_item_3_info_1, rect)

        if item_select == 0 and Game.paddle_lvl < 3:
            shop_item_arrow = Game.font.render(f"->", True, (255, 255, 255))
            rect = shop_item_arrow.get_rect(midright=(0.46*Game.windowSize[0], 0.34*Game.windowSize[1]))
            Game.screen.blit(shop_item_arrow, rect)

            shop_item_1_info_2 = Game.font.render(f"+{(Game.paddle_lvl+1)*int(100*Game.paddle_lvl_change)}%", True, (144, 255, 144))
            rect = shop_item_1_info_2.get_rect(midleft=(0.47*Game.windowSize[0], 0.34*Game.windowSize[1]))
            Game.screen.blit(shop_item_1_info_2, rect)
        elif item_select == 1 and Game.shield_lvl < 3:
            shop_item_arrow = Game.font.render(f"->", True, (255, 255, 255))
            rect = shop_item_arrow.get_rect(midright=(0.46*Game.windowSize[0], 0.54*Game.windowSize[1]))
            Game.screen.blit(shop_item_arrow, rect)

            shop_item_2_info_2 = Game.font.render(f"{5+(Game.shield_lvl+1)*Game.shield_lvl_change}s", True, (144, 255, 144))
            rect = shop_item_2_info_2.get_rect(midleft=(0.47*Game.windowSize[0], 0.54*Game.windowSize[1]))
            Game.screen.blit(shop_item_2_info_2, rect)
        elif item_select == 2 and Game.rocket_lvl < 3:
            shop_item_arrow = Game.font.render(f"->", True, (255, 255, 255))
            rect = shop_item_arrow.get_rect(midright=(0.46*Game.windowSize[0], 0.74*Game.windowSize[1]))
            Game.screen.blit(shop_item_arrow, rect)

            shop_item_3_info_2 = Game.font.render(f"{2-(Game.rocket_lvl+1)*Game.rocket_lvl_change}s", True, (144, 255, 144))
            rect = shop_item_3_info_2.get_rect(midleft=(0.47*Game.windowSize[0], 0.74*Game.windowSize[1]))
            Game.screen.blit(shop_item_3_info_2, rect)


    else:
        item_select = 0

    if in_menu:
        color1 = (100, 20, 0)
        color2 = (0, 0, 0)
        color3 = (50, 50, 55)
        color4 = (212, 175, 55)
        pygame.draw.rect(Game.screen, color1, (0.1*Game.windowSize[0], 0.1*Game.windowSize[1], 0.8*Game.windowSize[0], 0.8*Game.windowSize[1]))
        pygame.draw.rect(Game.screen, color2, (0.11*Game.windowSize[0], 0.12*Game.windowSize[1], 0.78*Game.windowSize[0], 0.76*Game.windowSize[1]))

        shop_text = Game.font2.render(f"MENU", True, (255, 200, 200))
        rect = shop_text.get_rect(midtop=(0.5*Game.windowSize[0], 0.15*Game.windowSize[1]))
        Game.screen.blit(shop_text, rect)

            
        menu_select = menu_select % 3

        if menu_select == 0:
            pygame.draw.rect(Game.screen, color4, (0.21*Game.windowSize[0], 0.24*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))
        elif menu_select == 1:
            pygame.draw.rect(Game.screen, color4, (0.21*Game.windowSize[0], 0.44*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))
        elif menu_select == 2:
            pygame.draw.rect(Game.screen, color4, (0.21*Game.windowSize[0], 0.64*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))


        pygame.draw.rect(Game.screen, color3, (0.2*Game.windowSize[0], 0.25*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))
        pygame.draw.rect(Game.screen, color3, (0.2*Game.windowSize[0], 0.45*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))
        pygame.draw.rect(Game.screen, color3, (0.2*Game.windowSize[0], 0.65*Game.windowSize[1], 0.6*Game.windowSize[0], 0.15*Game.windowSize[1]))

        if enter_name:
            menu_item_1 = Game.font2.render(f"ENTER NAME:", True, (255, 255, 255))
            rect = menu_item_1.get_rect(midleft=(0.25*Game.windowSize[0], 0.325*Game.windowSize[1]))
            Game.screen.blit(menu_item_1, rect)

            if not escape_pressed and not in_gameover_screen:
                Game.textinput_custom.update(events)
            player_text_length = len(Game.textinput_custom.value)
            rect = Game.textinput_custom.surface.get_rect(midleft=(0.45*Game.windowSize[0], 0.325*Game.windowSize[1]))
            Game.screen.blit(Game.textinput_custom.surface, rect)
        else:
            menu_item_1 = Game.font2.render(f"CONTINUE", True, (255, 255, 255))
            rect = menu_item_1.get_rect(midleft=(0.25*Game.windowSize[0], 0.325*Game.windowSize[1]))
            Game.screen.blit(menu_item_1, rect)

        menu_item_2 = Game.font2.render(f"SCOREBOARD", True, (255, 255, 255))
        rect = menu_item_2.get_rect(midleft=(0.25*Game.windowSize[0], 0.525*Game.windowSize[1]))
        Game.screen.blit(menu_item_2, rect)

        menu_item_3 = Game.font2.render(f"QUIT", True, (255, 50, 50))
        rect = menu_item_3.get_rect(midleft=(0.25*Game.windowSize[0], 0.725*Game.windowSize[1]))
        Game.screen.blit(menu_item_3, rect)
    else:
        menu_select = 0

    if in_highscore:
        color1 = (100, 20, 0)
        color2 = (0, 0, 0)
        color3 = (50, 50, 55)
        color4 = (212, 175, 55)
        pygame.draw.rect(Game.screen, color1, (0.1*Game.windowSize[0], 0.1*Game.windowSize[1], 0.8*Game.windowSize[0], 0.8*Game.windowSize[1]))
        pygame.draw.rect(Game.screen, color2, (0.11*Game.windowSize[0], 0.12*Game.windowSize[1], 0.78*Game.windowSize[0], 0.76*Game.windowSize[1]))

        shop_text = Game.font2.render(f"SCOREBOARD", True, (255, 200, 200))
        rect = shop_text.get_rect(midtop=(0.5*Game.windowSize[0], 0.15*Game.windowSize[1]))
        Game.screen.blit(shop_text, rect)

        with open("scoreboard.json", "r") as f:
            topTen = json.load(f)

        for x in range(0, 10):
            start_height = Game.windowSize[1] * 0.75
            spacing = Game.windowSize[1] * 0.05
            height = start_height - (x * spacing)
            
            name = Game.font2.render(topTen[x][0], True, (255, 255, 255))
            rect = name.get_rect(midleft=(Game.windowSize[0] * 0.155, height))
            Game.screen.blit(name, rect)

            date = Game.font.render(topTen[x][2], True, (255, 255, 255))
            rect = date.get_rect(midleft=(Game.windowSize[0] * 0.425, height))
            Game.screen.blit(date, rect)

            score = Game.font2.render(f"{int(topTen[x][1])}", True, (255, 255, 255))
            rect = score.get_rect(midleft=(Game.windowSize[0] * 0.7, height))
            Game.screen.blit(score, rect)
            
    if in_gameover_screen:
        Game.screen.fill((0,0,0))
        pos = Game.game_over.get_rect()
        pos.midtop = (0.5*Game.windowSize[0], 0)
        Game.screen.blit(Game.game_over, pos)
    
    last_time = current_time
    pygame.display.update()
    
    #clock.tick(30)
    



# save highscore
save_score()

# done
pygame.quit()
