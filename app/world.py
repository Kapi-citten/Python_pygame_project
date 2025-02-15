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
            all_text = ['']
            for j in self.text[i]:
                for txt in j:
                    all_text_draw = []
                    if txt != '|':
                        all_text[-1] += txt
                    else:
                        all_text.append('')
                    for one_text in all_text:
                        all_text_draw.append(font.render(one_text, True, (255, 255, 255)))
                    draw_method()
                    if self.main_hero:
                        SCREEN.blit(self.image_hero[self.n], (860, 170))
                    else:
                        SCREEN.blit(self.image_npc[self.n], (0, 200))
                    SCREEN.fill(pygame.Color(self.color), self.rect)
                    [CURSOR.update(event) for event in pygame.event.get() if
                     event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused()]
                    for index in range(len(all_text_draw)):
                        SCREEN.blit(all_text_draw[index], (self.x, self.y + index * 40))
                        CURSOR.draw(SCREEN)
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

                draw_method()
                if self.main_hero:
                    SCREEN.blit(self.image_hero[self.n], (860, 170))
                else:
                    SCREEN.blit(self.image_npc[self.n], (0, 200))

                SCREEN.fill(pygame.Color(self.color), self.rect)
                for index in range(len(all_text_draw)):
                    SCREEN.blit(all_text_draw[index], (self.x, self.y + index * 40))
                CURSOR.draw(SCREEN)

                CLOCK.tick(self.fps)
                pygame.display.flip()

            if self.main_hero:
                self.main_hero = False
                self.n += 1
            else:
                self.main_hero = True


def сhoice(draw_method):
    button_no = Button(400, 400, 200, 50, "Говорить", "main_menu/exit_1.png", "main_menu/exit_2.png")
    button_yes = Button(650, 400, 200, 50, "Драться", "fight/attack_1.png", "fight/attack_2.png")

    def draw():
        draw_method()
        button_yes.draw(pygame.mouse.get_pos())
        button_no.draw(pygame.mouse.get_pos())
        CURSOR.draw(SCREEN)

    t = True
    agree = False
    while t:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t = False
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                CURSOR.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
                button_no.event(pygame.mouse.get_pos(), event)
                button_yes.event(pygame.mouse.get_pos(), event)

            if event.type == pygame.USEREVENT and event.button == button_no:
                t = False
            if event.type == pygame.USEREVENT and event.button == button_yes:
                t = False
                agree = True
        draw()
        pygame.display.flip()

    if agree:
        return True
    return False


class NPC(Wall):
    def __init__(self, x, y, w, h, image_path, group, fight_info, dialog, npc_img, hero_img, draw, dialog_yes, dialog_no, other_music):
        super().__init__(x, y, w, h, image_path, group)

        self.dialog_yes = dialog_yes
        self.dialog_no = dialog_no
        self.draw = draw
        self.other_music = other_music
        self.dialog = dialog  # Текст диалога
        self.fight_info = fight_info
        self.npc_img = npc_img  # Изображение NPC в диалоге
        self.hero_img = hero_img  # Изображение героя в диалоге
        self.fight_done = False  # Проверка, был ли бой

    def start_dialog(self):
        if not self.fight_done:
            dialog_box = Dialog(self.dialog, self.npc_img, self.hero_img)
            dialog_box.dialog(self.draw)
            if сhoice(self.draw):
                self.dialog_yes.dialog(self.draw)
                self.other_music.stop()
                self.fight_info[0](self.fight_info[1],self.fight_info[2],self.fight_info[3])
                self.other_music.play()
                self.fight_done = True
            else:
                self.dialog_no.dialog(self.draw)


