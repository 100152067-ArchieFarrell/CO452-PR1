# coin.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the class for coins that enemies drop. It holds information such as the value, image and drop distance of the coin.
'''

# Importing modules to be used by the rest of the program
import pygame

class Coin(pygame.sprite.Sprite):
    # Constructor for the coin
    def __init__(self, value, image_path, position):
        # Uses super to call for the 'pygame.sprite.Sprite' constructor and bases itself from this
        super().__init__()
        self.value = 1
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.dropDistance = 0
        self.maxDistance = 32

    # Updates the position of the coin
    def update(self):
      if self.dropDistance < self.maxDistance:
        self.rect.y += 2 
        self.dropDistance += 2
      else:
        # Stop dropping and keep the coin at the current position
        self.rect.y = self.rect.y
      
    # Renders the coin onto the screen
    def render(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
