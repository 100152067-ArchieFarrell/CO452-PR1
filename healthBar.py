# healthBar.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the health bar used by both the player and boss. This didn't require a class as it was quite simple to set up and wouldn't need many customised instances
'''
# Importing modules to be used by the rest of the program
import pygame

# Health bar variables
playerHealth = 50
healthBarLength = 50
healthBarHeight = 10
healthBarOutlineColour = (0, 0, 0)

# Function to draw the health bar
def drawHealthBar(surface, x, y, health):
  # Colours to show how urgent it is that the player heals themselves
  stage1HealthBarColour = (0, 255, 0)
  stage2HealthBarColour = (255, 100, 0)
  stage3HealthBarColour = (255, 0, 0)
  healthBarColour = stage1HealthBarColour
  if health < 0:
    health = 0
  if health >= 30:
    healthBarColour = stage1HealthBarColour
  elif health >= 10:
    healthBarColour = stage2HealthBarColour
  else:
    healthBarColour = stage3HealthBarColour
  # Draws the healthbar and outline to the screen
  pygame.draw.rect(surface, healthBarColour,
                   (x, y, health, healthBarHeight))
  pygame.draw.rect(surface, healthBarOutlineColour,
                   (x, y, healthBarLength, healthBarHeight), 2)
