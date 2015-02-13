from os import mkdir, path
import pygame
from games import Game
import pyo
from global_variables import *
from enemy import Enemy
from psychopy import core
from sys import platform
    
         
def main():
    def checkData(subj):
        if Game.VERSION==1:
            if path.exists("Subject %s/PreTest/"%subj):
                subj = raw_input("Data already exists for that subject, Please choose a different subject number: ")
                return checkData(subj)
        elif Game.VERSION==3:
            if path.exists("Subject %s/TrainingLabels/"%subj):
                subj = raw_input("Data already exists for that subject, Please choose a different subject number: ")
                return checkData(subj)
        elif Game.VERSION==4:
            if path.exists("Subject %s/TrainingNoLabels/"%subj):
                subj = raw_input("Data already exists for that subject, Please choose a different subject number: ")
                return checkData(subj)
        elif Game.VERSION==5:
            if path.exists("Subject %s/PostTest/"%subj):
                subj = raw_input("Data already exists for that subject, Please choose a different subject number: ")
                return checkData(subj)
        return subj
    
    SUBJECT = checkData(subj = raw_input("Subject Number: "))
    if not path.exists("Subject %s"%SUBJECT):
        mkdir("Subject %s"%SUBJECT)
        print "Making subject directory"

    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.display.init()
    pygame.font.init()
    #start pyo sound, use lowest latency output
    if platform == "linux2":
        s = pyo.Server(audio = 'jack')
    elif platform == "win64" or platform == "win32":
        s = pyo.Server(duplex=0)
        s.setOutputDevice(14)
    else:
        s = pyo.Server()
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
        if not path.exists(directory):
            mkdir(directory)
    elif Game.VERSION==2:
        directory="Subject %s/TrainingLabelsCongruent/"%SUBJECT
        if not path.exists(directory):
            mkdir(directory)
    elif Game.VERSION==3:
        directory = "Subject %s/TrainingNoLabelsIncongruent/"%SUBJECT
        if not path.exists(directory):
            mkdir(directory)
    elif Game.VERSION==4:
        directory = "Subject %s/TrainingNoLabels/"%SUBJECT
        if not path.exists(directory):
            mkdir(directory)
    elif Game.VERSION == 5:
        directory = "Subject %s/PostTest/"%SUBJECT
        if not path.exists(directory):
            mkdir(directory)

    print Game.answer1Val
    print Game.answer2Val
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
    numberActual = open(directory+"numberActual.txt",'w')
    scoreActual = open(directory+"scoreActual.txt", 'w')
    for sight in Game.enemyASightTime:
        sightsA.write(str(sight)+'\n')
    for sight in Game.enemyBSightTime:
        sightsB.write(str(sight)+'\n')
    for shot in Game.shotTime:
        shots.write(str(shot)+'\n')
    for capture in Game.captureTime:
        captures.write(str(capture)+'\n')
    for kill in Game.enemyAKillTime1:
        AKills.write(str(kill)+'\n')
    for kill in Game.enemyBKillTime1:
        BKills.write(str(kill)+'\n')
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
    for answer in Game.answer1Actual:
        numberActual.write(str(answer)+'\n')
    for answer in Game.answer2Actual:
        scoreActual.write(str(answer)+'\n')


    shots.close()
    captures.close()
    AKills.close()
    BKills.close()
    AwrongHits.close()
    BwrongHits.close()
    AhitPlayer.close()
    BhitPlayer.close()
    numberPrediction.close()
    scorePrediction.close()
    sightsA.close()
    sightsB.close()
    scoreActual.close()
    numberActual.close()

    #shut down pyo server
    s.stop()
    # Close window and exit
    pygame.quit()
    core.quit()

 
# Call the main function, start up the game
if __name__ == "__main__":
    main()