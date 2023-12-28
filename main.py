from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

textures = [
    load_texture('assets/grass.png'),
]

class Block(Button):
    def __init__(self, position, block_id=0):
        super().__init__(
        parent = scene,
        model="assets/block",
        texture=textures[block_id],
        color = color.color(0,0,random.uniform(0.9, 1)),
        position = position,
        scale = 0.5,
        origin_y = 0.5,
        highlight_color=color.gray,
        )
    
    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                destroy(self)
            if key == "right mouse down":
                new_block = Block(position=self.position + mouse.normal)

for z in range(-10, 10):
    for x in range(-10, 10):
        new_block = Block((x, 0, z))

player = FirstPersonController()

app.run()