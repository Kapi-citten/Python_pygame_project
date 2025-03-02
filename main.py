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
    #        10, 0.5).battle_analysis()


    main_music = pygame.mixer.Sound('data/music/beginning/Make yourself at home.mp3')
    main_music.play(-1)
    main_music.set_volume(0.8)

    main_hero = pygame.sprite.Group()
    hero = Hero(main_hero)
    running = True
    walls_group = pygame.sprite.Group()
    map_image = load_image('world/map.png')
    map_image = pygame.transform.scale(map_image, (2624, 1554))
    texture_path = "world/wall.png"
    walls_data = pygame.sprite.Group(
        Wall(962, 763, 367, 40, texture_path, walls_group),
        Wall(1433, 763, 375, 40, texture_path, walls_group),
        Wall(1792, 779, 16, 112, texture_path, walls_group),
        Wall(1793, 892, 318, 15, texture_path, walls_group),
        Wall(2096, 908, 15, 289, texture_path, walls_group),
        Wall(551, 1182, 1544, 17, texture_path, walls_group),
        Wall(390, 1183, 161, 16, texture_path, walls_group),
        Wall(383, 870, 21, 314, texture_path, walls_group),
        Wall(404, 870, 561, 12, texture_path, walls_group),
        Wall(962, 779, 16, 104, texture_path, walls_group),
        Wall(964, 884, 19, 108, texture_path, walls_group),
        Wall(963, 1089, 17, 91, texture_path, walls_group),
        Wall(1792, 907, 13, 96, texture_path, walls_group),
        Wall(1783, 1074, 21, 108, texture_path, walls_group),
        Wall(826, 4, 1795, 8, texture_path, walls_group),
        Wall(15, 5, 811, 8, texture_path, walls_group),
        Wall(7, 5, 9, 989, texture_path, walls_group),
        Wall(6, 995, 13, 547, texture_path, walls_group),
        Wall(20, 1529, 1773, 15, texture_path, walls_group),
        Wall(1793, 1530, 823, 11, texture_path, walls_group),
        Wall(2608, 14, 12, 876, texture_path, walls_group),
        Wall(2609, 890, 7, 640, texture_path, walls_group),
    )

    npc_group = pygame.sprite.Group()
    doors_group = pygame.sprite.Group(
        Door(1329, 763, 104, 40, "world/door.jpg", "world/door_open.png", walls_group),
    )

    def draw():
        SCREEN.blit(map_image, camera.apply_rect(map_image.get_rect()))
        for sprite in walls_group:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        for sprite in main_hero:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        for sprite in npc_group:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        CURSOR.draw(SCREEN)


    kapi = Kapi(x=1000, y=600, w=45,
        image_path="world/NPC/Kapi.png",
        group=npc_group, dialog=Dialog(
            ['Я рад тебя видеть :3... |И в следующей версии я буду предлагать тебе обучение', 'Хорошо, увидимся!| Пока можешь, поговорить с Касуми'],
                                       ['dialog/Kapi^3/kapicute.png'], ['dialog/main_hero/cute_1.png']))

    kasumi = NPC(
        x=1100, y=900, w=46,
        image_path="world/NPC/Kasumi.png",
        group=npc_group,
        dialog=[
            "Хмм... *Подняла на тебя недобродушный взгляд* |Можешь не говорить кто ты, я и так знаю... Я Касуми. Ты наверное по поводу преступления?",
            "Ну...."],
        npc_img=["dialog/Kasumi/Kasumi.png"],
        hero_img=["dialog/main_hero/cute_1.png"], draw=draw,
        fight_info=[Kasumi, load_image('fight/Kasumi/Kasumi.png'), 10, 0.5],
        dialog_yes=Dialog(['Эх... Глупыш... Мне жаль.. но..', 'Я расследую это дело! Никаких "НО".',
                           '*Суёт руку в карман и что-то там нащупывает* |Ты думал я так просто скажу...? Ты ошибся...',
                           'Касуми... Постой, если ты не хочешь... |*Касуми нападает на вас*'],
                          ['dialog/Kasumi/Kasumi.png', 'dialog/Kasumi/Kasumi.png'],
                          ['dialog/main_hero/perplexed.png', 'dialog/main_hero/omg.png']),
        dialog_no=Dialog(
            ['Окей... *лицо приняло более миловидный вид* |Если что нужно обращайся ^^', 'Хорошо, увидимся!'],
            ['dialog/Kasumi/Kasumi_meow.png'], ['dialog/main_hero/cute_1.png']),
        other_music=main_music)

    # npc_group.add(kasumi)
    # npc_group.add(kapi)

    camera = Camera(1200, 630)

    while running:
        # Dialog(['Эх... Глупыш... Мне жаль.. но..', 'Я расследую это дело! Никаких "НО".',
        #         '*Суёт руку в карман и что-то там нащупывает* |Ты думал я так просто скажу...? Ты ошибся...',
        #         'Касуми... Постой, если ты не хочешь... |*Касуми нападает на вас*'],
        #        ['dialog/Kasumi/Kasumi.png', 'dialog/Kasumi/Kasumi.png'],
        #        ['dialog/main_hero/perplexed.png', 'dialog/main_hero/omg.png']).dialog(draw)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                CURSOR.update(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                for npc in npc_group:
                    if hero.rect.colliderect(npc.rect):
                        if npc.start_dialog():
                            main_menu()
                for door in doors_group:
                    door.interact(hero.rect)

        pressed = pygame.key.get_pressed()

        if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            main_hero.update('wd', walls_group, npc_group)

        elif (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            main_hero.update('wa', walls_group, npc_group)

        elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            main_hero.update('sd', walls_group, npc_group)

        elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            main_hero.update('sa', walls_group, npc_group)

        elif pressed[pygame.K_UP] or pressed[pygame.K_w]:
            main_hero.update('w', walls_group, npc_group)

        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            main_hero.update('d', walls_group, npc_group)

        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            main_hero.update('s', walls_group, npc_group)

        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            main_hero.update('a', walls_group, npc_group)

        else:
            main_hero.update(None, walls_group, npc_group)

        camera.update(hero, 2624, 1554)
        CLOCK.tick(FPS)
        draw()
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    from app.hero import Hero, HeroFight
    from app.fighting.main_fighters import Golem, Kasumi
    from app.system import Button, Camera
    from app.world import Wall, Door, Dialog, NPC, Kapi

    main_menu()
