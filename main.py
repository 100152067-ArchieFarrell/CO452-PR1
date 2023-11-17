"""
Importing important libraries
"""
import pygame, sys

"""
Setting up an environment to initialize pygame
"""
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((800, 640),0,0)

#Setting up the font that will be used
font = pygame.font.SysFont(None, 30)

#Setting up the player
player = pygame.Rect((370, 300, 50, 50))

"""
A function that can be used to write text on our screen and buttons
"""
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
        draw_text('Main Menu', font, (0,0,0), screen, 250, 40)

        mx, my = pygame.mouse.get_pos()

        #Creates the buttons on the screen
        button_1 = pygame.Rect(200, 100, 200, 50)
        button_2 = pygame.Rect(200, 180, 200, 50)

        #Funtions that will be run when a certain button is clicked
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                controls()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        #Text that will be displayed on the buttons
        draw_text('PLAY', font, (255,255,255), screen, 270, 115)
        draw_text('CONTROLS', font, (255,255,255), screen, 240, 195)

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

"""
This function is called when the "PLAY" button is clicked.
"""
def game():
            running = True
            player_image = pygame.image.load('player_image.png')
  #Size of the player
            player_image = pygame.transform.scale(player_image, (40, 40))

            camera_x, camera_y = 0, 0

            while running:
                screen.fill((0, 0, 0))
                # Loads the background for the game
                screen.blit(pygame.image.load('Images/Rough Draft Design.png'), (50 - camera_x, 50 - camera_y))

                # Draw the player at the relative position on the screen
                screen.blit(player_image, (player.x - camera_x, player.y - camera_y))

                # Gets the key that has been pressed
                key = pygame.key.get_pressed()

                # Depending on the key that has been pressed, the player moves that way
                if key[pygame.K_a] == True:
                    player.move_ip(-5, 0)
                elif key[pygame.K_d] == True:
                    player.move_ip(5, 0)
                elif key[pygame.K_w] == True:
                    player.move_ip(0, -5)
                elif key[pygame.K_s] == True:
                    player.move_ip(0, 5)

                # Adjust the camera position to follow the player
                camera_x = player.x - (screen.get_width() // 2)
                camera_y = player.y - (screen.get_height() // 2)

                # Game loop
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False

                pygame.display.update()
                mainClock.tick(60)




#This function is called when the "Controls" button is clicked.

def controls():
    running = True
    while running:
        screen.fill((0,190,255))

        draw_text('CONTROLS SCREEN', font, (255, 255, 255), screen, 200, 20)
        draw_text('UP - W', font, (255, 255, 255), screen, 260, 100)
        draw_text('DOWN - S', font, (255, 255, 255), screen, 260, 120)
        draw_text('LEFT - A', font, (255, 255, 255), screen, 260, 140)
        draw_text('RIGHT - D', font, (255, 255, 255), screen, 260, 160)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)



main_menu()

