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
small_font = pygame.font.SysFont("Outfit", 30)

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

def draw_text(text, font, color, y_offset=0):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surf, text_rect)

def draw_winner(winner_text, color):
    screen.fill(BLACK)
    draw_text(winner_text, font, color)
    pygame.display.flip()
    pygame.time.delay(3000)

def menu():
    selected_index = 0
    options = ["START GAME", "QUIT"]
    
    while True:
        screen.fill(BLACK)
        
        # Draw background elements
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, (30, 30, 30), (WIDTH // 2 - 2, y, 4, 20))

        draw_text("NEON PING PONG", font, CYAN, -150)

        # Draw options with highlighting
        for i, option in enumerate(options):
            color = WHITE if i == selected_index else (100, 100, 100)
            prefix = "> " if i == selected_index else "  "
            
            # Draw selection highlight
            text_surf = small_font.render(prefix + option, True, color)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (i * 60)))
            
            if i == selected_index:
                # Add a subtle glow to selection
                for g in range(3):
                    glow_surf = small_font.render(prefix + option, True, (0, 150, 150) if i == 0 else (150, 0, 150))
                    glow_rect = glow_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (i * 60)))
                    screen.blit(glow_surf, glow_rect.inflate(g*2, g*2))

            screen.blit(text_surf, text_rect)

        # Decorative neon paddles
        pygame.draw.rect(screen, CYAN, (50, HEIGHT // 2 - 50, 15, 100))
        pygame.draw.rect(screen, MAGENTA, (WIDTH - 65, HEIGHT // 2 - 50, 15, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        return # Start game
                    if selected_index == 1:
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

def game_loop():
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
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return # Back to menu

        # Movements
        p1.move(pygame.K_w, pygame.K_s)
        p2.move(pygame.K_UP, pygame.K_DOWN)
        ball.move()

        # Collisions with paddles
        if ball.rect.colliderect(p1.rect) or ball.rect.colliderect(p2.rect):
            ball.speed_x *= -1
            # Increase speed slightly after collision
            ball.speed_x *= 1.05
            ball.speed_y *= 1.05

        # Scoring
        if ball.rect.left <= 0:
            score2 += 1
            ball.reset()
        if ball.rect.right >= WIDTH:
            score1 += 1
            ball.reset()

        # Check for winner
        if score1 >= WINNING_SCORE:
            draw_winner("LEFT PLAYER WINS! 🏆", CYAN)
            running = False
        elif score2 >= WINNING_SCORE:
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

def main():
    while True:
        menu()
        game_loop()

if __name__ == "__main__":
    main()
