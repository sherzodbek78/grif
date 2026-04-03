import pygame
import sys
import random
from player import Player
from vehicle import Car
from world_map import generate_city, MAP_WIDTH, MAP_HEIGHT
from npc import Bot

pygame.init()

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GTA 2D - 3D Botlar qo'shildi")
clock = pygame.time.Clock()

print("Shahar generatsiya qilinmoqda...")
bg_surface, buildings = generate_city()
print("Shahar tayyor!")

start_x = MAP_WIDTH // 2
start_y = MAP_HEIGHT // 2

player = Player(start_x, start_y)

cars = pygame.sprite.Group()
cars.add(Car(start_x + 200, start_y + 100, (220, 50, 50))) 
cars.add(Car(start_x - 200, start_y + 100, (50, 50, 220)))
cars.add(Car(start_x + 400, start_y - 200, (50, 220, 50)))
cars.add(Car(start_x - 400, start_y - 200, (220, 220, 50)))

# Botlarni (Piyodalarni) yaratish
bots = pygame.sprite.Group()
print("3D Botlar ko'chaga chiqib ketishdi...")
for _ in range(80): # Shaharda 80 ta bot (sun'iy intellekt) mustaqil yuradi
    bx = random.randint(200, MAP_WIDTH - 200)
    by = random.randint(200, MAP_HEIGHT - 200)
    bots.add(Bot(bx, by))

camera_x = 0
camera_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if player.in_car:
                    player.exit_car()
                else:
                    closest_car = None
                    min_dist = 90 
                    for c in cars:
                        dist = pygame.math.Vector2(player.rect.center).distance_to(c.rect.center)
                        if dist < min_dist:
                            closest_car = c
                            min_dist = dist
                    
                    if closest_car:
                        player.enter_car(closest_car)

    keys = pygame.key.get_pressed()
    
    if not player.in_car:
        player.update(keys, buildings)
    else:
        player.current_car.update(keys, buildings)
        player.rect.center = player.current_car.rect.center
        
    for c in cars:
        if not c.player_inside:
            c.update({}, buildings) 
            
    # Botlarni yangilash
    for b in bots:
        # Pleyer yoki mashinadagi to'qnashuvlar ucnun faqat devorlarni beramiz
        b.update(buildings)

    # Kamera harakati
    target = player.current_car if player.in_car else player
    camera_x = target.rect.centerx - WIDTH // 2
    camera_y = target.rect.centery - HEIGHT // 2
    
    camera_x = max(0, min(camera_x, MAP_WIDTH - WIDTH))
    camera_y = max(0, min(camera_y, MAP_HEIGHT - HEIGHT))

    # --- CHIZISH ---
    
    # Orqafon shahar
    screen.blit(bg_surface, (0, 0), (camera_x, camera_y, WIDTH, HEIGHT))
    
    # Botlarni chizish (Faqat kameraga ko'rinadiganlarni) (fps ni ko'paytiradi)
    for b in bots:
        if camera_x - 50 < b.rect.x < camera_x + WIDTH + 50 and camera_y - 50 < b.rect.y < camera_y + HEIGHT + 50:
            screen.blit(b.image, (b.rect.x - camera_x, b.rect.y - camera_y))
            
    # Mashinalar        
    for c in cars:
        if camera_x - 100 < c.rect.x < camera_x + WIDTH + 100 and camera_y - 100 < c.rect.y < camera_y + HEIGHT + 100:
            screen.blit(c.image, (c.rect.x - camera_x, c.rect.y - camera_y))
        
    # O'yinchi
    if not player.in_car:
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))

    # --- UI ---
    font = pygame.font.SysFont("Arial", 28, bold=True)
    if player.in_car:
        speed_kmh = abs(int(player.current_car.speed * 8))
        ui_text = font.render(f"Tezlik: {speed_kmh} km/h", True, (255, 255, 255))
    else:
        ui_text = font.render("Mashinaga chiqish ucnun 'F' bosing", True, (255, 255, 255))
        
    ui_bg = pygame.Surface((ui_text.get_width() + 20, ui_text.get_height() + 10))
    ui_bg.set_alpha(150)
    ui_bg.fill((0, 0, 0))
    screen.blit(ui_bg, (15, 15))
    screen.blit(ui_text, (25, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
