from ursina import *

app = Ursina()

# Sahna fonini o'rnatish
window.color = color.rgb(0, 200, 255)

# Zamin
ground = Entity(model='plane', scale=(10,1,10), color=color.green, collider='box')

# Kub (o'yinchi)
player = Entity(model='cube', color=color.orange, scale=(1,1,1), position=(0,0.5,0), collider='box')

# Kamera sozlamasi
camera.position = (0, 10, -20)
camera.rotation_x = 30

# Harakat funksiyasi
def update():
    speed = 5 * time.dt
    if held_keys['w']:
        player.z -= speed
    if held_keys['s']:
        player.z += speed
    if held_keys['a']:
        player.x -= speed
    if held_keys['d']:
        player.x += speed

app.run()
