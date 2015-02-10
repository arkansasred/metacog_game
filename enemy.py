import pygame
import pyo
import random
from os import listdir
from global_variables import *
from psychopy import core
from vector import Vector
from player import Player

class Enemy(pygame.sprite.Sprite):
    """ This class represents the enemies """
    enemyA_images = listdir("Images/Enemies/EnemyA")
    enemyA_images = ["Images/Enemies/EnemyA/{0}".format(i) for i in enemyA_images if not i.startswith('.')]
    enemyB_images = listdir("Images/Enemies/EnemyB")
    enemyB_images = ["Images/Enemies/EnemyB/{0}".format(i) for i in enemyB_images if not i.startswith('.')]
    offscreen_time = 4 #seconds before appearance
    enemySightTime = []
    centerScreen = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
    target = centerScreen
    speed = 1
    targetReached = False
    offsetTime = speed*FPS*offscreen_time #multiply by FPS for fps-->s (FPS should be 60 and in global_variables file)
    offset_points = [(-offsetTime,-offsetTime),(SCREEN_WIDTH//2, -offsetTime),(SCREEN_WIDTH+offsetTime,-offsetTime),
    (SCREEN_WIDTH+offsetTime,SCREEN_HEIGHT//2),(SCREEN_WIDTH+offsetTime, SCREEN_HEIGHT+offsetTime), 
    (SCREEN_WIDTH//2, SCREEN_HEIGHT+offsetTime), (-offsetTime, SCREEN_HEIGHT+offsetTime), (-offsetTime, SCREEN_HEIGHT//2)]

    def __init__(self, enemy_type):
        """ Constructor, create the image of the enemy/sound for enemy. Selected from three enemy types """
        pygame.sprite.Sprite.__init__(self)
        self.targetReached = False
        self.enemy_type = enemy_type
        self.foove = pyo.SfPlayer("Sounds/foove.wav").mix(2)
        self.crelch = pyo.SfPlayer("Sounds/crelch.wav").mix(2)
        #self.env = pyo.Fader(fadein=.01,fadeout=.2, dur=0) #amplitude envelope to get rid of pops
        self.pop = pyo.SfPlayer("Sounds/kill.wav")#for when enemy dies
        if self.enemy_type == 'A1':
            self.image = pygame.image.load(self.enemyA_images[0])
        
        elif self.enemy_type == 'A2':
            self.image = pygame.image.load(self.enemyA_images[1])

        elif self.enemy_type == 'A3':
            self.image = pygame.image.load(self.enemyA_images[2])

        elif self.enemy_type == 'A4':
            self.image = pygame.image.load(self.enemyA_images[3])
        
        elif self.enemy_type == 'A5':
            self.image = pygame.image.load(self.enemyA_images[4])

        elif self.enemy_type == 'A6':
            self.image = pygame.image.load(self.enemyA_images[5])
        
        elif self.enemy_type == 'A7':
            self.image = pygame.image.load(self.enemyA_images[6])

        elif self.enemy_type == 'A8':
            self.image = pygame.image.load(self.enemyA_images[7])
        
        elif self.enemy_type == 'A9':
            self.image = pygame.image.load(self.enemyA_images[8])

        elif self.enemy_type == 'A10':
            self.image = pygame.image.load(self.enemyA_images[9])

        elif self.enemy_type == 'A11':
            self.image = pygame.image.load(self.enemyA_images[10])

        elif self.enemy_type == 'A12':
            self.image = pygame.image.load(self.enemyA_images[11])

        if self.enemy_type == 'B1':
            self.image = pygame.image.load(self.enemyB_images[0])
        
        elif self.enemy_type == 'B2':
            self.image = pygame.image.load(self.enemyB_images[1])

        elif self.enemy_type == 'B3':
            self.image = pygame.image.load(self.enemyB_images[2])

        elif self.enemy_type == 'B4':
            self.image = pygame.image.load(self.enemyB_images[3])
        
        elif self.enemy_type == 'B5':
            self.image = pygame.image.load(self.enemyB_images[4])

        elif self.enemy_type == 'B6':
            self.image = pygame.image.load(self.enemyB_images[5])
        
        elif self.enemy_type == 'B7':
            self.image = pygame.image.load(self.enemyB_images[6])

        elif self.enemy_type == 'B8':
            self.image = pygame.image.load(self.enemyB_images[7])

        elif self.enemy_type == 'B9':
            self.image = pygame.image.load(self.enemyB_images[8])

        elif self.enemy_type == 'B10':
            self.image = pygame.image.load(self.enemyB_images[9])

        elif self.enemy_type == 'B11':
            self.image = pygame.image.load(self.enemyB_images[10])

        elif self.enemy_type == 'B12':
            self.image = pygame.image.load(self.enemyB_images[11])
            
        self.image = pygame.transform.smoothscale(self.image, (85,85))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def set_speed(speed):
        self.speed = speed

    def set_target(self,targX,targY):
        self.target = (targX,targY)

    def generate(self):
        """ generate the enemy off screen """
        #distance for offset = desired time * velocity
        #ns.sync()
        self.offsetCoords = random.choice(self.offset_points)
        self.rect.x = self.offsetCoords[0]
        self.rect.y = self.offsetCoords[1]
    
    def wrong_hit(self):
        """play a sound, decrease score when wrong bullet hits enemy"""
        self.miss = pyo.SfPlayer("Sounds/beep.wav", loop=False).mix(2)
        self.miss.out()
    
    def update(self):
        """ Automatically called when we need to move the enemy. """
        """ Set Vector towards player"""
        if self.target:
            position = Vector(self.rect.x, self.rect.y) # create a vector from center x,y value
            targ = Vector(self.target[0],self.target[1]) # and one from the target x,y
            dist = targ - position # get total distance between target and position
            direction = dist.normalize() # normalize so its constant in all directions
            self.rect.x += (round(direction[0]) * self.speed) # calculate speed from direction to move and speed constant, rounding debugs the diagonal vectors
            self.rect.y += (round(direction[1]) * self.speed)
            dist_x = abs(dist[0]) # gets absolute value of the x distance
            dist_y = abs(dist[1]) # gets absolute value of the y distance
            t_dist = dist_x + dist_y # gets total absolute value distance
            speed = abs(self.speed) # gets aboslute value of the speed
            if t_dist < speed//2:
                self.target = None
                self.targetReached = True
