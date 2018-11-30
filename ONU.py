import pygame
import time
import random
import math
from enum import Enum

class GameUI:
    displayWidth = 800
    displayHeight = 620
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
    backgroundColor = (15,40,15)

    pygame.display.set_caption('ONU')
    clock = pygame.time.Clock()
     
    cardsSurface = pygame.image.load('UNO_cards_deck.png')
    cardsHighlight = pygame.image.load('UNO_cards_deck_brighter2.png')
    tableSurface = pygame.image.load('poker_table.png')
    cardWidth = 240
    cardHeight = 360
    cardScale = 0.2
    cardWidthScaled = math.floor(cardScale * cardWidth)
    cardHeightScaled = math.floor(cardScale * cardHeight)


    # the amount of space between each card in the UI
    handSpacing = math.floor(cardWidthScaled * 0.1)

    # the minimum height of hand1
    handHeight = 170

    # button coordinates
    buttonDrawHeight = 50
    buttonDrawWidth = 120
    buttonDrawLeft = 0
    buttonDrawBottom = handHeight + buttonDrawHeight + 40  # include some margin

    # Number of cards in hand at the start of the game
    numCardsStart = 7

    currentHandIndex = 0
    currentHand = None

    def computeSizes():
        GameUI.gameDisplay = pygame.display.set_mode((GameUI.displayWidth, GameUI.displayHeight), pygame.RESIZABLE)

        GameUI.centerX = GameUI.displayWidth // 2
        GameUI.centerY = GameUI.displayHeight // 2

        GameUI.tableW = GameUI.tableSurface.get_width()
        GameUI.tableH = GameUI.tableSurface.get_height()
        GameUI.tableX = GameUI.centerX - GameUI.tableW // 2
        GameUI.tableY = GameUI.centerY - GameUI.tableH // 2

        GameUI.discardX = GameUI.centerX - GameUI.cardWidthScaled // 2
        GameUI.discardY = GameUI.centerY - GameUI.cardHeightScaled // 2

        GameUI.cardsPerRow = math.floor(GameUI.displayWidth / (GameUI.cardWidthScaled + GameUI.handSpacing))

        GameUI.buttonDraw.rect = pygame.Rect(GameUI.buttonDrawLeft, GameUI.displayHeight - GameUI.buttonDrawBottom, GameUI.buttonDrawWidth, GameUI.buttonDrawHeight)
        GameUI.buttonNewGame.rect = pygame.Rect(GameUI.centerX - GameUI.buttonDrawWidth // 2, GameUI.displayHeight - GameUI.buttonDrawBottom, GameUI.buttonDrawWidth, GameUI.buttonDrawHeight)

    def textObjects(text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def initHands():
        GameUI.gameWinner = None
        GameUI.errorMsg = ErrorMessage("")
        GameUI.discardPile = DiscardPile()

        GameUI.hand1 = Hand("Player")
        GameUI.hand1.dealCards()

        GameUI.hand2 = Hand("Robot")
        GameUI.hand2.dealCards()        
        
        GameUI.playerHand = GameUI.hand1
        GameUI.aiplayer = AIPlayer(GameUI.hand2)

        GameUI.handList = []
        GameUI.handList.append(GameUI.hand1)
        GameUI.handList.append(GameUI.hand2)

    def initGame():
        GameUI.initHands()
        
        GameUI.centerX = GameUI.displayWidth // 2
        GameUI.centerY = GameUI.displayHeight // 2
        
        GameUI.buttonDraw = Button((GameUI.buttonDrawLeft,350,120,50))
        GameUI.buttonDraw.msg = "Draw card"
        GameUI.buttonDraw.color_inactive = GameUI.green
        GameUI.buttonDraw.color_active = GameUI.brightGreen
        GameUI.buttonDraw.action = GameUI.hand1.addRandomCard

        GameUI.buttonNewGame = Button((GameUI.centerX-60, GameUI.centerY+29, 120, 50))
        GameUI.buttonNewGame.msg = "New game"
        GameUI.buttonNewGame.color_inactive = GameUI.red
        GameUI.buttonNewGame.color_active = GameUI.brightRed
        GameUI.buttonNewGame.action = GameUI.initGame

        GameUI.listButtons = []
        GameUI.listButtons.append(GameUI.buttonDraw)
        GameUI.listButtons.append(GameUI.buttonNewGame)

    def render():
        GameUI.gameDisplay.fill(GameUI.backgroundColor)

        GameUI.gameDisplay.blit(GameUI.tableSurface, (GameUI.tableX, GameUI.tableY))

        GameUI.hand1.render(0, GameUI.displayHeight - GameUI.handHeight)
        GameUI.hand2.render(0, 50)

        GameUI.buttonDraw.render()
        
        GameUI.discardPile.render(GameUI.discardX, GameUI.discardY)
        GameUI.errorMsg.render(GameUI.displayWidth // 2, GameUI.displayHeight // 2)

        #pygame.display.update()
        # GameUI.clock.tick(GameUI.framerate)

    def renderWinOverlay():
        GameUI.errorMsg.changeMsg(GameUI.gameWinner.name + " won the game!")
        GameUI.buttonNewGame.render()
        pygame.display.update()

    def incrementTurn():
        GameUI.currentHandIndex += 1
        GameUI.currentHandIndex %= len(GameUI.handList)
        GameUI.currentHand = GameUI.handList[GameUI.currentHandIndex]

    # return the hand of the player who is going next.
    def getNextHand():
        nextHandIndex = GameUI.currentHandIndex + 1
        nextHandIndex %= len(GameUI.handList)
        return GameUI.handList[nextHandIndex]

    def mainLoop():
        intro = True
        winOverlayDebug = True

        while intro:
            GameUI.render()
            if (GameUI.gameWinner is not None) or winOverlayDebug:
                if winOverlayDebug:
                    GameUI.gameWinner = GameUI.playerHand
                GameUI.renderWinOverlay()
            pygame.display.update()

            GameUI.currentHand = GameUI.handList[GameUI.currentHandIndex]

            if GameUI.currentHand == GameUI.playerHand:
                for event in pygame.event.get():
                    # print(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type == pygame.VIDEORESIZE:
                        # set our constants accordingly
                        GameUI.displayWidth = event.w
                        GameUI.displayHeight = event.h
                        GameUI.computeSizes()
                        # There's some code to add back window content here.
                        surface = pygame.display.set_mode((event.w, event.h),
                                                          pygame.RESIZABLE)

                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        listClickableObjects = GameUI.listButtons + GameUI.playerHand.cards
                        for x in listClickableObjects:
                            if x.hover():
                                x.action()
                                break
            elif GameUI.currentHand == GameUI.aiplayer.hand:
                GameUI.aiplayer.perform_turn()



class ErrorMessage:
    def __init__(self, msg):
        self.msg = msg

    def render(self, x, y):
        largeText = pygame.font.Font('sans.ttf', 30)
        TextSurf, TextRect = GameUI.textObjects(self.msg, largeText, GameUI.red)
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

    def getAction(self):
        if self.rank == 10:
            return "skip"
        elif self.rank == 12:
            return "draw2"
        elif self.rank == 14:
            return "draw4"
        else:
            return None

    # the action to execute when the card is clicked
    def action(self):
        #print("Card clicked: {0}".format(self))
        if GameUI.discardPile.isCardPlayable(self):
            GameUI.errorMsg.changeMsg("")

            self.hand.playCard(self)
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
        GameUI.render()
        pygame.display.update()
        
        # add a delay for good looks
        pygame.time.wait(random.randrange(500, 501))

        selectedcard = None

        # Look for a playable card in the hand
        for card in self.hand.cards:
            if GameUI.discardPile.isCardPlayable(card):
                selectedcard = card

        # Keep drawing until we've got a playable card
        while not selectedcard:
            tempcard = self.hand.addRandomCard()
            GameUI.render()
            pygame.display.update()
            pygame.time.wait(random.randrange(500, 501))
            if GameUI.discardPile.isCardPlayable(tempcard):
                selectedcard = tempcard

        self.hand.playCard(selectedcard)


class DiscardPile:
    # size of the border around the discard pile
    borderSize = math.floor(GameUI.cardWidthScaled * 0.1)

    def __init__(self):
        self.topCard = None
        self.currentColor = None

    def addCard(self, c):
        self.topCard = c
        if c.isWild():
            # self.currentColor = 0
            self.currentColor = random.randint(0, Card.maxColor)
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
    def __init__(self, name):
        self.cards = []
        self.name = name

    def __str__(self):
        ret = "<Hand "
        for c in self.cards:
            ret += c.__str__()
            ret += ", "
        ret += ">"
        return ret

    def getNumCards(self):
        return len(self.cards)

    def checkWinCon(self):
        if self.getNumCards() == 0:
            GameUI.gameWinner = self

    def playCard(self, card):
        self.removeCard(card)
        GameUI.discardPile.addCard(card)
        GameUI.getNextHand().doSpecialAction(card.getAction())
        self.checkWinCon()
        GameUI.incrementTurn()

    def doSpecialAction(self, ac):
        if ac is None:
            return
        elif ac == "draw4":
            for i in range(0,4):
                self.drawAndDelay()
        elif ac == "draw2":
            for i in range(0,2):
                self.drawAndDelay()
        elif ac == "skip":
            # do nothing
            pass
        else:
            print("Error: invalid action")
        GameUI.incrementTurn()

    def drawAndDelay(self):
        pygame.time.wait(random.randrange(500, 501))
        self.addRandomCard()
        GameUI.render()
        pygame.display.update()

    def addCard(self, c):
        c.hand = self
        self.cards.append(c)
        #print("numCards={}".format(self.getNumCards()))

    def dealCards(self):
        for i in range(0, GameUI.numCardsStart):
            self.addRandomCard()

    def removeCard(self, c):
        for i in range(0,self.getNumCards()):
            curCard = self.cards[i]
            if curCard == c:
                del self.cards[i]
                break

    def render(self, x, y):
        for i in range(0, self.getNumCards()):
            x_multiplier = GameUI.cardWidthScaled + GameUI.handSpacing
            y_multiplier = GameUI.cardHeightScaled + GameUI.handSpacing
            x_offset = i % GameUI.cardsPerRow
            y_offset = i // GameUI.cardsPerRow
            self.cards[i].render(x + x_offset*x_multiplier,
                y + y_offset*y_multiplier)

        if GameUI.currentHand == self:
            textColor = GameUI.brightRed
        else:
            textColor = GameUI.white

        # render the name
        smallText = pygame.font.Font('sans.ttf',20)
        textSurf, textRect = GameUI.textObjects(self.name, smallText, textColor)
        textRect.left = x
        textRect.bottom = y
        GameUI.gameDisplay.blit(textSurf, textRect)

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
        textSurf, textRect = GameUI.textObjects(self.msg, smallText, GameUI.black)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        GameUI.gameDisplay.blit(textSurf, textRect)

def main():
    pygame.init()
    pygame.font.init()

    GameUI.initGame()
    GameUI.computeSizes()
    GameUI.mainLoop()

    pygame.quit()

main()
