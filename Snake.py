import pygame
import random

pygame.init()

#Fenstergröße
Width = 600
height = 400
Block = 20

#Farben
Black = (0, 0, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
White = (255, 255, 255)

screen = pygame.display.set_mode((Width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def game():
    snake = [(100, 100)]
    direction = (Block, 0)

    food = (
        random.randrange(0, Width, Block),
        random.randrange(0, height, Block)
    )

    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running == False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = (0, -Block)
                elif event.key == pygame.K_DOWN:
                    direction = (0, Block)
                elif event.key == pygame.K_LEFT:
                    direction = (-Block, 0)
                elif event.key == pygame.K_RIGHT:
                    direction = (Block, 0)

        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]
        new_head = (head_x, head_y)

        if (
            head_x < 0 or head_x >= Width or 
            head_y < 0 or head_y >= height
        ):
            running = False
        if new_head in snake:
            running = False

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = (
                random.randrange(0, Width, Block),
                random.randrange(0, height, Block)
            )
        else:
            snake.pop()

        screen.fill(Black)

        pygame.draw.rect(screen, Red,
                         (food[0], food[1], Block, Block))
        
        for segment in snake:
            pygame.draw.rect(screen, Green,
                             (segment[0], segment[1], Block, Block))
            
        draw_text(f"Punkte : {score}", White, 10, 10)

        pygame.display.update()

        clock.tick(10)

    pygame.quit()

game()


        