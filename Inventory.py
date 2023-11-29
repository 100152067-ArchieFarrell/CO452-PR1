import pygame
from InventorySlot import InventorySlot

class Inventory:
    def __init__(self):
        self.slots = []

        self.image = pygame.image.load("Images/Inventory.png")
        self.image = pygame.transform.scale(self.image, (360,432))
        self.rect = self.image.get_rect()
        self.rect.topleft = (220, 104)

        self.slots.append(InventorySlot("Images/Items/potion_03a.png",(297, 186)))
        self.slots.append(InventorySlot("Images/Items/potion_03a.png", (361, 186)))


    def render(self, screen):
        screen.blit(self.image, self.rect) 
        for slot in self.slots:
            slot.render(screen)