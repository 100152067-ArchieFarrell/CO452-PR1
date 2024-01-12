# spritesheet.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the way spritesheets are processed. They are transformed and colourkeyed so they can be used for displaying animations consistently and without background.
'''

# Importing modules to be used by the rest of the program
import pygame

class SpriteSheet():
  # Constructor for the spritesheet
  def __init__(self,image):
    self.sheet = image

  # Retrieves the given image and processes it
  def retrieveImage(self, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image