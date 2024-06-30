import pygame

# Создание групп спрайтов
magica_sprites = pygame.sprite.Group()
elemental_sprites = pygame.sprite.Group()
mode_sprites = pygame.sprite.Group()


# Класс меню выбора элементов
class ElementalWheel(pygame.sprite.Sprite):
    def __init__(self, image, coords):
        super().__init__(magica_sprites)
        self.sprite = image
        # self.image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]


# Класс элемента
class Elemental(pygame.sprite.Sprite):
    def __init__(self, image, coords):
        super().__init__(elemental_sprites)
        self.sprite = image
        # self.image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def action(self):
        pass

    def update(self):
        self.action()


# Класс оконтовки
class Mode(pygame.sprite.Sprite):
    def __init__(self, image, coords):
        super().__init__(mode_sprites)
        self.sprite = image
        # self.image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
