import pygame
import sys
import math

class Player:
  def __init__(self, x, y, width, height, strength, coins, score):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.strength = strength
      self.coins = coins
      self.score = score

  def render(self, screen):
      pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

  def render_animation_position(self, screen, animation_x, animation_y):
    pygame.draw.rect(screen, (255, 0, 0), (animation_x, animation_y, self.width, self.height))
