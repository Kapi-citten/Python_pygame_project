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
    class NPC(Wall):
        def __init__(self, x, y, w, h, image_path, group, fight_class, fight_image, hp, damage, dialog, npc_img, hero_img):
            super().__init__(x, y, w, h, image_path, group)

            self.fight_class = fight_class
            self.hp = hp
            self.damage = damage
            self.dialog = dialog  # Текст диалога
            self.fight_image = fight_image  # Изображение для боя
            self.npc_img = npc_img  # Изображение NPC в диалоге
            self.hero_img = hero_img  # Изображение героя в диалоге
            self.fight_done = False  # Проверка, был ли бой


            self.button_talk = Button(400, 400, 200, 50, "Говорить", "main_menu/exit_1.png", "main_menu/exit_2.png")
            self.button_fight = Button(650, 400, 200, 50, "Драться", "fight/attack_1.png", "fight/attack_2.png")

        def start_dialog(self):
            dialog_box = Dialog(self.dialog, self.npc_img, self.hero_img)
            dialog_box.dialog(self.draw_npc)

        def start_fight(self):
            if not self.fight_done:
                self.fight_class(load_image(self.fight_image), self.hp, self.damage)
                self.fight_done = True

        def interact(self):
            running = True
            menu_background = pygame.Surface((400, 200))
            menu_background.set_alpha(180)
            menu_background.fill((0, 0, 0))

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                        CURSOR.update(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.button_talk.rect.collidepoint(event.pos):
                            self.start_dialog()
                            running = False
                        elif self.button_fight.rect.collidepoint(event.pos):
                            self.start_fight()
                            running = False

                SCREEN.blit(map_image, camera.apply_rect(map_image.get_rect()))
                for sprite in walls_group:
                    SCREEN.blit(sprite.image, camera.apply(sprite))
                for sprite in main_hero:
                    SCREEN.blit(sprite.image, camera.apply(sprite))
                SCREEN.blit(self.image, camera.apply(self))

                SCREEN.blit(menu_background, (400, 350))

                self.button_talk.draw(pygame.mouse.get_pos())
                self.button_fight.draw(pygame.mouse.get_pos())

                CURSOR.draw(SCREEN)

                pygame.display.flip()

        def draw_npc(self):
            SCREEN.blit(self.image, self.rect)
    # Golem(load_image('fight/golem/golem.png'),
    #        10, 0.5)

    # Kasumi(load_image('fight/Kasumi/Kasumi.png'), 10, 0.5)

    main_music = pygame.mixer.Sound('data/music/beginning/Make yourself at home.mp3')
    main_music.play(-1)
    main_music.set_volume(0.8)

    camera = Camera(1200, 630)
    map_image = load_image('world/map.png')
    map_image = pygame.transform.scale(map_image, (2624, 1554))


    main_hero = pygame.sprite.Group()
    hero = Hero(main_hero)
    running = True
    walls_group = pygame.sprite.Group()
    texture_path = "world/wall.png"
    walls_data = pygame.sprite.Group(
        Wall(962, 763, 367, 16, texture_path, walls_group),
        Wall(1433, 764, 375, 14, texture_path, walls_group),
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

    kasumi = NPC(
        x=1100, y=900, w=50, h=100,
        image_path="fight/Kasumi/Kasumi.png",
        group=npc_group, fight_class=Kasumi, fight_image="fight/Kasumi/Kasumi.png",
        hp=10, damage=0.5,
        dialog=["Салам алейкум!", "Ты хочешь сразиться со мной?"],
        npc_img=["dialog/Kasumi/Kasumi.png"],
        hero_img=["dialog/main_hero/cute_1.png"]
    )

    npc_group.add(kasumi)


    def draw():
        SCREEN.blit(map_image, camera.apply_rect(map_image.get_rect()))
        for sprite in walls_group:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        for sprite in main_hero:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        for sprite in npc_group:
            SCREEN.blit(sprite.image, camera.apply(sprite))
        CURSOR.draw(SCREEN)

    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                CURSOR.update(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                for npc in npc_group:
                    if hero.rect.colliderect(npc.rect):
                        npc.interact()

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
    from app.fighting.fighting_system import MainFight
    from app.fighting.main_fighters import Golem, Kasumi
    from app.world import Wall, Door, Dialog
    from app.system import Button, Camera

    main_menu()
