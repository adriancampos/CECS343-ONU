
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division
import pygame
import random
import os

pygame.init()
folder = "data" # replace with "." if pictures lay in the same folder as program
try: # try to load images from the harddisk
    prettybackground = pygame.image.load(os.path.join(folder, "800px-La_naissance_de_Venus.jpg"))
    uglybackground = pygame.image.load(os.path.join(folder, "UNO_cards_deck.png"))
    snakesurface = pygame.image.load(os.path.join(folder,"snake.gif")) # with tranparent colour
except:
    msg = "\nCould not load image from file\n"
    raise(UserWarning, msg)
screen=pygame.display.set_mode((800,470)) # try out larger values and see what happens !
screenrect = screen.get_rect()
prettybackground = prettybackground.convert()  #convert (no alpha! because no tranparent parts) for faster blitting
uglybackground = uglybackground.convert() # no alpha !
background = uglybackground.copy() # the actual background
snakesurface = snakesurface.convert_alpha()
snakerect = snakesurface.get_rect()

# mypicture = pygame.image.load("picturefile.jpg") # simple method if picture in same folder
x = 1     # start position for the snake surface (topleft corner)
y = 1             
dx,dy  = 40, 85                    # speed of ball surface in pixel per second !

cardWidth = 240
cardHeight = 360

# x_offset, y_offset, width, height
def getCoords(x,y):
    return (cardWidth*x, cardHeight*y, cardWidth, cardHeight)

#blit the background on screen (overwriting all)
#screen.blit(uglybackground, (0,0))
#screen.blit(uglybackground, (0,0), (0, 0, cardWidth, cardHeight))
screen.blit(uglybackground, (0,0), getCoords(2,2))



#screen.blit(snakesurface, (x, y))  #blit the ball surface on the screen (on top of background)
clock = pygame.time.Clock()        #create pygame clock object
mainloop = True
FPS = 60                           # desired max. framerate in frames per second. 
playtime = 0
painting = False # do not overpaint the ugly background yet
dirty = False # do clear dirty part of screen

while mainloop:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    playtime += seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
                
    pygame.display.set_caption("FPS: {:.2f} dx:{} dy:{} [p]aint ({}) "
       "paint, [d]irtyrect ({}), [r]estore".format(clock.get_fps(), dx,
       dy, painting, dirty))
    #this would repaint the whole screen (secure, but slow)
    #screen.blit(background, (0,0))     #draw background on screen (overwriting all)
    #this only repaints the "dirty" part of the screen

    """
    if not dirty: # calculate dirtyrect and blit it
        dirtyrect = background.subsurface((x,y,snakerect.width, snakerect.height))
        screen.blit(dirtyrect, (x,y))"""

    pygame.display.flip()          # flip the screen 30 times a second
print("This 'game' was played for {:.2f} seconds".format(playtime))
