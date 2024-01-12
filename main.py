# main.py
'''
# * Authors: Natalie O'Callaghan, Charlie Glover, Archie Farrell
# * Date: January 11, 2024
# * Description: This is the main area of the program, where the game will run. It will open up by presenting the player with a main menu where they can select if they want to start the game, look at the controls or look at the credits.
'''
# Importing modules to be used by the rest of the program
import pygame, sys
import random
from pygame.locals import *
from userInterface import UserInterface
from inventorySlot import InventorySlot
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
pygame.mixer.init()

# Setting up the fonts that will be used throughout the game
smallFont = pygame.font.Font("Fonts/PixeloidSans.ttf", 16)
font = pygame.font.Font("Fonts/PixeloidSans.ttf", 24)
boldFont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 24)
titleFont = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 26)

# Setting up the enemy array that will be used to store enemy instances
enemies = []

# Setting up an "enemy wave" function that will spawn groups of enemies in different areas of the map as groups all at once to act as a "wave"
def enemyWave(Enemy, player, camera_x, camera_y):
  enemies=[]
  amountInGroup = 3
  groups = 4
  for i in range(0, groups):
    for x in range(0, amountInGroup):
      groupCoords = [(random.randint(850, 900), random.randint(430, 480)),((random.randint(1700, 1750), random.randint(730, 780))),(random.randint(700, 750), random.randint(1400, 1450)),(random.randint(430, 480), random.randint(1120, 1170))]
      enemy = Enemy(groupCoords[i][0], groupCoords[i][1], 50, random.randint(1, 2), random.randint(2,5), "Images/zombie.jpg")
      enemies.append(enemy)
  return enemies

# Loading the spritesheet for the player's animations
spriteSheetImage = pygame.image.load('Images/player spritesheet.png').convert_alpha()
spriteSheet = spritesheet.SpriteSheet(spriteSheetImage)

# List of animations and variables which will be used for updating the player's animation
animationList = []
animationSteps = [6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 3, 3]
action = 0 
lastUpdate = pygame.time.get_ticks()
animationCooldown = 500
frame = 0
stepCounter = 0

# Adding the player animations to the previously created array so the animations can be accessed in groups
for animation in animationSteps:
  tempImgList = []
  for _ in range(animation):
    tempImgList.append(spriteSheet.retrieveImage(stepCounter, 48, 32, 2, (17, 55, 4)))
    stepCounter += 1
  animationList.append(tempImgList)

# Loading the spritesheet for the shopkeeper's animations
skSpriteSheetImage = pygame.image.load('Images/shopkeeper spritesheet.png').convert_alpha()
skSpriteSheet = spritesheet.SpriteSheet(skSpriteSheetImage)

# List of animations and variables which will be used for updating the shopkeeper's animation
skAnimationList = []
skAnimationSteps = [2, 2, 2, 2, 2]
skAction = 0 
skLastUpdate = pygame.time.get_ticks()
animationCooldown = 500
skFrame = 0
stepCounter = 0

# Adding the player animations to the previously created array so the animations can be accessed in groups
for animation in skAnimationSteps:
  skTempImgList = []
  for _ in range(animation):
    skTempImgList.append(skSpriteSheet.retrieveImage(stepCounter, 48, 32, 2, (24, 0, 20)))
    stepCounter += 1
  skAnimationList.append(skTempImgList)

# Function that will draw text on the screen, will be used for putting text in different places on screen and on buttons
def drawText(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Function that makes the "chat" / "dialogue" interface that will be used for the shop interface and "cutscenes". It's made up of different coloured rectangles placed on top of each other.
def chat():
  chatBG = pygame.Rect(0, 0, 800, 150)
  pygame.draw.rect(screen, (10, 10, 10), chatBG)

  chatBox = pygame.Rect(10, 10, 620, 130)
  pygame.draw.rect(screen, (20, 20, 20), chatBox)

  chatBoxTop = pygame.Rect(10, 10, 620, 10)
  pygame.draw.rect(screen, (30, 30, 30), chatBoxTop)

  chatImageBox = pygame.Rect(640, 10, 150, 130)
  pygame.draw.rect(screen, (50, 50, 50), chatImageBox)

# Sets the "click" variable to False as default to stop errors happening as the program opens
click = False

# Menu music
menuMusic = pygame.mixer.Sound("Sounds/Minifantasy_Dungeon_Music/Minifantasy_Dungeon_Music/Music/Goblins_Den_(Regular).wav")

# Function that holds the main menu of the game, this is made up of a background image and buttons
def mainMenu():
    # Plays music on the main menu
    pygame.mixer.music.load('Sounds/dont_need_a_hero_sfx_and_musics/theme_ruine.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    # Sets the "click" variable to False so the user doesn't accidentally select something they didn't want to simply by being hovered over a button spot when they open the game
    click = False
    # Loop to keep the menu from being "static" and gives it more functionality
    while True:
        # Background image for the menu
        screen.blit(pygame.image.load('Images/title screen bg.png'), (0,0))
        # Gets the current position of the mouse, these values will be used for interacting with buttons
        mx, my = pygame.mouse.get_pos()

        # Creates the buttons on the screen (play, controls, credits)
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
        drawText('PLAY', font, (255,255,255), screen, 369, 291)
        drawText('CONTROLS', font, (255,255,255), screen, 336, 351)
        drawText('CREDITS', font, (255,255,255), screen, 348, 411)

        # Highlights the buttons when the mouse is hovering over them and runs functions when certain buttons are clicked
        if playButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), playButton)
            pygame.draw.rect(screen, (73, 0, 10), playButtonBorder, 4, 4)
            drawText('PLAY', font, (215,215,215), screen, 369, 291)
            if click:
                playerScore = 0
                game(lastUpdate, frame, action, Player, enemies, playerScore, skAction, skFrame, skLastUpdate)
        if controlsButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), controlsButton)
            pygame.draw.rect(screen, (73, 0, 10), controlsButtonBorder, 4, 4)
            drawText('CONTROLS', font, (215,215,215), screen, 336, 351)
            if click:
                controls(mx,my, lastUpdate, frame, action)
        if creditsButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), creditsButton)
            pygame.draw.rect(screen, (73, 0, 10), creditsButtonBorder, 4, 4)
            drawText('CREDITS', font, (215,215,215), screen, 348, 411)
            if click:
                credits()

        # Event loop that tracks when the "x" button, the esc key or the mouse is clicked
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

# Function that displays the player their score when they 'lose' the game and gives them the option to restart or go back to the main menu
def gameOver(playerScore):
  click = False
  while True:
      # Background image and buttons (try again, main menu) on the screen 
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

      # Text that will be displayed on the buttons
      drawText('GAME OVER', titleFont, (255,255,255), screen, 308, 110)
      drawText(f'SCORE: {playerScore}', boldFont, (255, 255, 255), screen, 316, 218)
      drawText('TRY AGAIN', font, (255, 255, 255), screen, 335, 352)
      drawText('MAIN MENU', font, (255, 255, 255), screen, 328, 410)
      drawText('QUIT', font, (255, 255, 255), screen, 372, 472)

      # Gets the current position of the mouse, these values will be used for interacting with buttons
      mx, my = pygame.mouse.get_pos()

      # Highlights the buttons when the mouse is hovering over them and runs functions when certain buttons are clicked
      if tryAgainButton.collidepoint((mx, my)):
          pygame.draw.rect(screen, (146, 19, 23), tryAgainButton)
          pygame.draw.rect(screen, (73, 0, 10), tryAgainButtonBorder, 4, 4)
          drawText('TRY AGAIN', font, (215,215,215), screen, 335, 352)
          if click:
              game(lastUpdate, frame, action, Player, enemies, playerScore, skAction, skFrame, skLastUpdate)

      if mainMenuButton.collidepoint((mx, my)):
          pygame.draw.rect(screen, (146, 19, 23), mainMenuButton)
          pygame.draw.rect(screen, (73, 0, 10), mainMenuButtonBorder, 4, 4)
          drawText('MAIN MENU', font, (215,215,215), screen, 328, 410)
          if click:
              mainMenu()

      if quitButton.collidepoint((mx, my)):
          pygame.draw.rect(screen, (146, 19, 23), quitButton)
          pygame.draw.rect(screen, (73, 0, 10), quitButtonBorder, 4, 4)
          drawText('QUIT', font, (215,215,215), screen, 372, 472)
          if click:
              pygame.quit()
              sys.exit()

      # Event loop that tracks when the "x" button or the mouse is clicked
      for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          if event.type == MOUSEBUTTONDOWN:
              if event.button == 1:
                  click = True

      pygame.display.update()
      mainClock.tick(60)

# Function that displays the player their score when they win the game and gives them the option to go back to the main menu or quit
def gameComplete(playerScore):
    click = False
    while True:
        # Background image and buttons (main menu, quit) on the screen 
        screen.blit(pygame.image.load('Images/screen bg.png'), (0,0))
        mainMenuButton = pygame.Rect(300, 340, 200, 50)
        mainMenuButtonBorder = mainMenuButton.inflate(2,2)
        quitButton = pygame.Rect(300, 400, 200, 50)
        quitButtonBorder = quitButton.inflate(2,2)

        pygame.draw.rect(screen, (156, 29, 43), mainMenuButton)
        pygame.draw.rect(screen, (83, 10, 20), mainMenuButtonBorder, 4, 4)
        pygame.draw.rect(screen, (156, 29, 43), quitButton)
        pygame.draw.rect(screen, (83, 10, 20), quitButtonBorder, 4, 4)

        # Text that will be displayed on the buttons
        drawText('GAME COMPLETE', titleFont, (255,255,255), screen, 270, 110)
        drawText(f'SCORE: {playerScore}', boldFont, (255, 255, 255), screen, 316, 218)
        drawText('MAIN MENU', font, (255, 255, 255), screen, 328, 350)
        drawText('QUIT', font, (255, 255, 255), screen, 372, 410)

        # Gets the current position of the mouse, these values will be used for interacting with buttons
        mx, my = pygame.mouse.get_pos()

        # Highlights the buttons when the mouse is hovering over them and runs functions when certain buttons are clicked
        if mainMenuButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), mainMenuButton)
            pygame.draw.rect(screen, (73, 0, 10), mainMenuButtonBorder, 4, 4)
            drawText('MAIN MENU', font, (215,215,215), screen, 328, 350)
            if click:
                mainMenu()

        if quitButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, (146, 19, 23), quitButton)
            pygame.draw.rect(screen, (73, 0, 10), quitButtonBorder, 4, 4)
            drawText('QUIT', font, (215,215,215), screen, 372, 410)
            if click:
                pygame.quit()
                sys.exit()

        # Event loop that tracks when the "x" button or the mouse is clicked
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

# Function that displays the game credits to the player
def credits():
  running = True
  while running:
      # Background image and text displayed on screen
      screen.blit(pygame.image.load('Images/screen bg.png'), (0,0))

      drawText('CREDITS SCREEN', titleFont, (255, 255, 255), screen, 266, 70)
      drawText('GAME BY:', boldFont, (255, 255, 255), screen, 275, 130)
      drawText('Natalie O Callaghan', font, (255, 255, 255), screen, 275, 170)
      drawText('Charlie Glover', font, (255, 255, 255), screen, 275, 210)
      drawText('Archie Farrell', font, (255, 255, 255), screen, 275, 250)
      drawText('ASSETS BY:', boldFont, (255, 255, 255), screen, 275, 320)
      drawText('Game Endeavor, Jamie Brownhill, cuddle bug, 0x72,', font, (255, 255, 255), screen, 70, 360)  
      drawText('o_lobster, Kyrise, Sagak Art (Pururu), Leohpaz,', font, (255, 255, 255), screen, 70, 400) 
      drawText('PaperHatLizard, JDWasabi, evilduckk, GGBotNet', font, (255, 255, 255), screen, 70, 440)

      drawText('PRESS "ESC" TO GO BACK', boldFont, (255, 255, 255), screen, 212, 540)

      # Event loop that tracks when the "x" button or the esc key is clicked
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            running = False

      pygame.display.update()
      mainClock.tick(60)
      
# Function that runs the game
def game(lastUpdate, frame, action, Player, enemies, playerScore, skAction, skFrame, skLastUpdate):
    # Coordinates of the mouse position
    mouse_pos = (0, 0)
    
    # Sets the running state of the game to "true"
    running = True
    
    # Sets the default states of variables used throughout the game
    hasKey = False
    complete = False
    inCutscene = True
    inFirstCutscene = True
    inSecondCutscene = False
    inThirdCutscene = True
    inFourthCutscene = False
    cutscenesComplete = False
    textCounter = 0
    shopActive = False
    playerUsedShop = False
    level = 1
    musicPlaying = False
    
    # Player setup
    player = Player(1114, 915, 50, 50, 1, 0, 0)
    
    # User interface setup
    UI = UserInterface(player)
    
    # enemy image
    boss = Enemy(1000, 800, 50, 4, 50, "Images/zombie.jpg")
    bossArray = []
    bossArray.append(boss)

    # Music / Sounds
    # Player Sounds
    playerWalk = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/12_Player_Movement_SFX/08_Step_rock_02.wav")
    playerAttack = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/12_Player_Movement_SFX/56_Attack_03.wav")

    # Shop and Inventory Sounds
    purchase = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/079_Buy_sell_01.wav")
    purchaseDenied = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/033_Denied_03.wav")
    itemUsed = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/051_use_item_01.wav")
  
    # Misc. Sounds
    dialogue = pygame.mixer.Sound("Sounds/8_bit_16_bit_Sound_Effects/Text 1.wav")
    coinCollect = pygame.mixer.Sound("Sounds/RPG_Essentials_Free/10_UI_Menu_SFX/013_Confirm_03.wav")
  
    # Loads map images to be displayed on the screen
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
    boundaryLeft = 514
    boundaryRight = 1770 - player.width
    boundaryTop = 483
    boundaryBottom = 1445 - player.height

    # Default coordinate values for the 'camera'
    camera_x, camera_y = 0, 0

    # Set up variables for player health, strength and combat
    playerHealth = 50  # Initial health of the player
    playerStrength = 1 # Initial strength of the player
    enemyAttackCooldown = 3000  # Cooldown for enemy attacks
    enemyCoins = []
    lastEnemyAttack = pygame.time.get_ticks()
    lastWaveTime = pygame.time.get_ticks()
    waveInterval = 32500
    # 'Starts' the game in a loop
    while running:
        # Sets up the music that will play for each level of the game
        if level == 1 and musicPlaying == False:
          pygame.mixer.music.stop()
          pygame.mixer.music.load('Sounds/dont_need_a_hero_sfx_and_musics/theme_foret.mp3')
          pygame.mixer.music.set_volume(0.1)
          pygame.mixer.music.play(-1)
          musicPlaying = True
        elif level == 2 and musicPlaying == False:
          pygame.mixer.music.stop()
          pygame.mixer.music.load('Sounds/dont_need_a_hero_sfx_and_musics/theme_ruine.mp3')
          pygame.mixer.music.set_volume(0.1)
          pygame.mixer.music.play(-1)
          musicPlaying = True
        
        # Variable to track the player's score    
        playerScore = player.score
        
        # Starts building the map
        currentTime = pygame.time.get_ticks()
        screen.fill((0, 0, 0))
        screen.blit(ground, (0 - camera_x, 0 - camera_y))
        screen.blit(dungeon, (0 - camera_x, 0 - camera_y))
        if level == 1:
          # Animations for the shopkeeper will play on this 'layer'
          skCurrentTime = pygame.time.get_ticks()
          if skCurrentTime - skLastUpdate >= animationCooldown:
            skFrame += 1
            skLastUpdate = skCurrentTime
            if skFrame >= len(skAnimationList[skAction]):
              skFrame = 0

          if skFrame < 0 or skFrame >= len(skAnimationList[skAction]):
            skFrame = 0  # Set the default frame if it's out of range
          
          skAction = 0
          
          # Shopkeeper with animations is put onto the screen alongside the shop
          screen.blit(skAnimationList[skAction][skFrame],(634 - camera_x, 538 - camera_y))
          screen.blit(shop, (0 - camera_x, 0 - camera_y))

        # Used to track the current key that is being pressed by the player 
        key = pygame.key.get_pressed()

        # Save the current position for boundary checking
        player_x, player_y = player.x, player.y

        # Animations for the player, constantly updates the frame of the animation so it gives the illusion of movement based upon the action the player is doing
        currentTime = pygame.time.get_ticks()
        if currentTime - lastUpdate >= animationCooldown:
          frame += 1
          lastUpdate = currentTime
          if frame >= len(animationList[action]):
            frame = 0

        if frame < 0 or frame >= len(animationList[action]):
          frame = 0  # Set the default frame if it's out of range

        # Player animations put onto the screen
        screen.blit(animationList[action][frame],(362, 312))

        # Enemy spawning and combat rules. They start spawning once the player has finished talking to the shopkeeper and combat is done through checking collisions between the enemy instance and player
        if playerUsedShop == True:
          if enemies:
            for enemy in enemies:
              # Moves the enemy towards the player and renders them on screen
              directionToGo = enemy.moveTowardsPlayer(player, camera_x, camera_y, level)
              enemy.render(screen, camera_x, camera_y, action, level)
              # Check for player-enemy collision and update health
              if (
                  player.x < enemy.map_x + enemy.size
                  and player.x + player.width > enemy.map_x
                  and player.y < enemy.map_y + enemy.size
                  and player.y + player.height > enemy.map_y
                  and action == 8  # Check if the player is attacking
              ):
                  enemy.health -= playerStrength  # Decrease enemy health on collision
                  if enemy.health <= 0:
                      enemies.remove(enemy)  # Remove enemy instance if health reaches 0
                      player.score += 10  # Increase player score for killing an enemy
                      # Spawns in a random amount of coins between 1 and 5 when the enemy is defeated
                      coinAmount = random.randint(1, 5)
                      for i in range(coinAmount):
                        coin = Coin(1, "Images/Items/coin.png", position=(enemy.map_x + random.randint(1,10), enemy.map_y + random.randint(1, 10)))
                        enemyCoins.append(coin)

              # Check for enemy-player collision and update health
              currentTime = pygame.time.get_ticks()
              if (
                  player.x < enemy.map_x + enemy.size
                  and player.x + player.width > enemy.map_x
                  and player.y < enemy.map_y + enemy.size
                  and player.y + player.height > enemy.map_y
                  and currentTime - lastEnemyAttack >= enemyAttackCooldown
              ):
                  playerHealth -= 5  # Decrease player health on collision
                  lastEnemyAttack = currentTime
          else:
            # Tracks the time before the next wave should spawn in once the last wave has been defeated
            nextWaveSpawn = waveInterval - (currentTime - lastWaveTime - 10000)
            # Spawns in the wave if it's time
            if nextWaveSpawn <= 0:
              enemies = enemyWave(Enemy, player, camera_x, camera_y)
              # Removes the 'walls' from the map
              spawnerWalls_visible = False
              lastWaveTime = currentTime
        
        for coin in enemyCoins:
          # Checks if the coordinates of the player and coin instance are overlapping
          if (
              player.x < coin.rect.x + coin.rect.width
              and player.x + player.width > coin.rect.x
              and player.y < coin.rect.y + coin.rect.height
              and player.y + player.height > coin.rect.y
          ):
            # If the player picked up the coin, add its value to the coin counter
            player.coins += coin.value
            # Remove the coin from the array
            enemyCoins.remove(coin)
            # Plays a coin collected sound
            coinCollect.play()
            coinCollect.set_volume(0.4)
          # Updates and renders the coins on the screen
          coin.update()
          coin.render(screen, camera_x, camera_y)

        # Builds the rest of the map
        if level == 1:
          screen.blit(bushesStumps, (0 - camera_x, 0 - camera_y))
        screen.blit(shopFence, (0 - camera_x, 0 - camera_y))
        screen.blit(trees, (0 - camera_x, 0 - camera_y))
        screen.blit(rocksBoxes, (0 - camera_x, 0 - camera_y))
        if spawnerWalls_visible:
          screen.blit(spawnerWalls, (0 - camera_x, 0 - camera_y))
        
        ## Cutscenes that will play throughout the game as the player progresses
        # Tracking the mouse position
        cutscenemx, cutscenemy = pygame.mouse.get_pos()
        # First 'cutscene'
        if inFirstCutscene == True:
          # Sets the variable of inCutscene to 'True' and starts the dialogue. Displays text of dialogue and gives the player a button they can click to progress the cutscene
          inCutscene = True
          chat()
          continueButton = pygame.Rect(500, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), continueButton)
          drawText('Continue', smallFont, (255, 255, 255), screen, 522, 100)
          
          # Array of text used for the cutscene
          cutsceneText = ["This is Frank.", "", "He's currently stuck in the middle of a forest, searching", "for a 'long lost treasure' after hearing some whispers about it.", "They led him right here. Surely after all of this travelling,", "the treasure must be closeby now.", "", ""]
          
          # Displays character, button and text
          screen.blit(animationList[action][frame],(666, 60))

          drawText(cutsceneText[textCounter], smallFont, (255, 255, 255), screen, 24, 30)

          drawText(cutsceneText[textCounter+1], smallFont, (255, 255, 255), screen, 24, 50)

          if continueButton.collidepoint((cutscenemx, cutscenemy)):
            pygame.draw.rect(screen, (60, 40, 150), continueButton, 2)
          
          # Stops the cutscene when all text has been seen
          if textCounter > 4:
            inFirstCutscene = False
            inCutscene = False
            textCounter = 0

        # Second 'cutscene'
        if inSecondCutscene == True:
          # Sets the variable of inCutscene to 'True' and starts the dialogue. Displays text of dialogue and gives the player a button they can click to progress the cutscene
          inCutscene = True
          chat()
          continueButton = pygame.Rect(500, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), continueButton)
          drawText('Continue', smallFont, (255, 255, 255), screen, 522, 100)
          
          # Array of text used for the cutscene
          cutsceneText = ["Hey there! Strange seeing someone around here for once...", "Who might you be?", "Frank.", "", "Hi Frank, I'm Sven. I've been running this shop round here for", "many years...","I suppose you're looking for the treasure, huh?", "", "Yes.", "", "Well, I have just the thing for you! Here in stock, I have the key", "to the dungeon where the treasure is kept!", "However, as the treasure has never actually been found, I do", "require a deposit on the key.", "... Why can't you just go into the dungeon yourself if you have", "the key?", "Well, you see.. I'm stuck in place. I don't have movement animations.", "Also I'm safe in my little stall, no monsters can get me from in here.","Oh yeah, the monsters. Hoards of them like to roam around and", "attack anyone they can find.", "The walls only stay up for so long unfortunately, then they'll", "keep coming in waves..", "Please note, you are only capable of having probably about 4", "strength potions before they stop working.", "Anyway! Have fun, come back to me if you want to purchase", "any items :)", "", ""]
          
          # Displays character, button and text
          if textCounter == 2 or textCounter == 8 or textCounter == 14:
            screen.blit(animationList[0][frame],(666, 60))
          else:
            screen.blit(skAnimationList[skAction][skFrame],(682, 60))

          drawText(cutsceneText[textCounter], smallFont, (255, 255, 255), screen, 24, 30)

          drawText(cutsceneText[textCounter+1], smallFont, (255, 255, 255), screen, 24, 50)

          if continueButton.collidepoint((cutscenemx, cutscenemy)):
            pygame.draw.rect(screen, (60, 40, 150), continueButton, 2)

          # Stops the cutscene when all text has been seen
          if textCounter > 24:
            inSecondCutscene = False
            inCutscene = False
            playerUsedShop = True
            textCounter = 0

        # Third 'cutscene'
        # Sets the variable of inCutscene to 'True' and starts the dialogue. Displays text of dialogue and gives the player a button they can click to progress the cutscene
        if inThirdCutscene == True and level == 2:
          inCutscene = True
          chat()
          continueButton = pygame.Rect(500, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), continueButton)
          drawText('Continue', smallFont, (255, 255, 255), screen, 522, 100)
          
          # Array of text used for the cutscene
          cutsceneText = ["Well this is spacious...", "Now, where's that treasure?", "HALT! Stop right there!", "You are NOT getting my treasure", "Oh really?", "", "Save the chat, intruder.", "Prepare to be taken out.", "", ""]

          # Displays character, button and text
          if textCounter == 0 or textCounter == 4:
            screen.blit(animationList[0][frame],(666, 60))
          else:
            drawText("?", titleFont, (255, 255, 255), screen, 706, 76)

          drawText(cutsceneText[textCounter], smallFont, (255, 255, 255), screen, 24, 30)

          drawText(cutsceneText[textCounter+1], smallFont, (255, 255, 255), screen, 24, 50)

          if continueButton.collidepoint((cutscenemx, cutscenemy)):
            pygame.draw.rect(screen, (60, 40, 150), continueButton, 2)

          # Stops the cutscene when all text has been seen
          if textCounter > 6:
            inThirdCutscene = False
            inCutscene = False
            textCounter = 0

        # Fourth 'cutscene'
        # Sets the variable of inCutscene to 'True' and starts the dialogue. Displays text of dialogue and gives the player a button they can click to progress the cutscene
        if inFourthCutscene == True and level == 2:
          inCutscene = True
          chat()
          continueButton = pygame.Rect(500, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), continueButton)
          drawText('Continue', smallFont, (255, 255, 255), screen, 522, 100)
          
          # Array of text used for the cutscene
          cutsceneText = ["The treasure is mine!!", "Now, how do I get out of here?", "Seems like the plan didn't work this time...", "", "I will avenge you, Steven...", "","To be continued...?", "", "", ""]

          # Displays character, button and text
          if textCounter == 0:
            screen.blit(animationList[action][frame],(666, 60))
          elif textCounter == 2:
            screen.blit(skAnimationList[skAction][skFrame],(682, 60))
          elif textCounter == 4:
            screen.blit(skAnimationList[4][0],(682, 60))
          else:
            drawText("?", titleFont, (255, 255, 255), screen, 706, 76)
            
          drawText(cutsceneText[textCounter], smallFont, (255, 255, 255), screen, 24, 30)

          drawText(cutsceneText[textCounter+1], smallFont, (255, 255, 255), screen, 24, 50)

          if continueButton.collidepoint((cutscenemx, cutscenemy)):
            pygame.draw.rect(screen, (60, 40, 150), continueButton, 2)
          
          # Stops the cutscene when all text has been seen
          if textCounter > 6:
            inFourthCutscene = False
            cutscenesComplete = True
            inCutscene = False
            textCounter = 0
        
        # Stops player movement if they are in a cutscene
        if inCutscene != True:
          # If the player is pressing a movement key and within the map boundaries, they will move the way they intend to and do the correlating action
          if key[pygame.K_a] == True and player.x > boundaryLeft:
              action = 6
              player.x -= 6
          elif key[pygame.K_d] == True and player.x < boundaryRight:
              action = 5
              player.x += 6
          elif key[pygame.K_w] == True and player.y > boundaryTop:
              action = 7
              player.y -= 6
          elif key[pygame.K_s] == True and player.y < boundaryBottom:
              action = 4
              player.y += 6
          elif key[pygame.K_SPACE] == True:
              action = 8
          else:
            action=0
                    
        # Shop system
        # Calculate the distance between the shop and the player
        shopDistanceX = player.x - 550
        shopDistanceY = player.y - 600
        shopDistance = (shopDistanceX ** 2 + shopDistanceY ** 2) ** 0.5
        # If the player gets within radius and is in the first level, this will activate the shop and the cutscene (if it is the player's first time interacting with the shop)
        if shopDistance < 108 and level == 1:
              action = 3
              if playerUsedShop == False:
                inSecondCutscene = True
              else:  
                shopActive = True
                playerUsedShop = True
        else:
              shopActive = False

        #Shop system
        if shopActive == True:
          # Shop setup with the dialogue UI, shopkeeper animation and text
          chat()
          screen.blit(skAnimationList[skAction][skFrame],(682, 60))

          drawText('Here to purchase an item? Health potions are 10 coins, strength', smallFont, (255, 255, 255), screen, 24, 30)

          drawText('potions are 20 coins and the key is 100 coins.', smallFont, (255, 255, 255), screen, 24, 50)

          # Buttons to purchase items
          healthPotionButton = pygame.Rect(20, 90, 180, 40)
          pygame.draw.rect(screen, (30, 0, 120), healthPotionButton)
          drawText('Buy Health Potion', smallFont, (255, 255, 255), screen, 34, 100)

          strengthPotionButton = pygame.Rect(210, 90, 200, 40)
          pygame.draw.rect(screen, (30, 10, 120), strengthPotionButton)
          drawText('Buy Strength Potion', smallFont, (255, 255, 255), screen, 223, 100)

          keyButton = pygame.Rect(420, 90, 120, 40)
          pygame.draw.rect(screen, (30, 20, 120), keyButton)
          drawText('Buy Key', smallFont, (255, 255, 255), screen, 446, 100)

          # Uses the mouse position to check if the player is hovering over the shop item
          shopmx, shopmy = pygame.mouse.get_pos()
          if healthPotionButton.collidepoint((shopmx, shopmy)):
            pygame.draw.rect(screen, (60, 40, 150), healthPotionButton, 2)

          if strengthPotionButton.collidepoint((shopmx, shopmy)):
              pygame.draw.rect(screen, (60, 40, 150), strengthPotionButton, 2)
               
          if keyButton.collidepoint((shopmx, shopmy)):
            pygame.draw.rect(screen, (60, 40, 150), keyButton, 2)

        # Text on top of every image layer so it's visible to the player. It lets them know a wave is spawning soon
        nextWaveSpawn = waveInterval - (currentTime - lastWaveTime - 10000)
        if level == 1 and 0 < nextWaveSpawn <= 6000:
          drawText('Enemy wave spawning soon!', boldFont, (0, 0, 0), screen, 180, 542)
          drawText('Enemy wave spawning soon!', boldFont, (255, 255, 255), screen, 178, 540)
          
        # Level 2 trigger
        for slot in UI.inventory.slots:
          if slot.item and slot.item.name == "Key" and slot.count > 0 and (1450 < player.x < 1620 and 1370 < player.y < 1400):
            level = 2
            slot.count = 0
            musicPlaying = False
            enemyCoins = []

        # Start of the second level (or dungeon)
        if level == 2:
          # Resets the enemy array to remove previous enemies and sets the playerUsedShop boolean to 'False' so enemies stop spawning
          enemies = []
          playerUsedShop = False
          
          # Replaces map images with the dungeon ones
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

          # If all cutscenes have been viewed and no more coins are present on the map, the game ends and the player wins
          if cutscenesComplete == True and len(enemyCoins) == 0:
            gameComplete(playerScore)

          # If the player has defeated the boss then they will be presented with the fourth "cutscene"
          if complete == True:
            action = 0
            inFourthCutscene = True
            
          # Start of the boss battle
          if inThirdCutscene == False and boss.health > 0:
            # Moves the boss towards the player and renders them on screen
            boss.moveTowardsPlayer(player, camera_x, camera_y, level)
            boss.render(screen, camera_x, camera_y, action, level)
            
            # Update health bar position with respect to the boss
            boss_health_bar_x = boss.map_x - camera_x + 54 
            boss_health_bar_y = boss.map_y - camera_y + 18
            
            # Draw the boss' health bar on the screen
            drawHealthBar(screen, boss_health_bar_x, boss_health_bar_y, boss.health)
  
            # Boss combat rules
            if (
              player.x < boss.map_x + boss.size
              and player.x + player.width > boss.map_x
              and player.y < boss.map_y + boss.size
              and player.y + player.height > boss.map_y
              and action == 8  # Check if the player is attacking
            ):
              boss.health -= playerStrength  # Decrease boss health on collision
              
              if boss.health <= 0:
                  bossArray.remove(boss)
                  player.score += 100  # Increase player score for killing the boss
                  player.score = round(player.score * (1+(playerHealth/50))) # Multiplies the player's score by a fraction of their health worth to give them a 'score boost'
                  # Spawns in 500 coins as the 'treasure' and sets complete to 'True'
                  coinAmount = 500
                  for i in range(coinAmount):
                    coin = Coin(1, "Images/Items/coin.png",(boss.map_x + random.randint(20,40), boss.map_y + random.randint(20, 40)))
                    enemyCoins.append(coin)
                  complete = True
                                
            # Check for enemy-player collision and update health
            currentTime = pygame.time.get_ticks()
            enemyAttackCooldown = 8000  # Cooldown for boss attacks
            if (
              player.x < boss.map_x + boss.size
              and player.x + player.width > boss.map_x
              and player.y < boss.map_y + boss.size
              and player.y + player.height > boss.map_y
              and currentTime - lastEnemyAttack >= enemyAttackCooldown
            ):
              playerHealth -= 15  # Decrease player health on collision
              lastEnemyAttack = currentTime  # Update last attack time
  
            for coin in enemyCoins:
            # Checks if the coordinates of the player and coin instance are overlapping
              if (
                player.x < coin.rect.x + coin.rect.width
                and player.x + player.width > coin.rect.x
                and player.y < coin.rect.y + coin.rect.height
                and player.y + player.height > coin.rect.y
              ):
                # If the player picked up the coin, add its value to the coin counter
                player.coins += coin.value
                # Remove the coin from the array
                enemyCoins.remove(coin)
              # Updates and renders the coins on the screen
              coin.update()
              coin.render(screen, camera_x, camera_y)

        # Adjust the camera position to follow the player
        camera_x = player.x - (screen.get_width() // 2)
        camera_y = player.y - (screen.get_height() // 2)

        # Update health bar position with respect to the player
        health_bar_x = player.x - camera_x - 13
        health_bar_y = player.y - camera_y - 13

        # Draw the player's health bar
        drawHealthBar(screen, health_bar_x, health_bar_y, playerHealth)

        # If the player's health goes to 0 and the player restarts, these values replace the previous ones so the next run isn't affected
        if playerHealth <= 0:
          if gameOver(playerScore):
              # Reset game state for a new try
              playerHealth = 50
              playerStrength = 1
          else:
              # Player chose to quit or go back to the main menu
              break
            
        # Game loop
        for event in pygame.event.get():
          # 'Cutscene' continue
          if continueButton.collidepoint(cutscenemx, cutscenemy) and inCutscene == True and event.type == MOUSEBUTTONDOWN:
              # Plays a dialogue noise and adds to the textCounter variable
              dialogue.play()
              dialogue.set_volume(0.4)
              textCounter = textCounter + 2
          # Inventory system
          if UI.inventoryRender:
            inventorymx, inventorymy = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN: # Left mouse button clicked
              for slot in UI.inventory.slots:
                if slot.rect.collidepoint((inventorymx, inventorymy)):
                  # Uses the currently selected item if player has a count of them. Applies the intended effect depending on the item used and plays a sound
                    if slot.item and slot.item.name == "Health Potion" and playerHealth < 50 and slot.count > 0:
                      slot.count -= 1
                      if playerHealth < 35:
                        playerHealth += 15
                      else:
                        playerHealth = playerHealth + (50 - playerHealth)
                      itemUsed.play()
                      itemUsed.set_volume(0.4)
                      
                    if slot.item and slot.item.name == "Strength Potion" and playerStrength < 5 and slot.count > 0 and slot.count < 5:
                      slot.count -= 1
                      playerStrength += 1
                      itemUsed.play()
                      itemUsed.set_volume(0.4)
          
          # Shop system
          if shopActive == True:
            # Checks if the health potion button is being clicked and, if the player has enough coins, adds the item to the player's inventory. Plays a sound correlating to if they can afford the item or not
            if healthPotionButton.collidepoint((shopmx, shopmy)) and event.type == MOUSEBUTTONDOWN: # Left mouse button clicked
              if player.coins >= 10:
                purchase.play()
                purchase.set_volume(0.4)
                player.coins -= 10
                
                for slot in UI.inventory.slots:
                  if slot.item and slot.item.name == "Health Potion":
                      slot.count += 1
                      break
              else:
                purchaseDenied.play()
                purchaseDenied.set_volume(0.4)
            
            # Checks if the strength potion button is being clicked and, if the player has enough coins, adds the item to the player's inventory. Plays a sound correlating to if they can afford the item or not
            if strengthPotionButton.collidepoint((shopmx, shopmy)) and event.type == MOUSEBUTTONDOWN: # Left mouse button clicked
              if player.coins >= 20:
                purchase.play()
                purchase.set_volume(0.4)
                player.coins -= 20

                for slot in UI.inventory.slots:
                    if slot.item and slot.item.name == "Strength Potion":
                        slot.count += 1
                        break
              else:
                purchaseDenied.play()
                purchaseDenied.set_volume(0.4)
                  
            # Checks if the key button is being clicked and, if the player has enough coins, adds the item to the player's inventory. Plays a sound correlating to if they can afford the item or not
            if keyButton.collidepoint((shopmx, shopmy)) and event.type == MOUSEBUTTONDOWN: # Left mouse button clicked
              if player.coins >= 100 and hasKey == False:
                purchase.play()
                purchase.set_volume(0.4)
                player.coins -= 100
                UI.inventory.slots.append(InventorySlot("Key", "Images/Items/key.png", (417, 176)))
                
                for slot in UI.inventory.slots:
                    if slot.item and slot.item.name == "Key":
                        hasKey = True
                        slot.count += 1
                        break
              else:
                purchaseDenied.play()
                purchaseDenied.set_volume(0.4)
                
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          # Plays sounds depending upon the key that the player presses
          if event.type == KEYDOWN:
              if event.key == K_ESCAPE:
                running = False
              if event.key == K_e:
                UI.toggleInventory()
              if event.key == K_w:
                playerWalk.play()
                playerWalk.set_volume(0.4)
              elif event.key == K_a:
                playerWalk.play()
                playerWalk.set_volume(0.4)
              elif event.key == K_s:
                playerWalk.play()
                playerWalk.set_volume(0.4)
              elif event.key == K_d:
                playerWalk.play()
                playerWalk.set_volume(0.4)
              elif event.key == K_SPACE:
                playerAttack.play()
                playerAttack.set_volume(0.4)
          # Checks if the mouse is being clicked
          if event.type == MOUSEBUTTONDOWN:
              if event.button == 1:
                click = True
          if event.type == MOUSEMOTION:  # Handle mouse movement
            mouse_pos = pygame.mouse.get_pos()  # Get the x and y coordinates of the mouse position

        # Renders the user interface above everything
        UI.render(screen, mouse_pos)
        pygame.display.update()
        mainClock.tick(60)

# Function that displays the game controls to the player
def controls(mx,my, lastUpdate, frame, action):
    running = True
    viewInventory = False
    while running:
        # Background image and text displayed on screen
        screen.blit(pygame.image.load('Images/screen bg.png'), (0,0))

        drawText('CONTROLS SCREEN', titleFont, (255, 255, 255), screen, 253, 70)
        drawText('UP - W', font, (255, 255, 255), screen, 275, 130)
        drawText('DOWN - S', font, (255, 255, 255), screen, 275, 170)
        drawText('LEFT - A', font, (255, 255, 255), screen, 275, 210)
        drawText('RIGHT - D', font, (255, 255, 255), screen, 275, 250)
        drawText('ATTACK - SPACEBAR', font, (255, 255, 255), screen, 275, 290)
        drawText('INVENTORY - E', font, (255, 255, 255), screen, 275, 330)
        
        drawText('PRESS "ESC" TO GO BACK', boldFont, (255, 255, 255), screen, 212, 540)

        # Displays player animations on the screen to show players how their movements will look
        currentTime = pygame.time.get_ticks()
        if currentTime - lastUpdate >= animationCooldown:
          frame += 1
          lastUpdate = currentTime
          if frame >= len(animationList[action]):
            frame = 0

        if frame < 0 or frame >= len(animationList[action]):
          frame = 0  # Set the default frame if it's out of range
          
        screen.blit(animationList[action][frame],(340, 360))
        
        # Retrieves the key that the player is pressing and uses that to decide the animation action to display
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
        else:
          action=0

        if viewInventory == True:
          inventory = pygame.image.load("Images/Inventory.png")
          inventory = pygame.transform.scale(inventory, (160, 188))
          screen.blit(inventory, (306, 354))

        # Event loop that tracks when the "x" button or the esc key is clicked
        for event in pygame.event.get():
          if event.type == QUIT:
            pygame.quit()
            sys.exit()
          if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
              running = False
            if event.key == K_e:
              viewInventory = not viewInventory

        pygame.display.update()
        mainClock.tick(60)

# Runs the main menu function so it is the first screen the user sees
mainMenu()