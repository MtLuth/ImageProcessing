import pygame

class Frame:

    def __init__(self, width, height, color, alpha):

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.set_alpha(alpha)
        self.surface.fill(color)
        self.rect = self.surface.get_rect()

    def draw(self, surface, x, y):
        surface.blit(self.surface, (x,y))
    
    def blit(self, img, width, height):
        img = pygame.transform.scale(img, (width, height))
        img_rect = img.get_rect()
        img_rect.center = self.rect.center
        self.surface.blit(img, img_rect)