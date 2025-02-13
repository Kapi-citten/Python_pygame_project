import pygame

from main import load_image, SCREEN
from main import FPS, CLOCK, terminate, CURSOR
from app.system import Button
from app.fighting.fighting_system import MainFight


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
        while running:
            SCREEN.fill((0, 0, 0))
            
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

            SCREEN.fill((0, 0, 0))
            SCREEN.blit(self.image, self.rect)
            self.button_talk.draw(pygame.mouse.get_pos())
            self.button_fight.draw(pygame.mouse.get_pos())

            pygame.display.flip()

    def draw_npc(self):
        SCREEN.blit(self.image, self.rect)
