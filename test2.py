import pygame
import random
import os

pygame.init()
folder = "."
try: # try to load images from the harddisk
    cardImage = pygame.image.load(os.path.join(folder, "UNO_cards_deck.png"))
except:
    msg = "\nCould not load image from file\n"
    raise(UserWarning, msg) # print error message and exit program 

screen=pygame.display.set_mode((800,470)) # try out larger values and see what happens !
screenrect = screen.get_rect()
cardImage = cardImage.convert()  #convert (no alpha! because no tranparent parts) for faster blitting
#background = cardImage.copy() # the actual background

#screen.blit(cardImage, (0,0))     #blit the background on screen (overwriting all)
screen.blit(cardImage, (0,0,0,0))     #blit the background on screen (overwriting all)

clock = pygame.time.Clock() 
mainloop = True
FPS = 60                           # desired max. framerate in frames per second. 
playtime = 0

while mainloop:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    playtime += seconds
    if playtime > 2:
        mainloop = False
