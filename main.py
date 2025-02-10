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
    cat_cursor = load_image('cursor/Cat_cursor.png')

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


SPEED = 2
FPS = 60
SIZE = WIDTH, HEIGHT = 1200, 630
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
CURSOR = pygame.sprite.Group()
pygame.init()
pygame.mouse.set_visible(False)
Cursor(CURSOR)


def main_menu():
    button_start = Button(WIDTH / 2 - (370 / 2), 70, 370, 150, '', 'main_menu/new_1.png', 'main_menu/new_2.png',
                          'data/music/main_menu/button/aim.mp3', 'data/music/main_menu/button/clik.mp3')
    button_exit = Button(900, 500, 300, 120, '', 'main_menu/exit_1.png', 'main_menu/exit_2.png',
                         'data/music/main_menu/button/aim.mp3', 'data/music/main_menu/button/clik.mp3')
    # button_music = Button
    main_music = pygame.mixer.Sound('data/music/main_menu/Night of Bloom.mp3')
    main_music.play(-1)
    main_music.set_volume(0.4)

    running = True
    new = False
    background = load_image('main_menu/main_background.jpg')

    def draw():
        SCREEN.blit(background, (0, 0))
        button_exit.draw(pygame.mouse.get_pos())
        button_start.draw(pygame.mouse.get_pos())
        CURSOR.draw(SCREEN)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                CURSOR.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
                button_start.event(pygame.mouse.get_pos(), event)
                button_exit.event(pygame.mouse.get_pos(), event)

            if event.type == pygame.USEREVENT and event.button == button_exit:
                running = False
            if event.type == pygame.USEREVENT and event.button == button_start:
                running = False
                new = True
        CLOCK.tick(FPS)
        draw()
        pygame.display.flip()

    if new:
        main_music.stop()
        start()
    terminate()


def start():
    # Golem(load_image('fight/golem/golem.png'),
    #        10, 0.5)

    Kasumi(load_image('fight/Kasumi/Kasumi.png'), 10, 0.5)

    main_music = pygame.mixer.Sound('data/music/beginning/Make yourself at home.mp3')
    main_music.play(-1)
    main_music.set_volume(0.8)

    main_hero = pygame.sprite.Group()
    hero = Hero(main_hero)
    running = True
    walls_group = pygame.sprite.Group()
    texture_path = "1-st floor/floor.png"
    walls_data = pygame.sprite.Group(
        Wall(665, 236, 582, 17, texture_path, walls_group),
        Wall(689, 114, 23, 120, texture_path, walls_group),
        Wall(410, 131, 372, 17, texture_path, walls_group),
        Wall(248, 128, 360, 14, texture_path, walls_group),
        Wall(608, 241, 21, 109, texture_path, walls_group),
        Wall(665, 260, 329, 18, texture_path, walls_group),
        Wall(651, 446, 11, 285, texture_path, walls_group),
        Wall(357, 429, 291, 18, texture_path, walls_group),
        Wall(771, 443, 705, 12, texture_path, walls_group),
        Wall(456, 443, 134, 12, texture_path, walls_group),
        Wall(153, 444, 19, 306, texture_path, walls_group),
        Wall(156, 444, 559, 12, texture_path, walls_group),
        Wall(394, 270, 29, 134, texture_path, walls_group),
        Wall(367, 347, 29, 84, texture_path, walls_group),
        Wall(503, 277, 17, 115, texture_path, walls_group),
        Wall(482, 350, 24, 80, texture_path, walls_group),
        Wall(801, 594, 28, 593, texture_path, walls_group),
        Wall(799, 598, 27, 554, texture_path, walls_group),
        Wall(796, 603, 21, 409, texture_path, walls_group),
        Wall(1, 599, 774, 20, texture_path, walls_group),
        Wall(0, 598, 750, 18, texture_path, walls_group),
        Wall(-1, 596, 752, 15, texture_path, walls_group),
        Wall(-4, 598, 328, 18, texture_path, walls_group),
        Wall(-2, 2, 20, 578, texture_path, walls_group),
        Wall(0, -1, 18, 554, texture_path, walls_group),
        Wall(2, 2, 17, 401, texture_path, walls_group),
        Wall(773, 14, 754, 11, texture_path, walls_group),
        Wall(745, 14, 722, 11, texture_path, walls_group),
        Wall(759, 17, 714, 14, texture_path, walls_group),
        Wall(769, 23, 383, 19, texture_path, walls_group),)

    # for wall in walls_data:
    #     x, y, width, height = wall
    #     Wall(x, y, width, height, texture_path, walls_group)

    camera = Camera(1500, 1000)

    def draw():
        SCREEN.fill((0, 0, 0))
        for sprite in walls_group:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        for sprite in main_hero:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        CURSOR.draw(SCREEN)

    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                CURSOR.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
                Dialog(['Похоже Капи сделал диалоги...', 'Я не очень понимаю зачем он себя так "убивает"', 'Мне его жалко...', 'Эй, не беспокойся, с ним всё будет хорошо.'],
                       ['dialog/Ann/meow.png', 'dialog/Ann/angru_sad.png'],
                       ['dialog/main_hero/perplexed.png', 'dialog/main_hero/cute_1.png']).dialog(draw)

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

        camera.update(hero)
        CLOCK.tick(FPS)
        draw()
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    from app.hero import Hero, HeroFight
    from app.fighting.fighting_systems import MainFight
    from app.fighting.main_fighters import Golem, Kasumi
    from app.system import Button, Camera
    from app.world import Wall, Door, Dialog

    main_menu()
