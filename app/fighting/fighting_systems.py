from app.hero import HeroFight
from main import SCREEN, CURSOR, CLOCK, pygame, terminate
from app.system import Button

class MainFight:
    def __init__(self, npc, hp, weapon, damage):
        SCREEN.fill((0, 0, 0))
        self.fps = 170

        self.mercy = True
        self.image_npc = npc
        self.rect_npc = self.image_npc.get_rect()
        self.rect_npc.center = (600, 120)
        self.n = 1

        self.weapon = weapon
        self.weapon_in_battle = pygame.sprite.Group()
        self.hp = hp
        self.damage = damage

        self.hero_group = pygame.sprite.Group()
        HeroFight(self.hero_group)
        self.hero = self.hero_group.sprites()[0]
        self.hero_hp = 50
        self.rect = pygame.Rect(100, 250, 1000, 370)

        self.button_attack = Button(50, 20, 270, 150, '', 'fight/attack_1.png', 'fight/attack_2.png',
                                   'data/music/main_menu/button/aim.mp3', 'data/music/main_menu/button/clik.mp3')
        self.button_mercy = Button(850, 20, 270, 150, '', 'fight/mercy_1.png', 'fight/mercy_2.png',
                                    'data/music/main_menu/button/aim.mp3', 'data/music/main_menu/button/clik.mp3')

        # self.mask = pygame.mask.Mask((self.rect.width, self.rect.height))
        # self.mask.fill()

        # self.rect_mask = pygame.mask.Mask.get_rect(width=1000, height=600, center=(10, 5))
        pygame.draw.rect(SCREEN, 'red', self.rect, 8)
        self.start_ticks = pygame.time.get_ticks()

        self.timer = 0.3
        self.weapon = weapon
        self.battle_analysis()

    def draw_fight(self):
        SCREEN.fill((0, 0, 0))
        pygame.draw.rect(SCREEN, 'red', self.rect, 8)
        SCREEN.blit(self.image_npc, self.rect_npc)
        self.hero_group.draw(SCREEN)
        self.weapon_in_battle.draw(SCREEN)
        CURSOR.draw(SCREEN)

    def draw(self):
        self.weapon_in_battle = pygame.sprite.Group()
        t = True
        while t:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    CURSOR.update(event)

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
                    self.button_mercy.event(pygame.mouse.get_pos(), event)
                    self.button_attack.event(pygame.mouse.get_pos(), event)

                if event.type == pygame.USEREVENT and event.button == self.button_mercy:
                    self.start_ticks = pygame.time.get_ticks()

                    if not self.mercy:
                        self.n = 2
                        self.mercy = False
                    else:
                        self.n += 1
                    t = False

                if event.type == pygame.USEREVENT and event.button == self.button_attack:
                    self.start_ticks = pygame.time.get_ticks()
                    self.hp -= 2
                    print(self.hp)
                    if self.mercy:
                        self.n = 2
                        self.mercy = False
                    else:
                        self.n += 1
                    t = False
            SCREEN.fill((0, 0, 0))
            pygame.draw.rect(SCREEN, 'red', self.rect, 8)
            SCREEN.blit(self.image_npc, self.rect_npc)
            self.hero_group.draw(SCREEN)
            self.button_attack.draw(pygame.mouse.get_pos())
            self.button_mercy.draw(pygame.mouse.get_pos())
            CURSOR.draw(SCREEN)
            pygame.display.flip()
        self.timer = 0.3
    def new_logic(self):
        pass

    def battle_analysis(self):
        self.start_ticks = pygame.time.get_ticks()
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    CURSOR.update(event)

            if self.rect.contains(self.hero.rect):
                pressed = pygame.key.get_pressed()

                if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
                    self.hero_group.update('wd', self.rect)

                elif (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
                    self.hero_group.update('wa', self.rect)

                elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (
                        pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
                    self.hero_group.update('sd', self.rect)

                elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (
                        pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
                    self.hero_group.update('sa', self.rect)

                elif pressed[pygame.K_UP] or pressed[pygame.K_w]:
                    self.hero_group.update('w', self.rect)

                elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                    self.hero_group.update('d', self.rect)

                elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                    self.hero_group.update('s', self.rect)

                elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                    self.hero_group.update('a', self.rect)
                else:
                    self.hero_group.update(None, self.rect)

            self.new_logic()

            for weapon in self.weapon_in_battle.sprites():
                if pygame.sprite.collide_mask(weapon, self.hero):
                    self.hero_hp -= self.damage

            if (pygame.time.get_ticks() - self.start_ticks) / 1000 > 10:
                self.draw()

            else:
                self.draw_fight()
            pygame.display.flip()
            CLOCK.tick(self.fps)
        # if not pygame.sprite.collide_mask(self.rect_mask, self.hero):
        #     self.rect = self.rect.move(0, 1)