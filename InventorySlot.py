import pygame
#pygame.mixer.init()

# Inventory Sounds
#itemHover = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/001_Hover_01.wav")

class InventorySlot:
    def __init__(self, name, image_path, pos):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count = 0
        self.item = self

        self.font = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 20)

    def render(self, screen, mouse_pos):
        text = self.font.render(str(self.count), True, (255, 255, 255))
        screen.blit(self.image, self.rect)

        # Change the appearance when the mouse hovers over the slot
        if self.rect.collidepoint(mouse_pos):
            #itemHover.play()
            pygame.draw.rect(screen, (250, 250, 250), self.rect, 2)

        screen.blit(text, self.rect.midright)