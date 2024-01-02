from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import os
from ursina.prefabs.sky import Sky
from ursina.shaders import basic_lighting_shader
import random
from perlin_noise import PerlinNoise
app = Ursina()


MAP_SIZE = 20
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
        #shader=basic_lighting_shader
        )
    
    def input(self, key):
        for i in range(10):
            if  key== str(i):
                Block.id = i

        if key =='scroll up':
            Block.id -= 1
            if Block.id < 0:
                Block.id = len(textures) - 1
        if key =='scroll down':
            if Block.id <= len(textures) - 1:
                Block.id += 1
            else:
                Block.id = 0
        
        if self.hovered:
            if key == "left mouse down":
                destroy(self)
            if key == "right mouse down":
                new_block = Block(position=self.position + mouse.normal, block_id=Block.id)

noise = PerlinNoise(octaves=3, seed = random.randint(1,1000))
for z in range(-MAP_SIZE, MAP_SIZE):
    for x in range(-MAP_SIZE, MAP_SIZE):
        height = noise([x*0.02, z* 0.02])
        height = math.floor(height * 7.5)
        new_block = Block((x, height, z))

window.fullscreen = True
scene.fog_density = 0.025
scene.fog_color = color.rgb(120, 146, 232)

pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True)

player = FirstPersonController()
sky = Sky(texture = "sky_sunset")
app.run()