import pygame
import sys
import os


# Инициализация Pygame
pygame.init()

# Установка размеров окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Меню")

background_image = pygame.image.load('magicfon.jpg')
background_rect = background_image.get_rect()

with open('chet.txt', 'r') as file:
    kill_count = int(file.read())

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)

# Шрифты
font = pygame.font.Font(None, 36)
pygame.mixer.music.load('gari.mp3')
pygame.mixer.music.play(-1)


# Функция для отображения текста на кнопке
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

with open('record.txt', 'r') as file:
    max_kill_count = int(file.read())


# Основной цикл меню
running = True
while running:
    screen.blit(background_image, background_rect)

    # Рисуем кнопки
    play_button = pygame.Rect(300, 260, 200, 50)
    exit_button = pygame.Rect(300, 320, 200, 50)
    draw_text('Вы проиграли!', font, black, screen, 300, 100)
    draw_text('Ваш счёт: ' + str(kill_count), font, black, screen, 300, 150)
    draw_text('Максимально убийств: ' + str(max_kill_count), font, black, screen, 250, 200)
    draw_text('Играть', font, black, screen, 325, 270)
    draw_text('Выйти', font, black, screen, 325, 330)
    pygame.draw.rect(screen, black, play_button, 2)
    pygame.draw.rect(screen, black, exit_button, 2)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if play_button.collidepoint(mouse_pos):
                pygame.quit()
                os.system('python Game.py')
            if exit_button.collidepoint(mouse_pos):
                running = False
                pygame.quit()
                sys.exit()

    pygame.display.update()
