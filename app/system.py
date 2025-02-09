import pygame
from main import load_image, SCREEN


class Button:
    def __init__(
            self,
            x,
            y,
            width,
            height,
            text,
            image_path,
            hover_image_path=None,
            sound_aim=None,
            sound_clik=None):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.is_aim_sound = True

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        if hover_image_path is None:
            self.hover_image = self.image
        else:
            self.hover_image = load_image(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

        if sound_aim:
            self.sound_aim = pygame.mixer.Sound(sound_aim)
        else:
            self.sound_aim = None

        if sound_clik:
            self.sound_clik = pygame.mixer.Sound(sound_clik)
        else:
            self.sound_clik = None

    def draw(self, mouse_pos):

        if self.rect.collidepoint(mouse_pos):
            SCREEN.blit(self.hover_image, (self.x, self.y))

            if self.sound_aim and self.is_aim_sound:
                self.sound_aim.play()
                self.is_aim_sound = False
        else:
            self.is_aim_sound = True
            SCREEN.blit(self.image, (self.x, self.y))

    def event(self, mouse_pos, *event):
        if self.rect.collidepoint(mouse_pos) and event[0].button == 1:
            if self.sound_clik:
                self.sound_clik.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN.get_width()), x)
        y = max(-(self.height - SCREEN.get_height()), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
