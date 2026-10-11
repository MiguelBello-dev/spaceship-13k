import pygame
from src.obj import Obj
from src.settings import *

class Scene:

    def __init__(self):

        self.display = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.active = True 

        self.fade = Fade(5)

    def events(self, event):
        pass

    def draw(self, display):
        self.all_sprites.draw(self.display)

    def update(self):
        self.fade.draw()
        self.all_sprites.update()

class Fade:

    def __init__(self, speed):

        self.display = pygame.display.get_surface()
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.fill("black")

        self.alpha = 255
        self.speed = speed

    def draw(self):

        if self.alpha > 0:
            self.alpha -= self.speed

        self.surface.set_alpha(self.alpha)
        self.display.blit(self.surface, [0,0])