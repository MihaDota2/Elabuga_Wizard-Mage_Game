import os
import pygame
from enemy import Enemy

pygame.init()


# Отрисовка кнопки для перехода на следующую волну
def draw_wave_button(screen, font, wave_number, color):
    button_text = f"Вызвать новую волну {wave_number}"
    button_rect = pygame.Rect(screen.get_width() - 330, 10, 320, 30)
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
    text_surface = font.render(button_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
