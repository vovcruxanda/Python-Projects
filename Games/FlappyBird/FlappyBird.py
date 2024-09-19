import random
import sys
import pygame
from pygame.locals import *

# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT * 0.8

# Initialize Pygame screen
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Flappy Bird')

# Game Sprites and Sounds
GAME_SPRITES = {}
GAME_SOUNDS = {}

# Game resources
PLAYER = 'D:/Learning&improving/Python Projects/Games/FlappyBird/img/bird.gif'
BACKGROUND = 'D:/Learning&improving/Python Projects/Games/FlappyBird/img/back3.jpg'
PIPE = 'D:/Learning&improving/Python Projects/Games/FlappyBird/img/plane.png'


def welcomeScreen():
    """
    Displays the welcome screen until the player presses a key to start the game.
    """
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    #messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    #messagey = int(SCREENHEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        #SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame():
    """
    Main game loop where the bird flies and interacts with pipes.
    """
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)
    basex = 0

    # Create 2 pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [{'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
                  {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']}]

    lowerPipes = [{'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
                  {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        # Check for collision
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        # Score check
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        # Bird movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # Move pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add new pipe
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # Remove off-screen pipes
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Blit sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        showScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    """
    Check if the player collides with a pipe or ground.
    """
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    """
    Generate random pipes for the game.
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    return [{'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]


def showScore(score):
    """
    Display the score on the screen.
    """
    myDigits = [int(x) for x in list(str(score))]
    width = 0
    for digit in myDigits:
        width += GAME_SPRITES['numbers'][digit].get_width()
    Xoffset = (SCREENWIDTH - width) / 2

    for digit in myDigits:
        SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
        Xoffset += GAME_SPRITES['numbers'][digit].get_width()


if __name__ == "__main__":
    # Initialize Pygame and load resources
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # Load game sprites and sounds
    GAME_SPRITES['numbers'] = [pygame.image.load(f'D:/Learning&improving/Python Projects/Games/FlappyBird/img/number/{i}.png').convert_alpha() for i in range(10)]
    #GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('D:/Learning&improving/Python Projects/Games/FlappyBird/img/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha())
    imageback=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['background'] = pygame.transform.scale(imageback, (289, 511))
    imageplayer = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['player'] = pygame.transform.scale(imageplayer, (105, 110))

    # Load sounds
   # GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
   # GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
   # GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')

    while True:
        welcomeScreen()  # Show welcome screen
        mainGame()  # Start the main game loop
