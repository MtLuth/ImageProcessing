import pygame
from pygame.sprite import Sprite

class CardParking(Sprite):

    def __init__(self, window, series_number, status):
        super().__init__()
        pygame.init()
        self.window = window
        self.status = status
        self.surface = pygame.image.load('./images/ticket.png')
        self.rect = self.surface.get_rect()
        self.series_number = series_number
        self.font = pygame.font.SysFont('timesnewroman', 32, bold=True)
        self.text = self.font.render(self.series_number, True, (0, 33, 94))
        self.surface.blit(self.text, (200, 125))

    def blitme(self):
        self.window.screen.blit(self.surface, self.rect)

    def click(self, x, y):
        top = self.rect.top
        bottom = self.rect.bottom
        left = self.rect.left
        right = self.rect.right
        return (left<=x<=right and top<=y<=bottom)