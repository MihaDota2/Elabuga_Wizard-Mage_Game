import pygame
import math
from functions import load_image

# Группа спрайтов заклинаний
spell_sprites = pygame.sprite.Group()


# Класс заклинаний
class Spell(pygame.sprite.Sprite):
    def __init__(self, image, coords, final_coords, size, type, mode, speed, damage, time):
        super().__init__(spell_sprites)
        self.sprite = image
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        # self.final_coords = final_coords
        self.x = final_coords[0] - self.rect.x
        self.y = final_coords[1] - self.rect.y
        self.counter = 0

        self.type = type
        self.mode = mode
        self.speed = speed
        self.damage = damage
        self.time = time

    def animation(self):
        pass

    # Выбор картинки спрайта в зависимости от типа снаряда
    def elemental(self):
        if self.mode == 1:
            if self.type == 1:
                self.image = load_image('Spell_fire.png')
            if self.type == 2:
                self.image = load_image('Spell_water.png')
            if self.type == 3:
                self.image = load_image('Spell_earth.png')
            if self.type == 4:
                self.image = load_image('Spell_wing.png')
        if self.mode == 2:
            if self.type == 1:
                self.image = load_image('Build_fire.png')
            if self.type == 2:
                self.image = load_image('Build_water.png')
            if self.type == 3:
                self.image = load_image('Build_earth.png')
            if self.type == 4:
                self.image = load_image('Build_wing.png')

    # Направление и движение спрайта
    def move(self):
        self.counter += 1
        x = self.x
        y = self.y
        vector_x = (1 if x > 0 else -1)
        vector_y = (1 if y > 0 else -1)
        if x != 0 and y != 0 and abs(x) > self.speed and abs(y) > self.speed:
            if max(abs(x), abs(y)) == abs(x):
                self.rect.x += self.speed * vector_x
                self.rect.y += self.speed * vector_y * (abs(y) / abs(x))
            else:
                self.rect.x += self.speed * vector_x * (abs(x) / abs(y))
                self.rect.y += self.speed * vector_y
        else:
            self.rect.x += self.speed * vector_x

    # Обновление функций снаряда
    def update(self):
        self.elemental()
        self.move()
        self.animation()
