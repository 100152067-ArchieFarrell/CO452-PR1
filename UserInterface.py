# userInterface.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the user interface which will be displayed to the user. Encompasses the inventory, coin counter and score counter.
'''

# Importing modules to be used by the rest of the program
import pygame
from inventory import Inventory

class UserInterface:
    # Constructor for the UI
    def __init__(self, player):
        self.player = player
        self.colourRed = (255, 0, 0)
        self.colourGreen = (0, 255, 0)
        self.colourBlue = (0, 0, 255)
        self.colourBlack = (0, 0, 0)
        self.colourWhite = (255, 255, 255)

        self.smallFont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 12)
        self.regularFont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 19)
        self.largeFont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 40)

        self.inventory = Inventory()
        self.inventoryRender = False
        
        self.text = self.regularFont.render("0", True, self.colourBlack)

    # FPS counter for the game. Goes undisplayed to the player
    def update(self, fps):
        self.text = self.regularFont.render(str(fps), True, self.colourBlack)

    # Renders the userinterface (inventory, coin counter, score counter)
    def render(self, screen, mouse_pos):
      self.displayCoins(screen)
      self.displayScore(screen)

      if self.inventoryRender == True:
          self.inventory.render(screen, mouse_pos)

    # Function to toggle the inventory based upon a boolean, this will be used to show and hide the inventory
    def toggleInventory(self):
        if self.inventoryRender == True:
            self.inventoryRender = False
        elif self.inventoryRender == False:
            self.inventoryRender = True

    # Text that shows the amount of coins that the player currently has
    def displayCoins(self, surface):
      if hasattr(self.player, 'coins'):
          coinCounter = f'Coins: {self.player.coins}'
          shadowSurface = self.regularFont.render(coinCounter, True, self.colourBlack)
          surface.blit(shadowSurface, (645, 12))

          coinCounterSurface = self.regularFont.render(coinCounter, True, self.colourWhite)
          surface.blit(coinCounterSurface, (643, 10))

    # Text that shows the amount of score that the player currently has
    def displayScore(self, surface):
      if hasattr(self.player, 'coins'):
          scoreCounter = f'Score: {self.player.score}'
          shadowSurface = self.regularFont.render(scoreCounter, True, self.colourBlack)
          surface.blit(shadowSurface, (645, 32))

          scoreCounterSurface = self.regularFont.render(scoreCounter, True, self.colourWhite)
          surface.blit(scoreCounterSurface, (643, 30))
              