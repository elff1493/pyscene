import sys

import pygame as pp
from pygame.locals import *

class Block(pp.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, screen, color, width, height):
       # Call the parent class (Sprite) constructor
       pp.sprite.Sprite.__init__(self)

       # add to the screen
       self.screen = screen

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pp.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

    def draw(self):
        """put the image on the screen"""
        self.screen.blit(self.image, self.rect.topleft)


"""


pp.init()

fps = 60
fpsClock = pp.time.Clock()

width, height = 640, 480
screen = pp.display.set_mode((width, height))


b = Block(screen, (2, 4, 230), 40, 40)
# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pp.event.get():
        if event.type == QUIT:
            pp.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            b.rect.topleft = pp.mouse.get_pos()
        elif event.type == JOYBUTTONDOWN:
            print()

    # Update.

    # Draw.
    b.draw()

    # finish
    pp.display.flip()
    fpsClock.tick(fps)




"""











