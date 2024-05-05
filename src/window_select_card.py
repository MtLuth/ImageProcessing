import pygame
from src.card import CardParking
from src.db_app import DBManager

class Window_Select_Card():

    def __init__(self, app, status):
        pygame.init()
        self.app = app
        self.width = 700
        self.height = 600
        self.screen = pygame.Surface((self.width, self.height))
        self.is_run = True
        self.all_tickets = pygame.sprite.Group()
        self.status = status

        self.rect = self.screen.get_rect()

        self.db_manager = DBManager()
    
        self.init_card()

        self.ticket_choosed = None

        pygame.display.set_caption("Choose Ticket Card")

    def init_card(self):
        self.cards = self.db_manager.get_card_by_status(self.status)
        for ind in range(len(self.cards)):
            series, status = self.cards[ind]
            card = CardParking(self, series, status)
            self.card_width = card.rect.width*0.5
            self.card_height = card.rect.height*0.5
            self.margin_x = (self.width - self.card_width*3)/4
            self.margin_y = (self.height - self.card_height*2)/3
            card.surface = pygame.transform.scale(card.surface, (self.card_width, self.card_height))
            card.rect = card.surface.get_rect()

            row = ind // 3
            col = ind % 3

            x = self.margin_x+self.margin_x*col+self.card_width*col
            y = self.margin_y+self.margin_y*row+self.card_height*row
            card.rect.x = x
            card.rect.y = y

            self.all_tickets.add(card)

    def update_screen(self, status):
        self.screen.fill((255,255,255))
        if status == False:
            for card in self.all_tickets:
                if card.status == False:
                    card.blitme()
        else:
            for card in self.all_tickets:
                if card.status == True:
                    card.blitme()

    def check_click(self, pos_x, pos_y):
        for item in self.all_tickets:
            if (item.click(pos_x, pos_y)):
                self.is_run = False
                self.ticket_choosed = item.series_number
                
    def blitme(self):
        self.update_screen(self.status)
        self.rect.center = self.app.screen.get_rect().center
        self.app.screen.blit(self.screen, self.rect)

    def click_outside(self, x, y):
        top = self.rect.top
        bottom = self.rect.bottom
        left = self.rect.left
        right = self.rect.right
        if ((left<=x<=right and top<=y<=bottom) == False):

            self.is_run = False
    
    def update_card_status(self, series, status):
        self.db_manager.update_card_status(series, status)
