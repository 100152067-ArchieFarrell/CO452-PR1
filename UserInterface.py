import pygame
from Inventory import Inventory

class UserInterface:
    def __init__(self, player):
        self.player = player
        self.color_red = (255, 0, 0)
        self.color_green = (0, 255, 0)
        self.color_blue = (0, 0, 255)
        self.color_black = (0, 0, 0)
        self.color_white = (255, 255, 255)

        self.smallfont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 12)
        self.regularfont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 20)
        self.largefont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 40)

        self.inventory = Inventory()
        self.inventoryRender = False
        
        self.text = self.regularfont.render("0", True, self.color_black)

    def update(self, fps):
        self.text = self.regularfont.render(str(fps), True, self.color_black)

    def render(self, screen, mouse_pos):
      self.displayCoins(screen)
      self.displayScore(screen)

      if self.inventoryRender == True:
          self.inventory.render(screen, mouse_pos)

    def toggleInventory(self):
        if self.inventoryRender == True:
            self.inventoryRender = False
        elif self.inventoryRender == False:
            self.inventoryRender = True

    def displayCoins(self, surface):
      if hasattr(self.player, 'coins'):
          coinCounter = f'Coins: {self.player.coins}'
          shadowSurface = self.regularfont.render(coinCounter, True, self.color_black)
          surface.blit(shadowSurface, (652, 12))

          coinCounterSurface = self.regularfont.render(coinCounter, True, self.color_white)
          surface.blit(coinCounterSurface, (650, 10))

    def displayScore(self, surface):
      if hasattr(self.player, 'coins'):
          scoreCounter = f'Score: {self.player.score}'
          shadowSurface = self.regularfont.render(scoreCounter, True, self.color_black)
          surface.blit(shadowSurface, (652, 32))

          scoreCounterSurface = self.regularfont.render(scoreCounter, True, self.color_white)
          surface.blit(scoreCounterSurface, (650, 30))