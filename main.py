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


move_map = {pygame.K_w: (0, 1),
            pygame.K_s: (0, -1),
            pygame.K_a: (1, 0),
            pygame.K_d: (-1, 0)
            }


def animation(sprite, x0, y0, x1, y1, size):
    all_sprites = pygame.sprite.Group()
    hero = pygame.sprite.Sprite(all_sprites)
    for k in range(size):
        subsurface = sprite.subsurface((x0 + x1 * k, y0, x1, y1))
        hero.image = subsurface
        hero.rect = hero.image.get_rect()


def main():
    size = 800, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('test')

    # группа, содержащая все спрайты
    all_sprites = pygame.sprite.Group()

    # изображение должно лежать в папке data
    hero_image = load_image("AnimationListCharacter_2.png").convert_alpha()

    subsurface = hero_image.subsurface((0, 0, 96, 192))

    hero = pygame.sprite.Sprite(all_sprites)
    hero.image = subsurface
    hero.rect = hero.image.get_rect()

    # шаг перемещения
    dist = 4
    clock = pygame.time.Clock()
    counter = 0

    running = True
    while running:
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed = pygame.key.get_pressed()

        # get all directions the ship should move
        move = [move_map[key] for key in move_map if pressed[key]]

        if move:
            # animation(hero_image, 0, 0, 96, 192, 3)
            if counter > 9:
                counter = 0

            image_spriteR = [hero_image.subsurface((0, 0, 96, 192)),
                            hero_image.subsurface((96, 0, 96, 192)),
                            hero_image.subsurface((192, 0, 96, 192))]

            image_spriteL = [hero_image.subsurface((0, 192, 96, 192)),
                            hero_image.subsurface((96, 192, 96, 192)),
                            hero_image.subsurface((192, 192, 96, 192))]
            if move[0][0] == 1 or move[-1][0] == 1:
                hero.image = image_spriteL[counter // 3 - 1]
            elif move[0][0] == -1 or move[-1][0] == -1:
                hero.image = image_spriteR[counter // 3 - 1]



            # subsurface = hero_image.subsurface((192, 0, 288, 192))
            # hero.image = subsurface
            # hero.rect = hero.image.get_rect()

            move = [(move[0][0] + move[-1][0], move[0][1] + move[-1][1])]
            move_vectorL = move[0][0] * dist
            move_vectorT = move[0][1] * dist
            hero.rect.top -= move_vectorT
            hero.rect.left -= move_vectorL
        else:
            if counter > 20:
                counter = 0

            image_sprite = [hero_image.subsurface((288, 0, 96, 192)),
                            hero_image.subsurface((384, 0, 96, 192))]
            hero.image = image_sprite[counter // 10 - 1]

        clock.tick(30)
        screen.fill(pygame.Color("white"))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
