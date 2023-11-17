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
screen = pygame.display.set_mode((600, 300),0,32)

#Setting up the font that will be used
font = pygame.font.SysFont(None, 30)

#Setting up the player
player = pygame.Rect((300, 250, 50, 50))

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
    while running:
        screen.fill((0,0,0))
        # 'Draws' the box for the player sprite
        pygame.draw.rect(screen, (255, 0, 0), player)
        # Gets the key that has been pressed
        key = pygame.key.get_pressed()
        # Depending on the key that has been pressed, the box moves that way
        if key[pygame.K_a] == True:
          player.move_ip(-1,0)
        elif key[pygame.K_d] == True:
          player.move_ip(1,0)
        elif key[pygame.K_w] == True:
          player.move_ip(0,-1)
        elif key[pygame.K_s] == True:
          player.move_ip(0,1)

        # Game loop ?
        draw_text('GAME SCREEN', font, (255,255 ,255 ), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            # Set up controls

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

