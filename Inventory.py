# inventory.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the inventory class and is an array made up of the slots from inventorySlot.py, uses an image as a background.
'''
# Importing modules to be used by the rest of the program
import pygame
from inventorySlot import InventorySlot

class Inventory:
    # Constructor for the inventory
    def __init__(self):
        self.slots = []

        self.image = pygame.image.load("Images/Inventory.png")
        self.image = pygame.transform.scale(self.image, (360,432))
        self.rect = self.image.get_rect()
        self.rect.topleft = (220, 104)

        self.slots.append(InventorySlot("Health Potion", "Images/Items/HealthPotion.png",(291, 176)))
        self.slots.append(InventorySlot("Strength Potion", "Images/Items/StrengthPotion.png", (354, 176)))

    # Renders the inventory along with its slots
    def render(self, screen, mouse_pos):
        screen.blit(self.image, self.rect) 
        for slot in self.slots:
            slot.render(screen, mouse_pos)