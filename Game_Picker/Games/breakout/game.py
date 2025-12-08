import pygame
import os

class Game:
    width, height = None, None
    scale_x = None
    screen = None
    brick_rows = None
    brick_cols = None
    brick_width = 120
    brick_height = 30
    balls = []
    rockets = []
    ships = []
    bombs = []
    scores = []
    font = None
    lifes = 0
    hard = 0
    level = 0
    ammo = 0
    ammo_refill = 0
    score_total = 0
    score = None
    reverse = 0

    def init():
        from score import Score
        from rocket import Rocket
        Game.score = Score
        Game.rocket = Rocket
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Startet zentriert (optional)
        os.environ['SDL_VIDEO_FULLSCREEN_HEAD'] = '0'  # Für bestimmte SDL-Versionen auf Pi
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        Game.display = pygame.display.set_mode((0, 0), flags)
        Game.display_w, Game.display_h = Game.display.get_size()

        Game.brick_rows = Game.display_h // Game.brick_height
        Game.brick_cols = Game.display_w // Game.brick_width

        Game.width = Game.brick_cols * Game.brick_width
        Game.height = Game.brick_rows * Game.brick_height
        Game.scale_x = Game.width / 1600

        Game.display_x = (Game.display_w - Game.width) // 2
        Game.display_y = (Game.display_h - Game.height) // 2
        Game.screen = pygame.Surface((Game.width, Game.height))

        Game.font = pygame.font.SysFont("monospace", 20)
        Game.exploding = pygame.mixer.Sound("data/exploding.wav")
        Game.bounce = pygame.mixer.Sound("data/bounce.mp3")
        Game.launch = pygame.mixer.Sound("data/launch.wav")
        Game.control_normal = pygame.mixer.Sound("data/control_normal.wav")
        Game.control_normal.set_volume(1)
        Game.control_reverse = pygame.mixer.Sound("data/control_reverse.wav")
        Game.control_reverse.set_volume(0.4)

        Game.heart_mode = pygame.mixer.Sound("data/Module.wav")
        Game.heart = 0
        Game.heart_rate = 5
        Game.score_total = 0

    def reset():
        Game.lifes = 3
        Game.level = 1
        Game.ships = []
        Game.bombs = []
        Game.hearts = []
        Game.rockets = []
        Game.reverse = 0
        Game.score_total = 0

    def set_heart():
        if Game.heart == 0:
            Game.heart_mode.play()
        Game.heart = 30 * 60

    def set_reverse():
        Game.control_reverse.play()
        Game.reverse = 30 * 15

    def add_score(x, y, val):
        Game.scores.append(Game.score(x, y, val))
        new_score = Game.score_total + val
        if new_score // 2500 > Game.score_total // 2500:
            Game.lifes += 1
        Game.score_total = new_score

    def draw():
        if Game.heart:
            Game.heart -= 1
            if Game.heart == 0:
                for h in Game.hearts:
                    Game.rockets.append(Game.rocket(h.x, h.y, -20))
                    h.alive = False
                    Game.launch.play()
        if Game.reverse:
            Game.reverse -= 1
            if Game.reverse == 0:
                Game.control_normal.play()
        if Game.ammo_refill == 0:
            Game.ammo_refill = 30 * 10
            Game.ammo = 40
        else:
            Game.ammo_refill -= 1
        for item in Game.balls + Game.rockets \
                + Game.ships + Game.bombs + Game.scores + Game.hearts:
            item.draw()
            item.move()
        Game.balls = [item for item in Game.balls if item.alive]
        Game.rockets = [item for item in Game.rockets if item.alive]
        Game.ships = [item for item in Game.ships if item.alive]
        Game.bombs = [item for item in Game.bombs if item.alive]
        Game.scores = [item for item in Game.scores if item.alive]
        Game.hearts = [item for item in Game.hearts if item.alive]
        label = f" Level {Game.level:3}  |  "
        label += f"Lifes {Game.lifes:3}  |  "
        label += f"Ammo {Game.ammo:>3}  |  "
        label += f"Score {Game.score_total:5}  "
        text = Game.font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(topleft=(10, 10))
        Game.screen.blit(text, text_rect)


    def quit():
        pygame.quit()
