from ursina import *
from ursina import Default, camera
from models import Block

class MenuButton(Button):
    def __init__(self, text, action, x, y, parent, **kwargs):
        super().__init__(text,  on_click = action,parent=parent,
                         color=color.rgb(107, 107, 107),
                         texture="assets/button.png",
                         scale = (1, 0.1),
                         text_size = 2,
                         text_color=color.white,
                         y = y, x = x, origin=(0,0),
                         ignore_paused = True,
                         **kwargs)


class Menu(Entity):
    def __init__(self, game, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused = True, **kwargs)
        self.menu_music = Audio("assets/b423b42.wav", loop = True)  
        self.background = Sprite(parent = self, scale = 0.3, texture = "assets/menu_minecraft_bg.png", color = color.gray, z = 1)
        Text.default_font = "assets/PressStart2P-Regular.ttf"

        Text("BlockBuilder", scale=3, parent=self, origin = (0,0), x = 0, y = 0.4)

        self.btns = [
            MenuButton("New Game", game.new_game, x=0,y=0.125   , parent=self),
            MenuButton("Continue", game.load_game, x=0,y=0.01, parent=self),
            MenuButton("Save Game", game.save_game, x=0,y=-0.105, parent=self),
            MenuButton("Exit", application.quit, x=0,y=-0.22, parent=self),
        ]

class Item(Button):
     def __init__(self, texture, x, y, parent, block_id, **kwargs):
        super().__init__(text="",  on_click = self.click,parent=parent,
                         color=color.white,
                         texture=texture,
                         scale = (0.1, 0.15),
                         y = y, x = x, origin=(- .5,.5),
                         z = -.1,
                         ignore_paused = True,
                         **kwargs)
        
        self.id = block_id

     def click(self):
         Block.id = self.id
         self.parent.toggle()
    
        
class Inventar(Entity):
    def __init__(self, textures, width=6, height=4, **kwargs):
        super().__init__(
            parent = camera.ui,
            model = Quad(radius=.015),
            texture = 'assets/button.png',
            texture_scale = (width, height),
            scale = (width*.1, height*.1),
            origin = (-.5,.5),
            position = (-.3,.4),
            color = color.rgba(200, 200, 200),
            ignore_paused = True
            )

        self.width = width
        self.height = height
        self.textures= textures
        self.items = []
        k = 0
        x = 0.025
        y = -0.05
        for row in range(self.height):
            for col in range(self.width):
                self.items.append(Item(self.textures[k], x,y, self, k))
                k+=1
                x += 0.165
            x = 0.025
            y -= 0.25

            

        self.enabled = False
        self.visible = False

    def toggle(self):
        application.paused = not application.paused
        self.enabled = not self.enabled
        self.visible = not self.visible
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.visible
    