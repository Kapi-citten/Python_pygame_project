import pygame
import os
import sys


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
    def __init__(self, x, y, width, height, texture_path, group):
        super().__init__(group)
        self.image = load_image(texture_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_collision(self, sprite):
        return self.rect.colliderect(sprite.rect)


class Button:
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None, sound_aim=None, sound_clik=None):
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

    def draw(self, scr, mouse_pos):

        if self.rect.collidepoint(mouse_pos):
            scr.blit(self.hover_image, (self.x, self.y))

            if self.sound_aim and self.is_aim_sound:
                self.sound_aim.play()
                self.is_aim_sound = False
        else:
            self.is_aim_sound = True
            scr.blit(self.image, (self.x, self.y))

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

        for wall in walls_group:
            if wall.check_collision(self):
                self.rect = old_rect

# class Dialog:
#     # TODO: базовое окно для диалога со всеми отдельными персонажами
#     def __init__(self, scp_text_list, hero_text_list, npc_img_list, hero_img_list, x=0, y=600, width=1200,
#                  height=100, color='blue'):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.scp_text = scp_text_list
#         self.hero_text = hero_text_list
#         self.rect = pygame.Rect(x, y, width, height)
#         self.color = color
#
#         self.image_npc = [load_image(npc_img_list[i]) for i in range(len(npc_img_list))]
#         self.image_hero = [load_image(hero_img_list[i]) for i in range(len(hero_img_list))]
#
#         self.image = pygame.transform.scale(self.image, (width, height))
#
#         self.rect = self.image.get_rect(topleft=(x, y))
#
#     def dialog(self):
#         screen.fill(pygame.Color(self.color), self.rect)

# class Fight:
#     def __init__(self, npc, weapon_list, hp, damage):
#         self.image = load_image(npc)
#         self.weapon = weapon_list
#         self.hp = hp
#         self.damage = damage
#
#         self.hero = load_image('')
#         self.mask = pygame.mask.from_surface(self.image)
#         self.hero_hp = 50


def main_menu():
    button_start = Button(width / 2 - (370 / 2), 70, 370, 150, '', 'main_menu/new_1.png', 'main_menu/new_2.png',
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
        button_exit.draw(screen, pygame.mouse.get_pos())
        button_start.draw(screen, pygame.mouse.get_pos())
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
    main_hero = pygame.sprite.Group()
    Hero(main_hero)
    running = True
    walls_group = pygame.sprite.Group()
    texture_path = "hero/down/move_s_1.png"
    walls_data = [
        (100, 100, 50, 200),
        (300, 50, 100, 50),
        (500, 300, 150, 50),
        (200, 400, 50, 150),
    ]

    for wall_data in walls_data:
        x, y, width, height = wall_data
        Wall(x, y, width, height, texture_path, walls_group)

    def draw():
        screen.blit('')
        main_hero.draw(screen)
        walls_group.draw(screen)
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

        clock.tick(fps)
        draw()
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    size = width, height = 1200, 630
    screen = pygame.display.set_mode(size)

    speed = 2

    fps = 60
    clock = pygame.time.Clock()
    cursor = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    Cursor(cursor)

    main_menu()
