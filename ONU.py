import pygame
import time
import random
import math
from enum import Enum

class GameUI:
    displayWidth = 800
    displayHeight = 700
    # maximum frames per second
    framerate = 15
     
    black = (0,0,0)
    white = (255,255,255)
    red = (200,0,0)
    green = (0,200,0)
    brightRed = (255,0,0)
    brightGreen = (0,255,0)
    brightBlue = (0,0,255)
    brightYellow = (255,255,0)

    gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
    pygame.display.set_caption('ONU')
    clock = pygame.time.Clock()
     
    cardsSurface = pygame.image.load('UNO_cards_deck.png')
    cardsHighlight = pygame.image.load('UNO_cards_deck_brighter2.png')
    cardWidth = 240
    cardHeight = 360
    cardScale = 0.2
    cardWidthScaled = math.floor(cardScale * cardWidth)
    cardHeightScaled = math.floor(cardScale * cardHeight)

    # the amount of space between each card in the UI
    handSpacing = math.floor(cardWidthScaled * 0.1)

    handList = []
    currentHandIndex = 0

    def textObjects(text, font):
        textSurface = font.render(text, True, GameUI.black)
        return textSurface, textSurface.get_rect()

    def initGame():
        GameUI.errorMsg = ErrorMessage("")
        GameUI.discardPile = DiscardPile()

        GameUI.hand1 = Hand()
        GameUI.hand1.addCard(Card(14,0))
        GameUI.hand1.addCard(Card(0,0))
        GameUI.hand1.addCard(Card(4,1))
        GameUI.hand1.addCard(Card(12,2))

        GameUI.hand2 = Hand()
        GameUI.hand2.addCard(Card(14,0))
        GameUI.hand2.addCard(Card(0,0))
        GameUI.hand2.addCard(Card(4,1))
        GameUI.hand2.addCard(Card(12,2))

        GameUI.playerHand = GameUI.hand1

        GameUI.buttonDraw = Button((0,350,120,50))
        GameUI.buttonDraw.msg = "Draw card"
        GameUI.buttonDraw.color_inactive = GameUI.green
        GameUI.buttonDraw.color_active = GameUI.brightGreen
        GameUI.buttonDraw.action = GameUI.hand1.addRandomCard

        GameUI.listButtons = []
        GameUI.listButtons.append(GameUI.buttonDraw)

        GameUI.handList.append(GameUI.hand1)
        GameUI.handList.append(GameUI.hand2)

        GameUI.aiplayer = AIPlayer(GameUI.hand2)

    def render():
        GameUI.gameDisplay.fill(GameUI.white)

        GameUI.hand1.render(0, 450)
        GameUI.hand2.render(0, 50)
        GameUI.buttonDraw.render()
        GameUI.discardPile.render(300, 200)
        GameUI.errorMsg.render(300, 250)

        pygame.display.update()
        # GameUI.clock.tick(GameUI.framerate)

    def mainLoop():
        intro = True

        while intro:
            GameUI.render()

            currentHand = GameUI.handList[GameUI.currentHandIndex]

            if currentHand == GameUI.playerHand:
                for event in pygame.event.get():
                    # print(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        listClickableObjects = GameUI.listButtons + GameUI.playerHand.cards
                        for x in listClickableObjects:
                            if x.hover():
                                x.action()
                                break
            elif currentHand == GameUI.aiplayer.hand:
                GameUI.aiplayer.perform_turn()



class ErrorMessage:
    def __init__(self, msg):
        self.msg = msg

    def render(self, x, y):
        largeText = pygame.font.Font('sans.ttf', 30)
        TextSurf, TextRect = GameUI.textObjects(self.msg, largeText)
        TextRect.center = (x, y)
        GameUI.gameDisplay.blit(TextSurf, TextRect)

    def changeMsg(self, m):
        self.msg = m

class ClickableObj:
    def __init__(self, rect):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    # returns True if the mouse is hovering over this object
    def hover(self):
        mouse = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse)

    # action to perform when clicked.
    # override this function in the subclasses.
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
    # constants
    maxRank = 14
    maxColor = 3

    def __init__(self, rank, color):
        self.id = Card.curID # unique identifier
        Card.curID += 1
        self.rank = rank
        self.color = color
        self.hand = None # reference to the hand this card belongs to
        self.rect = pygame.Rect(0, 0, GameUI.cardWidthScaled, GameUI.cardHeightScaled)

    def __str__(self):
        return "<Card rank={0}, color={1}>".format(self.rank, self.color)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    def isWild(self):
        return (self.rank == 13) or (self.rank == 14)

    # the action to execute when the card is clicked
    def action(self):
        #print("Card clicked: {0}".format(self))

        if GameUI.discardPile.isCardPlayable(self):
            self.hand.removeCard(self)
            GameUI.discardPile.addCard(self)
            GameUI.errorMsg.changeMsg("")

            # Increment turn
            GameUI.currentHandIndex += 1
            GameUI.currentHandIndex %= len(GameUI.handList)
        else:
            GameUI.errorMsg.changeMsg("Error: that card is not playable!")

    # get the Coordintes of the card on the image
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
        w = GameUI.cardWidth
        h = GameUI.cardHeight
        return pygame.Rect(w*x, h*y, w+pixelAdjust, h+pixelAdjust)

    def render(self, x, y):
        self.rect = pygame.Rect(x, y, GameUI.cardWidthScaled, GameUI.cardHeightScaled)
        if self.hover():
            surfaceSelected = GameUI.cardsHighlight
        else:
            surfaceSelected = GameUI.cardsSurface

        cropped = surfaceSelected.subsurface(self.getCoords()).copy()
        cropped = pygame.transform.smoothscale(cropped, (GameUI.cardWidthScaled, GameUI.cardHeightScaled))
        GameUI.gameDisplay.blit(cropped, (x,y))

    def getRandomCard():
        r = random.randint(0, Card.maxRank)
        c = random.randint(0, Card.maxColor)
        return Card(r,c)

class AIPlayer:
    def __init__(self, hand):
        self.hand = hand

    def perform_turn(self):

        # add a delay for good looks
        pygame.time.wait(random.randrange(400, 1500))

        selectedcard = None

        # Look for a playable card in the hand
        for card in self.hand.cards:
            if GameUI.discardPile.isCardPlayable(card):
                selectedcard = card

        # Keep drawing until we've got a playable card
        while not selectedcard:
            tempcard = self.hand.addRandomCard()
            GameUI.render()
            pygame.time.wait(random.randrange(400, 600))
            if GameUI.discardPile.isCardPlayable(tempcard):
                selectedcard = tempcard

        self.hand.removeCard(selectedcard)
        GameUI.discardPile.addCard(selectedcard)

        # Increment turn
        GameUI.currentHandIndex += 1
        GameUI.currentHandIndex %= len(GameUI.handList)


class DiscardPile:
    # size of the border around the discard pile
    borderSize = math.floor(GameUI.cardWidthScaled * 0.1)

    def __init__(self):
        self.topCard = None
        self.currentColor = None

    def addCard(self, c):
        self.topCard = c
        if c.isWild():
            self.currentColor = 0
        else:
            self.currentColor = c.color

    def isCardPlayable(self, c):
        if self.topCard is None:
            return True
        elif c.isWild():
            return True
        else:
            return (self.currentColor == c.color) or (self.topCard.rank == c.rank)

    def numToColor(n):
        if n == 0:
            return GameUI.brightRed
        elif n == 1:
            return GameUI.brightYellow
        elif n == 2:
            return GameUI.brightGreen
        elif n == 3:
            return GameUI.brightBlue

    def render(self, x, y):
        if self.topCard is None:
            return
        b = DiscardPile.borderSize
        w = GameUI.cardWidthScaled
        h = GameUI.cardHeightScaled
        col = DiscardPile.numToColor(self.currentColor)
        pygame.draw.rect(GameUI.gameDisplay, col, (x-b,y-b,w+2*b,h+2*b))
        self.topCard.render(x, y)

class Hand:
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

    def addCard(self, c):
        c.hand = self
        self.cards.append(c)
        #print("numCards={}".format(self.getNumCards()))

    def removeCard(self, c):
        for i in range(0,self.getNumCards()):
            curCard = self.cards[i]
            if curCard == c:
                del self.cards[i]
                break

    def render(self, x, y):
        CARDS_PER_ROW = 10
        for i in range(0, self.getNumCards()):
            x_multiplier = GameUI.cardWidthScaled + GameUI.handSpacing
            y_multiplier = GameUI.cardHeightScaled + GameUI.handSpacing
            x_offset = i % CARDS_PER_ROW
            y_offset = i // CARDS_PER_ROW
            self.cards[i].render(x + x_offset*x_multiplier,
                y + y_offset*y_multiplier)

    def addRandomCard(self):
        tempcard = Card.getRandomCard()
        self.addCard(tempcard)
        return tempcard

class Button(ClickableObj):
    def __init__(self, rect):
        ClickableObj.__init__(self, rect)

    def render(self):
        (x,y,w,h) = self.rect
        
        if self.hover():
            color_selected = self.color_active
        else:
            color_selected = self.color_inactive
        pygame.draw.rect(GameUI.gameDisplay, color_selected, self.rect)

        smallText = pygame.font.Font('sans.ttf',20)
        textSurf, textRect = GameUI.textObjects(self.msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        GameUI.gameDisplay.blit(textSurf, textRect)

def main():
    pygame.init()
    pygame.font.init()

    GameUI.initGame()
    GameUI.mainLoop()

    pygame.quit()

main()
