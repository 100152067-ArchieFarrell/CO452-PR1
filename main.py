import pygame, sys
from pygame.locals import *
from UserInterface import UserInterface
from healthBar import *

# Setting up the environment to initialize pygame
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('The Whispers')
screen = pygame.display.set_mode((800, 640),0,0)

# Setting up the font that will be used
font = pygame.font.SysFont(None, 30)

#UI
UI = UserInterface()

# Setting up the player (x location, y location, width, height)
player = pygame.Rect((1114, 915, 50, 50))

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
    while True:
        screen.fill((0,190,255))
        draw_text('Main Menu', font, (0,0,0), screen, 350, 250)

        mx, my = pygame.mouse.get_pos()

        # Creates the buttons on the screen
        button_1 = pygame.Rect(300, 280, 200, 50)
        button_2 = pygame.Rect(300, 340, 200, 50)

        # Functions that will be run when a certain button is clicked
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                controls()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        # Text that will be displayed on the buttons
        draw_text('PLAY', font, (255,255,255), screen, 376, 298)
        draw_text('CONTROLS', font, (255,255,255), screen, 343, 358)

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

# This function is called when the "PLAY" button is clicked.
def game():
    # sets the running state of the game to "true"
    running = True
    # loads the default image for the game's character
    player_image = pygame.image.load('Images/frank.png')
    player_image = pygame.transform.scale(player_image, (26, 42))

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

    # Set up boundaries
    boundary_left = 501
    boundary_right = 1770 - player.width
    boundary_top = 483
    boundary_bottom = 1445 - player.height

    camera_x, camera_y = 0, 0

    while running:
        screen.fill((0, 0, 0))
        screen.blit(ground, (0 - camera_x, 0 - camera_y))
        screen.blit(dungeon, (0 - camera_x, 0 - camera_y))
        screen.blit(shop, (0 - camera_x, 0 - camera_y))
        screen.blit(player_image, (player.x - camera_x, player.y - camera_y))
        screen.blit(bushesStumps, (0 - camera_x, 0 - camera_y))
        screen.blit(shopFence, (0 - camera_x, 0 - camera_y))
        screen.blit(trees, (0 - camera_x, 0 - camera_y))
        screen.blit(rocksBoxes, (0 - camera_x, 0 - camera_y))
        screen.blit(spawnerWalls, (0 - camera_x, 0 - camera_y))

        key = pygame.key.get_pressed()

        # Save the current position for boundary checking
        player_x, player_y = player.x, player.y

        if key[pygame.K_a] == True and player.x > boundary_left:
            player.move_ip(-8, 0)
        elif key[pygame.K_d] == True and player.x < boundary_right:
            player.move_ip(8, 0)
        elif key[pygame.K_w] == True and player.y > boundary_top:
            player.move_ip(0, -8)
        elif key[pygame.K_s] == True and player.y < boundary_bottom:
            player.move_ip(0, 8)
        elif key[pygame.K_e] == True:
          UI.toggleInventory()

        # Adjust the camera position to follow the player
        camera_x = player.x - (screen.get_width() // 2)
        camera_y = player.y - (screen.get_height() // 2)

        # Update health bar position with respect to the player
        health_bar_x = player.x - camera_x
        health_bar_y = player.y - camera_y - 20

        # Draw the health bar
        draw_health_bar(screen, health_bar_x, health_bar_y, player_health)

        # Game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        UI.render(screen)
        pygame.display.update()
        mainClock.tick(60)

# This function is called when the "Controls" button is clicked.
def controls():
    running = True
    while running:
        screen.fill((0,190,255))

        draw_text('CONTROLS SCREEN', font, (255, 255, 255), screen, 300, 20)
        draw_text('UP - W', font, (255, 255, 255), screen, 352, 100)
        draw_text('DOWN - S', font, (255, 255, 255), screen, 352, 120)
        draw_text('LEFT - A', font, (255, 255, 255), screen, 352, 140)
        draw_text('RIGHT - D', font, (255, 255, 255), screen, 352, 160)
        for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          if event.type == KEYDOWN:
              if event.key == K_ESCAPE:
                  running = False

        pygame.screen.update()
        mainClock.tick(60)

main_menu()