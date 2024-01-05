# enemy.py
import pygame
import spritesheet

# Loading the sprite sheets for animations
enemySpriteSheetImage = pygame.image.load('Images/zombie spritesheet.png').convert_alpha()
enemySpriteSheet = spritesheet.SpriteSheet(enemySpriteSheetImage)

# List of animations and variables which will be used for updating the enemy's animation
animation_list = []
animation_steps = [10, 10, 10, 10, 8, 8, 8, 8, 7, 7, 7, 7]
action = 0 
animation_cooldown = 500
step_counter = 0

for animation in animation_steps:
  temp_img_list = []
  for _ in range(animation):
    temp_img_list.append(enemySpriteSheet.get_image(step_counter, 32, 32, 2, (24, 0, 20)))
    step_counter += 1
  animation_list.append(temp_img_list)
  
class Enemy:
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
      
    def move_towards_player(self, player, camera_x, camera_y):
        direction_vector = pygame.Vector2(player.x - self.map_x, player.y - self.map_y)
        self.distance = direction_vector.length()
        if self.distance > 0:  # Check if the distance is non-zero
            direction = direction_vector.normalize()
            self.map_x += direction.x * self.speed
            self.map_y += direction.y * self.speed

            # Determine the direction based on the angle of the vector
            angle = direction.angle_to(pygame.Vector2(1, 0))  # Angle relative to the positive x-axis
            if 45 < angle <= 135:
                self.directionToGo = "Up"
            elif -45 >= angle > -135:
                self.directionToGo = "Down"
            elif angle > 135 or angle <= -135:
                self.directionToGo = "Left"
            else:
                self.directionToGo = "Right"
  
            return self.directionToGo  # Return the direction

    def render(self, screen, camera_x, camera_y, action):
        self.enemyCurrentTime = pygame.time.get_ticks()
        # Plays enemy animations depending upon the direction they are facing and other factors such as if they are in range to "attack" the player
        if self.directionToGo == "Up":
          if self.health <= 0:
            action = 9
          elif self.distance < 20:
            action = 5
          else:
            action = 1
        elif self.directionToGo == "Down":
          if self.health <= 0:
            action = 8
          elif self.distance < 20:
            action = 4
          else:
            action = 0
        elif self.directionToGo == "Left":
          if self.health <= 0:
            action = 11
          elif self.distance < 20:
            action = 6
          else:
            action = 3
        elif self.directionToGo == "Right":
          if self.health <= 0:
            action = 10
          elif self.distance < 20:
            action = 7
          else:
            action = 2
        else:
          action = 0
          
        if self.enemyCurrentTime - self.enemyLastUpdate >= animation_cooldown:
            self.enemyFrame += 1
            self.enemyLastUpdate = self.enemyCurrentTime

            # Reset frame to 0 when it reaches the end of the animation
            if self.enemyFrame >= len(animation_list[action]):
                self.enemyFrame = 0

        # Reset frame to 0 when action changes
        if action != self.enemyLastAction:
            self.enemyFrame = 0
            self.enemyLastAction = action

        # Reset frame to 0 when it's out of range
        if self.enemyFrame < 0 or self.enemyFrame >= len(animation_list[action]):
            self.enemyFrame = 0  # Set the default frame if it's out of range

        screen.blit(animation_list[action][self.enemyFrame],(self.map_x - camera_x, self.map_y - camera_y))