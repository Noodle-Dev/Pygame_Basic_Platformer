import pygame
import sys
from entities import PhysicalEntity
from utils import load_image, load_images
from tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Buneta")
        self.screen = pygame.display.set_mode((640, 480))
        self.display =  pygame.Surface((640, 480)) #Half if its needed

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]

        self.assets = {
            'decor' : load_images('../assets/Tiles/decoration'),
            'grass' : load_images('../assets/Tiles/grass'),
            'large_decor' : load_images('../assets/Tiles/large_decor'),
            'stone' : load_images('../assets/Tiles/stone'),
            'player':load_image('../assets/player.png')
        }
        print(self.assets)
        self.player = PhysicalEntity(self, 'player', (50,50), (8,15))
        
        self.tilemap = Tilemap(self, tile_size = 16)

    def run(self):
        while True:
            self.display.fill(('#000000'))

            self.tilemap.render(self.display)

            self.player.update((self.movement[1] - self.movement[0], 0)) 
            self.player.render(self.display)   

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #DOWN    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                #UP
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()