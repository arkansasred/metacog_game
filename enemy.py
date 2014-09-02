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
    offscreen_time = 1 #seconds before appearance
    enemySightTime = []
    centerScreen = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
    target = centerScreen
    speed = 2
    targetReached = False
    offsetTime = speed*FPS*offscreen_time #multiply by FPS for fps-->s
    offset_points = [(-offsetTime,-offsetTime),(SCREEN_WIDTH//2, -offsetTime),(SCREEN_WIDTH+offsetTime,-offsetTime),
    (SCREEN_WIDTH+offsetTime,SCREEN_HEIGHT//2),(SCREEN_WIDTH+offsetTime, SCREEN_HEIGHT+offsetTime), 
    (SCREEN_WIDTH//2, SCREEN_HEIGHT+offsetTime), (-offsetTime, SCREEN_HEIGHT+offsetTime), (-offsetTime, SCREEN_HEIGHT//2)]
    def __init__(self, enemy_type):
        """ Constructor, create the image of the enemy/sound for enemy. Selected from three enemy types """
        pygame.sprite.Sprite.__init__(self)
        self.targetReached = False
        self.enemy_type = enemy_type
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

            
        self.image = pygame.transform.smoothscale(self.image, (75,75))
        self.image.set_colorkey((255,255,255))
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
            self.rect.x += (direction[0] * self.speed) # calculate speed from direction to move and speed constant
            self.rect.y += (direction[1] * self.speed)
            dist_x = dist[0] ** 2 # gets absolute value of the x distance
            dist_y = dist[1] ** 2 # gets absolute value of the y distance
            t_dist = dist_x + dist_y # gets total absolute value distance
            speed = self.speed ** 2 # gets aboslute value of the speed
            if t_dist < speed:
                self.target = None
                self.targetReached = True
        """ Record time right when enemy fully enters screen """
        if -1<= self.rect.y <= 0 or -1<= self.rect.x <= 0 or SCREEN_WIDTH+1>=self.rect.x>=SCREEN_WIDTH or SCREEN_HEIGHT+1>=self.rect.y>=SCREEN_HEIGHT:
            t_sight = core.getTime()
            self.enemySightTime.append(t_sight)
