from os import mkdir, path
import pygame
from training_1 import Game
import pyo
from global_variables import *
<<<<<<< HEAD
from psychopy import core
from enemy import Enemy
=======
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
    
         
def main():
    def checkData(SUBJECT):
        if path.exists("Subject %s/Training"%SUBJECT):
            SUBJECT = raw_input("Data already exists for that subject, Please choose a different subject number: ")
<<<<<<< HEAD
            return checkData(SUBJECT)
=======
            checkData(SUBJECT)
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
        return SUBJECT
        print SUBJECT
    
    subject = checkData(SUBJECT = raw_input("Subject Number: "))
    print subject
    try:
<<<<<<< HEAD
=======
        mkdir("Subject %s"%subject)
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
        mkdir("Subject %s/Training"%subject)
    except:
        print "Woops, data already exists for this subject, check the subject folder and relaunch the game before proceeding"

    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
<<<<<<< HEAD
    s = pyo.Server(duplex=0) 
    s.setOutputDevice(14)  
=======
    s = pyo.Server(duplex=0)    
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
    s.boot()
    s.start()
    
    #start NetStation
    """ms_localtime = egi.ms_localtime

    ns.initialize(address, port)
    ns.BeginSession()
    ns.sync()
    ns.StartRecording()"""
    
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    bgimage = pygame.image.load("Images/planet.bmp")
    bgimage = pygame.transform.scale(bgimage, (SCREEN_WIDTH, SCREEN_HEIGHT))
     
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
     
    # Create an instance of the Game class
    game = Game()
    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
        #draw bg image
        screen.blit(bgimage, [0,0])

        # Update object positions, check for collisions
        game.run_logic()
         
        # Draw the current frame
        game.display_frame(screen)
         
        # Pause for the next frame
        clock.tick(FPS)

    directory = "Subject %s/Training/"%subject
    shots = open(directory+"shots.txt", 'w')
    captures = open(directory+"captures.txt", 'w')
    AKills = open(directory+"Akills.txt", 'w')
    BKills = open (directory+'Bkills.txt', 'w')
    AwrongHits = open(directory+"Awronghits.txt", 'w')
    BwrongHits = open(directory+"Bwronghits.txt", 'w')
    AhitPlayer = open(directory+"Ahitplayer.txt", 'w')
    BhitPlayer = open(directory+"Bhitplayer.txt", 'w')
    sights = open(directory+"sights.txt", 'w')
    for sight in Enemy.enemySightTime:
        sights.write(str(sight)+'\n')
    for shot in Game.shotTime:
        shots.write(str(shot)+'\n')
    for capture in Game.captureTime:
        captures.write(str(capture)+'\n')
    for kill in Game.enemyAKillTime:
        AKills.write(str(kill)+'\n')
    for kill in Game.enemyBKillTime:
        BKills.write(str(kill)+'\n')
    for hit in Game.enemyAWrongHitTime:
        AwrongHits.write(str(hit)+'\n')
<<<<<<< HEAD
    for hit in Game.enemyBWrongHitTime:
=======
    for hit in Game.enembyBWrongHitTime:
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
        BwrongHits.write(str(hit)+'\n')
    for hit in Game.enemyAHitPlayerTime:
        AhitPlayer.write(str(hit)+'\n')
    for hit in Game.enemyBHitPlayerTime:
<<<<<<< HEAD
        BhitPlayer.write(str(hit)+'\n')
=======
        Bhitplayer.write(str(hit)+'\n')
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea

    shots.close()
    captures.close()
    AKills.close()
    BKills.close()
    AwrongHits.close()
    BwrongHits.close()
    AhitPlayer.close()
    BhitPlayer.close()


    #shut down pyo server
    s.stop()
    # Close window and exit
    pygame.quit()
<<<<<<< HEAD
    core.quit()
=======
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea

 
# Call the main function, start up the game
if __name__ == "__main__":
    main()