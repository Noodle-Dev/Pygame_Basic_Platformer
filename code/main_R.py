import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from world_datas import World_data as wd

pygame.init()
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bunneta')

icon = pygame.image.load('../assets_img/app_icon.png')
pygame.display.set_icon(icon)

tile_size = 50
game_over = 0
main_menu = True

restart_img = pygame.image.load('../assets_img/UI/restart_btn.png')
start_img = pygame.image.load('../assets_img/UI/start_btn.png')
exit_img = pygame.image.load('../assets_img/UI/exit_btn.png')
enemies_group = pygame.sprite.Group()  # Initialize the enemies_group
lava_group = pygame.sprite.Group()

def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked == True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dy = 0
        dx = 0
        w_cooldown = 7
        if game_over == 0:
            key = pygame.key.get_pressed()
            on_ground = False
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x, self.rect.y + 1, self.width, self.height):
                    on_ground = True
                    break
            # Jump
            if key[pygame.K_SPACE] and on_ground and not self.jumped:
                self.vel_y += -20
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False

            # Movement
            dx = 0
            dy = 0
            w_cooldown = 7
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1

            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

            # Animation
            if self.counter > w_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

            # Jump animation
            if self.jumped:
                if self.direction == 1:
                    self.image = self.images_jump[0]
                else:
                    self.image = self.images_jump[1]
                if self.direction == -1:
                    self.image = pygame.transform.flip(self.image, True, False)

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Collision with tiles
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            #game over collisions
            if pygame.sprite.spritecollide(self, enemies_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            self.rect.x += dx
            self.rect.y += dy

            #if self.rect.bottom > screen_height:
             #   self.rect.bottom = screen_height
              #  dy = 0

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 5:
                self.rect.y -= 5
        
        
        
        screen.blit(self.image, self.rect)
        return game_over
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_jump = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load((f'../assets_img/Player/player_{num}.png'))
            img_right = pygame.transform.scale(img_right, (50, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 3):  # Add jump animation frames
            img_jump = pygame.image.load((f'../assets_img/Player/Jump/jump_{num}.png'))
            img_jump = pygame.transform.scale(img_jump, (50, 80))
            self.images_jump.append(img_jump)
            
        self.dead_import = pygame.image.load('../assets_img/Player/dead.png')
        self.dead_image = pygame.transform.scale(self.dead_import, (50, 80))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

class World():
    def __init__(self, data):
        self.tile_list = []
        gn_img = pygame.image.load('../assets_img/Tiles/gn.png')
        grass_img = pygame.image.load('../assets_img/Tiles/grass.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(gn_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemie = Enemy(col_count * tile_size, row_count * tile_size)
                    enemies_group.add(enemie)  # Add enemies to the enemies_group
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../assets_img/Enemies/enemie_1.png')
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the enemy image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height + 50
        self.move_direction = 1
        self.move_counter = 0
    def update(self):
        # Check if there's a ground tile below the enemy
        on_ground = False
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height):
                on_ground = True
                break

        # If not on the ground, adjust the y-coordinate
        if not on_ground:
            self.rect.y += 0

        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('../assets_img/Tiles/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height + 50
        self.move_direction = 1
        self.move_counter = 0

world = World(wd.world_data)
player = Player(100, screen_height - 130)
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 250, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 - 60, screen_height // 2, exit_img)

run = True
while run:
    screen.fill('#000000')
    clock.tick(60)

    world.draw()
    if main_menu == True:
       exit_button.draw()
       start_button.draw()
    else:
        pass

    if game_over == 0:
       enemies_group.update()  # Update the enemies
    enemies_group.draw(screen)  # Draw the enemies
    lava_group.draw(screen)
    game_over = player.update(game_over)

    if game_over == -1:
        if restart_button.draw():
           player.reset(100, screen_height - 130)
           game_over = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
