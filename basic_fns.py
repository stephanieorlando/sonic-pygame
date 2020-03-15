# Sound Objects

# similar mechanisms to squirrel: moving camera, playerObj, obstacleObj, soundObjs

# each sound object collided with triggers a sample in sonic pi
# objective of game is to touch enough objects to complete the composition
# while avoiding obstacles

# if obstacles are hit, this will affect the sound/params/trigger samples to stop
# trigger parameters such as sleep value/rate/amp?
# recover from obstacles and continue trying to complete composition

# to further work on:
# two different shapes/colors of obj related to two preconcieved compositions
# can eat one or both, will affect the sound that is produced
# two compositions can also work simultaneously, will contrast somehow?

import random, sys, time, math, pygame
from pygame.locals import *

FPS = 30 
WINWIDTH = 640 
WINHEIGHT = 480 
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

BGCOLOR = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CAMERASLACK = 90     
MOVERATE = 9         # how fast the player moves
INVULNTIME = 2       # how long the player is invulnerable after being hit in seconds
GAMEOVERTIME = 4     # how long the "game over" text stays on the screen in seconds
MAXHEALTH = 3        # how much health the player starts with
PLAYERSIZE = 25

NUMROCKS = 80        # number of rocks
NUMSOUNDS = 30    # number of sound objects
SOUNDMINSPEED = 3 # slowest sound speed
SOUNDMAXSPEED = 7 # fastest sound speed
DIRCHANGEFREQ = 10    # % chance of direction change per frame
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, ROCKIMG, PLAYERIMG, SOUNDIMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Sound Objects')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    # image files
    ROCKIMG = pygame.image.load('Rock.png')
    PLAYERIMG = pygame.image.load('Star.png')
    SOUNDIMG = pygame.image.load('gem1.png')

    while True:
        runGame()


def runGame():
    
    invulnerableMode = False  # if the player hits a rock
    invulnerableStartTime = 0 
    gameOverMode = False      
    gameOverStartTime = 0     
    winMode = False           

<<<<<<< Updated upstream:basic
    
    gameOverSurf = BASICFONT.render('Game Over', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    winSurf = BASICFONT.render('WIN', True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    winSurf2 = BASICFONT.render('(Press "r" to restart.)', True, WHITE)
    winRect2 = winSurf2.get_rect()
    winRect2.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 30)

    # the top left of where the camera view is
=======
    # the top left camera view
>>>>>>> Stashed changes:basic_fns.py
    camerax = 0
    cameray = 0

    rockObjs = []    
    soundObjs = [] 

    # stores the player object:
    playerObj = {'surface': PLAYERIMG,
                 'size': PLAYERSIZE,
                 'x': HALF_WINWIDTH,
                 'y': HALF_WINHEIGHT,
                 'health': MAXHEALTH}

    moveLeft  = False
    moveRight = False
    moveUp    = False
    moveDown  = False

    # start off with some random rocks on the screen
    for i in range(10):
        rockObjs.append(makeNewRocks(camerax, cameray))
        rockObjs[i]['x'] = random.randint(0, WINWIDTH)
        rockObjs[i]['y'] = random.randint(0, WINHEIGHT)

    while True: # main game loop
        
        if invulnerableMode and time.time() - invulnerableStartTime > INVULNTIME:
            invulnerableMode = False

        # move all the sounds
        for sObj in soundObjs:
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']

            # change direction
            if random.randint(0, 99) < DIRCHANGEFREQ:
                sObj['movex'] = getRandomVelocity()
                sObj['movey'] = getRandomVelocity()


        # see if need to delete objects off camera
        for i in range(len(rockObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, rockObjs[i]):
                del rockObjs[i]
        for i in range(len(soundObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, soundObjs[i]):
                del soundObjs[i]

        # add more rocks and sounds if not enough
        while len(rockObjs) < NUMROCKS:
            rockObjs.append(makeNewRocks(camerax, cameray))
        while len(soundObjs) < NUMSOUNDS:
            soundObjs.append(makeNewSounds(camerax, cameray))

        # adjust camera slack
        playerCenterx = playerObj['x'] + int(playerObj['size'] / 2)
        playerCentery = playerObj['y'] + int(playerObj['size'] / 2)
        
        if (camerax + HALF_WINWIDTH) - playerCenterx > CAMERASLACK:
            camerax = playerCenterx + CAMERASLACK - HALF_WINWIDTH
        elif playerCenterx - (camerax + HALF_WINWIDTH) > CAMERASLACK:
            camerax = playerCenterx - CAMERASLACK - HALF_WINWIDTH
        if (cameray + HALF_WINHEIGHT) - playerCentery > CAMERASLACK:
            cameray = playerCentery + CAMERASLACK - HALF_WINHEIGHT
        elif playerCentery - (cameray + HALF_WINHEIGHT) > CAMERASLACK:
            cameray = playerCentery - CAMERASLACK - HALF_WINHEIGHT

        # background
        DISPLAYSURF.fill(BGCOLOR)

        # rocks
        for rObj in rockObjs:
            rObj['rect'] = pygame.Rect( (rObj['x'] - camerax,
                                         rObj['y'] - cameray,
                                         rObj['width'],
                                         rObj['height']) )
            DISPLAYSURF.blit(ROCKIMG, rObj['rect'])


        # sound objs
        for sObj in soundObjs:
            sObj['rect'] = pygame.Rect( (sObj['x'] - camerax,
                                         sObj['y'] - cameray,
                                         sObj['width'],
                                         sObj['height']) )
            DISPLAYSURF.blit(SOUNDIMG, sObj['rect'])


        # player
        flashIsOn = round(time.time(), 1) * 10 % 2 == 1
        if not gameOverMode and not (invulnerableMode and flashIsOn):
            playerObj['rect'] = pygame.Rect( (playerObj['x'] - camerax,
                                              playerObj['y'] - cameray,
                                              playerObj['size'],
                                              playerObj['size']) )
            DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])


        # health meter
        drawHealthMeter(playerObj['health'])

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                elif winMode and event.key == K_r:
                    return

            elif event.type == KEYUP:
                # stop moving the player
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False

                elif event.key == K_ESCAPE:
                    terminate()

        if not gameOverMode:
            # move the player
            if moveLeft:
                playerObj['x'] -= MOVERATE
            if moveRight:
                playerObj['x'] += MOVERATE
            if moveUp:
                playerObj['y'] -= MOVERATE
            if moveDown:
                playerObj['y'] += MOVERATE

            # check if the player has collided with any soundobjs and delete
            for i in range(len(soundObjs) - 1, -1, -1):
                soObj = soundObjs[i]
                if 'rect' in soObj and playerObj['rect'].colliderect(soObj['rect']):
                    del soObj[i]

            # check if player has hit rock
            for i in range(len(rockObjs) - 1, -1, -1):
                roObj = rockObjs[i]
                if 'rect' in roObj and playerObj['rect'].colliderect(roObj['rect']):
                    # player takes damage
                    invulnerableMode = True
                    invulnerableStartTime = time.time()
                    playerObj['health'] -= 1
                    if playerObj['health'] == 0:
                        gameOverMode = True 
                        gameOverStartTime = time.time()
        else:
<<<<<<< Updated upstream:basic
            # show "game over" text
            DISPLAYSURF.blit(gameOverSurf, gameOverRect)
            if time.time() - gameOverStartTime > GAMEOVERTIME:
                return # end the current game

        # check if the player has won
        if winMode:
            DISPLAYSURF.blit(winSurf, winRect)
            DISPLAYSURF.blit(winSurf2, winRect2)
=======
            DISPLAYSURF.fill(WHITE)
            pygame.time.wait(1000)
            return # end the current game
>>>>>>> Stashed changes:basic_fns.py

        pygame.display.update()
        FPSCLOCK.tick(FPS)




def drawHealthMeter(currentHealth):
    for i in range(currentHealth): 
        pygame.draw.rect(DISPLAYSURF, RED,   (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
    for i in range(MAXHEALTH): 
        pygame.draw.rect(DISPLAYSURF, WHITE, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1)


def terminate():
    pygame.quit()
    sys.exit()


def getRandomVelocity():
    speed = random.randint(SOUNDMINSPEED, SOUNDMAXSPEED)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return -speed


def getRandomOffCameraPos(camerax, cameray, objWidth, objHeight):
    cameraRect = pygame.Rect(camerax, cameray, WINWIDTH, WINHEIGHT)
    while True:
        x = random.randint(camerax - WINWIDTH, camerax + (2 * WINWIDTH))
        y = random.randint(cameray - WINHEIGHT, cameray + (2 * WINHEIGHT))
        objRect = pygame.Rect(x, y, objWidth, objHeight)
        if not objRect.colliderect(cameraRect):
            return x, y


def makeNewSounds(camerax, cameray):
    so = {}
    generalSize = random.randint(5, 25)
    multiplier = random.randint(1, 3)
    so['surface'] = SOUNDIMG
    so['width']  = (generalSize + random.randint(0, 10)) * multiplier
    so['height'] = (generalSize + random.randint(0, 10)) * multiplier
    so['x'], so['y'] = getRandomOffCameraPos(camerax, cameray, so['width'], so['height'])
    so['movex'] = getRandomVelocity()
    so['movey'] = getRandomVelocity()
    return so


def makeNewRocks(camerax, cameray):
    ro = {}
    ro['surface'] = ROCKIMG
    ro['width']  = ROCKIMG.get_width()
    ro['height'] = ROCKIMG.get_height()
    ro['x'], ro['y'] = getRandomOffCameraPos(camerax, cameray, ro['width'], ro['height'])
    ro['rect'] = pygame.Rect( (ro['x'], ro['y'], ro['width'], ro['height']) )
    return ro


def isOutsideActiveArea(camerax, cameray, obj):
    boundsLeftEdge = camerax - WINWIDTH
    boundsTopEdge = cameray - WINHEIGHT
    boundsRect = pygame.Rect(boundsLeftEdge, boundsTopEdge, WINWIDTH * 3, WINHEIGHT * 3)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not boundsRect.colliderect(objRect)


if __name__ == '__main__':
    main()