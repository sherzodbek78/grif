from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Dastur boshlanishi
app = Ursina()

# Sapawn joyi (yer markazida, biroz yuqorida)
spawn_point = Vec3(20, 1, 20)

# O'yinchi
player = FirstPersonController()
player.position = spawn_point

# Osmon
Sky()

# Bloklar ro'yxati
blocks = []

# Blok yaratish funksiyasi
def create_block(position):
    block = Entity(
        model='cube',
        texture='grass',
        color=color.white,
        position=position,
        parent=scene
    )
    blocks.append(block)

# Yer maydonini kengaytiramiz (40x40)
for x in range(40):
    for z in range(40):
        create_block((x, 0, z))

# Foydalanuvchi kirishini qayta ishlash
def input(key):
    if key == 'left mouse down':
        for block in blocks:
            if block.hovered:
                new_pos = block.position + mouse.normal
                if not any(b.position == new_pos for b in blocks):
                    create_block(new_pos)
                break
    elif key == 'right mouse down':
        for block in blocks:
            if block.hovered:
                blocks.remove(block)
                destroy(block)
                break

# Qayta tug‘ilishni tekshiruvchi funksiya
def update():
    if player.y < -10:  # Agar o'yinchi pastga qulab tushsa
        player.position = spawn_point
        player.velocity = Vec3(0, 0, 0)  # Harakatni to‘xtatish

# Dastur ishga tushadi
app.run()
