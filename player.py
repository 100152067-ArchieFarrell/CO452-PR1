# player.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the player class and stores all of the information needed for it. This includes the coordinates, size, strength, coins and score of the player and has functions to render the player's animations.
'''
# Importing modules to be used by the rest of the program
import pygame
import sys
import math

class Player:
  # Constructor for the player
  def __init__(self, x, y, width, height, strength, coins, score):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.strength = strength
      self.coins = coins
      self.score = score

  # Renders the player on the screen
  def render(self, screen):
      pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

  # Renders the player's animations on the screen
  def render_animation_position(self, screen, animation_x, animation_y):
    pygame.draw.rect(screen, (255, 0, 0), (animation_x, animation_y, self.width, self.height))
