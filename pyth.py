import pygame
import sys

# Pygame'ni ishga tushiramiz
pygame.init()

# Oyna o'lchami
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oddiy Pygame Sahna")

# Ranglar
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Belgi (player) parametrlari
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# O'yin sikli
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # FPS: 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tugmalarni tekshirish
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Ekranni tozalash
    screen.fill(WHITE)

    # Belgini chizish
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    # Yangilash
    pygame.display.flip()

# Chiqish
pygame.quit()
sys.exit()
