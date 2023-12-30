from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import os

app = Ursina()

PATH = os.getcwd()
ASSETS_PATH = os.path.join(PATH, "assets")#game adress


def get_image_list(foldername):
    path_dir = os.path.join(ASSETS_PATH, foldername)#assets folder adress
    image_names = os.listdir(path_dir)#player down adress
    image_list = []

    for img in image_names:
        new_image = load_texture("assets/blocks/"+img)
        image_list.append(new_image)


    return image_list

textures = get_image_list("blocks")

class Block(Button):
    id = 0

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
        if  key== '1':
            Block.id = 0
        if  key== '2':
            Block.id = 1
        if  key== '3':
            Block.id = 2
        if key =='scrollup':
            Block.id -= 1
        if key =='scrolldown':
            Block.id += 1
        
        if self.hovered:
            if key == "left mouse down":
                destroy(self)
            if key == "right mouse down":
                new_block = Block(position=self.position + mouse.normal, block_id=Block.id)

for z in range(-10, 10):
    for x in range(-10, 10):
        new_block = Block((x, 0, z))

player = FirstPersonController()

app.run()