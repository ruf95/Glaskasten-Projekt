import pygame

class Game:
    width, height  = None, None
    screen = None
    brick_rows, brick_cols = 30,10
    brick_width, brick_height = 80,20
    balls = []
    rockets = []
    ships = []
    bombs = []
    font = None
    lifes = 0
    level = 0
    current_score = 0

    def init():
        Game.width = Game.brick_cols * Game.brick_width
        Game.height = Game.brick_rows * Game.brick_height
        pygame.init()
        Game.screen = pygame.display.set_mode((Game.width, Game.height))
        Game.font = pygame.font.SysFont(None,24)
        Game.exploding = pygame.mixer.Sound("breakout/asp-ulm-data/exploding.wav")
        Game.bounce = pygame.mixer.Sound("breakout/asp-ulm-data/bounce.mp3")
        Game.launch = pygame.mixer.Sound("breakout/asp-ulm-data/launch.wav")

    def draw():
        for item in Game.balls + Game.rockets + Game.ships + Game.bombs:
            item.draw()
            item.move()
        Game.balls = [item for item in Game.balls if item.alive]
        Game.rockets = [item for item in Game.rockets if item.alive]
        Game.ships = [item for item in Game.ships if item.alive]
        Game.bombs = [item for item in Game.bombs if item.alive]
        label = f"Level {Game.level} Lifes {Game.lifes}"
        text = Game.font.render(label,True,(255,255,255))
        text_rect = text.get_rect(topleft=(10,10))
        current_score_label = f"Score: {Game.current_score}"
        current_score_text = Game.font.render(current_score_label,True,(255,255,255))
        score_rect = current_score_text.get_rect(topright=(430,10))
        Game.screen.blit(text, text_rect)
        Game.screen.blit(current_score_text, score_rect)

    def quit():
        pygame.quit()
