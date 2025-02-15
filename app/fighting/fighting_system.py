from app.hero import HeroFight
from main import SCREEN, CURSOR, CLOCK, pygame, terminate, load_image
from app.system import Button


class MainFight:
    def __init__(self, npc, hp, damage):
        SCREEN.fill((0, 0, 0))
        self.fps = 60

        self.damage_music = pygame.mixer.Sound('data/music/fight/damage.mp3')
        self.mercy = True
        self.image_npc = npc
        self.rect_npc = self.image_npc.get_rect()
        self.rect_npc.center = (600, 120)
        self.n = 1

        self.weapon_in_battle = pygame.sprite.Group()
        self.hp = hp
        self.damage = damage

        self.hero_group = pygame.sprite.Group()
        HeroFight(self.hero_group)
        self.hero = self.hero_group.sprites()[0]
        self.hero_hp = 200
        self.rect = pygame.Rect(100, 250, 1000, 370)
        self.time = 4
        self.button_attack = Button(50, 20, 305, 150, '', 'fight/attack_1.png', 'fight/attack_2.png',
                                    'data/music/main_menu/button/aim.mp3', 'data/music/main_menu/button/clik.mp3')
        self.button_mercy = Button(850, 20, 305, 150, '', 'fight/mercy_1.png', 'fight/mercy_2.png',
                                   'data/music/main_menu/button/aim.mp3', 'data/music/main_menu/button/clik.mp3')

        # self.mask = pygame.mask.Mask((self.rect.width, self.rect.height))
        # self.mask.fill()

        # self.rect_mask = pygame.mask.Mask.get_rect(width=1000, height=600, center=(10, 5))
        pygame.draw.rect(SCREEN, 'red', self.rect, 8)
        self.start_ticks = pygame.time.get_ticks()

        self.timer = 0.5
        # self.battle_analysis()

    def draw_health_bar(self):
        hero_bar_width = 300
        hero_bar_height = 20
        hero_bar_x = 50
        hero_bar_y = 50
        max_hp = 200
        hero_health_ratio = self.hero_hp / max_hp

        pygame.draw.rect(SCREEN, (255, 0, 0), (hero_bar_x, hero_bar_y, hero_bar_width, hero_bar_height))
        pygame.draw.rect(SCREEN, (0, 255, 0),
                         (hero_bar_x, hero_bar_y, hero_bar_width * hero_health_ratio, hero_bar_height))
        pygame.draw.rect(SCREEN, (255, 255, 255), (hero_bar_x, hero_bar_y, hero_bar_width, hero_bar_height), 2)

    def draw_fight(self):
        SCREEN.fill((0, 0, 0))
        pygame.draw.rect(SCREEN, 'red', self.rect, 8)
        SCREEN.blit(self.image_npc, self.rect_npc)
        self.hero_group.draw(SCREEN)
        self.weapon_in_battle.draw(SCREEN)
        self.draw_health_bar()
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

                    if not self.n >= 5:
                        self.n += 1
                        self.mercy = True
                    else:
                        self.mercy_end()
                        return True
                    t = False

                if event.type == pygame.USEREVENT and event.button == self.button_attack:
                    self.hp -= 3
                    self.n += 1
                    self.mercy = False
                    if self.hp <= 0:
                        self.killer_end()
                        return True
                    t = False
            SCREEN.fill((0, 0, 0))
            pygame.draw.rect(SCREEN, 'red', self.rect, 8)
            SCREEN.blit(self.image_npc, self.rect_npc)
            self.hero_group.draw(SCREEN)
            self.button_attack.draw(pygame.mouse.get_pos())
            self.button_mercy.draw(pygame.mouse.get_pos())
            CURSOR.draw(SCREEN)
            pygame.display.flip()
        self.timer_apdate()
        self.start_ticks = pygame.time.get_ticks()

    def new_logic(self):
        pass

    def timer_apdate(self):
        pass

    def battle_analysis(self):
        self.start_ticks = pygame.time.get_ticks()
        run = True
        music = False
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
                    if not music:
                        self.damage_music.play()
                        music = True
                    else:
                        music = False

            if (pygame.time.get_ticks() - self.start_ticks) / 1000 > self.time:
                if self.draw():
                    self.main_music.stop()
                    return

            else:
                self.draw_fight()
            pygame.display.flip()
            CLOCK.tick(self.fps)

            if self.hero_hp <= 0:
                self.main_music.stop()
                self.game_over()
                return None

    def game_over(self):
        music_over = pygame.mixer.Sound('data/music/fight/over.mp3')
        music_over.play(-1)
        music_over.set_volume(0.5)
        run = True
        start_timer = pygame.time.get_ticks()
        index = 0
        over_image = [load_image(f'fight/game_over_{i}.jpg') for i in range(1, 5)]
        def draw(i):
            SCREEN.blit(over_image[i // 20], (0, 0))
            CURSOR.draw(SCREEN)
            CLOCK.tick(80)
            pygame.display.flip()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and (pygame.time.get_ticks() - start_timer) / 1000 >= 5:
                    run = False
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    CURSOR.update(event)
            index += 1
            if index == 80:
                index = 0
            draw(index)
        music_over.stop()
    def mercy_end(self):
        pass

    def killer_end(self):
        pass
