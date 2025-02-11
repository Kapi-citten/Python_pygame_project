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
        sound_clik=None,
    ):

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
    def __init__(self, screen_width, screen_height):
        self.offset_x = 0
        self.offset_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, target, map_width, map_height):
        x = target.rect.centerx - self.screen_width // 2
        y = target.rect.centery - self.screen_height // 2

        x = max(0, min(x, map_width - self.screen_width))
        y = max(0, min(y, map_height - self.screen_height))
        self.offset_x = x
        self.offset_y = y

    def apply(self, obj):
        if hasattr(obj, 'rect'):
            return obj.rect.move(-self.offset_x, -self.offset_y)
        elif isinstance(obj, pygame.Rect):
            return obj.move(-self.offset_x, -self.offset_y)
        else:
            raise TypeError("apply: объект не имеет атрибута rect")

    def apply_rect(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)
