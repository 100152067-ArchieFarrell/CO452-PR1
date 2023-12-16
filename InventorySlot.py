import pygame

class InventorySlot:
    def __init__(self, name, pos):
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count = 0

        self.font = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 20)

    def render(self, screen, mouse_pos):
        text = self.font.render(str(self.count), True, (255, 255, 255))
        screen.blit(self.image, self.rect)

        # Change the appearance when the mouse hovers over the slot
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 255, 0), self.rect, 2)
          
        screen.blit(text, self.rect.midright)