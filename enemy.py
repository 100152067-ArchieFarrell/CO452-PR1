# enemy.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the enemy class and stores all of the information needed for it. This includes the coordinates, size, speed, and health of the enemy and has functions to render their animations. Used for both level 1 and 2 (boss) enemies.
'''
# Importing modules to be used by the rest of the program
import pygame
import spritesheet
import random

# Loading the spritesheet for level 1 enemy animations
enemySpriteSheetImage = pygame.image.load('Images/zombie spritesheet.png').convert_alpha()
enemySpriteSheet = spritesheet.SpriteSheet(enemySpriteSheetImage)

# List of animations and variables which will be used for updating the enemy's animation
animationList = []
animationSteps = [10, 10, 10, 10, 8, 8, 8, 8, 7, 7, 7, 7]
action = 0 
animationCooldown = 500
stepCounter = 0

# Adding the enemy animations to the previously created array so the animations can be accessed in groups
for animation in animationSteps:
  tempImgList = []
  for _ in range(animation):
    tempImgList.append(enemySpriteSheet.retrieveImage(stepCounter, 32, 32, 2, (24, 0, 20)))
    stepCounter += 1
  animationList.append(tempImgList)

# Loading the spritesheet for boss enemy animations
bossSpriteSheetImage = pygame.image.load('Images/boss spritesheet.png').convert_alpha()
bossSpriteSheet = spritesheet.SpriteSheet(bossSpriteSheetImage)

# List of animations and variables which will be used for updating the boss' animation
bossAnimationList = []
bossAnimationSteps = [4, 4, 4, 4, 4, 4, 4, 4, 1]
action = 0
animationCooldown = 500
stepCounter = 0

# Adding the enemy animations to the previously created array so the animations can be accessed in groups
for animation in bossAnimationSteps:
  bossTempImgList = []
  for _ in range(animation):
    bossTempImgList.append(bossSpriteSheet.retrieveImage(stepCounter, 52, 52, 3, (17, 55, 4)))
    stepCounter += 1
  bossAnimationList.append(bossTempImgList)
  
class Enemy:
    # Constructor for the enemy
    def __init__(self, x, y, size, speed, health, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.map_x = x  # Store the initial x position relative to the map
        self.map_y = y  # Store the initial y position relative to the map
        self.size = size
        self.speed = speed
        self.health = health

        self.enemyFrame = 0
        self.enemyLastUpdate = 0
        self.directionToGo = "right"  # Initialize the direction as "right"
        self.distance = 0  # Initialize the distance from the player
        self.enemyLastAction = 0
    
    # Function to calculate the enemy movements towards the player and what direction they should be facing
    def moveTowardsPlayer(self, player, camera_x, camera_y, level):
        randomNumber = random.randint(1,50)
        if level == 1:
          directionVector = pygame.Vector2((player.x - self.map_x - randomNumber), (player.y - self.map_y - randomNumber))
        if level == 2:
          directionVector = pygame.Vector2((player.x - self.map_x - randomNumber) - 20, (player.y - self.map_y - randomNumber) - 20)
        self.distance = directionVector.length()
        if self.distance > 0:  # Check if the distance is non-zero
            direction = directionVector.normalize()
            self.map_x += direction.x * self.speed
            self.map_y += direction.y * self.speed

            # Determine the direction based on the angle of the vector
            angle = direction.angle_to(pygame.Vector2(1, 0))
            if 45 < angle <= 135:
                self.directionToGo = "Up"
            elif -45 >= angle > -135:
                self.directionToGo = "Down"
            elif angle > 135 or angle <= -135:
                self.directionToGo = "Left"
            else:
                self.directionToGo = "Right"
            # Return the direction
            return self.directionToGo

    # Renders the enemy to the screen (covers both the regular enemies and the boss)
    def render(self, screen, camera_x, camera_y, action, level):
        # Level 1 enemy animations
        if level == 1:
          self.enemyCurrentTime = pygame.time.get_ticks()
          # Plays enemy animations depending upon the direction they are facing and other factors such as if they are in range to "attack" the player
          if self.directionToGo == "Up":
            if self.health <= 0:
              action = 9
            elif self.distance < 30:
              action = 5
            else:
              action = 1
          elif self.directionToGo == "Down":
            if self.health <= 0:
              action = 8
            elif self.distance < 30:
              action = 4
            else:
              action = 0
          elif self.directionToGo == "Left":
            if self.health <= 0:
              action = 11
            elif self.distance < 30:
              action = 6
            else:
              action = 3
          elif self.directionToGo == "Right":
            if self.health <= 0:
              action = 10
            elif self.distance < 30:
              action = 7
            else:
              action = 2
          else:
            action = 0

          if self.enemyCurrentTime - self.enemyLastUpdate >= animationCooldown:
              self.enemyFrame += 1
              self.enemyLastUpdate = self.enemyCurrentTime

              # Reset frame to 0 when it reaches the end of the animation
              if self.enemyFrame >= len(animationList[action]):
                  self.enemyFrame = 0

          # Reset frame to 0 when action changes
          if action != self.enemyLastAction:
              self.enemyFrame = 0
              self.enemyLastAction = action

          # Reset frame to 0 when it's out of range
          if self.enemyFrame < 0 or self.enemyFrame >= len(animationList[action]):
              self.enemyFrame = 0  # Set the default frame if it's out of range

          screen.blit(animationList[action][self.enemyFrame],(self.map_x - camera_x, self.map_y - camera_y))

        # Level 2 boss animations
        if level == 2:
          self.enemyCurrentTime = pygame.time.get_ticks()
          # Plays enemy animations depending upon the direction they are facing and other factors such as if they are in range to "attack" the player
          if self.directionToGo == "Up":
            if self.distance < 30:
              action = 6
            else:
              action = 2
          elif self.directionToGo == "Down":
            if self.distance < 30:
              action = 4
            else:
              action = 0
          elif self.directionToGo == "Left":
            if self.distance < 30:
              action = 7
            else:
              action = 3
          elif self.directionToGo == "Right":
            if self.distance < 30:
              action = 5
            else:
              action = 1
          elif self.health <= 0:
              action = 8
          else:
            action = 0
          
          if self.enemyCurrentTime - self.enemyLastUpdate >= animationCooldown:
              self.enemyFrame += 1
              self.enemyLastUpdate = self.enemyCurrentTime

              # Reset frame to 0 when it reaches the end of the animation
              if self.enemyFrame >= len(bossAnimationList[action]):
                  self.enemyFrame = 0

          # Reset frame to 0 when action changes
          if action != self.enemyLastAction:
              self.enemyFrame = 0
              self.enemyLastAction = action

          # Reset frame to 0 when it's out of range
          if self.enemyFrame < 0 or self.enemyFrame >= len(bossAnimationList[action]):
              self.enemyFrame = 0  # Set the default frame if it's out of range

          screen.blit(bossAnimationList[action][self.enemyFrame],(self.map_x - camera_x, self.map_y - camera_y))
          