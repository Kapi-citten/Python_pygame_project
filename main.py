import pygame
import os
import sys
import random


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join("data/image", name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Cursor(pygame.sprite.Sprite):
    cat_cursor = load_image("cursor/Cat_cursor.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Cursor.cat_cursor
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        cord = args[0].pos
        self.rect.x = cord[0]
        self.rect.y = cord[1]


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image_path, group):
        super().__init__(group)
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Door(Wall):
    pass


class Button:
    def __init__(
            self,
            x,
            y,
            width,
            height,
            text,
            image_path,
            hover_image_path=None,
            sound_aim=None,
            sound_clik=None):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.is_aim_sound = True

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        if hover_image_path is None:
            self.hover_image = self.image
        else:
            self.hover_image = load_image(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

        if sound_aim:
            self.sound_aim = pygame.mixer.Sound(sound_aim)
        else:
            self.sound_aim = None

        if sound_clik:
            self.sound_clik = pygame.mixer.Sound(sound_clik)
        else:
            self.sound_clik = None

    def draw(self, mouse_pos):

        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hover_image, (self.x, self.y))

            if self.sound_aim and self.is_aim_sound:
                self.sound_aim.play()
                self.is_aim_sound = False
        else:
            self.is_aim_sound = True
            screen.blit(self.image, (self.x, self.y))

    def event(self, mouse_pos, *event):
        if self.rect.collidepoint(mouse_pos) and event[0].button == 1:
            if self.sound_clik:
                self.sound_clik.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


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
        self.rect.x = 0
        self.rect.y = 0
        self.mov_index = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, mov, walls_group):
        # mov = args[0].key
        old_rect = self.rect.copy()

        if mov == 'wd':
            self.image = self.hero_wd[self.mov_index // 8]
            self.rect = self.rect.move(speed, -speed)

        elif mov == 'wa':
            self.image = self.hero_wa[self.mov_index // 8]
            self.rect = self.rect.move(-speed, -speed)

        elif mov == 'sa':
            self.image = self.hero_sa[self.mov_index // 8]
            self.rect = self.rect.move(-speed, speed)

        elif mov == 'sd':
            self.image = self.hero_sd[self.mov_index // 8]
            self.rect = self.rect.move(speed, speed)

        elif mov == 'w':
            self.image = self.hero_w[self.mov_index // 8]
            self.rect = self.rect.move(0, -speed)

        elif mov == 's':
            self.image = self.hero_s[self.mov_index // 8]
            self.rect = self.rect.move(0, speed)

        elif mov == 'a':
            self.image = self.hero_a[self.mov_index // 8]
            self.rect = self.rect.move(-speed, 0)

        elif mov == 'd':
            self.image = self.hero_d[self.mov_index // 8]
            self.rect = self.rect.move(speed, 0)

        else:
            self.image = self.hero_s[0]

        self.mov_index += 1
        if self.mov_index >= 64:
            self.mov_index = 0

        # self.mask = pygame.mask.from_surface(self.image)
        for wall in walls_group:
            if pygame.sprite.collide_mask(self, wall):
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
            self.rect = self.rect.move(speed, -speed)

        elif mov == 'wa':
            self.rect = self.rect.move(-speed, -speed)

        elif mov == 'sa':
            self.rect = self.rect.move(-speed, speed)

        elif mov == 'sd':
            self.rect = self.rect.move(speed, speed)

        elif mov == 'w':
            self.rect = self.rect.move(0, -speed)

        elif mov == 's':
            self.rect = self.rect.move(0, speed)

        elif mov == 'a':
            self.rect = self.rect.move(-speed, 0)

        elif mov == 'd':
            self.rect = self.rect.move(speed, 0)

        if not walls.contains(self.rect):
            self.rect = old_rect


class Map:
    def __init__(self, image_path):
        self.image = load_image(image_path)
        self.rect = self.image.get_rect()

    def draw(self, camera_offset):
        # Рисуем карту с учётом сдвига камеры
        screen.blit(self.image, (-camera_offset[0], -camera_offset[1]))


class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.offset_x = 0
        self.offset_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height

    def update(self, target):
        target_x = target.rect.centerx - self.screen_width // 2
        target_y = target.rect.centery - self.screen_height // 2

        target_x = max(0, min(target_x, self.map_width - self.screen_width))
        target_y = max(0, min(target_y, self.map_height - self.screen_height))

        self.offset_x += (target_x - self.offset_x) * 0.1
        self.offset_y += (target_y - self.offset_y) * 0.1

        def update(self, target):
            self.offset_x = max(0,
                                min(target.rect.centerx - self.screen_width // 2, self.map_width - self.screen_width))
            self.offset_y = max(0, min(target.rect.centery - self.screen_height // 2,
                                       self.map_height - self.screen_height))

        print(self.offset_y, self.offset_x)

    def get_offset(self):
        return [self.offset_x, self.offset_y]


class Dialog:
    # TODO: базовое окно для диалога со всеми отдельными персонажами
    def __init__(self, scp_text_list, hero_text_list, npc_img_list, hero_img_list, x=0, y=600, width=1200,
                 height=100, color='blue'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scp_text = scp_text_list
        self.hero_text = hero_text_list
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

        self.image_npc = [load_image(npc_img_list[i]) for i in range(len(npc_img_list))]
        self.image_hero = [load_image(hero_img_list[i]) for i in range(len(hero_img_list))]

        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

    def dialog(self):
        screen.fill(pygame.Color(self.color), self.rect)


class MainFight:
    def __init__(self, npc, hp, weapon, damage):
        screen.fill((0, 0, 0))
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
        pygame.draw.rect(screen, 'red', self.rect, 8)
        self.start_ticks = pygame.time.get_ticks()

        self.timer = 0.3
        self.weapon = weapon
        self.battle_analysis()

    def draw_fight(self):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, 'red', self.rect, 8)
        screen.blit(self.image_npc, self.rect_npc)
        self.hero_group.draw(screen)
        self.weapon_in_battle.draw(screen)
        cursor.draw(screen)

    def draw(self):
        self.weapon_in_battle = pygame.sprite.Group()
        t = True
        while t:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    cursor.update(event)

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
                    self.n += 1
                    self.hp -= 2
                    print(self.hp)
                    if self.mercy:
                        self.n = 2
                        self.mercy = False
                    else:
                        self.n += 1
                    t = False
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, 'red', self.rect, 8)
            screen.blit(self.image_npc, self.rect_npc)
            self.hero_group.draw(screen)
            self.button_attack.draw(pygame.mouse.get_pos())
            self.button_mercy.draw(pygame.mouse.get_pos())
            cursor.draw(screen)
            pygame.display.flip()
        self.timer = 0.3
    def new_logic(self):
        pass

    def battle_analysis(self):
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    cursor.update(event)

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
                    print(self.hero_hp)

            if (pygame.time.get_ticks() - self.start_ticks) / 1000 > 10:
                self.draw()

            else:
                self.draw_fight()
            pygame.display.flip()
            clock.tick(self.fps)
        # if not pygame.sprite.collide_mask(self.rect_mask, self.hero):
        #     self.rect = self.rect.move(0, 1)


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



def main_menu():
    button_start = Button(WIDTH / 2 - (370 / 2), 70, 370, 150, '', 'main_menu/new_1.png', 'main_menu/new_2.png',
                          'data/music/main_menu/button/aim.mp3', 'data/music/main_menu/button/clik.mp3')
    button_exit = Button(900, 500, 300, 120, '', 'main_menu/exit_1.png', 'main_menu/exit_2.png',
                         'data/music/main_menu/button/aim.mp3', 'data/music/main_menu/button/clik.mp3')
    # button_music = Button
    main_music = pygame.mixer.Sound('data/music/main_menu/Night of Bloom.mp3')
    main_music.play(-1)

    running = True
    new = False
    background = load_image('main_menu/main_background.jpg')

    def draw():
        screen.blit(background, (0, 0))
        button_exit.draw(pygame.mouse.get_pos())
        button_start.draw(pygame.mouse.get_pos())
        cursor.draw(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                cursor.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
                button_start.event(pygame.mouse.get_pos(), event)
                button_exit.event(pygame.mouse.get_pos(), event)

            if event.type == pygame.USEREVENT and event.button == button_exit:
                running = False
            if event.type == pygame.USEREVENT and event.button == button_start:
                running = False
                new = True
        clock.tick(fps)
        draw()
        pygame.display.flip()

    if new:
        main_music.stop()
        start()
    terminate()


def start():
    Golem(load_image('fight/golem/golem.png'),
              10, [load_image(f'fight/golem/stone_{i}.png') for i in range(1, 4)], 0.5)

    main_hero = pygame.sprite.Group()
    Hero(main_hero)
    running = True
    walls_group = pygame.sprite.Group()
    texture_path = "1-st floor/floor.png"
    walls_data = pygame.sprite.Group(
        Wall(100, 100, 50, 200, texture_path, walls_group),
        Wall(300, 50, 100, 50, texture_path, walls_group),
        Wall(500, 300, 150, 50, texture_path, walls_group),
        Wall(200, 400, 50, 150, texture_path, walls_group))

    game_map = Map("main_menu/main.jpg")
    map_width, map_height = game_map.rect.size
    camera = Camera(1200, 630, map_width, map_height)

    # for wall in walls_data:
    #     x, y, width, height = wall
    #     Wall(x, y, width, height, texture_path, walls_group)

    def draw():
        walls_group.draw(screen)
        game_map.draw(camera.get_offset())  # Рисуем карту
        for sprite in walls_group:
            screen.blit(sprite.image, (sprite.rect.x - camera.offset_x, sprite.rect.y - camera.offset_y))
        main_hero.draw(screen)
        cursor.draw(screen)

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                cursor.update(event)

        pressed = pygame.key.get_pressed()

        if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            main_hero.update('wd', walls_group)

        elif (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            main_hero.update('wa', walls_group)

        elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            main_hero.update('sd', walls_group)

        elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            main_hero.update('sa', walls_group)

        elif pressed[pygame.K_UP] or pressed[pygame.K_w]:
            main_hero.update('w', walls_group)

        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            main_hero.update('d', walls_group)

        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            main_hero.update('s', walls_group)

        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            main_hero.update('a', walls_group)

        else:
            main_hero.update(None, walls_group)

        for hero in main_hero:
            camera.update(hero)

        clock.tick(fps)
        draw()
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    size = WIDTH, HEIGHT = 1200, 630
    screen = pygame.display.set_mode(size)
    speed = 2
    fps = 60
    clock = pygame.time.Clock()
    cursor = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    Cursor(cursor)
    main_menu()
