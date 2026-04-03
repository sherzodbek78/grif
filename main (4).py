from ursina import *
import random

app = Ursina()

# --- oyna sozlamalari ---
window.title = 'Dream League 3D (Mini Version)'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# --- Kamera sozlamalari ---
# Maydonni yuqoriroqdan, qiya burchak ostida ko'rsatish
camera.position = (0, 32, -35)
camera.rotation_x = 45

# --- Maydon va Chiziqlar ---
# Yashil maysazor
field = Entity(model='plane', scale=(40, 1, 60), color=color.green, collider='box')

# Markaziy oq chiziq
center_line = Entity(model='cube', scale=(40, 0.1, 0.5), color=color.white, y=0.01)

# --- Darvozalar ---
# Yuqori (Raqib darvozasi)
goal_top = Entity(model='cube', scale=(10, 0.5, 0.5), color=color.white, z=30, y=1.5, collider='box')
goal_left = Entity(model='cube', scale=(0.5, 3, 0.5), color=color.white, z=30, y=1.5, x=-5, collider='box')
goal_right = Entity(model='cube', scale=(0.5, 3, 0.5), color=color.white, z=30, y=1.5, x=5, collider='box')

# Pastki (Sizning darvozangiz)
goal2_top = Entity(model='cube', scale=(10, 0.5, 0.5), color=color.white, z=-30, y=1.5, collider='box')
goal2_left = Entity(model='cube', scale=(0.5, 3, 0.5), color=color.white, z=-30, y=1.5, x=-5, collider='box')
goal2_right = Entity(model='cube', scale=(0.5, 3, 0.5), color=color.white, z=-30, y=1.5, x=5, collider='box')

# --- O'yin Obyektlari ---
# Koptok
ball = Entity(model='sphere', color=color.white, scale=1.3, y=0.6, collider='sphere')
ball_velocity = Vec3(0, 0, 0)

# O'yinchi (Moviy kubik - Siz)
player = Entity(model='cube', color=color.azure, scale=(1.5, 3, 1.5), y=1.5, z=-15, collider='box')

# Dushman (Qizil kubik - AI raqib)
enemy = Entity(model='cube', color=color.red, scale=(1.5, 3, 1.5), y=1.5, z=15, collider='box')

# --- Hisob va Ekranga yozuv chiqarish ---
score_text = Text(text="HISOB: 0 - 0", position=(-0.85, 0.45), scale=2, color=color.yellow)
info_text = Text(text="W,A,S,D - Harakat. O'yinchi to'pga yaqinlashsa o'zi tepadi.", position=(-0.85, -0.45), scale=1, color=color.white)
player_score = 0
enemy_score = 0

# Koptok markazga qaytarish funksiyasi
def reset_positions():
    player.position = (0, 1.5, -15)
    enemy.position = (0, 1.5, 15)
    ball.position = (0, 0.6, 0)
    global ball_velocity
    ball_velocity = Vec3(0,0,0)

def update():
    global ball_velocity, player_score, enemy_score
    
    # 1. O'yinchini Boshqarish (Siz)
    speed = 15 * time.dt
    if held_keys['w']: player.z += speed
    if held_keys['s']: player.z -= speed
    if held_keys['a']: player.x -= speed
    if held_keys['d']: player.x += speed

    # Zarba (O'yinchi to'pga tekkanda kuchli itaramiz)
    dist = distance(player.position, ball.position)
    if dist < 2.0:
        dir_vec = (ball.position - player.position).normalized()
        dir_vec.y = 0
        ball_velocity = dir_vec * 25 # Zarba kuchi
        
    # 2. Raqib Sun'iy intellekti (AI to'p ketidan ergashadi)
    enemy.look_at(ball)
    enemy.position += enemy.forward * (8 * time.dt)
    
    enemy_dist = distance(enemy.position, ball.position)
    if enemy_dist < 2.0:
        enemy_dir = (ball.position - enemy.position).normalized()
        enemy_dir.y = 0
        ball_velocity = enemy_dir * 30 # Raqib ham kuchliroq tepoladi

    # 3. Koptok dinamikasi (Sekinlashishi va xarakatlanishi)
    ball.position += ball_velocity * time.dt
    ball_velocity = lerp(ball_velocity, Vec3(0,0,0), time.dt * 1.5) # asta-yon sekinlashish
    
    # 4. Maydon Chegaralari
    # Yon chiziqlar (Koptok maydondan chiqib ketsa sakrab qaytadi)
    if ball.x > 19.5: ball.x = 19.5; ball_velocity.x *= -0.8
    if ball.x < -19.5: ball.x = -19.5; ball_velocity.x *= -0.8
    
    # Raqib darvozasiga yaqinlashganda
    if ball.z > 29.5: 
        if -5 < ball.x < 5: # Darvoza ichiga kirdimi? GOL!
            player_score += 1
            score_text.text = f"HISOB: {player_score} - {enemy_score}"
            ball.z = 29.5; ball_velocity = Vec3(0,0,0)
            invoke(reset_positions, delay=2) # 2 soniyadan keyin boshiga qaytarish
        else: # Yon devorlarga tegdmi?
            ball.z = 29.5; ball_velocity.z *= -0.8
            
    # Sizning darvozangizga yaqinlashganda
    if ball.z < -29.5:
        if -5 < ball.x < 5: # Raqib gol urdimi?
            enemy_score += 1
            score_text.text = f"HISOB: {player_score} - {enemy_score}"
            ball.z = -29.5; ball_velocity = Vec3(0,0,0)
            invoke(reset_positions, delay=2)
        else:
            ball.z = -29.5; ball_velocity.z *= -0.8

# Dvigatelni ishga tushirish
app.run()
