# enemy.py
import pygame

class Enemy:
    def __init__(self, x, y, size, speed, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.map_x = x  # Store the initial x position relative to the map
        self.map_y = y  # Store the initial y position relative to the map
        self.size = size
        self.speed = speed

    def move_towards_player(self, player, camera_x, camera_y):
        direction_vector = pygame.Vector2(player.x - self.map_x, player.y - self.map_y)
        distance = direction_vector.length()
        if distance > 0:  # Check if the distance is non-zero
            direction = direction_vector.normalize()
            self.map_x += direction.x * self.speed
            self.map_y += direction.y * self.speed

    def render(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.map_x - camera_x, self.map_y - camera_y))
