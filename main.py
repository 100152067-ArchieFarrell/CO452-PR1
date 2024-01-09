import pygame, sys
import random
from pygame.locals import *
from UserInterface import UserInterface
from InventorySlot import InventorySlot
from healthBar import *
from coin import Coin
import spritesheet
from player import *

# Setting up the environment to initialize pygame
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('The Whispers')
screen = pygame.display.set_mode((800, 640),0,0)
from enemy import *
#pygame.mixer.init()

# Setting up the fonts that will be used
smallFont = pygame.font.Font("Fonts/PixeloidSans.ttf", 16)
font = pygame.font.Font("Fonts/PixeloidSans.ttf", 24)
boldFont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 24)
titleFont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 26)

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

# Loading the sprite sheets for player animations
sprite_sheet_image = pygame.image.load('Images/player spritesheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# List of animations and variables which will be used for updating the player's animation
animation_list = []
animation_steps = [6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 3, 3]
action = 0 
last_update = pygame.time.get_ticks()
animation_cooldown = 500
frame = 0
step_counter = 0

for animation in animation_steps:
  temp_img_list = []
  for _ in range(animation):
    temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 32, 2, (17, 55, 4)))
    step_counter += 1
  animation_list.append(temp_img_list)

# Loading the sprite sheets for shopkeeper animations
skSpriteSheetImage = pygame.image.load('Images/shopkeeper spritesheet.png').convert_alpha()
skSpriteSheet = spritesheet.SpriteSheet(skSpriteSheetImage)

# List of animations and variables which will be used for updating the shopkeeper's animation
skAnimationList = []
skAnimationSteps = [2, 2, 2, 2, 2]
skAction = 0 
skLastUpdate = pygame.time.get_ticks()
animation_cooldown = 500
skFrame = 0
step_counter = 0

for animation in skAnimationSteps:
  skTempImgList = []
  for _ in range(animation):
    skTempImgList.append(skSpriteSheet.get_image(step_counter, 48, 32, 2, (24, 0, 20)))
    step_counter += 1
  skAnimationList.append(skTempImgList)

# Function to write text on the screen and buttons
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def chat():
  chatBG = pygame.Rect(0, 0, 800, 150)
  pygame.draw.rect(screen, (10, 10, 10), chatBG)

  chatBox = pygame.Rect(10, 10, 620, 130)
  pygame.draw.rect(screen, (20, 20, 20), chatBox)

  chatBoxTop = pygame.Rect(10, 10, 620, 10)
  pygame.draw.rect(screen, (30, 30, 30), chatBoxTop)

  chatImageBox = pygame.Rect(640, 10, 150, 130)
  pygame.draw.rect(screen, (50, 50, 50), chatImageBox)

# A variable to check for the status later
click = False

#menuMusic = pygame.mixer.Sound("Sounds/Minifantasy_Dungeon_Music/Minifantasy_Dungeon_Music/Music/Goblins_Den_(Regular).wav")

# Main container function that holds the buttons and game functions
def main_menu():
    click = False
    while True:
        screen.blit(pygame.image.load('Images/title screen bg.png'), (0,0))
        mx, my = pygame.mouse.get_pos()

        # Creates the buttons on the screen
        playButton = pygame.Rect(300, 280, 200, 50)
        playButtonBorder = playButton.inflate(2,2)
        controlsButton = pygame.Rect(300, 340, 200, 50)
        controlsButtonBorder = controlsButton.inflate(2,2)
        creditsButton = pygame.Rect(300, 400, 200, 50)
        creditsButtonBorder = creditsButton.inflate(2,2)

        pygame.draw.rect(screen, (156, 29, 43), playButton)
        pygame.draw.rect(screen, (83, 10, 20), playButtonBorder, 4, 4)
        pygame.draw.rect(screen, (156, 29, 43), controlsButton)
        pygame.draw.rect(screen, (83, 10, 20), controlsButtonBorder, 4, 4)
        pygame.draw.rect(screen, (156, 29, 43), creditsButton)
        pygame.draw.rect(screen, (83, 10, 20), creditsButtonBorder, 4, 4)

        # Text that will be displayed on the buttons
        draw_text('PLAY', font, (255,255,255), screen, 369, 291)
        draw_text('CONTROLS', font, (255,255,255), screen, 336, 351)
        draw_text('CREDITS', font, (255,255,255), screen, 348, 411)

        # Functions that will be run when a certain button is clicked
        if playButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), playButton)
            pygame.draw.rect(screen, (73, 0, 10), playButtonBorder, 4, 4)
            draw_text('PLAY', font, (215,215,215), screen, 369, 291)
            if click:
                player_score = 0
                game(last_update, frame, action, Player, enemies, player_score, skAction, skFrame, skLastUpdate)
        if controlsButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), controlsButton)
            pygame.draw.rect(screen, (73, 0, 10), controlsButtonBorder, 4, 4)
            draw_text('CONTROLS', font, (215,215,215), screen, 336, 351)
            if click:
                controls(mx,my, last_update, frame, action)
        if creditsButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), creditsButton)
            pygame.draw.rect(screen, (73, 0, 10), creditsButtonBorder, 4, 4)
            draw_text('CREDITS', font, (215,215,215), screen, 348, 411)
            if click:
                credits()

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

def gameOver(player_score):
  click = False
  while True:
      screen.blit(pygame.image.load('Images/screen bg.png'), (0,0))
      tryAgainButton = pygame.Rect(300, 340, 200, 50)
      tryAgainButtonBorder = tryAgainButton.inflate(2,2)
      mainMenuButton = pygame.Rect(300, 400, 200, 50)
      mainMenuButtonBorder = mainMenuButton.inflate(2,2)
      quitButton = pygame.Rect(300, 460, 200, 50)
      quitButtonBorder = quitButton.inflate(2,2)
  
      pygame.draw.rect(screen, (156, 29, 43), tryAgainButton)
      pygame.draw.rect(screen, (83, 10, 20), tryAgainButtonBorder, 4, 4)
      pygame.draw.rect(screen, (156, 29, 43), mainMenuButton)
      pygame.draw.rect(screen, (83, 10, 20), mainMenuButtonBorder, 4, 4)
      pygame.draw.rect(screen, (156, 29, 43), quitButton)
      pygame.draw.rect(screen, (83, 10, 20), quitButtonBorder, 4, 4)

      draw_text('GAME OVER', titleFont, (255,255,255), screen, 308, 110)
      draw_text(f'SCORE: {player_score}', boldFont, (255, 255, 255), screen, 320, 218)
      draw_text('TRY AGAIN', font, (255, 255, 255), screen, 335, 352)
      draw_text('MAIN MENU', font, (255, 255, 255), screen, 328, 410)
      draw_text('QUIT', font, (255, 255, 255), screen, 372, 472)

      mx, my = pygame.mouse.get_pos()

      if tryAgainButton.collidepoint((mx, my)):
          pygame.draw.rect(screen, (146, 19, 23), tryAgainButton)
          pygame.draw.rect(screen, (73, 0, 10), tryAgainButtonBorder, 4, 4)
          draw_text('TRY AGAIN', font, (215,215,215), screen, 335, 352)
          if click:
              game(last_update, frame, action, Player, enemies, player_score, skAction, skFrame, skLastUpdate)

      if mainMenuButton.collidepoint((mx, my)):
          pygame.draw.rect(screen, (146, 19, 23), mainMenuButton)
          pygame.draw.rect(screen, (73, 0, 10), mainMenuButtonBorder, 4, 4)
          draw_text('MAIN MENU', font, (215,215,215), screen, 328, 410)
          if click:
              # Return to the main menu
              main_menu()

      if quitButton.collidepoint((mx, my)):
          pygame.draw.rect(screen, (146, 19, 23), quitButton)
          pygame.draw.rect(screen, (73, 0, 10), quitButtonBorder, 4, 4)
          draw_text('QUIT', font, (215,215,215), screen, 372, 472)
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

def gameComplete(player_score):
    click = False
    while True:
        screen.blit(pygame.image.load('Images/screen bg.png'), (0,0))
        mainMenuButton = pygame.Rect(300, 340, 200, 50)
        mainMenuButtonBorder = mainMenuButton.inflate(2,2)
        quitButton = pygame.Rect(300, 400, 200, 50)
        quitButtonBorder = quitButton.inflate(2,2)

        pygame.draw.rect(screen, (156, 29, 43), mainMenuButton)
        pygame.draw.rect(screen, (83, 10, 20), mainMenuButtonBorder, 4, 4)
        pygame.draw.rect(screen, (156, 29, 43), quitButton)
        pygame.draw.rect(screen, (83, 10, 20), quitButtonBorder, 4, 4)

        draw_text('GAME COMPLETE', titleFont, (255,255,255), screen, 270, 110)
        draw_text(f'SCORE: {player_score}', boldFont, (255, 255, 255), screen, 320, 218)
        draw_text('MAIN MENU', font, (255, 255, 255), screen, 328, 350)
        draw_text('QUIT', font, (255, 255, 255), screen, 372, 410)

        mx, my = pygame.mouse.get_pos()

        if mainMenuButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), mainMenuButton)
            pygame.draw.rect(screen, (73, 0, 10), mainMenuButtonBorder, 4, 4)
            draw_text('MAIN MENU', font, (215,215,215), screen, 328, 350)
            if click:
                # Return to the main menu
                main_menu()

        if quitButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), quitButton)
            pygame.draw.rect(screen, (73, 0, 10), quitButtonBorder, 4, 4)
            draw_text('QUIT', font, (215,215,215), screen, 372, 410)
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
      screen.blit(pygame.image.load('Images/screen bg.png'), (0,0))

      draw_text('CREDITS SCREEN', titleFont, (255, 255, 255), screen, 266, 70)
      draw_text('GAME BY:', boldFont, (255, 255, 255), screen, 275, 130)
      draw_text('Natalie O Callaghan', font, (255, 255, 255), screen, 275, 170)
      draw_text('Charlie Glover', font, (255, 255, 255), screen, 275, 210)
      draw_text('Archie Farrell', font, (255, 255, 255), screen, 275, 250)
      draw_text('ASSETS BY:', boldFont, (255, 255, 255), screen, 275, 310)
      draw_text('(asset credits)', font, (255, 255, 255), screen, 275, 350)

      draw_text('PRESS "ESC" TO GO BACK', boldFont, (255, 255, 255), screen, 212, 540)

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
def game(last_update, frame, action, Player, enemies, player_score, skAction, skFrame, skLastUpdate):
    mouse_pos = (0, 0)
    # sets the running state of the game to "true"
    running = True
    hasKey = False
    complete = False
    inCutscene = True
    inFirstCutscene = True
    inSecondCutscene = False
    inThirdCutscene = True
    inFourthCutscene = False
    cutscenesComplete = False
    textCounter = 0
    # loads the default image for the game's character
    player = Player(1114, 915, 50, 50, 1, 250, 0)
    UI = UserInterface(player)
    player_image = pygame.image.load('Images/frank.png')
    player_image = pygame.transform.scale(player_image, (26, 42))
    # enemy image
    boss = Enemy(1000, 800, 50, 4, 50, "player_image.png")
    bossArray = []
    bossArray.append(boss)
    enemy_image = pygame.image.load('Images/zombie.jpg')
    enemy_image = pygame.transform.scale(enemy_image, (45, 42))

    # Music / Sounds
    # Level Music
    #forestMusic = pygame.mixer.music.load('Sounds/dont_need_a_hero_sfx_and_musics/theme_foret.mp3')
    #dungeonMusic = pygame.mixer.music.load('Sounds/dont_need_a_hero_sfx_and_musics/theme_ruine.mp3')

    # Player Sounds
    #playerWalk = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/12_Player_Movement_SFX/08_Step_rock_02.wav")
    #playerAttack = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/12_Player_Movement_SFX/56_Attack_03.wav")
    #playerDamaged = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/12_Player_Movement_SFX/61_Hit_03.wav")

    # Shop and Inventory Sounds
    #purchase = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/079_Buy_sell_01.wav")
    #purchaseDenied = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/033_Denied_03.wav")
    #itemUsed = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/051_use_item_01.wav")
  
    # Misc. Sounds
    #dialogue = pygame.mixer.Sound("Sounds/8_bit_16_bit_Sound_Effects/Text 1.wav")
    #coinCollect = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/013_Confirm_03.wav")
  
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
    boundary_left = 514
    boundary_right = 1770 - player.width
    boundary_top = 483
    boundary_bottom = 1445 - player.height

    camera_x, camera_y = 0, 0

    # Set up variables for combat
    player_health = 50  # Initial health of the player
    player_strength = 1 # Initial strength of the player
    enemy_attack_cooldown = 15000  # Cooldown for enemy attacks in milliseconds
    
    enemyCoins = []
    last_enemy_attack = pygame.time.get_ticks()
    lastWaveTime = pygame.time.get_ticks()
    waveInterval = 10000

    shop_active = False
    playerUsedShop = False
    level = 1
    while running:
        player_score = player.score
        currentTime = pygame.time.get_ticks()
        screen.fill((0, 0, 0))
        screen.blit(ground, (0 - camera_x, 0 - camera_y))
        screen.blit(dungeon, (0 - camera_x, 0 - camera_y))
        if level == 1:
          # shopkeeper animation
          skCurrentTime = pygame.time.get_ticks()
          if skCurrentTime - skLastUpdate >= animation_cooldown:
            skFrame += 1
            skLastUpdate = skCurrentTime
            if skFrame >= len(skAnimationList[skAction]):
              skFrame = 0

          if skFrame < 0 or skFrame >= len(skAnimationList[skAction]):
            skFrame = 0  # Set the default frame if it's out of range
          
          skAction = 0
          screen.blit(skAnimationList[skAction][skFrame],(634 - camera_x, 538 - camera_y))
          screen.blit(shop, (0 - camera_x, 0 - camera_y))

        key = pygame.key.get_pressed()

      # Save the current position for boundary checking
        player_x, player_y = player.x, player.y

      # player animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
          frame += 1
          last_update = current_time
          if frame >= len(animation_list[action]):
            frame = 0

        if frame < 0 or frame >= len(animation_list[action]):
          frame = 0  # Set the default frame if it's out of range

        screen.blit(animation_list[action][frame],(362, 312))
          
        # enemy spawning
        if playerUsedShop == True:
          if currentTime - lastWaveTime >= waveInterval and enemies == []:
            enemies = enemyWave(Enemy, player, camera_x, camera_y)
            spawnerWalls_visible = False
            lastWaveTime = currentTime

        for enemy in enemies:
          directionToGo = enemy.move_towards_player(player, camera_x, camera_y, level)
          enemy.render(screen, camera_x, camera_y, action, level)
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
                  player.score += 10  # Increase player score for killing an enemy
                  coinAmount = random.randint(1, 5)
                  for i in range(coinAmount):
                    coin = Coin(1, "Images/Items/coin.png", position=(enemy.map_x + random.randint(1,10), enemy.map_y + random.randint(1, 10)))
                    enemyCoins.append(coin)

          # Check for enemy-player collision and update health
          current_time = pygame.time.get_ticks()
          if (
              player.x < enemy.map_x + enemy.size
              and player.x + player.width > enemy.map_x
              and player.y < enemy.map_y + enemy.size
              and player.y + player.height > enemy.map_y
              and current_time - last_enemy_attack >= enemy_attack_cooldown
          ):
              player_health -= 5  # Decrease player health on collision
              last_enemy_attack = current_time

        for coin in enemyCoins:
          # Checks if the coordinates of the player and coin instance are overlapping
          if (
              player.x < coin.rect.x + coin.rect.width
              and player.x + player.width > coin.rect.x
              and player.y < coin.rect.y + coin.rect.height
              and player.y + player.height > coin.rect.y
          ):
            # Player picked up the coin, add its value to the player's coin counter
            player.coins += coin.value
            # Remove the coin from the list
            enemyCoins.remove(coin)
            #coinCollect.play()
          coin.update()
          coin.render(screen, camera_x, camera_y)

        if level == 1:
          screen.blit(bushesStumps, (0 - camera_x, 0 - camera_y))
        screen.blit(shopFence, (0 - camera_x, 0 - camera_y))
        screen.blit(trees, (0 - camera_x, 0 - camera_y))
        screen.blit(rocksBoxes, (0 - camera_x, 0 - camera_y))
        if spawnerWalls_visible:
          screen.blit(spawnerWalls, (0 - camera_x, 0 - camera_y))
        ## Cutscenes
        # First 'cutscene'
        if inFirstCutscene == True:
          inCutscene = True
          cutscenemx, cutscenemy = pygame.mouse.get_pos()
          cutsceneClick = pygame.mouse.get_pressed()
          chat()
          continueButton = pygame.Rect(500, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), continueButton)
          draw_text('Continue', smallFont, (255, 255, 255), screen, 522, 100)
          cutsceneText = ["This is Frank.", "", "He's currently stuck in the middle of a forest, searching", "for a 'long lost treasure' after hearing some whispers about it.", "They led him right here. Surely after all of this travelling,", "the treasure must be closeby now."]
          
          screen.blit(animation_list[action][frame],(666, 60))

          draw_text(cutsceneText[textCounter], smallFont, (255, 255, 255), screen, 24, 30)

          draw_text(cutsceneText[textCounter+1], smallFont, (255, 255, 255), screen, 24, 50)

          if continueButton.collidepoint((cutscenemx, cutscenemy)):
            pygame.draw.rect(screen, (60, 40, 150), continueButton, 2)
            if cutsceneClick[0] == 1:
              #dialogue.play()
              textCounter = textCounter + 2
          
          if textCounter > 4:
            inFirstCutscene = False
            inCutscene = False
            textCounter = 0

        # Second 'cutscene'
        if inSecondCutscene == True:
          inCutscene = True
          cutscenemx, cutscenemy = pygame.mouse.get_pos()
          cutsceneClick = pygame.mouse.get_pressed()
          chat()
          continueButton = pygame.Rect(500, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), continueButton)
          draw_text('Continue', smallFont, (255, 255, 255), screen, 522, 100)
          cutsceneText = ["Hey there! Strange seeing someone around here for once...", "Who might you be?", "Frank.", "", "Hi Frank, I'm Sven. I've been running this shop round here for", "many years...","I suppose you're looking for the treasure, huh?", "", "Yes.", "", "Well, I have just the thing for you! Here in stock, I have the key", "to the dungeon where the treasure is kept!", "However, as the treasure has never actually been found, I do", "require a deposit on the key.", "... Why can't you just go into the dungeon yourself if you have", "the key?", "Well, you see.. I'm actually stuck in place.", "Also I'm safe in my little stall, no monsters can get me from in here.","Oh yeah, the monsters. Hoards of them like to roam around and", "attack anyone they can find.", "The walls only stay up for so long unfortunately, then they won't", "stop coming back..", "Anyway! Have fun, come back to me if you want to purchase", "any items :)"]
          if textCounter == 2 or textCounter == 8 or textCounter == 14:
            screen.blit(animation_list[0][frame],(666, 60))
          else:
            screen.blit(skAnimationList[skAction][skFrame],(682, 60))

          draw_text(cutsceneText[textCounter], smallFont, (255, 255, 255), screen, 24, 30)

          draw_text(cutsceneText[textCounter+1], smallFont, (255, 255, 255), screen, 24, 50)

          if continueButton.collidepoint((cutscenemx, cutscenemy)):
            pygame.draw.rect(screen, (60, 40, 150), continueButton, 2)
            if cutsceneClick[0] == 1:
              #dialogue.play()
              textCounter = textCounter + 2

          if textCounter > 20:
            inSecondCutscene = False
            inCutscene = False
            playerUsedShop = True
            textCounter = 0

        # Third 'cutscene'
        if inThirdCutscene == True and level == 2:
          inCutscene = True
          cutscenemx, cutscenemy = pygame.mouse.get_pos()
          cutsceneClick = pygame.mouse.get_pressed()
          chat()
          continueButton = pygame.Rect(500, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), continueButton)
          draw_text('Continue', smallFont, (255, 255, 255), screen, 522, 100)
          cutsceneText = ["Well this is spacious...", "Now, where's that treasure?", "HALT! Stop right there!", "You are NOT getting my treasure", "Oh really?", "", "Save the chat, intruder.", "Prepare to be taken out."]

          if textCounter == 0 or textCounter == 4:
            screen.blit(animation_list[0][frame],(666, 60))
          else:
            draw_text("?", titleFont, (255, 255, 255), screen, 706, 76)

          draw_text(cutsceneText[textCounter], smallFont, (255, 255, 255), screen, 24, 30)

          draw_text(cutsceneText[textCounter+1], smallFont, (255, 255, 255), screen, 24, 50)

          if continueButton.collidepoint((cutscenemx, cutscenemy)):
            pygame.draw.rect(screen, (60, 40, 150), continueButton, 2)
            if cutsceneClick[0] == 1:
              #dialogue.play()
              textCounter = textCounter + 2

          if textCounter > 6:
            inThirdCutscene = False
            inCutscene = False
            textCounter = 0

        # Fourth 'cutscene'
        if inFourthCutscene == True and level == 2:
          inCutscene = True
          cutscenemx, cutscenemy = pygame.mouse.get_pos()
          cutsceneClick = pygame.mouse.get_pressed()
          chat()
          continueButton = pygame.Rect(500, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), continueButton)
          draw_text('Continue', smallFont, (255, 255, 255), screen, 522, 100)
          cutsceneText = ["The treasure is now mine!!", "Now, how do I get out of here?", "Seems like the plan didn't work this time...", "", "I will avenge you, Steven...", "","To be continued...?", ""]

          if textCounter == 0:
            screen.blit(animation_list[action][frame],(666, 60))
          elif textCounter == 2:
            screen.blit(skAnimationList[skAction][skFrame],(682, 60))
          elif textCounter == 4:
            screen.blit(skAnimationList[4][0],(682, 60))
          else:
            draw_text("?", titleFont, (255, 255, 255), screen, 706, 76)
            
          draw_text(cutsceneText[textCounter], smallFont, (255, 255, 255), screen, 24, 30)

          draw_text(cutsceneText[textCounter+1], smallFont, (255, 255, 255), screen, 24, 50)

          if continueButton.collidepoint((cutscenemx, cutscenemy)):
            pygame.draw.rect(screen, (60, 40, 150), continueButton, 2)
            if cutsceneClick[0] == 1:
              #dialogue.play()
              textCounter = textCounter + 2

          if textCounter > 6:
            inFourthCutscene = False
            cutscenesComplete = True
            inCutscene = False
            textCounter = 0
        
        if inCutscene != True:
          if key[pygame.K_a] == True and player.x > boundary_left:
              #playerWalk.play()
              action = 6
              #player.x -= 8
              player.x -= 20
          elif key[pygame.K_d] == True and player.x < boundary_right:
              #playerWalk.play()
              action = 5
              #player.x += 8
              player.x += 20
          elif key[pygame.K_w] == True and player.y > boundary_top:
              #playerWalk.play()
              action = 7
              #player.y -= 8
              player.y -= 20
          elif key[pygame.K_s] == True and player.y < boundary_bottom:
              #playerWalk.play()
              action = 4
              #player.y += 8
              player.y += 20
          elif key[pygame.K_SPACE] == True:
              #playerAttack.play()
              action = 8
          elif key[pygame.K_e] == True:
            UI.toggleInventory()
          else:
            action=0

        # Inventory system
        if UI.inventoryRender:
          inventorymx, inventorymy = pygame.mouse.get_pos()
          inventoryClick = pygame.mouse.get_pressed()
          if inventoryClick[0] == 1:  # Left mouse button clicked
            for slot in UI.inventory.slots:
              if slot.rect.collidepoint((inventorymx, inventorymy)):
                  if slot.item and slot.item.name == "Health Potion" and player_health < 50 and slot.count > 0:
                    slot.count -= 1
                    if player_health < 35:
                      player_health += 15
                    else:
                      player_health = player_health + (50 - player_health)
                    #itemUsed.play()
                    print("Health Potion Used")
                    
                  if slot.item and slot.item.name == "Strength Potion" and player_strength < 5 and slot.count > 0:
                    slot.count -= 1
                    player_strength += 1
                    #itemUsed.play()
                    print("Strength Potion Used")
                    
        # Shop system
        # Calculate the distance between the shop and the player
        shopDistanceX = player.x - 550
        shopDistanceY = player.y - 600
        shopDistance = (shopDistanceX ** 2 + shopDistanceY ** 2) ** 0.5
        if shopDistance < 108 and level == 1:
              action = 3
              if playerUsedShop == False:
                inSecondCutscene = True
              else:  
                shop_active = True
                playerUsedShop = True
        else:
              shop_active = False

        if shop_active == True:
          #Shop
          chat()
          #dialogue.play()
          screen.blit(skAnimationList[skAction][skFrame],(682, 60))

          draw_text('Here to purchase an item? Health potions are 10 coins, strength', smallFont, (255, 255, 255), screen, 24, 30)

          draw_text('potions are 20 coins and the key is 100 coins.', smallFont, (255, 255, 255), screen, 24, 50)

          # Buttons for items
          healthPotionButton = pygame.Rect(20, 90, 180, 40)
          pygame.draw.rect(screen, (30, 0, 120), healthPotionButton)
          draw_text('Buy Health Potion', smallFont, (255, 255, 255), screen, 34, 100)

          strengthPotionButton = pygame.Rect(210, 90, 200, 40)
          pygame.draw.rect(screen, (30, 10, 120), strengthPotionButton)
          draw_text('Buy Strength Potion', smallFont, (255, 255, 255), screen, 223, 100)

          keyButton = pygame.Rect(420, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), keyButton)
          draw_text('Buy Key', smallFont, (255, 255, 255), screen, 446, 100)

          # Check if the player clicks on the shop item
          shopmx, shopmy = pygame.mouse.get_pos()
          shopClick = pygame.mouse.get_pressed()
          if healthPotionButton.collidepoint((shopmx, shopmy)):
            pygame.draw.rect(screen, (60, 40, 150), healthPotionButton, 2)
            if shopClick[0] == 1:
              if player.coins >= 10:
                #purchase.play()
                player.coins -= 10
                
                for slot in UI.inventory.slots:
                  if slot.item and slot.item.name == "Health Potion":
                      slot.count += 1
                      break
              else:
                #purchaseDenied.play()
                pass

          if strengthPotionButton.collidepoint((shopmx, shopmy)):
              pygame.draw.rect(screen, (60, 40, 150), strengthPotionButton, 2)
              if shopClick[0] == 1:
                if player.coins >= 20:
                  #purchase.play()
                  player.coins -= 20

                  for slot in UI.inventory.slots:
                      if slot.item and slot.item.name == "Strength Potion":
                          slot.count += 1
                          break
                else:
                  #purchaseDenied.play()
                  pass
                        
          if keyButton.collidepoint((shopmx, shopmy)):
            pygame.draw.rect(screen, (60, 40, 150), keyButton, 2)
            if shopClick[0] == 1:
              if player.coins >= 100 and hasKey == False:
                player.coins -= 100
                UI.inventory.slots.append(InventorySlot("Key", "Images/Items/key.png", (417, 176)))
                
                for slot in UI.inventory.slots:
                    if slot.item and slot.item.name == "Key":
                        hasKey = True
                        slot.count += 1
                        break
              else:
                #purchaseDenied.play()
                pass
        
        # Level 2
        for slot in UI.inventory.slots:
          if slot.item and slot.item.name == "Key" and slot.count > 0 and (1450 < player.x < 1620 and 1370 < player.y < 1400):
            level = 2
            slot.count = 0

        if level == 2:
          enemies = []
          playerUsedShop = False
          ground = pygame.image.load("Images/game map (image layers)/dungeonGround.png")
          ground = pygame.transform.scale(ground, (2400, 1920))
          dungeon = pygame.image.load("Images/game map (image layers)/shadowing.png")
          dungeon = pygame.transform.scale(dungeon, (2400, 1920))
          shopFence = pygame.image.load("Images/game map (image layers)/walls.png")
          shopFence = pygame.transform.scale(shopFence, (2400, 1920))
          trees = pygame.image.load("Images/game map (image layers)/boxes.png")
          trees = pygame.transform.scale(trees, (2400, 1920))
          rocksBoxes = pygame.image.load("Images/game map (image layers)/extras.png")
          rocksBoxes = pygame.transform.scale(rocksBoxes, (2400, 1920))
          playerUsedShop = False

          if cutscenesComplete == True and len(enemyCoins) == 0:
            gameComplete(player_score)

          if complete == True:
            action = 0
            inFourthCutscene = True
            
          if inThirdCutscene == False and boss.health > 0:
            boss.move_towards_player(player, camera_x, camera_y, level)
            boss.render(screen, camera_x, camera_y, action, level)
            
            # Update health bar position with respect to the boss
            boss_health_bar_x = boss.map_x - camera_x + 54 
            boss_health_bar_y = boss.map_y - camera_y + 18
            # Draw the health bar
            draw_health_bar(screen, boss_health_bar_x, boss_health_bar_y, boss.health)
  
            if (
              player.x < boss.map_x + boss.size
              and player.x + player.width > boss.map_x
              and player.y < boss.map_y + boss.size
              and player.y + player.height > boss.map_y
              and action == 8  # Check if the player is attacking
            ):
              boss.health -= player_strength  # Decrease boss health on collision
              
              if boss.health <= 0:
                  bossArray.remove(boss)
                  player.score += 100  # Increase player score for killing the boss
                  player.score = round(player.score * (1+(player_health/10)))
                  coinAmount = 500
                  for i in range(coinAmount):
                    coin = Coin(1, "Images/Items/coin.png",(boss.map_x + random.randint(20,40), boss.map_y + random.randint(20, 40)))
                    enemyCoins.append(coin)
                  complete = True
                  print("Game Complete")
              
            # Check for enemy-player collision and update health
            current_time = pygame.time.get_ticks()
            enemy_attack_cooldown = 30000  # Cooldown for enemy attacks in milliseconds
            if (
              player.x < boss.map_x + boss.size
              and player.x + player.width > boss.map_x
              and player.y < boss.map_y + boss.size
              and player.y + player.height > boss.map_y
              and current_time - last_enemy_attack >= enemy_attack_cooldown
            ):
              player_health -= 15  # Decrease player health on collision
              last_enemy_attack = current_time  # Update last attack time
  
            for coin in enemyCoins:
            # Checks if the coordinates of the player and coin instance are overlapping
              if (
                player.x < coin.rect.x + coin.rect.width
                and player.x + player.width > coin.rect.x
                and player.y < coin.rect.y + coin.rect.height
                and player.y + player.height > coin.rect.y
              ):
            # Player picked up the coin, add its value to the player's coin counter
                player.coins += coin.value
                # Remove the coin from the list
                enemyCoins.remove(coin)
              coin.update()
              coin.render(screen, camera_x, camera_y)

        # Adjust the camera position to follow the player
        camera_x = player.x - (screen.get_width() // 2)
        camera_y = player.y - (screen.get_height() // 2)

        # Update health bar position with respect to the player
        health_bar_x = player.x - camera_x - 13
        health_bar_y = player.y - camera_y - 13

        # Draw the health bar
        draw_health_bar(screen, health_bar_x, health_bar_y, player_health)

        if player_health <= 0:
          if gameOver(player_score):
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
def controls(mx,my, last_update, frame, action):
    running = True
    viewInventory = False
    while running:
        screen.blit(pygame.image.load('Images/screen bg.png'), (0,0))

        draw_text('CONTROLS SCREEN', titleFont, (255, 255, 255), screen, 253, 70)
        draw_text('UP - W', font, (255, 255, 255), screen, 275, 130)
        draw_text('DOWN - S', font, (255, 255, 255), screen, 275, 170)
        draw_text('LEFT - A', font, (255, 255, 255), screen, 275, 210)
        draw_text('RIGHT - D', font, (255, 255, 255), screen, 275, 250)
        draw_text('ATTACK - SPACEBAR', font, (255, 255, 255), screen, 275, 290)
        draw_text('INVENTORY - E', font, (255, 255, 255), screen, 275, 330)
        
        draw_text('PRESS "ESC" TO GO BACK', boldFont, (255, 255, 255), screen, 212, 540)

      # animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
          frame += 1
          last_update = current_time
          if frame >= len(animation_list[action]):
            frame = 0

        if frame < 0 or frame >= len(animation_list[action]):
          frame = 0  # Set the default frame if it's out of range
          
        screen.blit(animation_list[action][frame],(340, 360))
        
        key = pygame.key.get_pressed()

        if key[pygame.K_a] == True:
          action = 6
        elif key[pygame.K_d] == True:
          action = 5
        elif key[pygame.K_w] == True:
          action = 7
        elif key[pygame.K_s] == True:
          action = 4
        elif key[pygame.K_SPACE] == True:
          action = 8
        elif key[pygame.K_e] == True:
          viewInventory = not viewInventory
        else:
          action=0

        if viewInventory == True:
          inventory = pygame.image.load("Images/Inventory.png")
          inventory = pygame.transform.scale(inventory, (160, 188))
          screen.blit(inventory, (306, 354))

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