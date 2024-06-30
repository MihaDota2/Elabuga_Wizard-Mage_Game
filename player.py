import pygame

# Группа спрайтов (Игрок)
player_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(player_sprites)
        self.sprite = image
        self.image = pygame.transform.scale(image, (96, 168))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
        self.flag_right = True

        self.last_mana_time = pygame.time.get_ticks()
        self.mana = 100
        self.max_mana = 100

        self.speed = 5
        self.hp = 100
        self.max_hp = 100

        with open('record.txt', 'r') as file:
            self.max_kill_count = int(file.read())

        self.kill_count = 0
        self.energy = 0
        self.max_energy = 10

    # Направление движения в зависимости от нажатой кнопки на клавиатуре
    def input(self):
        move_map = {pygame.K_w: (0, 1),
                    pygame.K_s: (0, -1),
                    pygame.K_a: (1, 0),
                    pygame.K_d: (-1, 0)}

        pressed = pygame.key.get_pressed()
        move = [move_map[key] for key in move_map if pressed[key]]
        return move

    # Отрисовка колличества убийств
    def display_kill_count(self, screen, font, screen_width, screen_height):
        kill_text = font.render("Убийств: " + str(self.kill_count), True, (255, 255, 255))
        text_rect = kill_text.get_rect()
        text_rect.bottomright = (132, 200)  # Положение текста в нижнем правом углу
        screen.blit(kill_text, text_rect)

    # Отрисовка рекордного колличества убийств
    def max_display_kill_count(self, screen, font, screen_width, screen_height):
        kill_text = font.render("Максимально убийств: " + str(self.max_kill_count), True, (255, 255, 255))
        text_rect = kill_text.get_rect()
        text_rect.bottomright = (300, 250)  # Положение текста в нижнем правом углу
        screen.blit(kill_text, text_rect)

    # Надпись урона
    def display_damage(self, screen, font, screen_width, screen_height, damage):
        kill_text = font.render("Урон: " + str(round(damage, 1)), True, (255, 255, 255))
        text_rect = kill_text.get_rect()
        text_rect.bottomright = (125, screen_height - 100)  # Положение текста в нижнем правом углу
        screen.blit(kill_text, text_rect)

    # Надпись маны
    def display_mana(self, screen, font, screen_width, screen_height, mana):
        kill_text = font.render("Потребление маны: " + str(round(mana, 1)), True, (255, 255, 255))
        text_rect = kill_text.get_rect()
        text_rect.bottomright = (305, screen_height - 80)  # Положение текста в нижнем правом углу
        screen.blit(kill_text, text_rect)

    # Надпись скорости
    def display_speed(self, screen, font, screen_width, screen_height, speed):
        kill_text = font.render("Cкорость снарядов: " + str(round(speed, 1)), True, (255, 255, 255))
        text_rect = kill_text.get_rect()
        text_rect.bottomright = (300, screen_height - 60)  # Положение текста в нижнем правом углу
        screen.blit(kill_text, text_rect)

    # Надпись времени
    def display_time(self, screen, font, screen_width, screen_height, time):
        kill_text = font.render("Время жизни магии: " + str(round(time, 1)), True, (255, 255, 255))
        text_rect = kill_text.get_rect()
        text_rect.bottomright = (300, screen_height - 40)  # Положение текста в нижнем правом углу
        screen.blit(kill_text, text_rect)

    # Отрисовка плашки здоровья
    def draw_hp(self, screen, hp_bar_image, font):
        # Размеры изображения полоски здоровья
        hp_bar_rect = hp_bar_image.get_rect(topleft=(10, 10))

        # Пропорция текущего здоровья относительно максимального
        hp_ratio = self.hp / self.max_hp

        # Расчёт ширины заливаемой части полоски здоровья
        fill_width = int(hp_bar_rect.width * hp_ratio)

        # Создание нового поверхностного объекта для заливки
        fill = pygame.Surface((fill_width, hp_bar_rect.height)).convert_alpha()
        fill.fill((255, 0, 0))  # Заливка красным цветом

        # Отображение заливки на экране
        screen.blit(fill, hp_bar_rect.topleft)

        # Отображение изображения полоски здоровья поверх заливки
        screen.blit(hp_bar_image, hp_bar_rect.topleft)

        # Отрисовка текста с текущим здоровьем
        hp_text = font.render(str(self.hp), True, (255, 255, 255))
        text_rect = hp_text.get_rect(center=hp_bar_rect.center)

        screen.blit(hp_text, text_rect)

    # Отрисовка плашки маны
    def draw_mana(self, screen, mana_bar_image, font):
        # Размеры изображения полоски маны
        mana_bar_rect = mana_bar_image.get_rect(topleft=(10, 50))

        # Пропорция текущей маны относительно максимальной
        mana_ratio = self.mana / self.max_mana

        # Расчет ширины заливаемой части полоски маны
        fill_width = int(mana_bar_rect.width * mana_ratio)

        # Создание нового поверхностного объекта для заливки
        fill = pygame.Surface((fill_width, mana_bar_rect.height)).convert_alpha()
        fill.fill((0, 0, 255))  # Заливка синим цветом

        # Отображение заливки на экране
        screen.blit(fill, mana_bar_rect.topleft)

        # Отображение изображения полоски маны поверх заливки
        screen.blit(mana_bar_image, mana_bar_rect.topleft)

        # Отрисовка текста с текущей маной
        mana_text = font.render(str(round(self.mana, 2)), True, (255, 255, 255))
        text_rect = mana_text.get_rect(center=mana_bar_rect.center)

        screen.blit(mana_text, text_rect)

    # Отрисовка плашки опыта
    def draw_energy(self, screen, energy_bar_image, font):
        # Размеры изображения полоски энергии
        energy_bar_rect = energy_bar_image.get_rect(topleft=(10, 90))

        # Пропорция текущей энергии относительно максимальной
        energy_ratio = self.energy / self.max_energy

        # Расчет ширины заливаемой части полоски энергии
        fill_width = int(energy_bar_rect.width * energy_ratio)

        # Создание нового поверхностного объекта для заливки
        fill = pygame.Surface((fill_width, energy_bar_rect.height)).convert_alpha()
        fill.fill((255, 255, 0))  # Заливка желтым цветом

        # Отображение заливки на экране
        screen.blit(fill, energy_bar_rect.topleft)

        # Отображение изображения полоски энергии поверх заливки
        screen.blit(energy_bar_image, energy_bar_rect.topleft)

        # Отрисовка текста с текущей энергией
        energy_text = font.render(str(self.energy), True, (255, 255, 255))
        text_rect = energy_text.get_rect(center=energy_bar_rect.center)

        screen.blit(energy_text, text_rect)

    # Отрисовка кд
    def draw_cd(self, screen, cd):
        pygame.draw.rect(screen, (155, 155, 155), (self.rect.x + 52 - 3 * cd, self.rect.y + 170, 6 * cd, 10))

    # Анимация игрока
    def animation(self):
        move = self.input()
        self.counter += 1
        if move:
            if self.counter > 9:
                self.counter = 0
            image_spriteR = [self.sprite.subsurface((0, 0, 96, 192)),
                             self.sprite.subsurface((96, 0, 96, 192)),
                             self.sprite.subsurface((192, 0, 96, 192))]

            image_spriteL = [self.sprite.subsurface((0, 192, 96, 192)),
                             self.sprite.subsurface((96, 192, 96, 192)),
                             self.sprite.subsurface((192, 192, 96, 192))]
            if move[0][0] == 1 or move[-1][0] == 1:
                self.image = image_spriteL[self.counter // 3 - 1]
            elif move[0][0] == -1 or move[-1][0] == -1:
                self.image = image_spriteR[self.counter // 3 - 1]
            else:
                if self.flag_right:
                    self.image = image_spriteR[self.counter // 3 - 1]
                else:
                    self.image = image_spriteL[self.counter // 3 - 1]
        else:
            if self.counter > 20:
                self.counter = 0
            image_spriteR = [self.sprite.subsurface((288, 0, 96, 192)),
                             self.sprite.subsurface((384, 0, 96, 192))]
            image_spriteL = [self.sprite.subsurface((288, 192, 96, 192)),
                             self.sprite.subsurface((384, 192, 96, 192))]
            if self.flag_right:
                image_sprite = image_spriteR
            else:
                image_sprite = image_spriteL
            self.image = image_sprite[self.counter // 10 - 1]

    # Движение игрока
    def move(self):
        move = self.input()
        if move:
            if move[0] != move[-1]:
                move = [(move[0][0] + move[-1][0], move[0][1] + move[-1][1])]
            move_vectorL = move[0][0] * self.speed
            move_vectorT = move[0][1] * self.speed
            self.rect.top -= move_vectorT
            self.rect.left -= move_vectorL
            # print(self.flag_right, move)
            if move[0][0] == 1:
                self.flag_right = False
            elif move[0][0] == -1:
                self.flag_right = True

    # Коллизия игрока
    def collision(self):
        move = self.input()
        if move:
            self.rect.top += move[0][1] * self.speed
            self.rect.left += move[0][0] * self.speed
            self.rect.top += move[-1][1] * self.speed
            self.rect.left += move[-1][0] * self.speed

    # Обновление функций игрока
    def update(self):
        self.move()
        self.animation()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_mana_time >= 100:  # 3000 миллисекунд = 3 секунды
            self.mana = min(self.mana + 1, self.max_mana)
            self.last_mana_time = current_time
