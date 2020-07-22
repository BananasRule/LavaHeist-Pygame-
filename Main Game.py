#Import and config moduals
import pygame, threading, os, hashlib, secrets, sys, playsound
pg = pygame
import random
rd = random 
import time
pg.font.init()
pg.mixer.init()
displayfont = pg.font.SysFont('Calibri', 50)
fontii = pg.font.SysFont('Cooper', 68)
pg.init()


#Creating the timer
def timer():
    global ctdn
    ctdn = 120
    while True:
        time.sleep(1)
        ctdn = ctdn - 1
    ctdn = 0

timerthread = threading.Thread(target=timer, daemon=True)
timerthread.start()
while True:
    #Define Veriables 
    #Screen tiles
    xrelative = 0
    yrelative = 0
    tiletype = 0
    #Stores all visited tiles
    map = {(0, 0): 2, (0, 180): 2, (0, 360): 2, (0, 540): 2, (0, 720): 1, (0, 900): 2, (180, 0): 2, (180, 180): 1, (180, 360): 2, (180, 540): 2, (180, 720): 2, (180, 900): 1, (360, 0): 2, (360, 180): 2, (360, 360): 2, (360, 540): 1, (360, 720): 2, (360, 900): 1, (540, 0): 2, (540, 180): 2, (540, 360): 2, (540, 540): 2, (540, 720): 2, (540, 900): 2, (720, 0): 2, (720, 180): 1, (720, 360): 2, (720, 540): 1, (720, 720): 2, (720, 900): 2, 0: 2}
    #Current pos on map
    xpos = 0
    ypos = 0
    #Current tile mapped to pos
    xabsolute = 0
    yabsolute = 0
    #Current tile
    mappedtile = 0 
    #Ensures dirt tile
    dirttiles = []
    dirttilesfull = {}
    #Current movement
    movement = 0 #1 = LEFT, 2 = UP, 3 = RIGHT 4 = DOWN
    #Ensures dirt tile
    tilecheck = 0
    xcheck = 0
    ycheck = 0
    tilechecknum = 0
    setdirttile = 0
    xscan = 0 
    yscan = 0
    xtotal = 0
    ytotal = 0
    count = 0
    rdirttiles = 0
    #Tacking movement
    movementcount = 0
    #Animation to play
    movestage = 1
    movementx = 360
    movementy = 360
    #Which way the character should face when standing
    sndpos = 2
    #Movement
    xmoveoverwrite = 0
    ymoveoverwrite = 0
    #Creating gems
    gemchance = 0
    gemcheckx = 0
    gemchecky = 0
    score = 0
    death = False
    pescore = ''
    escore = ''
    salt = ''
    testscore = ''
    testhash = ''
    testsalt = ''
    trialhash = ''
    savedscore = open('highscore.txt')
    highscore = 0
    
    #Reading from file
    testscore = savedscore.readline()
    testhash = savedscore.readline()
    testsalt = savedscore.readline()
    #Removing end of line char
    testscore = testscore[:-1]
    testhash = testhash[:-1]
    testsalt = testsalt[:-1]
    #Converting to bytes
    testsalt = testsalt.encode()
    #Converting to String
    testscore = str(testscore)
    #Creating hash based on file. Uses pbkdf2_hmac to ensure that it is harder to conver from hash to score due to 100000 iterations of sha256
    #Also makes it much harder to find a online converter which can do convert it
    #This system is intended to stop most people from changing highscore in text file6
    trialscore = hashlib.pbkdf2_hmac('sha256', testscore.encode('utf-8'), testsalt, 100000)
    #Tests to see if hash matches hash in file
    if str(testhash) == str(trialscore):
        highscore = int(testscore)
    else:
        #If not overwrites file
        savedscore.close()
        savedscore = open("highscore.txt", "w")
        savedscore.write("000000000\n")
        savedscore.write("000000000000\n")
        savedscore.write("000000000\n")
        savedscore.write("You: I can change my high score (HACKERMAN)\n")
        savedscore.write("Me: Well yes but actually no\n")
    savedscore.close()



    #Import images
    lava = pg.image.load('Lava.png')
    dirt = pg.image.load('Dirt.png')
    walking1R = pg.image.load('Right (2).png')
    walking2R = pg.image.load('Right (3).png')
    standR = pg.image.load('Right (1).png')
    walking1U = pg.image.load('Up (2).png')
    walking2U = pg.image.load('Up (3).png')
    standU = pg.image.load('Up (1).png')
    walking1L = pg.image.load('Left (2).png')
    walking2L = pg.image.load('Left (3).png')
    standL = pg.image.load('Left (1).png')
    walking1D = pg.image.load('Down (2).png')
    walking2D = pg.image.load('Down (3).png')
    standD = pg.image.load('Down (1).png')
    gem = pg.image.load('Gem.png')
    scorebar = pg.image.load('scorebar.png')
    startscreen = pg.image.load('TSF.png')
    instructionscreen = pg.image.load('TSI.png')
    timeend = pg.image.load('time.png')
    deathend = pg.image.load('death.png')

    #Create Screen
    #Sets screen pos on computer screen
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (510,70)
    pygame.display.set_caption("Lava Heist")
    screen = pg.display.set_mode((900,990))



    def gameoverdeath():
        global ctdn 
        ctdn = 0
        global death
        death = True
    



    #Start Screen
    screen.blit(startscreen, (-45,0))
    pg.display.update()
    while True:
        highscored = fontii.render("Highscore: " + (str(highscore)), True, (0,0,0))
        screen.blit(highscored, (305,450)) 
        pg.display.update()
        event = pg.event.poll()
        #Instruction screen / start game
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_i:
                screen.blit(instructionscreen, (-45,0))
                pg.display.update()
                while True:
                    event = pg.event.poll()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            screen.blit(startscreen, (-45,0))
                            pg.display.update()
                            break
            else:
                break
            pg.event.clear()

    #Starting timer on sperate thread
    ctdn = 120
    while ctdn > 0:
        #Set char position 
        xabsolute = xpos
        yabsolute = ypos
        while xrelative != 900:
            #Check map
            if (xabsolute,yabsolute) not in map: 
                #Generate Random Tile 
                tiletype = rd.randint(1,2)
                #Set gems
                if tiletype == 2:
                    gemchance = rd.randint(1,15)
                    if gemchance == 12:
                        tiletype = 3
                #Saves to map
                map.update({(xabsolute,yabsolute):tiletype})
                #Checking previous tiles to generate a set dirt tile on the next row 
                if movement == 3:
                    xcheck = (xabsolute - 180)
                    ycheck = yabsolute
                    #print(xcheck)
                    #print(ycheck)
                    checktile = map.get((xcheck,ycheck))
                    if checktile == 2:
                        dirttiles.append((xabsolute,yabsolute))
                        dirttilesfull.update({(xabsolute, yabsolute):(xrelative, yrelative)})
                if movement == 1:
                    xcheck = (xabsolute + 180)
                    ycheck = yabsolute
                    #print(xcheck)
                    #print(ycheck)
                    checktile = map.get((xcheck,ycheck))
                    if checktile == 2:
                        dirttiles.append((xabsolute,yabsolute))
                        dirttilesfull.update({(xabsolute, yabsolute):(xrelative, yrelative)})
                if movement == 2:
                    xcheck = xabsolute
                    ycheck = (yabsolute + 180)
                    checktile = map.get((xcheck,ycheck))
                    if checktile == 2:
                        dirttiles.append((xabsolute,yabsolute))
                        dirttilesfull.update({(xabsolute, yabsolute):(xrelative, yrelative)})
                if movement == 4:
                    xcheck = xabsolute
                    ycheck = (yabsolute - 180)
                    checktile = map.get((xcheck,ycheck))
                    if checktile == 2:
                        dirttiles.append((xabsolute,yabsolute))
                        dirttilesfull.update({(xabsolute, yabsolute):(xrelative, yrelative)})
            #Printing Map to screen
            if (xabsolute,yabsolute) in map:
                mappedtile = map.get((xabsolute,yabsolute))
                if mappedtile == 1:
                    screen.blit(lava, (xrelative,yrelative))
                if mappedtile == 2:
                    screen.blit(dirt, (xrelative,yrelative))
                if mappedtile == 3:
                    screen.blit(gem, (xrelative,yrelative))
            #Tile movement
            if yrelative == 720:
                xrelative += 180
                yrelative = 0
                xabsolute += 180
                yabsolute = ypos
            else:
                yrelative += 180
                yabsolute += 180

    #Get key presses
        event = pg.event.poll()
    #MOVE UP
    #All other instances are similar and comments will apply to all (CODE BLOCK A)
    #A function was not created due to a number of vars being substantialy diffrent
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP or event.key == pg.K_w:
                playsound.playsound('walking.wav', False)
                #Takes 20 frames
                while movementcount != 21:
                    #Checking which move stage / frame
                    if movestage == 1:
                        #Clears previous movement with overright 
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,360))
                        if mappedtile == 2:
                            screen.blit(dirt, (360,360))
                        if mappedtile == 3:
                            screen.blit(gem, (360,360))
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 180
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,180))
                            if movementcount == 12:
                                gameoverdeath()
                        if mappedtile == 2:
                            screen.blit(dirt, (360,180))
                        if mappedtile == 3:
                            screen.blit(gem, (360,180))
                        #Send char to screen
                        screen.blit(walking1U,(movementx, movementy))
                        pg.display.update()
                        movestage = 2
                    #See above
                    if movestage == 2:
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,360))
                        if mappedtile == 2:
                            screen.blit(dirt, (360,360))
                        if mappedtile == 3:
                            screen.blit(gem, (360,360))
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 180
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,180))
                            if movementcount == 12:
                                gameoverdeath()
                        if mappedtile == 2:
                            screen.blit(dirt, (360,180))
                        if mappedtile == 3:
                            screen.blit(gem, (360,180))
                        screen.blit(walking2U,(movementx, movementy))
                        pg.display.update()
                        movestage = 1
                    #Updates movementb
                    movementcount += 1
                    movementy -= 9
                    #Wait in between frame
                    time.sleep(0.0125)
                #Resets Movement and updates location on screen and map. Also sends type of movement for standing pos and dirt override
                movementcount = 0
                ypos = ypos - 180
                movement = 2
                
                movementx = 360
                movementy = 360
                sndpos = 2
    #MOVE LEFT (CODE BLOCK A)
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                playsound.playsound('walking.wav', False)
                while movementcount != 21:
                    if movestage == 1:
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,360))
                        if mappedtile == 2:
                            screen.blit(dirt, (360,360))
                        if mappedtile == 3:
                            screen.blit(gem, (360,360))
                        xmoveoverwrite = xpos + 180
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (180,360))
                            if movementcount == 12:
                                gameoverdeath()
                        if mappedtile == 2:
                            screen.blit(dirt, (180,360))
                        if mappedtile == 3:
                            screen.blit(gem, (180,360))
                        screen.blit(walking1L,(movementx, movementy))
                        pg.display.update()
                        movestage = 2
                    if movestage == 2:
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,360))
                        if mappedtile == 2:
                            screen.blit(dirt, (360,360))
                        if mappedtile == 3:
                            screen.blit(gem, (360,360))
                        xmoveoverwrite = xpos + 180
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (180,360))
                            if movementcount == 12:
                                gameoverdeath()
                        if mappedtile == 2:
                            screen.blit(dirt, (180,360))
                        if mappedtile == 3:
                            screen.blit(gem, (180,360))
                        screen.blit(walking2L,(movementx, movementy))
                        pg.display.update()
                        movestage = 1
                    movementcount += 1
                    movementx -= 9
                    time.sleep(0.0125)
                movementcount = 0
                xpos = xpos - 180
                movement = 1
                movementx = 360
                movementy = 360
                sndpos = 1
    #MOVE RIGHT (CODE BLOCK A)
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                playsound.playsound('walking.wav', False)
                while movementcount != 21:
                    if movestage == 1:
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,360))
                        if mappedtile == 2:
                            screen.blit(dirt, (360,360))
                        if mappedtile == 3:
                            screen.blit(gem, (360,360))
                        xmoveoverwrite = xpos + 540
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (540,360))
                            if movementcount == 12:
                                gameoverdeath()
                        if mappedtile == 2:
                            screen.blit(dirt, (540,360))
                        if mappedtile == 3:
                            screen.blit(gem, (540,360))
                        screen.blit(walking1R,(movementx, movementy))
                        pg.display.update()
                        movestage = 2
                    if movestage == 2:
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,360))
                        if mappedtile == 2:
                            screen.blit(dirt, (360,360))
                        if mappedtile == 3:
                            screen.blit(gem, (360,360))
                        xmoveoverwrite = xpos + 540
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (540,360))
                            if movementcount == 12:
                                gameoverdeath()
                        if mappedtile == 2:
                            screen.blit(dirt, (540,360))
                        if mappedtile == 3:
                            screen.blit(gem, (540,360))
                        screen.blit(walking2R,(movementx, movementy))
                        pg.display.update()
                        movestage = 1
                    movementcount += 1
                    movementx += 9
                    time.sleep(0.0125)
                movementcount = 0
                xpos = xpos + 180
                movement = 3
                movementx = 360
                movementy = 360
                sndpos = 3
    #MOVE DOWN (CODE BLOCK A)
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                playsound.playsound('walking.wav', False)
                while movementcount != 21:
                    if movestage == 1:
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,360))
                        if mappedtile == 2:
                            screen.blit(dirt, (360,360))
                        if mappedtile == 3:
                            screen.blit(gem, (360,360))
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 540
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,540))
                            if movementcount == 12:
                                gameoverdeath()
                        if mappedtile == 2:
                            screen.blit(dirt, (360,540))
                        if mappedtile == 3:
                            screen.blit(gem, (360,540))
                        screen.blit(walking1D,(movementx, movementy))
                        pg.display.update()
                        movestage = 2
                    elif movestage == 2:
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 360
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,360))
                        if mappedtile == 2:
                            screen.blit(dirt, (360,360))
                        if mappedtile == 3:
                            screen.blit(gem, (360,360))
                        xmoveoverwrite = xpos + 360
                        ymoveoverwrite = ypos + 540
                        mappedtile = map.get((xmoveoverwrite,ymoveoverwrite))
                        if mappedtile == 1:
                            screen.blit(lava, (360,540))
                            if movementcount == 12:
                                gameoverdeath()
                        if mappedtile == 2:
                            screen.blit(dirt, (360,540))
                        if mappedtile == 3:
                            screen.blit(gem, (360,540))
                        screen.blit(walking2D,(movementx, movementy))
                        pg.display.update()
                        movestage = 1
                    movementcount += 1
                    movementy += 9
                    time.sleep(0.0125)
                movementcount = 0
                ypos = ypos + 180
                movementx = 360
                movementy = 360
                sndpos = 4
            #Exits game when esc key pushed
            elif event.key == pg.K_ESCAPE:
                exit()
        #Removes excess key presses 
        pg.event.clear()
        #Sets dirt tile to help create a full map
        if len(dirttiles) != 0:
            setdirttile = rd.choice(dirttiles)
        map.update({setdirttile:2})
        rdirttiles = dirttilesfull.get(setdirttile)
        if setdirttile in map:
            mappedtile = map.get(setdirttile)
            if mappedtile == 2:
                if rdirttiles:
                    screen.blit(dirt, rdirttiles)
        #Sets standing posititon 
        if sndpos == 2:
            screen.blit(standU,(360,360))
        if sndpos == 1:
            screen.blit(standL,(360,360))
        if sndpos == 3:
            screen.blit(standR,(360,360))
        if sndpos == 4:
            screen.blit(standD,(360,360))
        #Checks current tile for gem and collects
        gemcheckx = xpos + 360
        gemchecky = ypos + 360
        mappedtile = map.get((gemcheckx,gemchecky))
        if mappedtile == 3:
            map.update({(gemcheckx,gemchecky):2})
            score += 1
            screen.blit(dirt, (360,360))
            playsound.playsound('gemcollect.wav', False)
        #Prints timer and score to screen
        printscore = displayfont.render(str(score), True, (255,255,255))
        printtimer = displayfont.render(str(ctdn), True, (255,255,255))
        screen.blit(scorebar, (0,900))
        screen.blit(printtimer, (550, 923))
        screen.blit(printscore, (100, 923))
        #Update display
        pg.display.update()
        pg.event.pump() #Silas said it was a good idea lol
        #Resets to start of screen
        xrelative = 0
        yrelative = 0
        dirttiles = []
    time.sleep(0.1)
    #Checks how the player dies (Displays diffrent screens)
    if death == True:
        screen.blit(deathend, (0,0))
    else:
        screen.blit(timeend, (0,0))
    #Clears Events
    pg.event.clear
    pg.display.update()
    #Checks to restart or exit
    #Dark patten used 
    #Player will restart game unless esc key pressed which is out of way on keyboard.
    #This ensures that the player remains playing the game
    while True:
        event = pg.event.poll()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()
            else:
                break
    #Checks if score is higher than highscore
    if score > highscore:
        #Creates cryptographicly secure key from OS (Overkill)
        salt = secrets.token_hex(32)
        salt = salt.encode()
        #Pre encrypted
        pescore = str(score)
        #Hashes score with salt
        escore = hashlib.pbkdf2_hmac('sha256', pescore.encode('utf-8'), salt, 100000)
        #Saves details to file
        savedscore = open("highscore.txt", "w")
        savedscore.write(str(score) + "\n")
        savedscore.write(str(escore) + "\n")
        savedscore.write(str(salt.decode()) + "\n")
        #Closes file
        savedscore.close()