import pygame
import math

# Создание группы спрайтов волшебной палочки
stick_sprites = pygame.sprite.Group()


# Класс волшебной палочки
class Stick(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(stick_sprites)
        self.sprite = image
        self.image = image
        self.image_copy = pygame.transform.scale(image, (110, 110))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0

    # Функция поворота палочки в зависимости от положения мыши
    def rotate(self, center):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        new_image = pygame.transform.rotate(self.image_copy, angle - 45)
        self.rect = new_image.get_rect(center=center)

        self.rect.y += 24
        self.image = new_image

    # Обновление функций палочки
    def update(self, center):
        self.rotate(center)
