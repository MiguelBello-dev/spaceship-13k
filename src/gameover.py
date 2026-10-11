import pygame
from src.animatedbg import AnimatedBg
from src.scene import Scene
from src.text import Text

class GameOver(Scene):

    def __init__(self):
        super().__init__()
   
        self.bg = AnimatedBg("assets/menu/bg.png", [0,0], [1280,0], [self.all_sprites])
        self.title = Text("assets/font/batmfa_.ttf", 70, "GameOver", "white", [400,300])

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
        return super().events(event)

    def update(self):

        self.bg.update()
        self.title.draw()
        return super().update()