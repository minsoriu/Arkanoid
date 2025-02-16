import pygame
import sys

WIDTH = 800
HEIGHT = 525


class Screen():
    def __init__(self):
        self.but1 = pygame.Rect(330, 400, 140, 50)

    def butt(self, screen):
        image = pygame.image.load('kart.png')
        screen.blit(image, (0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render('Play', True, (0, 0, 0))

        pygame.draw.rect(screen, (255, 255, 255), self.but1)
        text_rect = text.get_rect(center=(400, 425))
        screen.blit(text, text_rect)

        font = pygame.font.Font('ofont.ru_Pixel Cyr.ttf', 70)
        text1 = font.render('Арканоид', True, (0, 0, 0))
        screen.blit(text1, (240, 20))

        image = pygame.image.load("button.png")
        new_image = pygame.transform.scale(image, (60, 60))
        self.im = new_image.get_rect(center=(750, 490))
        screen.blit(new_image, self.im)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
button = Screen()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    button.butt(screen)
    pygame.display.flip()

pygame.quit()