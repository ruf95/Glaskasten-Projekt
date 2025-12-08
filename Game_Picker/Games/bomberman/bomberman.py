import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Platzhalter-Spiel")

font = pygame.font.SysFont(None, 64)
text_surface = font.render(
    "Hier könnte ein Bomberman Spiel stattfinden :-)", True, (255, 255, 255)
)

screen_rect = screen.get_rect()
text_rect = text_surface.get_rect(center=screen_rect.center)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
