import pygame
from main import load_image, SCREEN


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image_path, group):
        super().__init__(group)
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Door(Wall):
    pass


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
        SCREEN.fill(pygame.Color(self.color), self.rect)