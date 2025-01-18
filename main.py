import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data/image', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print("Файл с изображением '{fullname}' не найден")
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
    image = load_image("hero_stay.png")

    def __init__(self, group):
        super().__init__(group)

        hero_d = [load_image('hero/down/move_d_1.png'), load_image('hero/down/move_d_2.png'),
                  load_image('hero/down/move_d_3.png'), load_image('hero/down/move_d_4.png'),
                  load_image('hero/down/move_d_5.png'), load_image('hero/down/move_d_6.png'),
                  load_image('hero/down/move_d_7.png'), load_image('hero/down/move_d_8.png')]

        hero_a = [load_image('hero/down/move_a_1.png'), load_image('hero/down/move_a_2.png'),
                  load_image('hero/down/move_a_3.png'), load_image('hero/down/move_a_4.png'),
                  load_image('hero/down/move_a_5.png'), load_image('hero/down/move_a_6.png'),
                  load_image('hero/down/move_a_7.png'), load_image('hero/down/move_a_8.png')]

        hero_s = [load_image('hero/down/move_s_1.png'), load_image('hero/down/move_s_2.png'),
                  load_image('hero/down/move_s_3.png'), load_image('hero/down/move_s_4.png'),
                  load_image('hero/down/move_s_5.png'), load_image('hero/down/move_s_6.png'),
                  load_image('hero/down/move_s_7.png'), load_image('hero/down/move_s_8.png')]

        hero_w = [load_image('hero/down/move_w_1.png'), load_image('hero/down/move_w_2.png'),
                  load_image('hero/down/move_w_3.png'), load_image('hero/down/move_w_4.png'),
                  load_image('hero/down/move_w_5.png'), load_image('hero/down/move_w_6.png'),
                  load_image('hero/down/move_w_7.png'), load_image('hero/down/move_w_8.png')]

        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mov_index = 0

    def update(self, mov):
        # mov = args[0].key
        if mov == 119:
            self.rect = self.rect.move(0, -10)
        elif mov == 115:
            self.rect = self.rect.move(0, 10)
        elif mov == 97:
            self.image = load_image("K.png")
            self.rect = self.rect.move(-10, 0)
        elif mov == 100:
            self.image = load_image("K_r.png")
            self.rect = self.rect.move(10, 0)


def m():
    running = True

    def draw():
        cursor.draw(screen)

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                cursor.update(event)

        draw()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    cursor = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    Cursor(cursor)

    m()
