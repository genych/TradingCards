""" Simple GUI app with Trading Cards"""

import os
import pygame as pg
import TradingCards as tc
import hashlib
from urllib.request import urlretrieve

pg.init()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60
FONT_SIZE = 16
FONT = pg.font.Font(None, FONT_SIZE)
IMAGES_PATH = './images'

class Deck(pg.sprite.Sprite):
    """ Graphical representation of the pack """
    def __init__(self, packname='Beginner Booster'):
        super().__init__()
        self.pack = tc.packs[packname]
        self.cards = list(self.pack.openPack())
        self.image = pg.Surface((100, 100))
        self.rect = self.image.get_rect()
        self.color = pg.Color('blue')
        self.update()

    def deal(self):
        """ Have a card """
        if self.cards:
            return Card(self.cards.pop())

    def update(self):
        """ How deck looks """
        if not self.cards:
            self.color = pg.Color('black')
        self.image.fill(self.color)
        name = FONT.render(self.pack.packName, 1, pg.Color('white'))
        amount = FONT.render('%s cards left' % len(self.cards), 1, pg.Color('white'))
        self.image.blit(name, (0, 0))
        self.image.blit(amount, (0, FONT_SIZE))
        

class Card(pg.sprite.Sprite):
    """ Wrapper around Trading Card. Sprite with two sides """
    def __init__(self, trading_card):
        super().__init__()
        self.card = trading_card
        self.closed = False
        self.back = self._make_back()
        self.face = pg.image.load(get_image(self.card.cardName)).convert()
        self.image = self.face
        self.rect = self.image.get_rect()

    def flip(self):
        self.closed = not self.closed
        self.image = self.back if self.closed else self.face

    def _make_back(self):
        """ Some information about a card """
        back = pg.Surface((100, 100))
        try:
            color = pg.Color(self.card.cardTier)        # Some tiers are colors
        except ValueError:                              # Some are not
            color = pg.Color('red')
        back.fill(color)
        name = FONT.render(self.card.cardName, 1, pg.Color('white'))
        tier = FONT.render('tier %s' % self.card.cardTier, 1, pg.Color('white'))
        back.blit(name, (0, 0))
        back.blit(tier, (0, FONT_SIZE))
        return back


class Game(object):
    """ Not really a game. Just table with clickable deck and cards """ 
    def __init__(self):
        self.screen = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.deck = self.load_deck()
        self.sprites = pg.sprite.Group(self.deck)
        self.hand = []

    def load_deck(self):
        """ Create deck and place it on the screen (midtop) """
        deck = Deck()
        deck.rect.midtop = self.rect.midtop
        return deck

    def update_cards(self):
        """ Place cards in grid """
        x = 0
        y = WINDOWHEIGHT // 5
        gap = 5
        for card in self.hand:
            if x >= WINDOWWIDTH - card.rect.width + gap:
                y += card.rect.height + gap
                x = 0
            card.rect.topleft = (x, y)
            x += card.rect.width + gap

    def manage_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:                   # Close window
                pg.display.quit()
            if event.type == pg.MOUSEBUTTONDOWN:        # Mouse click
                self.click(pg.mouse.get_pos())

    def click(self, position):
        """ Apply rules to clicked cards """
        if self.deck.rect.collidepoint(position):       # Deck deals card
            new_card = self.deck.deal()
            if new_card is not None:
                self.hand.append(new_card)
        for card in self.hand:
            if card.rect.collidepoint(position):        # Cards are clickable
                card.flip()

    def mainloop(self):
        """ Refresh screen, update state """
        while True:
            self.clock.tick(FPS)
            self.screen.fill(pg.Color('black'))
            self.manage_events()
            self.update_cards()
            self.sprites.add(*self.hand)
            self.sprites.update()
            self.sprites.draw(self.screen)
            pg.display.flip()


def get_image(cardname):
    """ Return path to cached image associated with card. Download image if it isn't cached yet """
    hash_ = hashlib.md5(cardname.encode()).hexdigest()
    path = os.path.join(IMAGES_PATH, hash_ + '.png')
    if not os.path.exists(path):
        get_gravatar(hash_, path)
    return path

def get_gravatar(hash_, path):
    """ Request image from gravatar.com and save it to path """
    url = 'http://www.gravatar.com/avatar/{hash}?d=monsterid&f=y&s=100'
    urlretrieve(url.format(hash=hash_), path)


if __name__ == '__main__':
    os.makedirs(IMAGES_PATH, exist_ok=True)
    Game().mainloop()
