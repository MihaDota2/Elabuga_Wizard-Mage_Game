import pygame
from tile import Tile
from tile import CollisionTile


# Создание карты из объектов тайлов
class Map:
    # tileset = (image, width, height)
    def __init__(self, map, image, width, height):
        self.map = map
        self.image = image
        self.width = width
        self.height = height

        self.col_tiles = {0: False, 1: True}

        self.display_surface = pygame.display.get_surface()
        # self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

    def tiles(self):
        image_tiles = []
        for y in range(0, self.height, 96):
            for x in range(0, self.width, 96):
                image_tiles.append(self.image.subsurface((x, y, 96, 96)))
        return image_tiles

    def generate(self):
        image_tiles = self.tiles()
        x, y = 0, 0
        for t_y in self.map:
            for t_x in t_y:
                if self.col_tiles[t_x]:
                    Tile(image_tiles[t_x], x, y)
                else:
                    CollisionTile(image_tiles[t_x], x, y)
                x += 96
            x = 0
            y += 96
