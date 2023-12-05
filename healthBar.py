import pygame

# Health bar variables
player_health = 50
health_bar_length = 50
health_bar_height = 10
health_bar_color = (0, 255, 0)
health_bar_outline_color = (0, 0, 0)

# Function to draw the health bar
def draw_health_bar(surface, x, y, health):
    if health < 0:
        health = 0
    pygame.draw.rect(surface, health_bar_color, (x, y, health, health_bar_height))
    pygame.draw.rect(surface, health_bar_outline_color, (x, y, health_bar_length, health_bar_height), 2)