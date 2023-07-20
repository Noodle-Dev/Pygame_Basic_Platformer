import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Buneta")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        #Player Setup
        self.img = pygame.image.load('../assets/player.png')
        self.img.set_colorkey((0, 0, 0))
        self.img_pos = [160, 260]
        self.movement = [False, False]

        self.collision_area = pygame.rect(50, 50, 300, 50)

    def run(self):
        while True:
            self.screen.fill(('#000000'))
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
            self.screen.blit(self.img, self.img_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #DOWN    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                #UP
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)

Game().run()