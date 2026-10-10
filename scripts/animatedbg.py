import pygame
from scripts.obj import Obj
from scripts.settings import *


class AnimatedBg:

    def __init__(self, img, pos1, pos2,  group):
        self.bg = Obj(img, pos1, group)
        self.bg2 = Obj(img, pos2, group)

    def update(self):

        self.bg.rect.x += -1
        self.bg2.rect.x += -1
        
        if self.bg.rect.x <= -self.bg.rect.width:
            self.bg.rect.x = self.bg2.rect.x + self.bg2.rect.width
        elif self.bg2.rect.x <= -self.bg2.rect.width:
            self.bg2.rect.x = self.bg.rect.x + self.bg.rect.width