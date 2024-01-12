# inventorySlot.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the class for slots within the inventory. It holds information such as the name, count and font related with the item to be displayed within the slot.
'''
# Importing modules to be used by the rest of the program
import pygame

class InventorySlot:
    # Constructor for the inventory slot
    def __init__(self, name, image_path, pos):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count = 0
        self.item = self

        self.font = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 20)

    # Renders the inventory slot within the inventory
    def render(self, screen, mouse_pos):
        text = self.font.render(str(self.count), True, (255, 255, 255))
        screen.blit(self.image, self.rect)

        # Change the appearance when the mouse hovers over the slot
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (250, 250, 250), self.rect, 2)

        screen.blit(text, self.rect.midright)