from ursina import *

class Menu(Entity):
    def __init__(self, game, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused = True, **kwargs)
        
        self.background = Sprite(parent = self, scale = 0.3, texture = "assets/menu_minecraft_bg.png", color = color.gray, z = 1)
        Text.default_font = "assets/PressStart2P-Regular.ttf"