import pygame
import random
from main import load_image
from app.fighting.fighting_systems import MainFight

class Golem(MainFight):
    def __init__(self,  npc, hp, weapon, damage):
        super().__init__(npc, hp, weapon, damage)


    class Stone(pygame.sprite.Sprite):
        def __init__(self, group, weapon, phase):
            super().__init__(group)
            self.image = weapon[random.randint(0, 2)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            if phase == 1:
                self.rect.x = random.randint(200, 1000)
                self.rect.y = 0

            elif phase == 2:
                self.rect.x = 0
                self.rect.y = random.randint(200, 600)
            else:
                self.rect.x = 350
                self.rect.y = 360
            self.phase = phase
        def update(self):
            if self.phase == 1:
                self.rect.y += 4

            elif self.phase == 2:
                self.rect.x += 4

    def new_logic(self):
        if self.n == 4:
            self.timer = 0.3

        else:
            if (pygame.time.get_ticks() - self.start_ticks) / 1000 >= self.timer:
                print('ok')
                self.timer += 0.3
                print(self.timer)
                self.Stone(self.weapon_in_battle, self.weapon, self.n)

        self.weapon_in_battle.update()