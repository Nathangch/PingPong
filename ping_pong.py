import pygame
import sys
import random

# Initializing Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
FPS = 60
WINNING_SCORE = 20

# Screen configuration
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Ping Pong 🚀")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Outfit", 50)

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 7

    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, surface):
        # Draw neon glow effect
        for i in range(4):
            pygame.draw.rect(surface, self.color, self.rect.inflate(i*2, i*2), 1)
        pygame.draw.rect(surface, self.color, self.rect)

class Ball:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.speed_x = 5 * random.choice([1, -1])
        self.speed_y = 5 * random.choice([1, -1])
        self.initial_speed = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ceiling and floor collision
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = self.initial_speed * random.choice([1, -1])
        self.speed_y = self.initial_speed * random.choice([1, -1])

    def draw(self, surface):
        # Draw neon glow effect
        for i in range(5):
            pygame.draw.circle(surface, self.color, self.rect.center, (self.rect.width // 2) + i, 1)
        pygame.draw.ellipse(surface, self.color, self.rect)

def draw_winner(winner_text, color):
    text = font.render(winner_text, True, color)
    # Background for text to make it readable
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 20))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

def main():
    # Game objects
    p1 = Paddle(20, HEIGHT // 2 - 50, 15, 100, CYAN)
    p2 = Paddle(WIDTH - 35, HEIGHT // 2 - 50, 15, 100, MAGENTA)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 15, WHITE)

    score1 = 0
    score2 = 0

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Movements
        p1.move(pygame.K_w, pygame.K_s)
        p2.move(pygame.K_UP, pygame.K_DOWN)
        ball.move()

        # Collisions with paddles
        if ball.rect.colliderect(p1.rect) or ball.rect.colliderect(p2.rect):
            ball.speed_x *= -1
            # Increase speed slightly after collision
            ball.speed_x *= 1.1
            ball.speed_y *= 1.1

        # Scoring
        if ball.rect.left <= 0:
            score2 += 1
            ball.reset()
        if ball.rect.right >= WIDTH:
            score1 += 1
            ball.reset()

        # Check for winner
        if score1 >= WINNING_SCORE:
            screen.fill(BLACK)
            p1.draw(screen)
            p2.draw(screen)
            ball.draw(screen)
            draw_winner("LEFT PLAYER WINS! 🏆", CYAN)
            running = False
        elif score2 >= WINNING_SCORE:
            screen.fill(BLACK)
            p1.draw(screen)
            p2.draw(screen)
            ball.draw(screen)
            draw_winner("RIGHT PLAYER WINS! 🏆", MAGENTA)
            running = False
        
        if not running:
            break

        # Drawing
        screen.fill(BLACK)
        
        # Center line (dotted neon)
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, (50, 50, 50), (WIDTH // 2 - 2, y, 4, 20))

        p1.draw(screen)
        p2.draw(screen)
        ball.draw(screen)

        # Draw scores
        score_text1 = font.render(str(score1), True, CYAN)
        score_text2 = font.render(str(score2), True, MAGENTA)
        screen.blit(score_text1, (WIDTH // 4, 30))
        screen.blit(score_text2, (WIDTH * 3 // 4 - score_text2.get_width(), 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
