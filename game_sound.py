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

# currently working on: ideal number of rocks/soundObjs and speed
# basically want it to be enough of a challenge that it's engaging
# experiment with different values for cameraslack?

# thinking of removing 'lives' instead hitting an obstacle will change a parameter and possibly trigger a sample to stop


import random, sys, time, pygame
from pygame.locals import *
from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 4560

sonic_pi = SimpleUDPClient(ip, port)

FPS = 30 
WINWIDTH = 640 
WINHEIGHT = 480 
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

BGCOLOR = (255, 255, 255, 0)
WHITE = (255, 255, 255)
PURPLE = (178, 102, 255)

CAMERASLACK = 75     
MOVERATE = 8         # how fast the player moves
INVULNTIME = 2       # how long the player is invulnerable after being hit in seconds
GAMEOVERTIME = 4     # how long the "game over" text stays on the screen in seconds
STARTSCREENTIME = 2  # how long the start instructions stay on the screen
STARTHEALTH = 3      # how much health the player starts with
MAXHEALTH = 13       # how much health to win game
PLAYERSIZE = 20

NUMROCKS = 45      # number of rocks
NUMSOUNDS = 10     # number of sound objects
SOUNDMINSPEED = 5  # slowest sound speed
SOUNDMAXSPEED = 10 # fastest sound speed

UP = 'up'
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, ROCKIMAGES, PLAYERIMG, R_PLAYERIMG, L_PLAYERIMG, SOUNDIMG, BGIMAGE

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Sounding Stars')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    # image files
    PLAYERIMG = pygame.image.load('Arrow.png')
    R_PLAYERIMG = pygame.image.load('Arrow_r.png')
    L_PLAYERIMG = pygame.transform.flip(R_PLAYERIMG, True, False)
    SOUNDIMG = pygame.image.load('Star3.png')
    SOUNDIMG = pygame.transform.smoothscale(SOUNDIMG, (85, 85))
    BGIMAGE = pygame.image.load('gradient.png')
    ROCKIMAGES = []
    for i in range(1,5):
        ROCKIMAGES.append(pygame.image.load('blackhole%s.png' % i))
    

    while True:
        runGame()


def runGame():
    
    invulnerableMode = False
    invulnerableStartTime = 0 
    gameOverMode = False      
    gameOverStartTime = 0     
    winMode = False
    startMode = True
    startTime = time.time()

    # start game screen
    startSurf = BASICFONT.render('catch the stars', True, WHITE)
    startRect = startSurf.get_rect()
    startRect.center = (HALF_WINWIDTH - 150, HALF_WINHEIGHT - 75)

    # obstacles screen
    obstSurf = BASICFONT.render('don\'t hit the black holes', True, WHITE)
    obstRect = obstSurf.get_rect()
    obstRect.center = (HALF_WINWIDTH + 50, HALF_WINHEIGHT + 50)

    # game over screen
    gameOverSurf = BASICFONT.render('try again', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    # win screen
    winSurf = BASICFONT.render('nice', True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (HALF_WINWIDTH - 150, HALF_WINHEIGHT - 75)

    # restart screen
    restartSurf = BASICFONT.render('press r to restart', True, WHITE)
    restartRect = restartSurf.get_rect()
    restartRect.center = (HALF_WINWIDTH + 50, HALF_WINHEIGHT + 50)

    # top left camera corner
    camerax = 0
    cameray = 0

    rockObjs = []    
    soundObjs = []

    # player dictionary
    playerObj = {'surface': PLAYERIMG,
                 'facing': UP,
                 'size': PLAYERSIZE,
                 'x': HALF_WINWIDTH,
                 'y': HALF_WINHEIGHT,
                 'health': STARTHEALTH}

    moveLeft  = False
    moveRight = False
    moveUp    = True
    moveDown  = False

    # start off with some random rocks on the screen
    #for i in range(10):
        #rockObjs.append(makeNewRocks(camerax, cameray))
        #rockObjs[i]['x'] = random.randint(0, WINWIDTH)
        #rockObjs[i]['y'] = random.randint(0, WINHEIGHT)

    while True: # main game loop
        
        if invulnerableMode and time.time() - invulnerableStartTime > INVULNTIME:
            invulnerableMode = False
        elif winMode:
            invulnerableMode = True

        # move all the sounds
        for sObj in soundObjs:
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']

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
        BACKGROUND = pygame.transform.smoothscale(BGIMAGE, (WINWIDTH, WINHEIGHT))
        DISPLAYSURF.blit(BACKGROUND, BGIMAGE.get_rect())

        # rocks
        for rObj in rockObjs:
            rObj['rect'] = pygame.Rect( (rObj['x'] - camerax,
                                         rObj['y'] - cameray,
                                         rObj['width'],
                                         rObj['height']) )
            DISPLAYSURF.blit(ROCKIMAGES[rObj['blackholeImage']], rObj['rect'])


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
                    moveRight = False
                    moveLeft = False
                    if playerObj['facing'] != UP: # change image UP
                        playerObj['surface'] = PLAYERIMG
                    playerObj['facing'] = UP
                #elif event.key in (K_DOWN, K_s):
                    #moveUp = False
                    #moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                    if playerObj['facing'] != LEFT: # change image L
                        playerObj['surface'] = L_PLAYERIMG
                    playerObj['facing'] = LEFT
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                    if playerObj['facing'] != RIGHT: # change image R
                        playerObj['surface'] = R_PLAYERIMG
                    playerObj['facing'] = RIGHT
                elif winMode and event.key == K_r:
                    return

            #elif event.type == KEYUP:
                # stop moving the player
                #if event.key in (K_LEFT, K_a):
                    #moveLeft = False
                #elif event.key in (K_RIGHT, K_d):
                    #moveRight = False
                #elif event.key in (K_UP, K_w):
                    #moveUp = False
                #elif event.key in (K_DOWN, K_s):
                    #moveDown = False

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
            for i in range(len(soundObjs)-1, -1, -1):
                soObj = soundObjs[i]
                if 'rect' in soObj and playerObj['rect'].colliderect(soObj['rect']):
                    del soundObjs[i]
                    if not winMode:
                        playerObj['health'] += 1

                    if playerObj['facing'] == UP:
                        playerObj['surface'] = PLAYERIMG
                    if playerObj['facing'] == LEFT:
                        playerObj['surface'] = L_PLAYERIMG
                    if playerObj['facing'] == RIGHT:
                        playerObj['surface'] = R_PLAYERIMG
                    
                    if playerObj['health'] == MAXHEALTH:
                        winMode = True

            # check if player has hit rock
            for i in range(len(rockObjs)-1, -1, -1):
                roObj = rockObjs[i]
                if 'rect' in roObj and playerObj['rect'].colliderect(roObj['rect']):
                    if not invulnerableMode:
                        # player takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        if not winMode:
                            playerObj['health'] -= 1

                        if playerObj['health'] == 0:
                            gameOverMode = True 
                            gameOverStartTime = time.time()

        else:
            # show game over screen
            DISPLAYSURF.blit(gameOverSurf, gameOverRect)
            if time.time() - gameOverStartTime > GAMEOVERTIME:
                return # end of game

        if startMode:
            DISPLAYSURF.blit(startSurf, startRect)
            DISPLAYSURF.blit(obstSurf, obstRect)

        if time.time() - startTime > STARTSCREENTIME:
            startMode = False

        if winMode:
            gameOverMode = False
            DISPLAYSURF.blit(winSurf, winRect)
            DISPLAYSURF.blit(restartSurf, restartRect)
            
        # game sound

        if playerObj['health'] >= 3:
            sonic_pi.send_message("/trigger/rtms_3", 1)
            sonic_pi.send_message("/trigger/rtms_3_1", 1)
            sonic_pi.send_message("/trigger/rtms_1", 1)
        elif playerObj['health'] >= 2:
            sonic_pi.send_message("/trigger/rtms_3", 0)
            sonic_pi.send_message("/trigger/rtms_3_1", 1)
            sonic_pi.send_message("/trigger/rtms_1", 1)
        elif playerObj['health'] >= 1:
            sonic_pi.send_message("/trigger/rtms_1", 1)
            sonic_pi.send_message("/trigger/rtms_3_1", 0)
        
        if playerObj['health'] in range(4, 6):
            sonic_pi.send_message("/trigger/rtms_2", 1)
        elif playerObj['health'] > 6:
            sonic_pi.send_message("/trigger/rtms_2", 0)

        if playerObj['health'] == 5:
            sonic_pi.send_message("/trigger/ring", [1, 0.98, 0.25])
        elif playerObj['health'] == 6:
            sonic_pi.send_message("/trigger/ring", [1, 0.97, 0.3])
            sonic_pi.send_message("/trigger/guitar_scrape", 0)
        elif playerObj['health'] == 7:
            sonic_pi.send_message("/trigger/ring", [1, 0.96, 0.35])
            sonic_pi.send_message("/trigger/rtms_2", 0)
        elif playerObj['health'] == 8:
            sonic_pi.send_message("/trigger/ring", [0, 0.98, 0.25])
        elif playerObj['health'] in range(8, 12):
            sonic_pi.send_message("/trigger/M3", 1)

        pygame.display.update()
        FPSCLOCK.tick(FPS)




def drawHealthMeter(currentHealth):
    for i in range(currentHealth): 
        pygame.draw.rect(DISPLAYSURF, PURPLE,   (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
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
    so['surface'] = SOUNDIMG
    so['width']  = SOUNDIMG.get_width()
    so['height'] = SOUNDIMG.get_height()
    so['x'], so['y'] = getRandomOffCameraPos(camerax, cameray, so['width'], so['height'])
    so['movex'] = getRandomVelocity()
    so['movey'] = abs(getRandomVelocity())
    return so


def makeNewRocks(camerax, cameray):
    ro = {}
    ro['blackholeImage'] = random.randint(0, len(ROCKIMAGES) - 1)
    ro['surface'] = ROCKIMAGES
    ro['width']  = ROCKIMAGES[0].get_width()
    ro['height'] = ROCKIMAGES[0].get_height()
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
