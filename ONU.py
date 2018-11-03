import pygame
import time
import random
import math
from enum import Enum

 
pygame.init()
pygame.font.init()
 
display_width = 800
display_height = 600
 
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('ONU')
clock = pygame.time.Clock()
 

cardsSurface = pygame.image.load('UNO_cards_deck.png')
cardsHighlight = pygame.image.load('UNO_cards_deck_brighter2.png')
cardWidth = 240
cardHeight = 360
cardScale = 0.3
cardWidthScaled = math.floor(cardScale * cardWidth)
cardHeightScaled = math.floor(cardScale * cardHeight)
maxRank = 14
maxColor = 3


class ClickableObj:
    def __init__(self, rect):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    # returns True if the mouse is hovering over this button
    def hover(self):
        mouse = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse)

    # override this function in the subclasses
    def action(self):
        pass

# Color is in range [0-3]
# Rank is in range [0-14]
# 0-9: normal card
# 10: skip
# 11: reverse
# 12: draw 2
# 13: wild
# 14: wild draw 4
class Card(ClickableObj):
    curID = 0
        
    def __init__(self, rank, color):
        self.id = Card.curID # unique identifier
        Card.curID += 1
        self.rank = rank
        self.color = color
        self.hand = None # reference to the hand this card belongs to
        self.rect = pygame.Rect(0, 0, cardWidthScaled, cardHeightScaled)

    def __str__(self):
        return "<Card rank={0}, color={1}>".format(self.rank, self.color)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    def action(self):
        print("Card clicked: {0}".format(self))
        #print(self.hand)
        self.hand.removeCard(self)

    def getCoords(self):
        if self.rank == 14:
            # special case for wild draw 4
            x = 13
            y = 5
        else:
            x = self.rank
            y = self.color
        pixelAdjust = 2 # need to add small amount to avoid cut-off edges
        # x_offset, y_offset, width, height
        return pygame.Rect(cardWidth*x, cardHeight*y, cardWidth+pixelAdjust, cardHeight+pixelAdjust)

    def render(self, x, y):
        self.rect = pygame.Rect(x, y, cardWidthScaled, cardHeightScaled)
        if self.hover():
            surfaceSelected = cardsHighlight
        else:
            surfaceSelected = cardsSurface

        cropped = surfaceSelected.subsurface(self.getCoords()).copy()
        cropped = pygame.transform.smoothscale(cropped, (cardWidthScaled, cardHeightScaled))
        gameDisplay.blit(cropped, (x,y))

    def getRandomCard():
        r = random.randint(0, maxRank)
        c = random.randint(0, maxColor)
        return Card(r,c)

class Hand:
    handSpacing = math.floor(cardWidthScaled * 0.1)

    def __init__(self):
        self.cards = []

    def __str__(self):
        ret = "<Hand "
        for c in self.cards:
            ret += c.__str__()
            ret += ", "
        ret += ">"
        return ret

    def getNumCards(self):
        return len(self.cards)

    def addCard(self,c):
        c.hand = self
        self.cards.append(c)
        #print("numCards={}".format(self.getNumCards()))

    def removeCard(self,c):
        for i in range(0,self.getNumCards()):
            curCard = self.cards[i]
            if curCard == c:
                del self.cards[i]
                break

    def render(self,x,y):
        for i in range(0,self.getNumCards()):
            offset = i * (cardWidthScaled+Hand.handSpacing)
            self.cards[i].render(x + offset, y)

    def addRandomCard(self):
        self.addCard(Card.getRandomCard())

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

class Button(ClickableObj):
    def __init__(self, rect):
        ClickableObj.__init__(self, rect)

    def render(self):
        (x,y,w,h) = self.rect
        
        if self.hover():
            color_selected = self.color_active
        else:
            color_selected = self.color_inactive
        pygame.draw.rect(gameDisplay, color_selected, self.rect)

        smallText = pygame.font.Font('freesansbold.ttf',20)
        textSurf, textRect = text_objects(self.msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        gameDisplay.blit(textSurf, textRect)


card0 = Card(14,0)
card1 = Card(0,0)
card2 = Card(4,1)
card3 = Card(12,2)

hand1 = Hand()
hand1.addCard(card0)
hand1.addCard(card1)
hand1.addCard(card2)
hand1.addCard(card3)

playerHand = hand1

buttonDraw = Button((0,350,120,50))
buttonDraw.msg = "Draw card"
buttonDraw.color_inactive = green
buttonDraw.color_active = bright_green
buttonDraw.action = hand1.addRandomCard


listButtons = []
listButtons.append(buttonDraw)
 

def mainLoop():
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                listClickableObjects = listButtons + playerHand.cards
                for x in listClickableObjects:
                    if x.hover():
                        x.action()
                        break
                
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',30)
        
        TextSurf, TextRect = text_objects("some text", largeText)
        TextRect.center = (150,50)
        gameDisplay.blit(TextSurf, TextRect)

        hand1.render(0,450)
        buttonDraw.render()

        pygame.display.update()
        clock.tick(15)


mainLoop()
pygame.quit()
quit()
