import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Screen setup
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)

# Snake and food setup
def random_food_position():
    return (
        random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE),
        random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE)
    )

def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(position):
    pygame.draw.rect(screen, RED, (*position, CELL_SIZE, CELL_SIZE))

def show_text(text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, rect)

def main():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"
    food = random_food_position()
    score = 0
    speed = 10
    game_over = False
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w] and direction != "DOWN":
                    direction = "UP"
                elif event.key in [pygame.K_DOWN, pygame.K_s] and direction != "UP":
                    direction = "DOWN"
                elif event.key in [pygame.K_LEFT, pygame.K_a] and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_p:  # Pause
                    paused = not paused
                elif event.key == pygame.K_r:  # Restart
                    main()

        if paused or game_over:
            if game_over:
                screen.fill(BLACK)
                show_text("Game Over", big_font, RED, -30)
                show_text(f"Score: {score}", font, WHITE, 20)
                show_text("Press R to Restart or Q to Quit", font, GRAY, 60)
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
            continue

        # Move snake
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        # Check collisions
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            new_head in snake
        ):
            game_over = True
            continue

        # Check if food eaten
        if new_head == food:
            score += 1
            food = random_food_position()
        else:
            snake.pop()  # remove tail if no food eaten

        snake.insert(0, new_head)

        # Drawing
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    main()
