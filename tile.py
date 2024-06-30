import pygame

# Создание группы спрайтов тайликов
tile_sprites = pygame.sprite.Group()
collision_tile_sprites = pygame.sprite.Group()


# Класс тайлов
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(tile_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Класс тайлов с коллизией
class CollisionTile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(collision_tile_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
