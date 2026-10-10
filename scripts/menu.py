import pygame

from scripts.scene import Scene
from scripts.obj import Obj
from scripts.text import Text
from scripts.settings import *
from scripts.animatedbg import AnimatedBg

class Menu(Scene):

    def __init__(self):
        super().__init__()

        self.bg = AnimatedBg("assets/menu/bg.png", [0,0], [1280,0], [self.all_sprites])
        self.title = Text("assets/font/batmfa_.ttf", 70, "SpaceShip 13K", "white", [325,200])
        self.text_info = Text("assets/font/batmfa_.ttf", 15, "Press start to play", "white", [535,508])

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
        return super().events(event)

    def update(self):

        self.bg.update()
        self.title.draw()
        self.text_info.drawFade()
        return super().update()