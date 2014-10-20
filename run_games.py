from os import mkdir, path
import pygame
from games import Game
import pyo
from global_variables import *
from enemy import Enemy
from psychopy import core
    
         
def main():
    def checkData(SUBJECT):
        if path.exists("/Subject %s"%SUBJECT):
            SUBJECT = raw_input("Data already exists for that subject, Please choose a different subject number: ")
            return checkData(SUBJECT)
        return SUBJECT
        print SUBJECT
    
    subject = checkData(SUBJECT = raw_input("Subject Number: "))
    print subject

    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
    #start pyo sound, use lowest latency output
    s = pyo.Server(duplex=0)
    #s.setOutputDevice(14)
    s.boot()
    s.start()
    
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
    
    if Game.VERSION==1:
        directory="Subject %s/PreTest/"%SUBJECT
    elif Game.VERSION==2:
        directory="Subject %s/TrainingLabels/"%SUBJECT
    elif Game.VERSION==3:
        directory = "Subject %s/TrainingNoLabels/"%SUBJECT
    elif Game.VERSION == 4:
        directory = "Subject %s/PostTest/"%SUBJECT

    shots = open(directory+"shots.txt", 'w')
    captures = open(directory+"captures.txt", 'w') # this is the capture 'attempt' timestamp
    AKills = open(directory+"Akills.txt", 'w')
    BKills = open (directory+'Bkills.txt', 'w')
    AwrongHits = open(directory+"Awronghits.txt", 'w')
    BwrongHits = open(directory+"Bwronghits.txt", 'w')
    AhitPlayer = open(directory+"Ahitplayer.txt", 'w')
    BhitPlayer = open(directory+"Bhitplayer.txt", 'w')
    sightsA = open(directory+"sightsA.txt", 'w')
    sightsB = open(directory+"sightsB.txt", 'w')
    numberPrediction = open(directory+"numberPrediction.txt", 'w')
    scorePrediction = open(directory+"scorePrediction.txt", 'w')
    for sight in Game.enemyASightTime:
        sightsA.write(str(sight)+'\n')
    for sight in Game.enemyBSightTime:
        sightsB.write(str(sight)+'\n')
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
    for hit in Game.enemyBWrongHitTime:
        BwrongHits.write(str(hit)+'\n')
    for hit in Game.enemyAHitPlayerTime:
        AhitPlayer.write(str(hit)+'\n')
    for hit in Game.enemyBHitPlayerTime:
        BhitPlayer.write(str(hit)+'\n')
    for prediction in Game.answer1Val:
        numberPrediction.write(str(prediction)+'\n')
    for prediction in Game.answer2Val:
        scorePrediction.write(str(prediction)+'\n')


    shots.close()
    captures.close()
    AKills.close()
    BKills.close()
    AwrongHits.close()
    BwrongHits.close()
    AhitPlayer.close()
    BhitPlayer.close()
    numberPrediction.close()
    scorePrediction.clost()
    sightsA.close()
    sightsB.close()

    #shut down pyo server
    s.stop()
    # Close window and exit
    pygame.quit()
    core.quit()

 
# Call the main function, start up the game
if __name__ == "__main__":
    main()