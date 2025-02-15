import pygame
from main import load_image, SPEED

SPEED_FIGHT = 6
class Hero(pygame.sprite.Sprite):
    image = load_image("hero/down/move_s_1.png")

    def __init__(self, group):
        super().__init__(group)

        self.hero_d = [load_image(f"hero/right/move_d_{i}.png") for i in range(1, 9)]

        self.hero_a = [load_image(f"hero/left/move_a_{i}.png") for i in range(1, 9)]

        self.hero_s = [load_image(f"hero/down/move_s_{i}.png") for i in range(1, 9)]

        self.hero_w = [load_image(f"hero/up/move_w_{i}.png") for i in range(1, 9)]

        self.hero_wd = [load_image(f"hero/up_right/move_w_d_{i}.png") for i in range(1, 9)]
        self.hero_wa = [load_image(f"hero/up_left/move_w_a_{i}.png") for i in range(1, 9)]
        self.hero_sa = [load_image(f"hero/down_left/move_s_a_{i}.png") for i in range(1, 9)]
        self.hero_sd = [load_image(f"hero/down_right/move_s_d_{i}.png") for i in range(1, 9)]

        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.mov_index = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, mov, walls_group, npc_group, plants_group):
        # mov = args[0].key
        old_rect = self.rect.copy()

        if mov == 'wd':
            self.image = self.hero_wd[self.mov_index // 8]
            self.rect = self.rect.move(SPEED, -SPEED)

        elif mov == 'wa':
            self.image = self.hero_wa[self.mov_index // 8]
            self.rect = self.rect.move(-SPEED, -SPEED)

        elif mov == 'sa':
            self.image = self.hero_sa[self.mov_index // 8]
            self.rect = self.rect.move(-SPEED, SPEED)

        elif mov == 'sd':
            self.image = self.hero_sd[self.mov_index // 8]
            self.rect = self.rect.move(SPEED, SPEED)

        elif mov == 'w':
            self.image = self.hero_w[self.mov_index // 8]
            self.rect = self.rect.move(0, -SPEED)

        elif mov == 's':
            self.image = self.hero_s[self.mov_index // 8]
            self.rect = self.rect.move(0, SPEED)

        elif mov == 'a':
            self.image = self.hero_a[self.mov_index // 8]
            self.rect = self.rect.move(-SPEED, 0)

        elif mov == 'd':
            self.image = self.hero_d[self.mov_index // 8]
            self.rect = self.rect.move(SPEED, 0)

        else:
            self.image = self.hero_s[0]

        self.mov_index += 1
        if self.mov_index >= 64:
            self.mov_index = 0

        # self.mask = pygame.mask.from_surface(self.image)
        for wall in walls_group:
            if pygame.sprite.collide_mask(self, wall):
                self.rect = old_rect
        
        for npc in npc_group:
            if pygame.sprite.collide_mask(self, npc):
                self.rect = old_rect
        
        if pygame.sprite.spritecollide(self, plants_group, False, pygame.sprite.collide_mask):
            self.rect = old_rect  

    def get(self):
        return self.image


class HeroFight(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = load_image('fight/heart.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 301
        self.rect.y = 301

    def update(self, mov, walls):
        old_rect = self.rect.copy()

        if mov == 'wd':
            self.rect = self.rect.move(SPEED_FIGHT, -SPEED_FIGHT)

        elif mov == 'wa':
            self.rect = self.rect.move(-SPEED_FIGHT, -SPEED_FIGHT)

        elif mov == 'sa':
            self.rect = self.rect.move(-SPEED_FIGHT, SPEED_FIGHT)

        elif mov == 'sd':
            self.rect = self.rect.move(SPEED_FIGHT, SPEED_FIGHT)

        elif mov == 'w':
            self.rect = self.rect.move(0, -SPEED_FIGHT)

        elif mov == 's':
            self.rect = self.rect.move(0, SPEED_FIGHT)

        elif mov == 'a':
            self.rect = self.rect.move(-SPEED_FIGHT, 0)

        elif mov == 'd':
            self.rect = self.rect.move(SPEED_FIGHT, 0)

        if not walls.contains(self.rect):
            self.rect = old_rect