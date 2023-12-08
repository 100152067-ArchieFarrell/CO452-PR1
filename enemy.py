# enemy.py

# enemy.py
import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red color for simplicity
        self.rect = self.image.get_rect()

        # Set initial position randomly
        self.rect.x = random.randrange(500, 600)
        self.rect.y = random.randrange(500, 600)

        # Set speed
        self.speed = 8

    #def update(self, player):
        # Calculate the direction vector towards the player
        #dx = player.x - self.rect.x
        #dy = player.y - self.rect.y

        # Calculate the distance between the enemy and the player
        #distance = hypot(dx, dy)

        # Normalize the direction vector
        #if distance != 0:
            #dx /= distance
            #dy /= distance

        # Move the enemy towards the player
        #self.rect.x += dx * self.speed
        #self.rect.y += dy * self.speed

    def render(self, screen):
      screen.blit(self.image, self.rect)

        # You can add attack logic here if needed




def hypot(dx, dy):
    # Helper function to calculate the hypotenuse
    return (dx ** 2 + dy ** 2) ** 0.5
