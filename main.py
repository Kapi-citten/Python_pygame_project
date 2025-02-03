import pygame
import os
import sys

SPEED = 2
FPS = 60
SIZE = WIDTH, HEIGHT = 1200, 630
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
CURSOR = pygame.sprite.Group()


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
    #           10, [load_image(f'fight/golem/stone_{i}.png') for i in range(1, 4)], 0.5)

    main_hero = pygame.sprite.Group()
    hero = Hero(main_hero)
    running = True
    walls_group = pygame.sprite.Group()
    texture_path = "1-st floor/floor.png"
    walls_data = pygame.sprite.Group(
        Wall(100, 100, 50, 200, texture_path, walls_group),
        Wall(300, 50, 100, 50, texture_path, walls_group),
        Wall(500, 300, 150, 50, texture_path, walls_group),
        Wall(200, 400, 50, 150, texture_path, walls_group))

    # for wall in walls_data:
    #     x, y, width, height = wall
    #     Wall(x, y, width, height, texture_path, walls_group)

    camera = Camera(1500, 1500)

    def draw():
        for sprite in walls_group:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        for sprite in main_hero:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        CURSOR.draw(SCREEN)

    while running:
        SCREEN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                CURSOR.update(event)

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
    from app.fighting.main_fighters import Golem
    from app.system import Button, Cursor, Camera
    from app.world import Wall, Door, Dialog
    pygame.init()
    pygame.mouse.set_visible(False)
    Cursor(CURSOR)
    main_menu()
