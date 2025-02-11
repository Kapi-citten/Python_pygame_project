from cmath import phase

import pygame
import random
from app.world import Dialog
from main import load_image
from app.fighting.fighting_systems import MainFight


class Golem(MainFight):
    def __init__(self, npc, hp, weapon, damage):
        self.weapon = [load_image(f'fight/golem/stone_{i}.png') for i in range(1, 4)]
        self.main_music = pygame.mixer.Sound('data/music/beginning/Stone_heart.mp3')
        self.main_music.play(-1)
        self.main_music.set_volume(0.5)
        super().__init__(npc, hp, damage)

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



class Kasumi(MainFight):
    def __init__(self, npc, hp, damage):
        # self.main_music = pygame.mixer.Sound('data/music/fight/Dangerous sweetness.mp3')
        # self.main_music.play(-1)
        # self.main_music.set_volume(0.5)
        super().__init__(npc, hp, damage)

    class Knife(pygame.sprite.Sprite):
        def __init__(self, group, phase, n = True):
            super().__init__(group)
            self.image = load_image('fight/Kasumi/knife_1.png')

            self.knife_img = [load_image(f'fight/Kasumi/knife_{i}.png') for i in range(1, 19)]
            self.counter = 0
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()

            if phase == 1:
                self.rect.x = random.randint(100, 1000)
                self.rect.y = 0

            elif phase == 2:
                self.rect.x = 0
                self.rect.y = random.randint(200, 550)

            elif phase == 3:
                if n:
                    self.rect.x = 0
                    self.rect.y = random.randint(200, 550)

                else:
                    self.rect.x = random.randint(100, 1000)
                    self.rect.y = 0

                self.n = n


            elif phase == 5:
                if n:
                    self.rect.y = random.randint(200, 600)
                    self.rect.x = 0

                else:
                    self.rect.y = random.randint(200, 600)
                    self.rect.x = 1100

                self.n = n
            else:
                self.rect.x = 350
                self.rect.y = 360
            self.phase = phase

        def update(self):
            if self.phase == 1:
                self.rect.y += 4

            elif self.phase == 2:
                self.rect.x += 1
                self.image = self.knife_img[self.counter//4]
                self.counter += 1
                if self.counter >= 72:
                    self.counter = 0

            elif self.phase == 3:
                if self.n:
                    self.image = self.knife_img[self.counter // 4]
                    self.counter += 1
                    if self.counter >= 72:
                        self.counter = 0
                    self.rect.x += 5
                else:
                    self.image = self.knife_img[self.counter // 4]
                    self.counter += 1
                    if self.counter >= 72:
                        self.counter = 0
                    self.rect.y += 4

            elif self.phase == 5:
                if self.n:
                    self.image = self.knife_img[self.counter // 4]
                    self.counter += 1
                    if self.counter >= 72:
                        self.counter = 0
                    self.rect.x += 2
                else:
                    self.image = self.knife_img[self.counter // 4]
                    self.counter += 1
                    if self.counter >= 72:
                        self.counter = 0
                    self.rect.x -= 2


    class Fireball(pygame.sprite.Sprite):
        def __init__(self, group, phase, n = True):
            super().__init__(group)
            self.image = load_image('fight/Kasumi/fireball_right.png')
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()

            if phase == 4 or phase == 5:
                if n:
                    self.rect.x = random.randint(100, 800)
                else:
                    self.rect.x = random.randint(300, 1000)
                self.rect.y = 0
                self.n = n

            self.phase = phase


        def update(self):
            if self.phase == 4 or self.phase == 5:
                if self.n:
                    self.rect.x += 1
                else:
                    self.rect.x -= 1
                self.rect.y += 3

    def new_logic(self):
        if (pygame.time.get_ticks() - self.start_ticks) / 1000 >= self.timer:
            if self.n == 1:
                    self.timer += 0.09
                    self.Knife(self.weapon_in_battle, self.n)

            if self.n == 2:
                    self.timer += 0.7
                    self.Knife(self.weapon_in_battle, self.n)

            if self.n == 3:
                    self.timer += 0.5
                    self.Knife(self.weapon_in_battle, self.n)
                    self.Knife(self.weapon_in_battle, self.n, False)

            if self.n == 4:
                    self.timer += 0.4
                    self.Fireball(self.weapon_in_battle, self.n)
                    self.Fireball(self.weapon_in_battle, self.n, False)

            if self.n == 5:
                    self.timer += 0.7
                    self.Fireball(self.weapon_in_battle, self.n)
                    self.Fireball(self.weapon_in_battle, self.n, False)
                    self.Knife(self.weapon_in_battle, self.n)
                    self.Knife(self.weapon_in_battle, self.n, False)
        self.weapon_in_battle.update()

    def timer_apdate(self):
        if self.n == 2:
            self.timer = 0.2
            if self.mercy:
                Dialog(['Пощада... Хорошо, придётся просто бить беспомощного котика...',
                        'Эй! Я не беспомощный!'],
                       ['dialog/Kasumi/Kasumi.png'],
                       ['dialog/main_hero/perplexed.png']).dialog(self.draw_fight)

            else:
                Dialog(['Хе-хе... Что ж... Я приподам тебе урок фехтования... Последний в твоей жизни!',
                        'Ещё посмотрим кто кого!'],
                       ['dialog/Kasumi/Kasumi.png'],
                       ['dialog/main_hero/perplexed.png']).dialog(self.draw_fight)

        elif self.n == 3:
            self.timer = 0.2
        elif self.n == 4:
            self.timer = 0.2
        elif self.n == 5:
            self.time = 15
            self.timer = 2


class Ann(MainFight):
    def __init__(self, npc, hp, damage):
        self.main_music = pygame.mixer.Sound()
        self.main_music.play(-1)
        self.main_music.set_volume(0.5)
        super().__init__(npc, hp, damage)

    class Lian(pygame.sprite.Sprite):
        def __init__(self, group, phase, n = True):
            super().__init__(group)
            self.image = load_image('fight/Kasumi/knife.png')
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
                    self.Knife(self.weapon_in_battle, self.n)

            if self.n == 2:
                    self.timer += 0.21
                    self.Knife(self.weapon_in_battle, self.n)

            if self.n == 3:
                    self.timer += 0.17
                    self.Knife(self.weapon_in_battle, self.n)

            if self.n == 4:
                    self.timer += 0.21
                    self.Knife(self.weapon_in_battle, self.n)

            if self.n == 5:
                    self.timer += 0.4
                    self.Knife(self.weapon_in_battle, self.n)
                    self.Knife(self.weapon_in_battle, self.n, False)
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
