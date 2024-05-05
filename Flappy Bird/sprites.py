from typing import Any
import pygame
from settings import *
from random import randint

class BG(pygame.sprite.Sprite):
    def __init__(self, groups,scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load("fundo.png").convert()
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width*2, full_height))
        self.image.blit(full_sized_image,(0,0))
        self.image.blit(full_sized_image,(full_width,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 150*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups,scale_factor):
        super().__init__(groups)

        #image
        ground_surf = pygame.image.load("chao.png").convert_alpha()
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)

        #position
        self.rect = self.image.get_rect(bottomleft = (0, WIN_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 250*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

class Birdo(pygame.sprite.Sprite):
    def __init__(self, groups,scale_factor):
        super().__init__(groups)

        #image
        self.import_frames(scale_factor)
        self.fram_index = 0
        self.image = self.frames[self.fram_index]

        #rect
        self.rect = self.image.get_rect(midleft = (WIN_WIDTH / 20, WIN_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #movement
        self.gravity = 1200
        self.direction = 0

        #mask
        self.mask = pygame.mask.from_surface(self.image)
        
    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            birdoSprite = pygame.image.load(f"birdo{i}.png").convert_alpha()
            birdoScaled = pygame.transform.scale(birdoSprite, pygame.math.Vector2(birdoSprite.get_size()) * scale_factor)
            self.frames.append(birdoScaled)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = -350

    def animate(self, dt):
        self.fram_index += 5 * dt
        if self.fram_index >= len(self.frames):
            self.fram_index = 0
        self.image = self.frames[int(self.fram_index)]

    def rotate(self):
        rotated_birdo = pygame.transform.rotozoom(self.image, -self.direction*0.06, 1)
        self.image = rotated_birdo
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Cano(pygame.sprite.Sprite):
    def __init__(self, groups,scale_factor):
        super().__init__(groups)

        distancia = randint(0, 2)
        cano = pygame.image.load(f"cano{distancia}.png").convert_alpha()
        self.image = pygame.transform.scale(cano, pygame.math.Vector2(cano.get_size()) * scale_factor)
        
        correcao = 110
        if distancia == 1:
            correcao = 145
        elif distancia == 2:
            correcao = 180

        altura_maxima = - self.image.get_height()/2 + correcao
        altura_minima = WIN_HEIGHT - self.image.get_height()/2 - correcao - 80

        x = WIN_WIDTH + self.image.get_width()
        y = randint(round(altura_maxima), round(altura_minima))

        self.rect = self.image.get_rect(topleft = (x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 300 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()