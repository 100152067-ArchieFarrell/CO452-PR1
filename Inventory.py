import pygame
from InventorySlot import InventorySlot

class Inventory:
    def __init__(self):
        self.slots = []

        self.image = pygame.image.load("Images/Inventory.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        self.slots.append(InventorySlot("player_image.png", (0, 0)))
        self.slots.append(InventorySlot("player_image.png", (0, 0)))


    def render(self, screen):
        screen.blit(self.image, self.rect) 
        for slot in self.slots:
            slot.render(screen)