# enemy.py
import pygame
import spritesheet
#pygame.mixer.init()

# Enemy and Boss Sounds
#enemyWalk = pygame.mixer.Sound("Sounds/Minifantasy_Dungeon_SFX/25_orc_walk_stone_2.wav")

#bossAttack = pygame.mixer.Sound("Sounds/dont_need_a_hero_sfx_and_musics/sfx_sword.mp3")
#bossWalk = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/12_Player_Movement_SFX/08_Step_rock_02.wav")

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

# Loading the sprite sheets for animations
bossSpriteSheetImage = pygame.image.load('Images/boss spritesheet.png').convert_alpha()
bossSpriteSheet = spritesheet.SpriteSheet(bossSpriteSheetImage)

# List of animations and variables which will be used for updating the enemy's animation
bossAnimationList = []
bossAnimationSteps = [4, 4, 4, 4, 4, 4, 4, 4, 1]
action = 0
animation_cooldown = 500
step_counter = 0

for animation in bossAnimationSteps:
  bossTempImgList = []
  for _ in range(animation):
    bossTempImgList.append(bossSpriteSheet.get_image(step_counter, 52, 52, 3, (17, 55, 4)))
    step_counter += 1
  bossAnimationList.append(bossTempImgList)
  
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
      
    def move_towards_player(self, player, camera_x, camera_y, level):
        if level == 1:
          direction_vector = pygame.Vector2((player.x - self.map_x), (player.y - self.map_y))
        if level == 2:
          direction_vector = pygame.Vector2((player.x - self.map_x) - 36, (player.y - self.map_y) - 36)
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

    def render(self, screen, camera_x, camera_y, action, level):
        if level == 1:
          self.enemyCurrentTime = pygame.time.get_ticks()
          # Plays enemy animations depending upon the direction they are facing and other factors such as if they are in range to "attack" the player
          if self.directionToGo == "Up":
            if self.health <= 0:
              #enemyWalk.play()
              action = 9
            elif self.distance < 30:
              action = 5
            else:
              action = 1
          elif self.directionToGo == "Down":
            if self.health <= 0:
              #enemyWalk.play()
              action = 8
            elif self.distance < 30:
              action = 4
            else:
              action = 0
          elif self.directionToGo == "Left":
            #enemyWalk.play()
            if self.health <= 0:
              action = 11
            elif self.distance < 30:
              action = 6
            else:
              action = 3
          elif self.directionToGo == "Right":
            #enemyWalk.play()
            if self.health <= 0:
              action = 10
            elif self.distance < 30:
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

        if level == 2:
          self.enemyCurrentTime = pygame.time.get_ticks()
          # Plays enemy animations depending upon the direction they are facing and other factors such as if they are in range to "attack" the player
          if self.directionToGo == "Up":
            #bossWalk.play()
            if self.distance < 30:
              #bossAttack.play()
              action = 6
            else:
              action = 2
          elif self.directionToGo == "Down":
            #bossWalk.play()
            if self.distance < 30:
              #bossAttack.play()
              action = 4
            else:
              action = 0
          elif self.directionToGo == "Left":
            #bossWalk.play()
            if self.distance < 30:
              #bossAttack.play()
              action = 7
            else:
              action = 3
          elif self.directionToGo == "Right":
            #bossWalk.play()
            if self.distance < 30:
              #bossAttack.play()
              action = 5
            else:
              action = 1
          elif self.health <= 0:
              action = 8
          else:
            action = 0

          if self.enemyCurrentTime - self.enemyLastUpdate >= animation_cooldown:
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
          