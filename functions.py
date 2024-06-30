import os
import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


function_sprites = pygame.sprite.Group()


class Pause(pygame.sprite.Sprite):
    def __init__(self, image, coords):
        super().__init__(function_sprites)
        self.sprite = image
        color = image.get_at((0, 0))
        image.set_colorkey(color)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def input(self):
        pass

    def animation(self):
        pass

    def move(self):
        pass

    def update(self):
        self.move()
        self.animation()
