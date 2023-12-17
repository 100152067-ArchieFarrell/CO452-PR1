import pygame
from InventorySlot import InventorySlot

class Inventory:
    def __init__(self):
        self.slots = []

        self.image = pygame.image.load("Images/Inventory.png")
        self.image = pygame.transform.scale(self.image, (360,432))
        self.rect = self.image.get_rect()
        self.rect.topleft = (220, 104)

        self.slots.append(InventorySlot("Health Potion", "Images/Items/HealthPotion.png",(291, 176)))
        self.slots.append(InventorySlot("Strength Potion", "Images/Items/StrengthPotion.png", (354, 176)))

    def render(self, screen, mouse_pos):
        screen.blit(self.image, self.rect) 
        for slot in self.slots:
            slot.render(screen, mouse_pos)