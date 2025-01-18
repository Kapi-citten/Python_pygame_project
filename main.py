import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data/image', name)
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


class Hero(pygame.sprite.Sprite):
    image = load_image("hero/down/move_s_1.png")

    def __init__(self, group):
        super().__init__(group)

        self.hero_d = [load_image('hero/right/move_d_1.png'), load_image('hero/right/move_d_2.png'),
                  load_image('hero/right/move_d_3.png'), load_image('hero/right/move_d_4.png'),
                  load_image('hero/right/move_d_5.png'), load_image('hero/right/move_d_6.png'),
                  load_image('hero/right/move_d_7.png'), load_image('hero/right/move_d_8.png')]

        self.hero_a = [load_image('hero/left/move_a_1.png'), load_image('hero/left/move_a_2.png'),
                  load_image('hero/left/move_a_3.png'), load_image('hero/left/move_a_4.png'),
                  load_image('hero/left/move_a_5.png'), load_image('hero/left/move_a_6.png'),
                  load_image('hero/left/move_a_7.png'), load_image('hero/left/move_a_8.png')]

        self.hero_s = [load_image('hero/down/move_s_1.png'), load_image('hero/down/move_s_2.png'),
                  load_image('hero/down/move_s_3.png'), load_image('hero/down/move_s_4.png'),
                  load_image('hero/down/move_s_5.png'), load_image('hero/down/move_s_6.png'),
                  load_image('hero/down/move_s_7.png'), load_image('hero/down/move_s_8.png')]

        self.hero_w = [load_image('hero/up/move_w_1.png'), load_image('hero/up/move_w_2.png'),
                  load_image('hero/up/move_w_3.png'), load_image('hero/up/move_w_4.png'),
                  load_image('hero/up/move_w_5.png'), load_image('hero/up/move_w_6.png'),
                  load_image('hero/up/move_w_7.png'), load_image('hero/up/move_w_8.png')]

        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mov_index = 0

    def update(self, mov):
        # mov = args[0].key

        if mov == 119:
            self.image = self.hero_w[self.mov_index // 8]
            self.rect = self.rect.move(0, -3)

        elif mov == 115:
            self.image = self.hero_s[self.mov_index // 8]
            self.rect = self.rect.move(0, 3)

        elif mov == 97:
            self.image = self.hero_a[self.mov_index // 8]
            self.rect = self.rect.move(-3, 0)

        elif mov == 100:
            self.image = self.hero_d[self.mov_index // 8]
            self.rect = self.rect.move(3, 0)

        else:
            self.image = self.hero_s[0]
        self.mov_index += 1
        if self.mov_index >= 64:
            self.mov_index = 0

def m():
    main_hero = pygame.sprite.Group()
    Hero(main_hero)
    running = True

    def draw():
        cursor.draw(screen)
        main_hero.draw(screen)

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                cursor.update(event)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            main_hero.update(119)

        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            main_hero.update(100)

        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            main_hero.update(115)

        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            main_hero.update(97)

        else:
            main_hero.update(None)

        clock.tick(fps)
        draw()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    fps = 60
    clock = pygame.time.Clock()
    cursor = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    Cursor(cursor)

    m()
