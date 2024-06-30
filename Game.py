# Импорт библиотек
import os
import random
import pygame
from math import ceil

# Импорт классов и их функций
from functions import load_image
from map import Map
from tile import tile_sprites, collision_tile_sprites
from player import Player, player_sprites
from enemy import Enemy, enemy_sprites
from stick import Stick, stick_sprites
from spell import Spell, spell_sprites
from functions import function_sprites, Pause
from magica import ElementalWheel, magica_sprites, Elemental, elemental_sprites, Mode, mode_sprites
from Volna import draw_wave_button
from upgrade import UpgradeWheel, upgrade_sprites, Upgrade, UpgradeWheel_sprites

# Генерация массива карты
map_1 = [[1] * 15] * 10
# map_1 = [[1] * 2, [0] * 2] * 2

# Запись рекорда по убийствам
with open('record.txt', 'r') as file:
    max_kill_count = int(file.read())

# здоровье
pygame.font.init()  # Инициализация модуля шрифтов
font = pygame.font.Font(None, 36)  # Создание объекта шрифта

if __name__ == '__main__':
    # Инициализация звукого миксера, экрана, часов и кнопки
    pygame.init()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)
    # size = width, height = 1360, 760
    size = width, height = 1360, 760
    # window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    button_rect = pygame.Rect(screen.get_width() - 300, 10, 290, 30)

    # Создание объекта игрока, который наследует класс player
    hero = Player(load_image('AnimationListCharacter_3.png'), width // 2 - 48, height // 2 - 96)
    # Загрузка изображения полоски здоровья
    hp_bar_image = load_image('hp.png', color_key=-1)
    # Считывание клавиатуры для передвижения игрока
    move = hero.input()

    # Обьявление переменных состояния игры (запуск, пауза, меню стихий)
    running = True
    pause = False
    magica = False
    level_up = False
    counter = 0

    # Отрисовка тайлов и игрока на экране
    tile_sprites.draw(screen)
    player_sprites.draw(screen)

    # Объявление картинок для тайлов и создание тайлов карты по массиву
    Level_Map = Map(map_1, load_image('tileset_1.png'), 192, 92)
    Level_Map.generate()

    # Отрисовка тайлов карты
    tile_sprites.draw(screen)

    # Отрисовка волшебной палочки
    stick = Stick(load_image('Stick_2.png'), 500, 500)
    # Отрисовка заклинаний
    spell = Spell(load_image('Spell_1.png'), (0, 0), pygame.mouse.get_pos(), (0, 0),
                  1, 1, 1, 1, 0)
    # Отрисовка знака паузы
    pause_btn = Pause(load_image('pause_button.png'), (width // 2 - 192, height // 2 - 192))

    # Отрисовка меню выбора элементов и самих элементов
    ElementalWheel(load_image('Whill_1.png'), (width // 2 - 384, height // 2 - 384))
    fire = Elemental(load_image('Fire.png'), (width // 2 - 160, height // 2 - 290))
    water = Elemental(load_image('Water.png'), (width // 2 + 16, height // 2 - 290))
    earth = Elemental(load_image('Earth.png'), (width // 2 - 304, height // 2 - 170))
    wing = Elemental(load_image('Wing.png'), (width // 2 + 160, height // 2 - 170))

    UpgradeWheel(load_image('Whill_1.png'), (width // 2 - 384, height // 2 - 384))
    damage = Upgrade(load_image('LevelUp_damage.png'), (width // 2 - 160, height // 2 - 290))
    mana = Upgrade(load_image('LevelUp_mana.png'), (width // 2 + 16, height // 2 - 290))
    time = Upgrade(load_image('LevelUp_time.png'), (width // 2 - 304, height // 2 - 170))
    speed = Upgrade(load_image('LevelUp_speed.png'), (width // 2 + 160, height // 2 - 170))
    # Нереализованные стихии (в доработке)
    # light = Elemental(load_image('Light.png'), (width // 2 + 16, height // 2 + 146))
    # life = Elemental(load_image('Life.png'), (width // 2 - 160, height // 2 + 146))
    # death = Elemental(load_image('Death.png'), (width // 2 + 160, height // 2 + 26))
    # star = Elemental(load_image('Star.png'), (width // 2 - 304, height // 2 + 26))

    # Отображение кольца возле стихий при наведении мышки
    elem_frame = Elemental(load_image('0.png'), (0, 0))
    mode_sprite = Mode(load_image('Mode_1.png'), (width - 54, height - 54))

    # Переменные настройки волшебной палочки (тип элемента, вид элемента, кд, текущая волна)
    element_type = 1
    upgrade = 0
    element_mode = 1
    cooldown = 0
    current_wave = 1

    # Характеристика (коэффициент) снарядов игрока игрока (урон от снарядов, скорость снарядов, потребление маны, время жизни снарядов)
    hero_spell_damage = 1
    hero_spell_speed = 4
    hero_spell_mana = 10
    hero_spell_time = 2

    # Таймер действия эффекта снаряда
    slow_timer = 0

    # Цвет кнопки перехода на новую волну
    btn_color = (174, 186, 0)

    # Характеристики снарядов
    spell_types_spec = {1: ((1, 1, 1), (1, 1, 1), (1, 1, 1)),
                        2: ((1, 1, 1), (1, 1, 1), (1, 1, 1)),
                        3: ((2, 0.6, 2), (0, 0, 2), (1, 1, 1)),
                        4: ((0.5, 2.2, 0.5), (1, 1, 1), (1, 1, 1)),
                        5: ((1, 1, 1), (1, 1, 1), (1, 1, 1)),
                        6: ((1, 1, 1), (1, 1, 1), (1, 1, 1)),
                        7: ((1, 1, 1), (1, 1, 1), (1, 1, 1)),
                        8: ((1, 1, 1), (1, 1, 1), (1, 1, 1))}

    # Характеристики врагов
    enemy_sprite_image = load_image('Enemy_list.png')
    enemy_spec = {1: ([load_image('Enemy_list.png').subsurface((288, 0, 96, 96)),
                       load_image('Enemy_list.png').subsurface((384, 0, 96, 96))],
                      (96, 96), 3, 5, 3, load_image('Die_sprite.png')),
                  2: ([load_image('Enemy_list.png').subsurface((0, 0, 96, 192)),
                       load_image('Enemy_list.png').subsurface((96, 0, 96, 192)),
                       load_image('Enemy_list.png').subsurface((192, 0, 96, 192))],
                      (96, 168), 4, 6, 4, load_image('Die_sprite.png')),
                  3: ([load_image('Enemy_list.png').subsurface((0, 192, 96, 192)),
                       load_image('Enemy_list.png').subsurface((96, 192, 96, 192)),
                       load_image('Enemy_list.png').subsurface((192, 192, 96, 192))],
                      (96, 168), 3, 10, 4, load_image('Die_sprite.png')),
                  4: ([load_image('Enemy_list.png').subsurface((288, 192, 96, 96)),
                       load_image('Enemy_list.png').subsurface((384, 192, 96, 96))],
                      (96, 96), 5, 15, 5, load_image('Die_sprite.png')),
                  10: ([load_image('Enemy_list.png').subsurface((288, 0, 96, 96)),
                        load_image('Enemy_list.png').subsurface((384, 0, 96, 96))],
                       (240, 240), 3, 20, 50, load_image('Die_sprite.png')),
                  20: ([load_image('Enemy_list.png').subsurface((0, 0, 96, 192)),
                        load_image('Enemy_list.png').subsurface((96, 0, 96, 192)),
                        load_image('Enemy_list.png').subsurface((192, 0, 96, 192))],
                       (240, 480), 3, 30, 65, load_image('Die_sprite.png')),
                  30: ([load_image('Enemy_list.png').subsurface((0, 192, 96, 192)),
                        load_image('Enemy_list.png').subsurface((96, 192, 96, 192)),
                        load_image('Enemy_list.png').subsurface((192, 192, 96, 192))],
                       (240, 480), 3, 35, 70, load_image('Die_sprite.png')),
                  40: ([load_image('Enemy_list.png').subsurface((288, 192, 96, 96)),
                        load_image('Enemy_list.png').subsurface((384, 192, 96, 96))],
                       (240, 240), 3, 45, 75, load_image('Die_sprite.png'))}

    # Сложность волны для более долгой игры
    # wave_dif = {1: ((1,), 5),
    #             10: ((10,), 1),
    #             2: ((1, 2), 8),
    #             20: ((20,), 1),
    #             3: ((1, 2, 3), 14),
    #             30: ((30,), 1),
    #             4: ((1, 2, 3, 4), 16),
    #             40: ((40,), 1),
    #             5: ((1, 2, 3, 4), 20)}

    # Сложность волны для более быстрой игры
    wave_dif = {1: ((1,), 1),
                2: ((1,), 2),
                3: ((1,), 3),
                4: ((1,), 5),
                5: ((10,), 1),
                6: ((1, 2), 4),
                7: ((1, 2), 5),
                8: ((1, 2), 6),
                9: ((1, 2), 8),
                10: ((20,), 1),
                11: ((1, 2, 3), 9),
                12: ((1, 2, 3), 10),
                13: ((1, 2, 3), 12),
                14: ((1, 2, 3), 14),
                15: ((30,), 1),
                16: ((1, 2, 3, 4), 14),
                17: ((1, 2, 3, 4), 14),
                18: ((1, 2, 3, 4), 15),
                19: ((1, 2, 3, 4), 16),
                20: ((40,), 1),
                21: ((1, 2, 3, 4), 18)}


    # Функция спавна врагов
    def spawn_wave(col, en_type):
        enemies = []  # Создаем пустой список для хранения врагов
        pos = [[[0, width], [-96, 0]],
               [[0, width], [height - 96, height]],
               [[0, 96], [0, height]],
               [[width - 96, width], [0, height]]]  # Обозначаем границы их спавна (края экрана)
        # Генерация места спавна врагов
        x = random.choice(pos)[0][0], random.choice(pos)[0][1]
        y = random.choice(pos)[1][0], random.choice(pos)[1][1]
        # Генерация позиции для каждого врага
        enemy_positions = [[random.randint(min(x), max(x)), random.randint(min(y), max(y))] for _ in
                           range(col)]
        # enemy_positions = [[random.randint(pos[0][0], pos[0][1]),
        #                     random.randint(pos[1][0], pos[1][1])] for _ in
        #                    range(current_wave)]  # Позиции для каждого врага в волне
        # Создание объектов врагов
        for i in range(len(enemy_positions)):
            if i < len(enemy_positions):
                enemy_position = enemy_positions[i]
                enemy_type = enemy_spec[random.choice(en_type)]
            enemy = Enemy(enemy_type[0][0], enemy_type[0], enemy_position[0], enemy_position[1], enemy_type[1],
                          enemy_type[2], enemy_type[3], enemy_type[4], enemy_type[5])
            enemies.append(enemy)  # Добавляем врага в список
        return enemies  # Возвращаем список созданных врагов


    # Основной игровой цикл
    while running:
        # Отслеживание нажатий клавиш клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause  # Пауза на пробел
            if pygame.mouse.get_pressed()[0] and not pause and cooldown == 0:  # Выстел на левую кнопку мыши
                if element_mode == 1:
                    cooldown = 10 - ceil(hero_spell_speed - 4)  # кд выстрела
                    mana_cell = hero_spell_mana * spell_types_spec[element_type][0][2]  # Расчёт цены выстрела
                    hero_speed = hero_spell_speed * spell_types_spec[element_type][0][1]  # Расчёт скорости снаряда
                    hero_damage = hero_spell_damage * spell_types_spec[element_type][0][0]  # Расчёт урона снаряда
                    # Если игроку хватает маны чтобы использовать заклинание, то он использует его
                    if hero.mana > mana_cell:
                        spell = Spell(load_image('Spell_1.png'), stick.rect.center, pygame.mouse.get_pos(), (32, 32),
                                      element_type, element_mode, hero_speed, hero_damage, hero_spell_time)
                        hero.mana -= mana_cell
                # Второй тип снарядов, работает по аналогии с первым, но не имеет скорости и стоит на земле
                if element_mode == 2:
                    cooldown = 20 - ceil(hero_spell_speed - 4)
                    mana_cell = hero_spell_mana * spell_types_spec[element_type][1][2]
                    hero_speed = 0
                    hero_damage = hero_spell_damage * spell_types_spec[element_type][1][0]
                    if hero.mana > mana_cell:
                        spell = Spell(load_image('Spell_1.png'),
                                      (pygame.mouse.get_pos()[0] - 48, pygame.mouse.get_pos()[1] - 48),
                                      pygame.mouse.get_pos(), (32, 32),
                                      element_type, element_mode, hero_speed, hero_damage, hero_spell_time)
                        hero.mana -= mana_cell
            # Меню стихий на E
            if not level_up and not pause:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    if not pause:
                        magica = not magica
            # Вызов меню прокачки (только для демонстрации возможностей)
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            #     if not pause:
            #         level_up = not level_up
            # Esc чтобы выйти
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                hero.hp = 0

            # Смена стихии в зависимости от нажатой иконки стихии
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                element_mode = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                element_mode = 2
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            #     element_mode = 3
            # События при нажатии мышки
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проигрывание звука выстрела
                magic_sound = pygame.mixer.Sound('magic.mp3')
                magic_sound.play()
                # Если нет врагов и нажата кнопка запуска новой волны то создаётся новая волна
                if len(enemy_sprites) == 0:
                    if event.button == pygame.BUTTON_LEFT and button_rect.collidepoint(event.pos):
                        # Более долгая игра
                        # if current_wave % 10 == 0 and current_wave <= 40:
                        #     spawn_wave(wave_dif[current_wave][1], wave_dif[current_wave][0])
                        # if current_wave <= 40:
                        #     spawn_wave(wave_dif[current_wave // 9 + 1][1], wave_dif[current_wave // 9 + 1][0])
                        # elif current_wave < 45:
                        #     spawn_wave(wave_dif[current_wave // 9 + 1][1] + current_wave // 2,
                        #                wave_dif[current_wave // 9 + 1][0])
                        # else:
                        #     spawn_wave(wave_dif[5][1] + current_wave // 2,
                        #                wave_dif[5][0])

                        # Более быстрая игра
                        if current_wave <= 20:
                            spawn_wave(wave_dif[current_wave][1], wave_dif[current_wave][0])
                        else:
                            spawn_wave(wave_dif[21][1], wave_dif[21][0])

                        current_wave += 1
        # При смерти врага сохраняется рекордное колличество убийств врагов и запускается игровое меню
        if hero.hp <= 0:
            with open('chet.txt', 'w') as file:
                file.write(str(hero.kill_count))
            if hero.kill_count > max_kill_count:
                max_kill_count = hero.kill_count
                with open('record.txt', 'w') as file:
                    file.write(str(max_kill_count))
            pygame.quit()
            os.system('python menu.py')

        # Цвет кнопки в зависимости от наличия врагов
        if len(enemy_sprites) == 0:
            btn_color = (174, 186, 0)
        else:
            btn_color = (155, 155, 155)

        # Уничтожение заклинаний по истечению времени их жизни
        for spell in spell_sprites:
            if spell.rect.x > width or spell.rect.x < 0:
                spell_sprites.remove(spell)
            if spell.counter == 30 * spell.time:
                spell_sprites.remove(spell)

        # Очищение экрана перед новым кадром
        screen.fill((255, 255, 255))

        # Игровые события, которые работают когда нет паузы или одного из меню
        if not pause and not magica and not level_up:
            # Апдейты основных спрайтов
            hero.update()
            stick.update(hero.rect.center)
            enemy_sprites.update([hero.rect.x, hero.rect.y], screen)
            spell_sprites.update()
            mode_sprite.image = load_image(f'Mode_{element_mode}.png')
            # Атака врага и нанесение урона врагу, смерть врага
            for enemy in enemy_sprites.sprites():
                col_enemys = pygame.sprite.spritecollide(enemy, enemy_sprites.sprites(), False)
                if len(col_enemys) > 1:
                    for i in range(len(col_enemys) - 1):
                        if i % 2 == 0:
                            col_enemys[i].enemy_collision(col_enemys[i + 1], 0.7)
                            col_enemys[i + 1].enemy_collision(col_enemys[i], 0.7)

                enemy.attack_player(hero, pygame.time.get_ticks())
                for spell in spell_sprites.sprites():
                    if spell.rect.x > width or spell.rect.x < 0:
                        spell_sprites.remove(spell)
                    if spell.counter == 30 * spell.time:
                        spell_sprites.remove(spell)
                    if spell.mode == 1:
                        if pygame.sprite.spritecollideany(enemy, spell_sprites):
                            pygame.sprite.groupcollide(enemy_sprites, spell_sprites, False, True)
                            enemy.taking_damage(spell.damage)
                    if spell.mode == 2:
                        if pygame.sprite.spritecollideany(enemy, spell_sprites):
                            if spell.type == 1:
                                if counter % 30 == 0:
                                    enemy.taking_damage(spell.damage)
                            if spell.type == 2:
                                if not enemy.slow:
                                    enemy.slow = True
                                    slow_timer = counter
                                    enemy.speed = 0.9
                            if spell.type == 4:
                                enemy.update(spell.rect, screen)
                            if spell.type == 3:
                                enemy.collision(1)

                # Уничтожение врага, когда у него заканчивается хп
                if enemy.hp <= 0:
                    enemy.die()
                    if enemy.die_counter == 60:
                        hero.kill_count += 1
                        enemy_sprites.remove(enemy)
                        if hero.energy <= 9:
                            hero.energy += 1
        # Отрисовка спрайтов и надписей
        tile_sprites.draw(screen)
        collision_tile_sprites.draw(screen)
        player_sprites.draw(screen)
        stick_sprites.draw(screen)
        enemy_sprites.draw(screen)
        spell_sprites.draw(screen)
        hero.display_kill_count(screen, font, width, height)
        hero.max_display_kill_count(screen, font, width, height)
        hero.draw_energy(screen, hp_bar_image, font)
        hero.display_damage(screen, font, width, height, hero_spell_damage)
        hero.display_mana(screen, font, width, height, hero_spell_mana)
        hero.display_speed(screen, font, width, height, hero_spell_speed)
        hero.display_time(screen, font, width, height, hero_spell_time)
        if hero.hp > 0:
            hero.draw_hp(screen, hp_bar_image, font)  # здоровье

        # Отрисовка полоски здоровья врагов если они живы
        for enemy in enemy_sprites.sprites():
            if not enemy.die_counter:
                enemy.draw_hp(screen)

        # Кд после выстрела
        if cooldown:
            hero.draw_cd(screen, cooldown)
            cooldown -= 1

        hero.draw_mana(screen, hp_bar_image, font)
        mode_sprites.draw(screen)
        draw_wave_button(screen, font, current_wave, btn_color)

        # Отрисовка меню выбора стихий
        if magica:
            n = 0
            magica_sprites.draw(screen)
            elemental_sprites.draw(screen)
            for elem in elemental_sprites:
                n += 1
                if n == 9:
                    n = 0
                # Подсвечивание элемента при наведении мыши и выбор элемента при нажатии
                if elem.rect.collidepoint(pygame.mouse.get_pos()):
                    elem_frame.image = load_image('Frame.png')
                    elem_frame.rect = elem.rect
                    if n != 0 and pygame.mouse.get_pressed()[0]:
                        if n != 5:
                            element_type = n
                        magica = False
                else:
                    elem_frame.image = load_image('0.png')

        # Прокачка героя при достижении 10 убийств
        if hero.energy == 10:
            level_up = True
            hero.energy = 0

        # Отрисовка меню выбора прокачки
        if level_up:
            n = 0
            UpgradeWheel_sprites.draw(screen)
            upgrade_sprites.draw(screen)
            for ups in upgrade_sprites:
                n += 1
                if n == 9:
                    n = 0
                if ups.rect.collidepoint(pygame.mouse.get_pos()):
                    # Выбор прокачки при нажатии на неё
                    if n != 0 and pygame.mouse.get_pressed()[0]:
                        if n != 5:
                            if n == 1:
                                hero_spell_damage += 0.3
                            if n == 2:
                                if hero_spell_mana > 0.1:
                                    hero_spell_mana -= 0.1
                            if n == 3:
                                hero_spell_time += 0.2
                            if n == 4:
                                if hero_spell_speed < 13.8:
                                    hero_spell_speed += 0.2

                        level_up = False
                else:
                    elem_frame.image = load_image('0.png')

        # Отрисовка значка паузы на экране когда игрок поставил на паузу
        if pause:
            function_sprites.draw(screen)

        # Обновление экрана
        pygame.display.flip()

        # Частота кадров в игре
        counter += 1
        clock.tick(30)

        # Отталкивание героя от границ экрана
        if (pygame.sprite.spritecollideany(hero, collision_tile_sprites) or hero.rect.top < 0 or hero.rect.top > 792
                or hero.rect.left < 0 or hero.rect.right > 1440):
            hero.collision()

    # Обновление экрана
    pygame.display.flip()
    # Закрытие игры при закрытии окна
    while pygame.event.wait().type != pygame.QUIT:
        pygame.quit()
