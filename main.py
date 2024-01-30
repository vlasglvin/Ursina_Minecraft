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
from ui import Menu, Inventar


class Controller(Entity):
    def __init__(self):
        super().__init__(ignore_paused = True)
        window.fullscreen = True
        scene.fog_density = 0.025
        scene.fog_color = color.rgb(120, 146, 232)
        self.player = Player()
        #self.sky = Sky(texture = "sky_sunset")
        
        self.sky = NightSky()

        pivot = Entity()
        DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
        self.menu = Menu(self)
        self.inventar = Inventar(Block.textures)
        self.game_music = Audio("assets\life_in_corrupted_binary.flac", loop = True, volume = 0.7)
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
        if application.paused:
            self.menu.menu_music.play()
            self.game_music.stop()
        else:
            self.menu.menu_music.stop()
            self.game_music.play()

    def new_game(self):
        self.clear_map()

        noise = PerlinNoise(octaves=3, seed = random.randint(1,1000))
        for z in range(-MAP_SIZE, MAP_SIZE):
            for x in range(-MAP_SIZE, MAP_SIZE):
                height = noise([x*0.02, z* 0.02])
                height = math.floor(height * 7.5)
                new_block = Block((x, height, z))
                rand_num = random.randint(1, 100)
                if rand_num == 15:
                    tree = Tree(position=(x, height+1, z), scale=random.randint(3,5))
        
        self.player.position = (0, 50, 0)
        self.player.start_pos = self.player.position

        self.toggle_menu()

    

    def input(self, key):
        if key == "escape" and len(Block.map)>0:
            self.toggle_menu()

        if key == "e" and len(Block.map)>0:
            self.inventar.toggle()

    def save_game(self):

        with open("save.dat", "wb") as file:
            pickle.dump(self.player.position, file)
            pickle.dump(len(Block.map),file)
            for  block in Block.map:
                pickle.dump(block.position, file)
                pickle.dump(block.id, file)
            pickle.dump(len(Tree.map), file)
            for  tree in Tree.map:
                pickle.dump(tree.position, file)
                pickle.dump(tree.scale, file)  

        self.toggle_menu()     

    def clear_map(self):
        for block in Block.map:
            destroy(block)
        for tree in Tree.map:
            destroy(tree)
        Block.map.clear()
        Tree.map.clear()

    def load_game(self):
        self.clear_map()


        with open("save.dat", "rb") as file:
            self.player.position = pickle.load(file)
            self.player.start_pos = self.player.position
            len_map = pickle.load(file)
            for i in range(len_map):
                pos = pickle.load(file)
                block_id = pickle.load(file)
                Block(pos, block_id)
            len_tree = pickle.load(file)
            for i in range(len_tree):
                pos = pickle.load(file)
                scale = pickle.load(file)
                Tree(pos, scale)

            self.toggle_menu()

        




# entity = Entity()
# chest = Actor("assets/minecraft_chest/scene.gltf")
# chest.reparent_to(entity)
# chest.loop("Chest_0_A|Chest_0_AAction")
# entity.position = player.position
# entity.rotation = Vec3(90, 90, 90)
game = Controller()
#game.new_game()
app.run()