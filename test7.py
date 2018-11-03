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
cardScale = 0.4
cardWidthScaled = math.floor(cardScale * cardWidth)
cardHeightScaled = math.floor(cardScale * cardHeight)

# Rank
# 0-9: normal card
# 10: skip
# 11: reverse
# 12: draw 2
# 13: wild
# 14: wild draw 4

class Card:
    def __init__(self, rank, color):
        self.rank = rank
        self.color = color

    def __str__(self):
        return "<Card rank={0}, color={1}>".format(self.rank, self.color)

    def clickEvent(self):
        print("Card clicked: {0}".format(self))

    def getCoords(self):
        if self.rank == 14:
            # special case for wild draw 4
            x = 13
            y = 5
        else:
            x = self.rank
            y = self.color
        # x_offset, y_offset, width, height
        return pygame.Rect(cardWidth*x, cardHeight*y, cardWidth, cardHeight)

    def draw(self, x, y):
        #surfaceSelected = 0

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+cardWidthScaled > mouse[0] > x and y+cardHeightScaled > mouse[1] > y:
            surfaceSelected = cardsHighlight
            if click[0] == 1:
                self.clickEvent()
        else:
            surfaceSelected = cardsSurface

        cropped = surfaceSelected.subsurface(self.getCoords()).copy()
        cropped = pygame.transform.smoothscale(cropped, (cardWidthScaled, cardHeightScaled))
        gameDisplay.blit(cropped, (x,y))


cardR3 = Card(14,0)
        



def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 

def button(msg,x,y,w,h,color_inactive,color_active,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, color_active,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, color_inactive,(x,y,w,h))

    #smallText = pygame.font.SysFont("comicsansms",20)
    smallText = pygame.font.Font('freesansbold.ttf',20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        #largeText = pygame.font.SysFont("comicsansms",115)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        
        TextSurf, TextRect = text_objects("some text", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)


        cardR3.draw(50,50)

        button("GO!",150,450,100,50,green,bright_green,pygame.quit)
        button("Quit",550,450,100,50,red,bright_red,pygame.quit)

        pygame.display.update()
        clock.tick(15)


game_intro()
#game_loop()
pygame.quit()
quit()
