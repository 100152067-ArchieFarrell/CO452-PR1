import pygame, sys
import random
from pygame.locals import *
from UserInterface import UserInterface
from InventorySlot import InventorySlot
from healthBar import *
from enemy import *
from player import *
import spritesheet

# Setting up the environment to initialize pygame
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('The Whispers')
screen = pygame.display.set_mode((800, 640),0,0)

# Setting up the font that will be used
font = pygame.font.SysFont(None, 30)

# Setting up the enemy
enemies = []

# Setting up an "enemy wave" function
def enemyWave(Enemy, player, camera_x, camera_y):
  enemies=[]
  amountInGroup = 3
  groups = 4
  for i in range(0, groups):
    for x in range(0, amountInGroup):
      groupCoords = [(random.randint(850, 900), random.randint(430, 480)),((random.randint(1700, 1750), random.randint(730, 780))),(random.randint(700, 750), random.randint(1400, 1450)),(random.randint(430, 480), random.randint(1120, 1170))]
      enemy = Enemy(groupCoords[i][0], groupCoords[i][1],50, random.randint(1, 3), 2, "Images/zombie.jpg")
      enemies.append(enemy)
  return enemies

# Loading the sprite sheets for animations
sprite_sheet_image = pygame.image.load('Images/player spritesheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# List of animations and variables which will be used for updating the player's animation
animation_list = []
animation_steps = [6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 3, 3]
action = 0 
last_update = pygame.time.get_ticks()
animation_cooldown = 500
frame = 0
step_counter = 0

for animation in animation_steps:
  temp_img_list = []
  for _ in range(animation):
    temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 64, 2, (17, 55, 4)))
    step_counter += 1
  animation_list.append(temp_img_list)

# Function to write text on the screen and buttons
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# A variable to check for the status later
click = False

# Main container function that holds the buttons and game functions
def main_menu():
    click = False
    while True:
        screen.fill((0,190,255))
        draw_text('Main Menu', font, (0,0,0), screen, 350, 250)

        mx, my = pygame.mouse.get_pos()

        # Creates the buttons on the screen
        button_1 = pygame.Rect(300, 280, 200, 50)
        button_2 = pygame.Rect(300, 340, 200, 50)
        button_3 = pygame.Rect(300, 400, 200, 50)

        # Functions that will be run when a certain button is clicked
        if button_1.collidepoint((mx, my)):
            if click:
                game(last_update, frame, action, Player, enemies)
        if button_2.collidepoint((mx, my)):
            if click:
                controls(mx,my)
        if button_3.collidepoint((mx, my)):
            if click:
                credits()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)

        # Text that will be displayed on the buttons
        draw_text('PLAY', font, (255,255,255), screen, 376, 298)
        draw_text('CONTROLS', font, (255,255,255), screen, 343, 358)
        draw_text('CREDITS', font, (255,255,255), screen, 358, 418)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def gameOver():
  click = False
  # Game over variables
  game_over_font = pygame.font.SysFont(None, 50)
  game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
  try_again_button = pygame.Rect(300, 280, 200, 50)
  main_menu_button = pygame.Rect(300, 340, 200, 50)
  quit_button = pygame.Rect(300, 400, 200, 50)
  while True:
      screen.fill((0,190,255))
      screen.blit(game_over_text, (300, 220))
      pygame.draw.rect(screen, (255, 0, 0), try_again_button)
      pygame.draw.rect(screen, (255, 0, 0), main_menu_button)
      pygame.draw.rect(screen, (255, 0, 0), quit_button)

      draw_text('Try Again', font, (255, 255, 255), screen, 345, 298)
      draw_text('Main Menu', font, (255, 255, 255), screen, 342, 358)
      draw_text('Quit', font, (255, 255, 255), screen, 370, 418)

      mx, my = pygame.mouse.get_pos()

      if try_again_button.collidepoint((mx, my)):
          if click:
              game(last_update, frame, action, Player, enemies)

      if main_menu_button.collidepoint((mx, my)):
          if click:
              # Return to the main menu
              main_menu()

      if quit_button.collidepoint((mx, my)):
          if click:
              # Quit the game
              pygame.quit()
              sys.exit()

      for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          if event.type == MOUSEBUTTONDOWN:
              if event.button == 1:
                  click = True

      pygame.display.update()
      mainClock.tick(60)

# This function is called when the "CREDITS" button is clicked.
def credits():
  running = True
  while running:
      screen.fill((0,190,255))

      draw_text('CREDITS SCREEN', font, (255, 255, 255), screen, 300, 20)
      draw_text('(ASSETS CREDITS)', font, (255, 255, 255), screen, 304, 100)
      draw_text('PRESS "ESC" TO GO BACK', font, (255, 255, 255), screen, 272, 180)

      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            running = False

      pygame.display.update()
      mainClock.tick(60)
      
# This function is called when the "PLAY" button is clicked.
def game(last_update, frame, action, Player, enemies):
    mouse_pos = (0, 0)
    # sets the running state of the game to "true"
    running = True
    # loads the default image for the game's character
    player = Player(1114, 915, 50, 50, 1, 200)
    UI = UserInterface(player)
    player_image = pygame.image.load('Images/frank.png')
    player_image = pygame.transform.scale(player_image, (26, 42))
    # enemy image
    enemy_image = pygame.image.load('Images/zombie.jpg')
    enemy_image = pygame.transform.scale(enemy_image, (45, 42))

    # map images
    ground = pygame.image.load('Images/game map (image layers)/Ground.png')
    ground = pygame.transform.scale(ground, (2400, 1920))

    dungeon = pygame.image.load('Images/game map (image layers)/Dungeon.png')
    dungeon = pygame.transform.scale(dungeon, (2400, 1920))

    bushesStumps = pygame.image.load('Images/game map (image layers)/Bushes and Stumps.png')
    bushesStumps = pygame.transform.scale(bushesStumps, (2400, 1920))

    rocksBoxes = pygame.image.load('Images/game map (image layers)/Rocks and Boxes.png')
    rocksBoxes = pygame.transform.scale(rocksBoxes, (2400, 1920))

    shop = pygame.image.load('Images/game map (image layers)/Shop.png')
    shop = pygame.transform.scale(shop, (2400, 1920))

    shopFence = pygame.image.load('Images/game map (image layers)/Shop Fence and Sign.png')
    shopFence = pygame.transform.scale(shopFence, (2400, 1920))

    trees = pygame.image.load('Images/game map (image layers)/Trees.png')
    trees = pygame.transform.scale(trees, (2400, 1920))

    spawnerWalls = pygame.image.load('Images/game map (image layers)/Spawner walls.png')
    spawnerWalls = pygame.transform.scale(spawnerWalls, (2400, 1920))
    spawnerWalls_visible = True

    # Set up boundaries
    boundary_left = 501
    boundary_right = 1770 - player.width
    boundary_top = 483
    boundary_bottom = 1445 - player.height

    camera_x, camera_y = 0, 0

    # Set up variables for combat
    player_health = 50  # Initial health of the player
    player_strength = 1 # Initial strength of the player
    enemy_attack_cooldown = 1000  # Cooldown for enemy attacks in milliseconds

    last_enemy_attack = pygame.time.get_ticks()

    shop_active = False
    while running:
        screen.fill((0, 0, 0))
        screen.blit(ground, (0 - camera_x, 0 - camera_y))
        screen.blit(dungeon, (0 - camera_x, 0 - camera_y))
        screen.blit(shop, (0 - camera_x, 0 - camera_y))

        key = pygame.key.get_pressed()

      # Save the current position for boundary checking
        player_x, player_y = player.x, player.y

      # animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
          frame += 1
          last_update = current_time
          if frame >= len(animation_list[action]):
            frame = 0

        if frame < 0 or frame >= len(animation_list[action]):
          frame = 0  # Set the default frame if it's out of range

        screen.blit(animation_list[action][frame],(362, 280))

        # enemy spawning
        if key[pygame.K_l] == True:
          enemies = enemyWave(Enemy, player, camera_x, camera_y)
          spawnerWalls_visible = False
        for enemy in enemies:
          enemy.move_towards_player(player, camera_x, camera_y)
          enemy.render(screen, camera_x, camera_y)
          # Check for player-enemy collision and update health
          if (
              player.x < enemy.map_x + enemy.size
              and player.x + player.width > enemy.map_x
              and player.y < enemy.map_y + enemy.size
              and player.y + player.height > enemy.map_y
              and action == 8  # Check if the player is attacking
          ):
              enemy.health -= player_strength  # Decrease enemy health on collision
              if enemy.health <= 0:
                  enemies.remove(enemy)  # Remove enemy instance if health reaches 0

          # Check for enemy-player collision and update health
          current_time = pygame.time.get_ticks()
          if (
              player.x < enemy.map_x + enemy.size
              and player.x + player.width > enemy.map_x
              and player.y < enemy.map_y + enemy.size
              and player.y + player.height > enemy.map_y
              and current_time - last_enemy_attack >= enemy_attack_cooldown
          ):
              player_health -= 10  # Decrease player health on collision
              last_enemy_attack = current_time

        screen.blit(bushesStumps, (0 - camera_x, 0 - camera_y))
        screen.blit(shopFence, (0 - camera_x, 0 - camera_y))
        screen.blit(trees, (0 - camera_x, 0 - camera_y))
        screen.blit(rocksBoxes, (0 - camera_x, 0 - camera_y))
        if spawnerWalls_visible:
          screen.blit(spawnerWalls, (0 - camera_x, 0 - camera_y))

        if key[pygame.K_a] == True and player.x > boundary_left:
            action = 6
            #player.x -= 8
            player.x -= 20
        elif key[pygame.K_d] == True and player.x < boundary_right:
            action = 5
            #player.x += 8
            player.x += 20
        elif key[pygame.K_w] == True and player.y > boundary_top:
            action = 7
            #player.y -= 8
            player.y -= 20
        elif key[pygame.K_s] == True and player.y < boundary_bottom:
            action = 4
            #player.y += 8
            player.y += 20
        elif key[pygame.K_SPACE] == True:
            action = 8
        elif key[pygame.K_SPACE] and key[pygame.K.s] == True:
            action = 9
        elif key[pygame.K_e] == True:
          UI.toggleInventory()
        else:
          action=0

        # Inventory system
        if UI.inventoryRender:
          click = pygame.mouse.get_pressed()
          if click[0] == 1:  # Left mouse button clicked
            for slot in UI.inventory.slots:
              if slot.rect.collidepoint((mx, my)):
                  if slot.item and slot.item.name == "Health Potion" and player_health < 50 and slot.count > 0:
                    slot.count -= 1
                    player_health += 10
                    print("Health Potion Used")
                    
                  if slot.item and slot.item.name == "Strength Potion" and player_strength < 5 and slot.count > 0:
                    slot.count -= 1
                    player_strength += 1
                    print("Strength Potion Used")
                    
        # Shop system
        # Calculate the distance between the shop and the player
        distance_x = player.x - 500
        distance_y = player.y - 600
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        if distance < 250 and key[pygame.K_i] == True:
            # Used as a "switch" for the shop. Inverts the current state of the shop_active variable.
            shop_active = not shop_active

        if shop_active == True:
          #Shop / Chat UI
          shopUIbg = pygame.Rect(0, 0, 800, 150)
          pygame.draw.rect(screen, (10, 10, 10), shopUIbg)

          shopUIchatbox = pygame.Rect(10, 10, 540, 130)
          pygame.draw.rect(screen, (20, 20, 20), shopUIchatbox)

          shopUIchatboxTop = pygame.Rect(10, 10, 540, 10)
          pygame.draw.rect(screen, (30, 30, 30), shopUIchatboxTop)

          shopUIimagebox = pygame.Rect(560, 10, 230, 130)
          pygame.draw.rect(screen, (50, 50, 50), shopUIimagebox)

          # Buttons for items
          healthPotionButton = pygame.Rect(20, 90, 200, 40)
          pygame.draw.rect(screen, (30, 0, 120), healthPotionButton)
          draw_text('Buy Health Potion', font, (255, 255, 255), screen, 30, 100)

          strengthPotionButton = pygame.Rect(230, 90, 230, 40)
          pygame.draw.rect(screen, (30, 10, 120), strengthPotionButton)
          draw_text('Buy Strength Potion', font, (255, 255, 255), screen, 240, 100)

          keyButton = pygame.Rect(470, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), keyButton)
          draw_text('Buy Key', font, (255, 255, 255), screen, 490, 100)

          # Check if the player clicks on the shop item
          mx, my = pygame.mouse.get_pos()
          click = pygame.mouse.get_pressed()
          if healthPotionButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (60, 40, 150), healthPotionButton, 2)
            if click[0] == 1:
              if player.coins >= 10:
                player.coins -= 10
                
                for slot in UI.inventory.slots:
                  if slot.item and slot.item.name == "Health Potion":
                      slot.count += 1
                      break

          if strengthPotionButton.collidepoint((mx, my)):
              pygame.draw.rect(screen, (60, 40, 150), strengthPotionButton, 2)
              if click[0] == 1:
                if player.coins >= 20:
                  player.coins -= 20

                  for slot in UI.inventory.slots:
                      if slot.item and slot.item.name == "Strength Potion":
                          slot.count += 1
                          break
                        
          if keyButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (60, 40, 150), keyButton, 2)
            if click[0] == 1:
              if player.coins >= 100:
                player.coins -= 100
                UI.inventory.slots.append(InventorySlot("Key", "Images/Items/key.png", (417, 176)))
                
                for slot in UI.inventory.slots:
                    if slot.item and slot.item.name == "Key":
                        slot.count += 1
                        break
                      

        # Adjust the camera position to follow the player
        camera_x = player.x - (screen.get_width() // 2)
        camera_y = player.y - (screen.get_height() // 2)

        # Update health bar position with respect to the player
        health_bar_x = player.x - camera_x - 13
        health_bar_y = player.y - camera_y - 13

        # Draw the health bar
        draw_health_bar(screen, health_bar_x, health_bar_y, player_health)

        if player_health <= 0:
          if gameOver():
              # Reset game state for a new try
              player_health = max_player_health
          else:
              # Player chose to quit or go back to the main menu
              break
            
        # Game loop
        for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          if event.type == KEYDOWN:
              if event.key == K_ESCAPE:
                running = False
          if event.type == MOUSEBUTTONDOWN:
              if event.button == 1:
                click = True
          if event.type == MOUSEMOTION:  # Handle mouse movement
            mouse_pos = pygame.mouse.get_pos()  # Get the x and y coordinates of the mouse position

        UI.render(screen, mouse_pos)
        pygame.display.update()
        mainClock.tick(60)

# This function is called when the "Controls" button is clicked.
def controls(mx,my):
    running = True
    while running:
        screen.fill((0,190,255))

        draw_text('CONTROLS SCREEN', font, (255, 255, 255), screen, 300, 20)
        draw_text('UP - W', font, (255, 255, 255), screen, 352, 100)
        draw_text('DOWN - S', font, (255, 255, 255), screen, 352, 120)
        draw_text('LEFT - A', font, (255, 255, 255), screen, 352, 140)
        draw_text('RIGHT - D', font, (255, 255, 255), screen, 352, 160)
        draw_text('PRESS "ESC" TO GO BACK', font, (255, 255, 255), screen, 272, 180)

        for event in pygame.event.get():
          if event.type == QUIT:
            pygame.quit()
            sys.exit()
          if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
              running = False

        pygame.display.update()
        mainClock.tick(60)

# Runs the main menu function so it is the first thing the user sees.
main_menu()