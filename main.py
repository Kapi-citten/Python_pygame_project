import pygame
import os
import sys


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


def m():
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
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    speed = 2

    fps = 60
    clock = pygame.time.Clock()
    cursor = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    Cursor(cursor)

    m()