import pygame
class Form:

    def __init__(self):
        self.color = (71, 159, 206)
        self.lines = ['Mã thẻ: ', 'Biển số xe: ', 'Giờ vào: ', 'Giờ ra: ', 'Tổng tiền: ']
        self.n = len(self.lines)
        self.font = pygame.font.SysFont('timesnewroman', 24)
        self.font_rect = self.font.render("test", False, (255,255,255)).get_rect()
        self.font_height = self.font_rect.height
        self.space_y = 10
        self.width = 300
        self.height = self.space_y*(self.n + 1) + self.font_height*self.n
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()

    def draw_form(self):
        margin_left = 10
        for ind in range(len(self.lines)):
            font = self.font.render(self.lines[ind], False, (255,255,255))
            rect = font.get_rect()
            height = rect.height
            rect.x = margin_left
            rect.y = self.space_y+(self.space_y*ind)+height*ind
            self.surface.blit(font, rect)

    def blitme(self, surface, rect):
        self.draw_form()
        surface.blit(self.surface, rect)
