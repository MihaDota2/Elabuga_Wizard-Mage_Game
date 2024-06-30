import pygame

# Создание групп спрайтов
UpgradeWheel_sprites = pygame.sprite.Group()
upgrade_sprites = pygame.sprite.Group()
upgrade_mode_sprites = pygame.sprite.Group()


# Класс меню прокачки
class UpgradeWheel(pygame.sprite.Sprite):
    def __init__(self, image, coords):
        super().__init__(UpgradeWheel_sprites)
        self.sprite = image
        # self.image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]


# Класс прокачек
class Upgrade(pygame.sprite.Sprite):
    def __init__(self, image, coords):
        super().__init__(upgrade_sprites)
        self.sprite = image
        # self.image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
