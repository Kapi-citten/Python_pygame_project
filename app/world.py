import pygame

from main import load_image, SCREEN
from main import FPS, CLOCK, terminate, CURSOR


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
    def __init__(self, text_list, npc_img_list, hero_img_list, x=0, y=500, width=1200,
                 height=100, color='blue'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text_list
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.fps = FPS - 40
        self.main_hero = False
        self.n = 0

        self.image_npc = [load_image(npc_img_list[i]) for i in range(len(npc_img_list))]
        self.image_hero = [load_image(hero_img_list[i]) for i in range(len(hero_img_list))]

        # self.image = pygame.transform.scale(self.image, (width, height))

        # self.rect = self.image.get_rect(topleft=(x, y))

    def dialog(self, draw_method):
        font = pygame.font.Font(None, 36)
        for i in range(len(self.text)):
            s = ''

            for j in self.text[i]:
                for txt in j:
                    s += txt
                    text = font.render(s, True, (255, 255, 255))
                    draw_method()
                    if self.main_hero:
                        SCREEN.blit(self.image_hero[self.n], (860, 170))
                    else:
                        SCREEN.blit(self.image_npc[self.n], (0, 200))
                    SCREEN.fill(pygame.Color(self.color), self.rect)
                    [CURSOR.update(event) for event in pygame.event.get() if
                     event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused()]
                    CURSOR.draw(SCREEN)
                    SCREEN.blit(text, (self.x, self.y))
                    CLOCK.tick(self.fps)
                    pygame.display.flip()
            t = True
            while t:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                        CURSOR.update(event)

                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused() and self.rect.collidepoint(
                            pygame.mouse.get_pos()):
                        t = False

                text = font.render(s, True, (255, 255, 255))
                draw_method()
                if self.main_hero:
                    SCREEN.blit(self.image_hero[self.n], (860, 170))
                else:
                    SCREEN.blit(self.image_npc[self.n], (0, 200))

                SCREEN.fill(pygame.Color(self.color), self.rect)
                CURSOR.draw(SCREEN)
                SCREEN.blit(text, (self.x, self.y))
                CLOCK.tick(self.fps)
                pygame.display.flip()

            if self.main_hero:
                self.main_hero = False
                self.n += 1
            else:
                self.main_hero = True
