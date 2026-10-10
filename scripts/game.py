import pygame
import random
from scripts.scene import Scene
from scripts.obj import Obj
from scripts.animatedbg import AnimatedBg
from scripts.settings import *
from scripts.text import Text


class Game(Scene):

    def __init__(self):
        super().__init__()

        self.bg = AnimatedBg("assets/menu/bg.png", [0,0], [1280,0], [self.all_sprites])
        self.spaceship = SpaceShip("assets/nave/nave1.png", [30, 360], [self.all_sprites])

        self.pts = 0
        self.score_text = Text("assets/font/batmfa_.ttf", 20, "Score: ", "white", [560,30])
        self.score_pts = Text("assets/font/batmfa_.ttf", 20, "0", "white", [670,30])

        self.life = Obj("assets/hud/coracao.png", [550, 60], [self.all_sprites])
        self.life2 = Obj("assets/hud/coracao.png", [610, 60], [self.all_sprites])
        self.life3 = Obj("assets/hud/coracao.png", [670, 60], [self.all_sprites])

        self.tick = 0
        self.enemy_colision = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.music = pygame.mixer.Sound("assets/sons/bg.ogg")
        self.music.play(-1)

    def hud(self):
        if self.spaceship.life == 2:
            self.life3.kill()
        elif self.spaceship.life == 1:
            self.life2.kill()
        elif self.spaceship.life == 0:
            self.life.kill()

    def spanw_enemy(self):
        self.tick += 1
        if self.tick == 60:
            SmallShip("assets/nave/inimigo0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.enemy_colision])
        elif self.tick == 180:
            MediumShip("assets/nave/inimigo2-0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.enemy_colision])
            MediumShip("assets/nave/inimigo2-0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.enemy_colision])
        elif self.tick == 270:
            SmallShip("assets/nave/inimigo0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.enemy_colision])
            SmallShip("assets/nave/inimigo0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.enemy_colision])
            SmallShip("assets/nave/inimigo0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.enemy_colision])
            SmallShip("assets/nave/inimigo0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.enemy_colision])
            PowerUp("assets/nave/powerup0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.powerups])
        elif self.tick == 320:
            BigShip("assets/nave/inimigo3-0.png", [1380, random.randint(50, 670)], [self.all_sprites, self.enemy_colision])

            self.tick = 0

    def colision(self):
        for shot in self.spaceship.shots:
            for enemy in self.enemy_colision:
                if shot.rect.colliderect(enemy.rect):
                    shot.kill()
                    enemy.life -= 1
                    self.pts += 1
                    self.score_pts.update_text(str(self.pts))

                    sound = pygame.mixer.Sound("assets/sons/block.ogg")
                    sound.play()

                    if enemy.life <= 0:
                        x = enemy.rect.x + enemy.image.get_width() / 2
                        y = enemy.rect.y + enemy.image.get_height() / 2
                        Explosion("assets/explosao/0.png", [x, y], [self.all_sprites])

        for enemy in self.enemy_colision:
            if self.spaceship.rect.colliderect(enemy.rect):
                enemy.kill()
                self.spaceship.life -= 1
                self.spaceship.level = 1
                sound = pygame.mixer.Sound("assets/sons/damage.ogg")
                sound.play()

        for powerup in self.powerups:
            if self.spaceship.rect.colliderect(powerup.rect):
                powerup.kill()
                self.spaceship.level += 1
                sound = pygame.mixer.Sound("assets/sons/levelup.ogg")
                sound.play()

    def gameover(self):

        if self.spaceship.life <= 0:
            self.music.stop()
            self.active = False

    def update(self):
        self.spaceship.shots.draw(self.display)
        self.spaceship.shots.update()
        self.colision()
        self.bg.update()
        self.spaceship.input()
        self.spanw_enemy()
        self.score_text.draw()
        self.score_pts.draw()
        self.gameover()
        self.hud()
        return super().update()

class SpaceShip(Obj):

    def __init__(self, img, pos, *groups):
        super().__init__(img, pos, *groups)

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.life = 3
        self.level = 1
        self.shots = pygame.sprite.Group()
        self.ticks = 0

    def input(self):

        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.direction.y = -1
        elif key[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if key[pygame.K_a]:
            self.direction.x = -1
        elif key[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if key[pygame.K_SPACE]:
            self.ticks += 1
            if self.ticks > 30:
                self.ticks = 0
                sound = pygame.mixer.Sound("assets/sons/shot.ogg")
                sound.play()
                if self.level == 1:
                    Shot("assets/tiro/tiro.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                elif self.level == 2:
                    Shot("assets/tiro/tiro2.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                elif self.level == 3:
                    Shot("assets/tiro/tiro3.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                elif self.level == 4:
                    Shot("assets/tiro/tiro4.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                    Shot("assets/tiro/tiro4.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                elif self.level == 5:
                    Shot("assets/tiro/tiro.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                    Shot("assets/tiro/tiro.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                elif self.level == 6:
                    Shot("assets/tiro/tiro2.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                    Shot("assets/tiro/tiro2.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                elif self.level == 7:
                    Shot("assets/tiro/tiro3.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                    Shot("assets/tiro/tiro3.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                else:
                    Shot("assets/tiro/tiro4.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                    Shot("assets/tiro/tiro4.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                    Shot("assets/tiro/tiro4.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])
                    Shot("assets/tiro/tiro4.png", [self.rect.x + 195, self.rect.y + 15], [self.shots])

    def limit(self):

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - self.image.get_width():
            self.rect.x = WIDTH -  self.image.get_width()

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > HEIGHT - self.image.get_width():
            self.rect.y = HEIGHT - self.image.get_width()

    def move(self):

        self.rect.center += self.direction * self.speed

    def update(self):
        self.animation(8, 3, "assets/nave/nave")
        self.limit()
        self.input()
        self.move()

class Shot(Obj):

    def __init__(self, img, pos, *groups):
        super().__init__(img, pos, *groups)

        self.speed = 10

    def update(self):
        self.rect.x += self.speed

        if self.rect.x > 1300:
            self.kill()

class Enemy(Obj):

    def __init__(self, img, pos, *groups):
        super().__init__(img, pos, *groups)

        self.speed = 6
        self.life = 3

    def destruction(self):

        if self.life <= 0:
            self.kill()

    def limits(self):

        if self.rect.x < 0:
            self.kill()

    def move(self):

        self.rect.x -= self.speed

    def update(self):

        self.destruction()
        self.limits()
        self.move()

class SmallShip(Enemy):

    def __init__(self, img, pos, *groups):
        super().__init__(img, pos, *groups)

        self.speeed = 7
        self.life = 1

    def update(self):
        self.animation(8, 4, "assets/nave/inimigo")
        return super().update()

class MediumShip(Enemy):

    def __init__(self, img, pos, *groups):
        super().__init__(img, pos, *groups)

        self.speed = 5
        self.life = 3

    def update(self):
        self.animation(8, 4, "assets/nave/inimigo2-")
        return super().update()

class BigShip(Enemy):

    def __init__(self, img, pos, *groups):
        super().__init__(img, pos, *groups)

        self.speed = 1 
        self.life = 20

    def update(self):
        self.animation(8, 4, "assets/nave/inimigo3-")
        return super().update()

class PowerUp(Enemy):

    def __init__(self, img, pos, *groups):
        super().__init__(img, pos, *groups)

        self.speed = 2

    def update(self):
        self.animation(16, 1, "assets/nave/powerup")
        return super().update()

class Explosion(Obj):

    def __init__(self, img, pos, *groups):
        super().__init__(img, pos, *groups)

        self.ticks = 0

    def update(self):
        self.animation(5, 5, "assets/explosao/")
        self.ticks += 1
        if self.ticks > 25:
            self.kill()
        return super().update()