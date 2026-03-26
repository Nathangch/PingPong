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
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

COLORS = [CYAN, MAGENTA, YELLOW, GREEN, RED, BLUE, ORANGE, WHITE]
COLOR_NAMES = ["CYAN", "MAGENTA", "YELLOW", "GREEN", "RED", "BLUE", "ORANGE", "WHITE"]

PLAYER1_COLOR = CYAN
PLAYER2_COLOR = MAGENTA
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

    def move_cpu(self, ball_rect):
        # Simple AI: Follow the ball's center with a bit of "smoothness"
        # We add a small chance to "lose focus" or limit the reaction speed
        if self.rect.centery < ball_rect.centery - 10 and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed - 1 # Slightly slower for balance
        elif self.rect.centery > ball_rect.centery + 10 and self.rect.top > 0:
            self.rect.y -= self.speed - 1

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

def color_selection_menu():
    global PLAYER1_COLOR, PLAYER2_COLOR
    p1_index = COLORS.index(PLAYER1_COLOR)
    p2_index = COLORS.index(PLAYER2_COLOR)
    selected_row = 0 # 0 for P1, 1 for P2, 2 for Back

    while True:
        screen.fill(BLACK)
        draw_text("CHOOSE COLORS", font, WHITE, -200)

        # Player 1 selection
        p1_text = f"PLAYER 1: {COLOR_NAMES[p1_index]}"
        p1_color = WHITE if selected_row == 0 else (100, 100, 100)
        draw_text(p1_text, small_font, p1_color, -50)
        pygame.draw.rect(screen, COLORS[p1_index], (WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 20))

        # Player 2 selection
        p2_text = f"PLAYER 2: {COLOR_NAMES[p2_index]}"
        p2_color = WHITE if selected_row == 1 else (100, 100, 100)
        draw_text(p2_text, small_font, p2_color, 50)
        pygame.draw.rect(screen, COLORS[p2_index], (WIDTH // 2 - 50, HEIGHT // 2 + 80, 100, 20))

        # Back option
        back_color = WHITE if selected_row == 2 else (100, 100, 100)
        draw_text("BACK", small_font, back_color, 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_row = (selected_row - 1) % 3
                if event.key == pygame.K_DOWN:
                    selected_row = (selected_row + 1) % 3
                if event.key == pygame.K_LEFT:
                    if selected_row == 0:
                        p1_index = (p1_index - 1) % len(COLORS)
                    elif selected_row == 1:
                        p2_index = (p2_index - 1) % len(COLORS)
                if event.key == pygame.K_RIGHT:
                    if selected_row == 0:
                        p1_index = (p1_index + 1) % len(COLORS)
                    elif selected_row == 1:
                        p2_index = (p2_index + 1) % len(COLORS)
                if event.key == pygame.K_RETURN:
                    if selected_row == 2:
                        PLAYER1_COLOR = COLORS[p1_index]
                        PLAYER2_COLOR = COLORS[p2_index]
                        return
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)

def mode_selection_menu():
    selected_index = 0
    options = ["PLAYER VS PLAYER", "PLAYER VS CPU", "BACK"]

    while True:
        screen.fill(BLACK)
        draw_text("SELECT MODE", font, WHITE, -150)

        for i, option in enumerate(options):
            color = WHITE if i == selected_index else (100, 100, 100)
            prefix = "> " if i == selected_index else "  "
            text_surf = small_font.render(prefix + option, True, color)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (i * 60)))
            
            if i == selected_index:
                for g in range(3):
                    glow_color = (0, 150, 150) if i == 0 else (150, 0, 150) if i == 1 else (150, 150, 150)
                    glow_surf = small_font.render(prefix + option, True, glow_color)
                    glow_rect = glow_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (i * 60)))
                    screen.blit(glow_surf, glow_rect.inflate(g*2, g*2))

            screen.blit(text_surf, text_rect)

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
                        return "pvp"
                    if selected_index == 1:
                        return "cpu"
                    if selected_index == 2:
                        return None
                if event.key == pygame.K_ESCAPE:
                    return None

        pygame.display.flip()
        clock.tick(FPS)

def menu():
    selected_index = 0
    options = ["START GAME", "CHOOSE COLORS", "QUIT"]
    
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
                    # Use a dynamic glow color or a fixed one
                    glow_color = (0, 150, 150) if i == 0 else (150, 0, 150) if i == 2 else (150, 150, 0)
                    glow_surf = small_font.render(prefix + option, True, glow_color)
                    glow_rect = glow_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (i * 60)))
                    screen.blit(glow_surf, glow_rect.inflate(g*2, g*2))

            screen.blit(text_surf, text_rect)

        # Decorative neon paddles
        pygame.draw.rect(screen, PLAYER1_COLOR, (50, HEIGHT // 2 - 50, 15, 100))
        pygame.draw.rect(screen, PLAYER2_COLOR, (WIDTH - 65, HEIGHT // 2 - 50, 15, 100))

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
                        mode = mode_selection_menu()
                        if mode:
                            return mode
                    if selected_index == 1:
                        color_selection_menu()
                    if selected_index == 2:
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

def game_loop(mode):
    # Game objects
    p1 = Paddle(20, HEIGHT // 2 - 50, 15, 100, PLAYER1_COLOR)
    p2 = Paddle(WIDTH - 35, HEIGHT // 2 - 50, 15, 100, PLAYER2_COLOR)
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
        if mode == "cpu":
            p2.move_cpu(ball.rect)
        else:
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
            draw_winner("LEFT PLAYER WINS! 🏆", PLAYER1_COLOR)
            running = False
        elif score2 >= WINNING_SCORE:
            draw_winner("RIGHT PLAYER WINS! 🏆", PLAYER2_COLOR)
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
        score_text1 = font.render(str(score1), True, PLAYER1_COLOR)
        score_text2 = font.render(str(score2), True, PLAYER2_COLOR)
        screen.blit(score_text1, (WIDTH // 4, 30))
        screen.blit(score_text2, (WIDTH * 3 // 4 - score_text2.get_width(), 30))

        pygame.display.flip()
        clock.tick(FPS)

def main():
    while True:
        mode = menu()
        if mode:
            game_loop(mode)

if __name__ == "__main__":
    main()
