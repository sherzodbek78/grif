import pygame
import sys
import random

# 1. Sozlamalar
pygame.init()
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Head Ball: Final")
clock = pygame.time.Clock()

# Ranglar
SKY_BLUE = (135, 206, 235)
PITCH_GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
font = pygame.font.SysFont("Impact", 40)

# --- KLASSLAR ---
class Player:
    def __init__(self, x, color, up, left, right):
        self.rect = pygame.Rect(x, HEIGHT - 110, 60, 60)
        self.color = color
        self.vel_y = 0
        self.controls = {'up': up, 'left': left, 'right': right}
        self.is_jumping = False
        self.score = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']] and self.rect.left > 0: self.rect.x -= 9
        if keys[self.controls['right']] and self.rect.right < WIDTH: self.rect.x += 9
        if keys[self.controls['up']] and not self.is_jumping:
            self.vel_y = -18
            self.is_jumping = True
        self.vel_y += 0.8
        self.rect.y += self.vel_y
        if self.rect.bottom >= HEIGHT - 20:
            self.rect.bottom = HEIGHT - 20
            self.is_jumping = False
            self.vel_y = 0

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2, 250, 30, 30)
        self.vel_x = 0
        self.vel_y = 0
    def reset(self):
        self.rect.center = (WIDTH//2, 250)
        self.vel_x = 0; self.vel_y = 0
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

# --- DRAW FUNCTIONS ---
def draw_fans():
    pygame.draw.rect(screen, SKY_BLUE, (0, 0, WIDTH, 200))
    pygame.draw.rect(screen, GRAY, (0, 200, WIDTH, HEIGHT-200))
    for y in range(215, HEIGHT-120, 45):
        for x in range(20, WIDTH, 35):
            fan_color = (random.randint(100, 255), 50, 50)
            pygame.draw.circle(screen, (255, 220, 180), (x, y), 8)
            pygame.draw.rect(screen, fan_color, (x-10, y+8, 20, 15), border_radius=3)

def play_game(mode):
    p1 = Player(150, (220, 0, 0), pygame.K_w, pygame.K_a, pygame.K_d)
    p2 = Player(700, (0, 0, 220), pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT)
    ball = Ball()
    while True:
        draw_fans()
        pygame.draw.rect(screen, PITCH_GREEN, (0, HEIGHT-20, WIDTH, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        p1.move()
        if mode == "FRIEND": p2.move()
        else:
            if ball.rect.centerx > p2.rect.centerx: p2.rect.x += 6
            elif ball.rect.centerx < p2.rect.centerx: p2.rect.x -= 6
            if ball.rect.y < p2.rect.y - 100 and not p2.is_jumping:
                p2.vel_y = -18; p2.is_jumping = True
        ball.update()
        if p1.rect.colliderect(ball.rect) or p2.rect.colliderect(ball.rect):
            p = p1 if p1.rect.colliderect(ball.rect) else p2
            ball.vel_y = -15
            ball.vel_x = (ball.rect.centerx - p.rect.centerx) // 2
        if ball.rect.left <= 0 and ball.rect.bottom > HEIGHT - 180:
            p2.score += 1; ball.reset()
        if ball.rect.right >= WIDTH and ball.rect.bottom > HEIGHT - 180:
            p1.score += 1; ball.reset()
        pygame.draw.rect(screen, WHITE, (0, HEIGHT-160, 10, 140))
        pygame.draw.rect(screen, WHITE, (WIDTH-10, HEIGHT-160, 10, 140))
        pygame.draw.ellipse(screen, p1.color, p1.rect)
        pygame.draw.ellipse(screen, p2.color, p2.rect)
        pygame.draw.circle(screen, WHITE, ball.rect.center, 15)
        score_txt = font.render(f"{p1.score} : {p2.score}", True, BLACK)
        screen.blit(score_txt, (WIDTH//2 - 40, 30))
        pygame.display.flip()
        clock.tick(60)

# --- START ---
if __name__ == "__main__":
    # Soddalashtirilgan boshlash
    play_game("BOT") # Do'st bilan o'ynash uchun "FRIEND" deb yozingdddddddddddddddddddddddddddddddddd