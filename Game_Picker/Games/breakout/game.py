import pygame
import pygame_textinput

class Game:
    width, height = None, None
    screen = None
    brick_rows = 30
    brick_cols = 15

    balls = []
    rockets = []
    ships = []
    bombs = []
    coin = []
    hearts = []
    font = None
    lifes = 3
    level = 0
    def init():
        Game.brick_width = 80
        Game.brick_height = 20

        Game.highscore = 0.0
        Game.highscore_mult = 1.0

        Game.width = Game.brick_cols * Game.brick_width 
        Game.height = Game.brick_rows * Game.brick_height
        pygame.init()

        Game.bomb_image = pygame.image.load("data/bomb.png")
        Game.explosion_image = pygame.image.load("data/explosion.png")
        Game.invader_image1 = pygame.image.load("data/space_invader0.png")
        Game.invader_image2 = pygame.image.load("data/space_invader2.png")
        Game.rocket_image = pygame.image.load("data/rocket0.png")
        Game.coin_image = pygame.image.load("data/coin.png")
        Game.heart_image = pygame.image.load("data/heart.png")
        Game.game_over = pygame.image.load("data/Gameover.png")

        Game.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        Game.windowSize = pygame.display.get_window_size()

        Game.font_size = int(0.05 * Game.windowSize[1])
        Game.font = pygame.font.SysFont(None, Game.font_size)

        Game.font_size2 = int(0.065 * Game.windowSize[1])
        Game.font2 = pygame.font.SysFont(None, Game.font_size2)

        Game.manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 20)
        Game.textinput_custom = pygame_textinput.TextInputVisualizer(manager=Game.manager, font_object=Game.font2)
        Game.textinput_custom.cursor_width = 4
        Game.textinput_custom.antialias = True
        Game.textinput_custom.font_color = (255, 255, 255)

        Game.brick_width = Game.windowSize[0] // Game.brick_cols
        Game.brick_height = Game.windowSize[1] // Game.brick_rows

        Game.exploding = pygame.mixer.Sound("data/exploding.wav")
        Game.bounce = pygame.mixer.Sound("data/bounce.mp3")
        Game.launch = pygame.mixer.Sound("data/launch.wav")
        Game.gameover_sound = pygame.mixer.Sound("data/gameover.mp3")

        Game.bomb_image_original = pygame.Surface.convert_alpha(Game.bomb_image)
        Game.explosion_image_original = pygame.Surface.convert_alpha(Game.explosion_image)
        Game.invader_image1_original = pygame.Surface.convert_alpha(Game.invader_image1)
        Game.invader_image2_original = pygame.Surface.convert_alpha(Game.invader_image2)
        Game.rocket_image_original = pygame.Surface.convert_alpha(Game.rocket_image)
        Game.rocket_image_original = pygame.Surface.convert_alpha(Game.rocket_image)
        Game.coin_image_original = pygame.Surface.convert_alpha(Game.coin_image)
        Game.heart_image_original = pygame.Surface.convert_alpha(Game.heart_image)
        Game.game_over_original = pygame.Surface.convert_alpha(Game.game_over)

        Game.invader_image1 = pygame.transform.smoothscale(Game.invader_image1_original, (0.03*Game.windowSize[0], 0.04*Game.windowSize[1]))
        Game.invader_image2 = pygame.transform.smoothscale(Game.invader_image2_original, (0.03*Game.windowSize[0], 0.04*Game.windowSize[1]))
        Game.explosion_image = pygame.transform.smoothscale(Game.explosion_image_original, (0.04*Game.windowSize[0], 0.06*Game.windowSize[1]))
        Game.bomb_image = pygame.transform.smoothscale(Game.bomb_image_original, (0.03*Game.windowSize[0], 0.05*Game.windowSize[1]))
        Game.rocket_image = pygame.transform.smoothscale(Game.rocket_image_original, (0.01*Game.windowSize[0], 0.06*Game.windowSize[1]))
        Game.coin_image = pygame.transform.smoothscale(Game.coin_image_original, (0.03*Game.windowSize[0], 0.04*Game.windowSize[1]))
        Game.heart_image = pygame.transform.smoothscale(Game.heart_image_original, (0.03*Game.windowSize[0], 0.045*Game.windowSize[1]))
        Game.game_over = pygame.transform.smoothscale(Game.game_over_original, (Game.windowSize[0], Game.windowSize[1]))

        Game.paddle_lvl = 0
        Game.shield_lvl = 0
        Game.rocket_lvl = 0

        Game.coins = 0

        pygame.display.set_icon(Game.invader_image1)
        pygame.display.set_caption("Breakout")
    def draw(dt):
        for item in Game.balls + Game.rockets + Game.ships + Game.bombs + Game.coin + Game.hearts:
            item.draw(dt)
            item.move(dt)
        Game.balls = [item for item in Game.balls if item.alive]
        Game.rockets = [item for item in Game.rockets if item.alive]
        Game.ships = [item for item in Game.ships if item.alive]
        Game.bombs = [item for item in Game.bombs if item.alive]
        Game.coin = [item for item in Game.coin if item.alive]
        Game.hearts = [item for item in Game.hearts if item.alive]
        label = f"Level {Game.level} Lifes {Game.lifes}"
        text = Game.font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(topleft=(0.005*Game.windowSize[0], 0.005*Game.windowSize[1]))
        Game.screen.blit(text, text_rect)
    def quit():
        pygame.quit()
