import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, value, image_path, position):
        super().__init__()
        self.value = 1
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.dropDistance = 0
        self.maxDistance = 32  # Adjust this value based on how far you want the coins to drop

    def update(self):
      if self.dropDistance < self.maxDistance:
        self.rect.y += 2  # Adjust the drop speed based on your preference
        self.dropDistance += 2
      else:
        # Stop dropping and keep the coin at the current position
        self.rect.y = self.rect.y
      
    def render(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
