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
                player_image = pygame.transform.scale(player_image, (40, 40))

                background = pygame.image.load('Images/Rough Draft Design.png')
                background = pygame.transform.scale(background, (2400, 1920))

                # Set up boundaries
                boundary_left = 0
                boundary_right = 1600 - player.width
                boundary_top = 0
                boundary_bottom = 1280 - player.height

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