import pygame, sys

# Setting up the environment to initialize pygame
mainClock = pygame.time.Clock()
from pygame.locals import *
from UserInterface import UserInterface
pygame.init()
pygame.display.set_caption('The Whispers')
screen = pygame.display.set_mode((800, 640),0,0)

# Setting up the font that will be used
font = pygame.font.SysFont(None, 30)

#UI
UI = UserInterface()

# Setting up the player (x location, y location, width, height)
player = pygame.Rect((1170, 915, 50, 50))

# Health bar variables
player_health = 100
health_bar_length = 50
health_bar_height = 10
health_bar_color = (0, 255, 0)
health_bar_outline_color = (0, 0, 0)

# Function to write text on the screen and buttons
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# A variable to check for the status later
click = False

# Function to draw the health bar
def draw_health_bar(surface, x, y, health):
    if health < 0:
        health = 0
    pygame.draw.rect(surface, health_bar_color, (x, y, health, health_bar_height))
    pygame.draw.rect(surface, health_bar_outline_color, (x, y, health_bar_length, health_bar_height), 2)

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
    running = True
    player_image = pygame.image.load('player_image.png')
    player_image = pygame.transform.scale(player_image, (40, 40))

    background = pygame.image.load('Images/Rough Draft Design.png')
    background = pygame.transform.scale(background, (2400, 1920))

    # Set up boundaries
    boundary_left = 401
    boundary_right = 2010 - player.width
    boundary_top = 321
    boundary_bottom = 1607 - player.height

    camera_x, camera_y = 0, 0

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0 - camera_x, 0 - camera_y))
        screen.blit(player_image, (player.x - camera_x, player.y - camera_y))

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
