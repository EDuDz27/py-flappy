import pygame, sys, time
from settings import *
from sprites import BG, Ground, Birdo, Cano

class Game:
    def __init__(self):

        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        #sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        #scale factor
        bg_height = pygame.image.load("fundo.png").get_height()
        self.scale_factor = WIN_HEIGHT / bg_height
        print(self.scale_factor)

        #sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.birdo = Birdo(self.all_sprites, self.scale_factor)

        #timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

    #collisions
    def collisions(self):
        if pygame.sprite.spritecollide(self.birdo, self.collision_sprites, False, pygame.sprite.collide_mask) or self.birdo.rect.top <= 0:
            pygame.quit()
            sys.exit()

    def run(self):
        last_time = time.time()
        #loop
        while True:

            #delta time
            dt = time.time() - last_time
            last_time = time.time()

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.birdo.jump()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.birdo.jump()

                if event.type == self.obstacle_timer: 
                    Cano([self.all_sprites, self.collision_sprites], self.scale_factor)

            #game logic
            self.display_surface.fill("black")
            self.all_sprites.update(dt)
            self.collisions()
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == "__main__":
    game = Game()
    game.run()