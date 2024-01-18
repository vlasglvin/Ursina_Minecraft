from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import os
from direct.actor.Actor import Actor
from ursina.prefabs.sky import Sky
from ursina.shaders import basic_lighting_shader,lit_with_shadows_shader
import random
from perlin_noise import PerlinNoise
import pickle

from config import *

app = Ursina()

from models import *
from ui import Menu


class Controller(Entity):
    def __init__(self):
        super().__init__(ignore_paused = True)
        window.fullscreen = True
        scene.fog_density = 0.025
        scene.fog_color = color.rgb(120, 146, 232)
        self.player = Player()
        self.sky = Sky(texture = "sky_sunset")
        self.blocks = []
        self.menu = Menu(self)
        self.toggle_menu()
        mouse.locked = False
        mouse.visible = True

    def toggle_menu(self):
        application.paused = not application.paused
        self.menu.enabled = application.paused
        self.menu.visible = application.paused
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.visible
        axe.enabled = not axe.enabled

    def new_game(self):
        noise = PerlinNoise(octaves=3, seed = random.randint(1,1000))
        for z in range(-MAP_SIZE, MAP_SIZE):
            for x in range(-MAP_SIZE, MAP_SIZE):
                height = noise([x*0.02, z* 0.02])
                height = math.floor(height * 7.5)
                new_block = Block((x, height, z))
                self.blocks.append(new_block)
                rand_num = random.randint(1, 100)
                if rand_num == 15:
                    tree = Tree(position=(x, height+1, z), scale=random.randint(3,5))
        
        pivot = Entity()
        DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
        self.player.position = (0, 50, 0)
        self.player.start_pos = self.player.position

        self.toggle_menu()

    

    def input(self, key):
        if key == "escape" and len(self.blocks)>0:
            self.toggle_menu()

    def save_game(self):

        with open("save.dat", "wb") as file:
            pickle.dump(self.player.position, file)


# entity = Entity()
# chest = Actor("assets/minecraft_chest/scene.gltf")
# chest.reparent_to(entity)
# chest.loop("Chest_0_A|Chest_0_AAction")
# entity.position = player.position
# entity.rotation = Vec3(90, 90, 90)
game = Controller()
#game.new_game()
app.run()