import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set title of the window
pygame.display.set_caption('Arcanoid')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (106, 159, 181)
RED = (255, 0, 0)

# Define font
font = pygame.font.Font(None, 30)

# Game variables
ball_x = screen_width / 2
ball_y = screen_height / 2
ball_speed_x = 5
ball_speed_y = 5
paddle_x = screen_width / 2
paddle_y = screen_height - 50
paddle_speed = 20

attempts_left = 5

blocks = []
for _ in range(10):
    x = random.randint(0, screen_width // 2)
    y = random.randint(50, screen_height // 2)
    blocks.append([x, y])  # Используем списки вместо кортежей

def draw_menu():
    screen.fill(BLACK)
    title_surface = font.render("Arcanoid Game", True, WHITE)
    start_surface = font.render("Press SPACE to start", True, WHITE)
    screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, screen_height // 2 - 50))
    screen.blit(start_surface, (screen_width // 2 - start_surface.get_width() // 2, screen_height // 2))
    pygame.display.flip()


def main():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, blocks, attempts_left

    # Игра не начнется до нажатия SPACE
    game_active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True  # Запуск игры

        if not game_active:
            draw_menu()  # Рисуем меню
            continue  # Переходим к следующему кадру

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - 100:
            paddle_x += paddle_speed

        # Clear screen
        screen.fill(BLACK)

        text_surface = font.render(f"Attempts left: {attempts_left}", True, RED)
        screen.blit(text_surface, (screen_width - 150, 20))

        # Game loop
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Collision with edges
        if ball_y <= 0:
            ball_speed_y *= -1
        if ball_x <= 0 or ball_x >= screen_width:
            ball_speed_x *= -1

        # Collision with paddle
        if ball_y + 10 >= paddle_y and paddle_x <= ball_x <= paddle_x + 100:
            ball_speed_y *= -1

        # Collision with blocks
        for block in blocks[:]:
            if (block[0] <= ball_x <= block[0] + 50 and block[1] <= ball_y <= block[1] + 20):
                blocks.remove(block)
                ball_speed_y *= -1

        # Draw the ball
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), 10)

        # Draw the paddle
        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, 100, 10))

        for block in blocks:
            pygame.draw.rect(screen, WHITE, (block[0], block[1], 50, 20))

        if ball_y > paddle_y + 10:
            attempts_left -= 1
            ball_x = screen_width / 2
            ball_y = screen_height / 2

        if attempts_left == 0:
            attempts_left = 5
            blocks = []
            for _ in range(10):
                x = random.randint(0, screen_width // 2)
                y = random.randint(50, screen_height // 2)
                blocks.append([x, y])

        # Update screen
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
    
