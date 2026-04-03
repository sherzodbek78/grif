from ursina import *

app = Ursina()

window.title = 'Dream League 3D (Graphic Mods)'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

camera.position = (0, 32, -35)
camera.rotation_x = 45

# Chiziq markazi
center_line = Entity(model='cube', scale=(40, 0.1, 0.5), color=color.white, y=0.01)

# Darvozalar
goal_top = Entity(model='cube', scale=(10, 0.5, 0.5), color=color.white, z=30, y=1.5, collider='box')
goal_left = Entity(model='cube', scale=(0.5, 3, 0.5), color=color.white, z=30, y=1.5, x=-5, collider='box')
goal_right = Entity(model='cube', scale=(0.5, 3, 0.5), color=color.white, z=30, y=1.5, x=5, collider='box')

goal2_top = Entity(model='cube', scale=(10, 0.5, 0.5), color=color.white, z=-30, y=1.5, collider='box')
goal2_left = Entity(model='cube', scale=(0.5, 3, 0.5), color=color.white, z=-30, y=1.5, x=-5, collider='box')
goal2_right = Entity(model='cube', scale=(0.5, 3, 0.5), color=color.white, z=-30, y=1.5, x=5, collider='box')

# PITCH (Stadion yuzasi - Papkadagi rasmni o'qiydi)
field = Entity(
    model='plane', 
    scale=(40, 1, 60), 
    texture='soccer_pitch_1774008492666.png', 
    texture_scale=(4,6), 
    collider='box'
)

# BALL (Haqiqiy 3D futol to'pi yuzasi)
ball = Entity(
    model='sphere', 
    scale=1.5, 
    y=0.7, 
    texture='soccer_ball_1774008668586.png', 
    collider='sphere'
)
ball_velocity = Vec3(0, 0, 0)

# O'YINCHI (Siz - Ko'k kub)
player = Entity(model='cube', color=color.azure, scale=(1.5, 3, 1.5), y=1.5, z=-15, collider='box')

# RAQIB (Qizil Haqiqiy mato teksturasi)
enemy = Entity(
    model='cube', 
    scale=(1.5, 3, 1.5), 
    y=1.5, 
    z=15, 
    texture='p_red_1774008884175.png', 
    collider='box'
)

# UI va Matnlar
score_text = Text(text="SCORE: 0 - 0", position=(-0.85, 0.45), scale=2, color=color.yellow)
info_text = Text(text="DLS Mantiqi. Teksturalar ulandi! (W,A,S,D - Yurish)", position=(-0.85, -0.45), scale=1)
player_score = 0
enemy_score = 0

def reset_positions():
    player.position = (0, 1.5, -15)
    enemy.position = (0, 1.5, 15)
    ball.position = (0, 0.6, 0)
    global ball_velocity
    ball_velocity = Vec3(0,0,0)

def update():
    global ball_velocity, player_score, enemy_score
    
    speed = 15 * time.dt
    if held_keys['w']: player.z += speed
    if held_keys['s']: player.z -= speed
    if held_keys['a']: player.x -= speed
    if held_keys['d']: player.x += speed

    dist = distance(player.position, ball.position)
    if dist < 2.0:
        dir_vec = (ball.position - player.position).normalized()
        dir_vec.y = 0
        ball_velocity = dir_vec * 28 # Sizning zarbangiz biroz kuchaytirildi
        
    enemy.look_at(ball)
    enemy.position += enemy.forward * (8 * time.dt)
    
    enemy_dist = distance(enemy.position, ball.position)
    if enemy_dist < 2.0:
        enemy_dir = (ball.position - enemy.position).normalized()
        enemy_dir.y = 0
        ball_velocity = enemy_dir * 30

    ball.position += ball_velocity * time.dt
    
    # Koptok sekin dumalab aniq ko'rinishi uchun
    ball.rotation_x += ball_velocity.z * 10
    ball.rotation_z -= ball_velocity.x * 10
    
    ball_velocity = lerp(ball_velocity, Vec3(0,0,0), time.dt * 1.5)
    
    if ball.x > 19.5: ball.x = 19.5; ball_velocity.x *= -0.8
    if ball.x < -19.5: ball.x = -19.5; ball_velocity.x *= -0.8
    
    # Raqib darvozasiga yetib borganda
    if ball.z > 29.5: 
        if -5 < ball.x < 5:
            player_score += 1
            score_text.text = f"SCORE: {player_score} - {enemy_score}"
            ball.z = 29.5; ball_velocity = Vec3(0,0,0)
            invoke(reset_positions, delay=2)
        else:
            ball.z = 29.5; ball_velocity.z *= -0.8
            
    # Sizning darvozangizga kelganda
    if ball.z < -29.5:
        if -5 < ball.x < 5:
            enemy_score += 1
            score_text.text = f"SCORE: {player_score} - {enemy_score}"
            ball.z = -29.5; ball_velocity = Vec3(0,0,0)
            invoke(reset_positions, delay=2)
        else:
            ball.z = -29.5; ball_velocity.z *= -0.8

app.run()
