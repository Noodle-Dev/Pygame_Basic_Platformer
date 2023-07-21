import pygame
import sys
from entities import PhysicalEntity
from utils import load_image

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Buneta")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            'player':load_image('../assets/player.png')
        }
        self.player = PhysicalEntity(self, 'player', (50,50), (8,15))

    def run(self):
        while True:
            self.screen.fill(('#000000'))
            self.player.update((self.movement[1] - self.movement[0], 0)) 
            self.player.render(self.screen)   

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

            pygame.display.update()
            self.clock.tick(60)

Game().run()