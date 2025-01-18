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

# класс глав героя
class Hero(pygame.sprite.Sprite):
    image = load_image("hero_stay.png")

    def __init__(self, group):
        super().__init__(group)
        hero_d = [load_image(f'hero_d_{i}.png') for i in range(1, 5)]
        hero_a = [load_image(f'hero_a_{i}.png') for i in range(1, 5)]
        hero_s = [load_image(f'hero_s_{i}.png') for i in range(1, 5)]
        hero_w = [load_image(f'hero_w_{i}.png') for i in range(1, 5)]
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.frame_index = 0
        self.direction = 'stay'
        self.animations = {
            'w': self.hero_w,
            's': self.hero_s,
            'a': self.hero_a,
            'd': self.hero_d
        }

    def update(self, mov):
        if mov == 119:
            self.direction = 'w'
            self.rect = self.rect.move(0, -10)
        elif mov == 115:
            self.direction = 's'
            self.rect = self.rect.move(0, 10)
        elif mov == 97:
            self.direction = 'a'
            self.rect = self.rect.move(-10, 0)
        elif mov == 100:
            self.direction = 'd'
            self.rect = self.rect.move(10, 0)
        else:
            self.direction = 'stay'

    def update_animation(self):
        if self.direction in self.animations:
            frames = self.animations[self.direction]
            self.frame_index += 0.2
            if self.frame_index >= len(frames):
                self.frame_index = 0
            self.image = frames[int(self.frame_index)]


def main():
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

    main()
