import pygame
import random
from app.world import Dialog
from main import load_image
from app.fighting.fighting_systems import MainFight


class Golem(MainFight):
    def __init__(self, npc, hp, weapon, damage):
        self.main_music = pygame.mixer.Sound('data/music/beginning/Stone_heart.mp3')
        self.main_music.play(-1)
        self.main_music.set_volume(0.5)
        super().__init__(npc, hp, weapon, damage)

    class Stone(pygame.sprite.Sprite):
        def __init__(self, group, weapon, phase, n = True):
            super().__init__(group)
            self.image = weapon[random.randint(0, 2)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            if phase == 1:
                self.rect.x = random.randint(100, 1000)
                self.rect.y = 0

            elif phase == 2:
                self.rect.x = 0
                self.rect.y = random.randint(200, 600)

            elif phase == 3:
                self.rect.x = random.randint(100, 1000)
                self.rect.y = 600

            elif phase == 4:
                self.rect.x = 1150
                self.rect.y = random.randint(200, 600)

            elif phase == 5:
                if n:
                    self.rect.x = 0
                    self.rect.y = random.randint(200, 600)
                else:
                    self.rect.x = random.randint(100, 1000)
                    self.rect.y = 0
                self.n = n


            else:
                self.rect.x = 350
                self.rect.y = 360
            self.phase = phase

        def update(self):
            if self.phase == 1:
                self.rect.y += 4

            elif self.phase == 2:
                self.rect.x += 4

            elif self.phase == 3:
                self.rect.y -= 4

            elif self.phase == 4:
                self.rect.x -= 4

            elif self.phase == 5:
                if self.n:
                    self.rect.x += 5
                else:
                    self.rect.y += 4


    def new_logic(self):
        if (pygame.time.get_ticks() - self.start_ticks) / 1000 >= self.timer:
            if self.n == 1:
                    self.timer += 0.17
                    self.Stone(self.weapon_in_battle, self.weapon, self.n)

            if self.n == 2:
                    self.timer += 0.21
                    self.Stone(self.weapon_in_battle, self.weapon, self.n)

            if self.n == 3:
                    self.timer += 0.17
                    self.Stone(self.weapon_in_battle, self.weapon, self.n)

            if self.n == 4:
                    self.timer += 0.21
                    self.Stone(self.weapon_in_battle, self.weapon, self.n)

            if self.n == 5:
                    self.timer += 0.4
                    self.Stone(self.weapon_in_battle, self.weapon, self.n)
                    self.Stone(self.weapon_in_battle, self.weapon, self.n, False)
        self.weapon_in_battle.update()

    def timer_apdate(self):
        if self.n == 2:
            self.timer = 0.2
            if self.mercy:
                Dialog(['Ты щадишь меня...? Это шутка? Давай, бей пока я не распластал тебя об камни!',
                        'Я...Не шучу...', ],
                       ['dialog/Golem/golem.png'],
                       ['dialog/main_hero/perplexed.png']).dialog(self.draw_fight)

            else:
                Dialog(['Готовься к настоящеё атаке!','Пфф.. Ты не сильнее пугала'],
                       ['dialog/Golem/golem.png'],
                       ['dialog/main_hero/perplexed.png']).dialog(self.draw_fight)

        elif self.n == 3:
            self.timer = 0.2
        elif self.n == 4:
            self.timer = 0.2
        elif self.n == 5:
            self.time = 15
            self.timer = 2
