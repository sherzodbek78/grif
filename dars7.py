import pygame
import sys
import random

# 1. Sozlamalar
pygame.init()
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Head Ball Mobile")
clock = pygame.time.Clock()

# Ranglar
SKY_BLUE = (135, 206, 235)
PITCH_GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
font = pygame.font.SysFont("Impact", 40)

# --- TUGMA KOORDINATALARI (Sensor uchun) ---
btn_left = pygame.Rect(40, 430, 90, 90)
btn_right = pygame.Rect(150, 430, 90, 90)
btn_jump = pygame.Rect(770, 430, 90, 90)


# --- KLASSLAR ---
class Player:
    def __init__(self, x, color):
        self.rect = pygame.Rect(x, HEIGHT - 110, 60, 60)
        self.color = color
        self.vel_y = 0
        self.is_jumping = False
        self.score = 0

    def apply_physics(self):
        self.vel_y += 0.8
        self.rect.y += self.vel_y
        if self.rect.bottom >= HEIGHT - 20:
            self.rect.bottom = HEIGHT - 20
            self.is_jumping = False
            self.vel_y = 0


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, 250, 30, 30)
        self.vel_x = 0
        self.vel_y = 0

    def reset(self):
        self.rect.center = (WIDTH // 2, 250)
        self.vel_x = 0;
        self.vel_y = 0

    def update(self):
        self.vel_y += 0.35
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.bottom >= HEIGHT - 20:
            self.rect.bottom = HEIGHT - 20
            self.vel_y *= -0.85
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vel_x *= -1
        if self.rect.top <= 200: self.vel_y *= -1


# --- FUNKSIYALAR ---
def draw_fans():
    pygame.draw.rect(screen, SKY_BLUE, (0, 0, WIDTH, 200))
    pygame.draw.rect(screen, GRAY, (0, 200, WIDTH, HEIGHT - 200))
    for y in range(215, HEIGHT - 140, 45):
        for x in range(20, WIDTH, 35):
            fan_color = (random.randint(100, 255), 50, 50)
            pygame.draw.circle(screen, (255, 220, 180), (x, y), 8)
            pygame.draw.rect(screen, fan_color, (x - 10, y + 8, 20, 15), border_radius=3)


def draw_mobile_controls():
    # Tugmalar ko'rinishi (shaffof oq)
    s = pygame.Surface((90, 90), pygame.SRCALPHA)
    pygame.draw.rect(s, (255, 255, 255, 80), (0, 0, 90, 90), border_radius=20)
    screen.blit(s, (btn_left.x, btn_left.y))
    screen.blit(s, (btn_right.x, btn_right.y))
    screen.blit(s, (btn_jump.x, btn_jump.y))
    # Belgilar
    f = pygame.font.SysFont("Arial", 40, bold=True)
    screen.blit(f.render("<", True, BLACK), (70, 450))
    screen.blit(f.render(">", True, BLACK), (180, 450))
    screen.blit(f.render("^", True, BLACK), (805, 450))


def play_game():
    p1 = Player(150, (220, 0, 0))
    bot = Player(700, (0, 0, 220))
    ball = Ball()

    while True:
        draw_fans()
        pygame.draw.rect(screen, PITCH_GREEN, (0, HEIGHT - 20, WIDTH, 20))
        draw_mobile_controls()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        # --- SENSORLI BOSHQARUV (P1) ---
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if btn_left.collidepoint(mouse_pos) and p1.rect.left > 0: p1.rect.x -= 10
            if btn_right.collidepoint(mouse_pos) and p1.rect.right < WIDTH: p1.rect.x += 10
            if btn_jump.collidepoint(mouse_pos) and not p1.is_jumping:
                p1.vel_y = -18
                p1.is_jumping = True

        # --- BOT HARAKATI ---
        if ball.rect.centerx > bot.rect.centerx:
            bot.rect.x += 6
        elif ball.rect.centerx < bot.rect.centerx:
            bot.rect.x -= 6
        if ball.rect.y < bot.rect.y - 100 and not bot.is_jumping:
            bot.vel_y = -18;
            bot.is_jumping = True

        p1.apply_physics();
        bot.apply_physics();
        ball.update()

        # To'qnashuv
        if p1.rect.colliderect(ball.rect) or bot.rect.colliderect(ball.rect):
            p = p1 if p1.rect.colliderect(ball.rect) else bot
            ball.vel_y = -15
            ball.vel_x = (ball.rect.centerx - p.rect.centerx) // 2

        # Gollar
        if ball.rect.left <= 0 and ball.rect.bottom > HEIGHT - 180:
            bot.score += 1;
            ball.reset()
        if ball.rect.right >= WIDTH and ball.rect.bottom > HEIGHT - 180:
            p1.score += 1;
            ball.reset()

        # Chizish
        pygame.draw.rect(screen, WHITE, (0, HEIGHT - 160, 10, 140))
        pygame.draw.rect(screen, WHITE, (WIDTH - 10, HEIGHT - 160, 10, 140))
        pygame.draw.ellipse(screen, p1.color, p1.rect)
        pygame.draw.ellipse(screen, bot.color, bot.rect)
        pygame.draw.circle(screen, WHITE, ball.rect.center, 15)

        score_txt = font.render(f"{p1.score} : {bot.score}", True, BLACK)
        screen.blit(score_txt, (WIDTH // 2 - 40, 30))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    play_game()