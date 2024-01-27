from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import os
from ursina.shaders import basic_lighting_shader,lit_with_shadows_shader
from config import *


def get_image_list(foldername):
    path_dir = os.path.join(ASSETS_PATH, foldername)#assets folder adress
    image_names = os.listdir(path_dir)#player down adress
    image_list = []

    for img in image_names:
        new_image = load_texture("assets/blocks/"+img)
        image_list.append(new_image)


    return image_list

textures = get_image_list("blocks")


class Player(FirstPersonController):
    def input(self, key):
        if key == "g":
            if self.gravity == 0:
                 self.gravity = 1
                 self.jumping = True
            else:
                self.gravity = 0
                 

    def update(self):
        super().update()
        if held_keys["shift"]:
            self.speed = 10
        else:
            self.speed = 5

        if held_keys["z"]:
            self.y -= 1

        if held_keys["q"]:
            self.y += 1
        
        
        if self.y < -30:
            self.position = self.start_pos


class Axe(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model="assets\minecraft-diamond-pickaxe\source\Diamond Pickaxe\Diamond Pickaxe\model\obj\Diamond-Pickaxe.obj",
            texture = "assets\minecraft-diamond-pickaxe\source\Diamond Pickaxe\Diamond Pickaxe\material\Diffuse.png",
            scale = 0.03,
            position = Vec2(0.5, -0.4),
            rotation = Vec3(100, 448, -70),
            shader=basic_lighting_shader
            )

        self.build_sound = Audio("assets\gravel.ogg")
        self.destroy_sound = Audio("assets\mud02.ogg")

    def active(self):
        self.rotation = Vec3(67, 468, -70)
        self.position = Vec2(0.5, -0.3)
    
    def pasive(self):
        self.rotation = Vec3(100, 448, -70)
        self.position = Vec2(0.5, -0.4)


class Tree(Entity):
    map = []
    def __init__(self, position, scale = 5):
        super().__init__(
        parent = scene,
        model="assets/minecraft_tree/scene",
        scale = scale,
        position = (position),
        origin_y = 0.6,
        shader=lit_with_shadows_shader
            )
            
        Tree.map.append(self)   

class Block(Button):
    id = 0
    map = []
    textures = textures

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
        shader=lit_with_shadows_shader
        )
        self.id = block_id  
        Block.map.append(self)


    def input(self, key):
        for i in range(10):
            if  key== str(i):
                Block.id = i

        if key =='scroll up':
            Block.id -= 1
            if Block.id < 0:
                Block.id = len(textures) - 1
        if key =='scroll down':
            if Block.id < len(textures) - 1:
                Block.id += 1
            else:
                Block.id = 0
        
        if self.hovered:
            if key == "left mouse down":
                axe.active()
                axe.destroy_sound.play()
                Block.map.remove(self)
                destroy(self)
            elif key == "right mouse down":
                axe.active()
                axe.build_sound.play()
                new_block = Block(position=self.position + mouse.normal, block_id=Block.id)
            else:
                axe.pasive()

axe = Axe()