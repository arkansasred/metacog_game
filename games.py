from os import mkdir, path, listdir
import pygame 
from psychopy import core
import pyo
from bullet import Bullet
from enemy import Enemy
from player import Player
from global_variables import *
from random import shuffle, randrange
import eztext


"""
IMPORTANT, versions are as follows:
    1: pre-test
    2:training with labels
    3:training without labels
    4: post-test

    familiarization game to be loaded seperately
"""

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def whichVersion(version):
        if int(version) >= 5:
            version = raw_input("Not a valid version, please input version number 1-5: ")
            return whichVersion(version)
        else:
            return version


    VERSION = whichVersion(version = int(raw_input("Version number (1-5): ")))


    # --- Class attributes. 
     
    # Sprite lists
    enemyA_list = None
    enemyB_list = None

    if VERSION == 1:
        numberEnemies = 5
    elif VERSION == 2 or VERSION == 3 or VERSION == 4:
        numberEnemies = 8
    elif VERSION == 5:
        numberEnemies = 5
    print VERSION

    #define all the enemies
    A1Enemies = ['A2' for i in range (numberEnemies)]
    A2Enemies = ['A4' for i in range (numberEnemies)]
    A3Enemies = ['A7' for i in range (numberEnemies)]
    A4Enemies = ['A8' for i in range (numberEnemies)]
    A5Enemies = ['A9' for i in range (numberEnemies)]
    A6Enemies = ['A10' for i in range (numberEnemies)]
    A7Enemies = ['A11' for i in range (numberEnemies)]
    A8Enemies = ['A12' for i in range (numberEnemies)]
    B1Enemies = ['B1' for i in range(numberEnemies)]
    B2Enemies = ['B2' for i in range(numberEnemies)]
    B3Enemies = ['B7' for i in range(numberEnemies)]
    B4Enemies = ['B8' for i in range(numberEnemies)]
    B5Enemies = ['B9' for i in range(numberEnemies)]
    B6Enemies = ['B10' for i in range(numberEnemies)]
    B7Enemies = ['B11' for i in range(numberEnemies)]
    B8Enemies = ['B12' for i in range(numberEnemies)]

    enemies_list = A1Enemies + A2Enemies + A3Enemies + A4Enemies + A5Enemies + A6Enemies + A7Enemies + A8Enemies + B1Enemies + B2Enemies + B3Enemies + B4Enemies + B5Enemies + B6Enemies + B7Enemies + B8Enemies
    bullet_list = None
    all_sprites_list = None
    player = None
    #Time measurements
    shotTime = []
    captureTime = []
    enemyAKillTime = []
    enemyBKillTime = []
    #will be used to store "kill" time measurements for 1st half of game (kill refers to both kill/capture)
    enemyAKillTime1 = []
    enemyBKillTime1 = []
    enemyAWrongHitTime = []
    enemyBWrongHitTime = []
    answer1Val= []
    answer2Val= []
    answer1Actual = []
    answer2Actual = []
    #record when player does not hit the enemy at all (enemy hits player)
    enemyAHitPlayerTime = []
    enemyBHitPlayerTime = []
    enemyASightTime = []
    enemyBSightTime = []
    enemy_live = False #bool to tell us if there is a live enemy
    elapsedTime = 0.0 #keep track of elapsed time via frame rate changes
    enemySpawnTime= 120.0 # of frames between enemy death and next enemy spawn
    ammo = numberEnemies*24 #3 bullets per true 'enemy'
    if VERSION==2 or VERSION == 3:
        #experimental
        fontRenderTime = 0.0
        fontRenderRemoval = 120.0
        renderA = None
        renderB = None
    elif VERSION==4:
        #control
        renderTime = 0.0
        renderRemoval = 120.0
        render = None

    #this is for making animated explosions
    isExplosion_center = False
    isExplosion_enemy = False
    isExplosion_player = False
    explosion_img = pygame.image.load('Images/explosion1.bmp')

    exp1 = pygame.transform.scale(explosion_img, (10,10))
    exp2 = pygame.transform.scale(explosion_img, (15,15))
    exp3 = pygame.transform.scale(explosion_img, (20,20))
    exp4 = pygame.transform.scale(explosion_img, (25,25))
    exp5 = pygame.transform.scale(explosion_img, (30,30))
    exp6 = pygame.transform.scale(explosion_img, (35,35))
    exp7 = pygame.transform.scale(explosion_img, (40,40))
    exp8 = pygame.transform.scale(explosion_img, (45,45))
    exp9 = pygame.transform.scale(explosion_img, (50,50))
    explosionDur = 0 #keep track of timing of explosion animation
    getMetacogEval = False
    answer1 = True
    sight = False
    halfway=False #elicit another prospective assesment at halfway point
    previousKill= False #helps keep track of whether previous trial was successful
    score = None
    score1 = None

    # --- Class methods
    # Set up the game
    def __init__(self):
        shuffle(self.enemies_list)
        shuffle(self.enemies_list)
        self.score = 0
        self.game_over = False
        self.game_start = True
         
        # Create sprite lists
        self.enemyA_list = pygame.sprite.Group()
        self.enemyB_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()

        self.q1=eztext.Input(x=10, y=SCREEN_HEIGHT//2, font = pygame.font.Font(None,28), maxlength=45, color=GREEN, prompt='For the next series of %s Aliens, how many do you think you will successfully shoot or capture?:  '%(self.numberEnemies*8))
        self.q2=eztext.Input(x=SCREEN_WIDTH//2-400, y=SCREEN_HEIGHT//2, maxlength=45,color=GREEN,prompt="What do you think your score will be for this segment of the game?:  ")          
         
        # Create the player
        self.player = Player()
        #shot sound
        self.shot_sound = pyo.SfPlayer("Sounds/laser_shot.aif", mul=0.4)
        #explosion sound
        self.wrong_button = pyo.SfPlayer("Sounds/wrong_hit.wav")
        self.explosionSound = pyo.SfPlayer("Sounds/explosion.wav", speed=[1,1], mul=0.5)
        self.env = pyo.Adsr(attack=.01, decay=.05, sustain=.2, release=.1, dur=.5, mul=.5)
        self.bell = pyo.Sine(freq=[800,800], mul=self.env).out()
 
    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        def shoot(color, target, degree, origin):
            #shoot to the point where the player is facing (given by target)
            if self.ammo > 0:
                self.bullet = Bullet(color, target, degree, origin)
                self.bullet.color = str(color)
                #play bullet sound
                self.shot_sound.out()
                #decrease ammo supply by 1
                self.ammo-=1
                # Add the bullet to the lists
                self.all_sprites_list.add(self.bullet)
                shot = core.getTime()
                self.shotTime.append(shot)
                self.bullet_list.add(self.bullet)
            
            else:
                self.wrong_button.out()
         
        #Event handling

        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.turnLeft = True
                elif event.key == pygame.K_RIGHT:
                    self.player.turnRight = True
                elif event.key == pygame.K_RETURN:
                    if self.getMetacogEval and self.answer1:
                        """log the estimate in the answer1Val list, go to second question"""
                        estimate=self.q1.value
                        print estimate
                        self.answer1Val.append(estimate)
                        self.q1.value=""
                        self.answer1=False
                    elif self.getMetacogEval and not self.answer1:
                        """next question"""
                        estimate=self.q2.value
                        self.answer2Val.append(estimate)
                        self.q2.value=""
                        self.getMetacogEval=False
                        self.answer1=True
                        self.elapsedTime = 1
                    else:
                        shoot(RED, self.player.currTarget, self.player.degree, (self.player.trueX,self.player.trueY))
                elif event.key == pygame.K_SPACE:
                    if self.game_start:
                        self.game_start = False
                        self.getMetacogEval=True
                    elif self.halfway:
                        #record then reset score, record, same for the enemy kill times
                        self.halfway = False
                        self.getMetacogEval = True
                        self.answer1Actual.append(str(len(self.enemyAKillTime)+len(self.enemyBKillTime)))
                        self.answer2Actual.append(self.score)
                        self.enemyAKillTime1.extend(self.enemyAKillTime)
                        del self.enemyAKillTime[:]
                        self.enemyBKillTime1.extend(self.enemyBKillTime)
                        del self.enemyBKillTime[:]
                        self.score1 = self.score
                        self.score = 0
                    else: 
                        self.player.capture()
                        capture = core.getTime()
                        self.captureTime.append(capture)
                elif event.key == pygame.K_ESCAPE:
                    return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.turnLeft = False
                elif event.key == pygame.K_RIGHT:
                    self.player.turnRight = False

        return False #for exiting game
 
    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions, records data, and checks for collisions.
        """



        def kill_enemy(enemy_type):
            font = pygame.font.Font(None, 25)
            time = core.getTime()
            if enemy_type=='A':
                self.enemyAKillTime.append(time)
                if self.VERSION==2 or self.VERSION == 3:
                    self.renderA = True
                elif self.VERSION==4:
                    self.render = True
            elif enemy_type=='B':
                self.enemyBKillTime.append(time)
                if self.VERSION==2 or self.VERSION == 3:
                    self.renderB = True
                elif self.VERSION==4:
                    self.render = True
            self.enemy.pop.out()
            self.score += 20
            self.elapsedTime = 0
            self.enemy_live = False
            self.previousKill = True

        if self.sight:
            time = core.getTime()
            if self.enemy_type[0]=='A':
                self.enemyASightTime.appned(time)
            elif self.enemy_type[0]=='B':
                self.enemyBSightTime.append(time)

        if not self.game_start and not self.game_over and not self.halfway:
        # Create the enemy sprites
            if not self.enemy_live and not self.getMetacogEval and self.elapsedTime==60:
                #play sound 1 second preceding alien spawn
                if self.VERSION==2:
                    if self.enemy_type[0] == 'A':
                        self.enemy.crelch.out()
                    elif self.enemy_type[0] == 'B':
                        self.enemy.foove.out()
                elif self.VERSION == 3:
                    if self.enemy_type[0] == 'A':
                        self.enemy.foove.out()
                    elif self.enemy_type[0] == 'B':
                        self.enemy.crelch.out()
                elif self.VERSION == 4:
                    #play sine tone
                    self.env.play()
            
            if not self.enemy_live and not self.getMetacogEval and self.elapsedTime==self.enemySpawnTime:
                self.enemy_type = self.enemies_list.pop()
                self.enemy = Enemy(self.enemy_type)
                self.enemy.generate()
                self.all_sprites_list.add(self.enemy)
                if self.enemy_type[0]=='A':
                    self.enemyA_list.add(self.enemy)
                
                elif self.enemy_type[0]=='B':
                    self.enemyB_list.add(self.enemy)

                """for every 20 enemies killed/captured, increase speed"""

                if len(self.enemies_list)<(self.numberEnemies*16-1) and self.previousKill and (len(self.enemyAKillTime)+len(self.enemyBKillTime))%(self.numberEnemies*4) == 0:
                    self.player.rotationSpeed+=1
                    Enemy.speed+=1
                    self.player.speed+=1
                
                self.enemy_live = True
            
            if self.enemy_live:
                #when enemy enters screen, decrease score
                """ Record time right when enemy fully enters screen """
                if 0<= self.enemy.rect.y<=SCREEN_HEIGHT or 0 <= self.enemy.rect.x <=SCREEN_WIDTH:
                    self.sight = True
                    self.sight=False
                    self.score -= 1/float(60) # decrease score by 1 for every second that enemy is alive
         
            
            # Move all the sprites
            self.all_sprites_list.update()
            self.player.update()
            
            #increase time for enemy spawn    
            self.elapsedTime +=1
            
            #collision detection
            for bullet in self.bullet_list:
                self.enemy_hit_list = pygame.sprite.spritecollide(bullet, self.enemyA_list, True)
                for enemy in self.enemy_hit_list:
                    kill_enemy('A')
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                    self.isExplosion_enemy = True
                    """if bullet goes off screen, remove it from sprites lists"""
                if bullet.rect.x>SCREEN_WIDTH or bullet.rect.x<0 or bullet.rect.y>SCREEN_HEIGHT or bullet.rect.y<0:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                """give audio feedback if wrong sprite shot"""
                if pygame.sprite.spritecollide(bullet, self.enemyB_list, True):
                    time = core.getTime()
                    self.enemyBWrongHitTime.append(time)
                    self.enemy.wrong_hit()
                    self.score -= 10
                    self.isExplosion_enemy = True
                    self.elapsedTime = 0
                    self.enemy_live = False
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                    if self.VERSION==2 or self.VERSION == 3:
                        self.renderB = True
                    elif self.VERSION==4:
                        self.render = True
                    self.previousKill=False
            
 

            if self.player.atCenter:
                if pygame.sprite.spritecollide(self.player, self.enemyB_list, True):
                    time = core.getTime()
                    self.enemyBHitPlayerTime.append(time)
                    self.enemy_live = False
                    self.elapsedTime = 0
                    self.score -= 20
                    self.enemy.wrong_hit()
                    if self.VERSION==2 or self.VERSION == 3:
                        self.renderB = True
                    elif self.VERSION==4:
                        self.render = True
                    self.previousKill=False
                
                if pygame.sprite.spritecollide(self.player, self.enemyA_list, True):
                    time = core.getTime()
                    self.enemyAHitPlayerTime.append(time)
                    self.enemy_live = False
                    self.elapsedTime = 0
                    self.score -= 20
                    self.isExplosion_center=True
                    self.explosionSound.out()
                    if self.VERSION==2 or self.VERSION == 3:
                        self.renderA=True
                    elif self.VERSION==4:
                        self.render = True
                    self.previousKill=False
            
            elif not self.player.atCenter and self.enemy_live:
                
                if pygame.sprite.spritecollide(self.player, self.enemyB_list, True):
                    if not self.enemy.targetReached:
                        kill_enemy('B')
                        self.player.targetReached = True
                    else:
                        time = core.getTime()
                        self.enemyBHitPlayerTime.append(time)
                        self.enemy_live = False
                        self.enemy.wrong_hit()
                        self.elapsedTime = 0
                        self.score -= 20
                        if self.VERSION==2 or self.VERSION == 3:
                            self.renderB=True
                        elif self.VERSION==4:
                            self.render = True
                        self.previousKill=False
                
                if pygame.sprite.spritecollide(self.player, self.enemyA_list, True):
                    if not self.enemy.targetReached:
                        time = core.getTime()
                        self.enemyAHitPlayerTime.append(time)
                        self.enemy.wrong_hit()
                        self.enemy_live = False
                        self.elapsedTime = 0
                        self.score -= 10
                        self.isExplosion_enemy=True
                        self.player.targetReached=True
                        if self.VERSION==2 or self.VERSION == 3:
                            self.renderA=True
                        elif self.VERSION==4:
                            self.render = True
                        self.previousKill=False
                    else:
                        time = core.getTime()
                        self.enemyAWrongHitTime.append(time)
                        self.explosionSound.out()
                        self.score -= 20
                        self.isExplosion_player = True
                        self.elapsedTime = 0
                        self.enemy_live = False
                        if self.VERSION==2 or self.VERSION == 3:
                            self.renderA=True
                        elif self.VERSION==4:
                            self.render = True
                        self.previousKill=False

            if len(self.enemies_list)==(self.numberEnemies*16)//2 and self.elapsedTime==0:
                self.halfway = True

            """define end of level"""
            if len(self.enemies_list)==0 and not self.enemy_live:
                self.answer1Actual.append(str(len(self.enemyAKillTime)+len(self.enemyBKillTime)))
                self.answer2Actual.append(self.score)
                self.game_over = True

                 
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        def center_text(text):
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
        def next_line(text, spacing):
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2) + spacing
            screen.blit(text, [center_x,center_y])

        if self.halfway:  
            font = pygame.font.Font(None, 25)
            text2 = font.render("You successfully killed or captured a total of "+ str(len(self.enemyAKillTime)+len(self.enemyBKillTime)) +
                                " of the " + str(self.numberEnemies*8) + " aliens you encountered, for a score of %d.  Hit space to continue"%(self.score),
                                True, GREEN)
            center_x = (SCREEN_WIDTH // 2) - (text2.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) + (text2.get_height() // 2) + 2
            screen.blit(text2, [center_x, center_y])

        elif self.game_start:
            font = pygame.font.Font(None, 25)
            text = font.render("Hello, thank you for participating in this experiment! You will be using the following buttons for the first level:",
                               True, WHITE)
            text2 = font.render("Space:            Enter:", True, WHITE)
            text3 = font.render ("Press the Space bar to begin", True, WHITE)
            shoot = font.render("SHOOT",True, RED)
            capture = font.render("CAPTURE", True, GREEN)
            center_text(text)
            next_line(text2, 40)
            next_line(text3, 140)
            screen.blit(shoot, [520,440])
            screen.blit(capture, [420,440])

        elif self.getMetacogEval:
            if self.answer1:
                """ask for perecent correct estimate"""
                self.q1.update(self.events)
                self.q1.draw(screen)
                
            else:
                self.q2.update(self.events)
                self.q2.draw(screen)

        elif self.game_over:  
            font = pygame.font.Font(None, 18)
            font2 = pygame.font.Font(None, 25)
            text2 = font.render("For the second half of the game, you successfully killed or captured a total of "+ str(len(self.enemyAKillTime)+len(self.enemyBKillTime)) +
                                " of the " + str(self.numberEnemies*8) + " aliens you encountered, for a score of %d."%(self.score),
                                True, GREEN)
            center_x = (SCREEN_WIDTH // 2) - (text2.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) + (text2.get_height() // 2) + 2
            screen.blit(text2, [center_x, center_y])
            text3 = font2.render("Overall, you successfully killed or captured a total of "+ str(len(self.enemyAKillTime1)+len(self.enemyBKillTime1)+len(self.enemyAKillTime)+len(self.enemyBKillTime)) +
                                " of the " + str(self.numberEnemies*16) + " aliens you encountered, for a total score of {:.0f}".format(self.score + self.score1),
                                True, GREEN)
            center_x = (SCREEN_WIDTH // 2) - (text3.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) + (text3.get_height() // 2) + 40
            screen.blit(text3, [center_x, center_y])  
            
         
        else:
            #draw sprites, print score
            self.all_sprites_list.draw(screen)
            screen.blit(self.player.rotated,self.player.rect)
            font = pygame.font.Font(None, 15)
            score = font.render('Score: %s'%"{:,.0f}".format(self.score), True, RED)
            ammo = font.render('Ammo: %d'%self.ammo, True, YELLOW)
            x_pos = 6
            """screen.blit(lives, [x_pos, lives.get_height()])"""
            screen.blit(score, [x_pos, score.get_height()])
            screen.blit(ammo, [x_pos, score.get_height()+ammo.get_height()])
            if self.isExplosion_center:
                """animate the explosion"""
                pos = (SCREEN_WIDTH//2-20,SCREEN_HEIGHT//2-20)
                self.explosionDur+=1
                if 1<self.explosionDur<=3:
                    screen.blit(self.exp1,pos)
                elif 3 < self.explosionDur <= 5:
                    screen.blit(self.exp2,pos)
                elif 5 < self.explosionDur <=7:
                    screen.blit(self.exp3,pos)
                elif 7 < self.explosionDur <=9:
                    screen.blit(self.exp4,pos)
                elif 9 < self.explosionDur <=11:
                    screen.blit(self.exp5,pos)
                elif 11 < self.explosionDur <=13:
                    screen.blit(self.exp6,pos)
                elif 13 < self.explosionDur <=15:
                    screen.blit(self.exp7,pos)
                elif 15 < self.explosionDur <=17:
                    screen.blit(self.exp8,pos)
                elif 20<self.explosionDur:
                    screen.blit(self.exp9,pos)

                if self.explosionDur>22:
                    self.explosionDur = 0
                    self.isExplosion_center = False

            elif self.isExplosion_enemy:
                pos = self.enemy.rect       
                self.explosionDur+=1
                if 1<self.explosionDur<=3:
                    screen.blit(self.exp1,pos)
                elif 3 < self.explosionDur <= 5:
                    screen.blit(self.exp2,pos)
                elif 5 < self.explosionDur <=7:
                    screen.blit(self.exp3,pos)
                elif 7 < self.explosionDur <=9:
                    screen.blit(self.exp4,pos)
                elif 9 < self.explosionDur <=11:
                    screen.blit(self.exp5,pos)
                elif 11 < self.explosionDur <=13:
                    screen.blit(self.exp6,pos)
                elif 13 < self.explosionDur <=15:
                    screen.blit(self.exp7,pos)
                elif 15 < self.explosionDur <=17:
                    screen.blit(self.exp8,pos)
                elif 20<self.explosionDur:
                    screen.blit(self.exp9,pos)

                if self.explosionDur>22:
                    self.explosionDur = 0
                    self.isExplosion_enemy = False


            elif self.isExplosion_player:
                pos = self.player.rect       
                self.explosionDur+=1
                if 1<self.explosionDur<=3:
                    screen.blit(self.exp1,pos)
                elif 3 < self.explosionDur <= 5:
                    screen.blit(self.exp2,pos)
                elif 5 < self.explosionDur <=7:
                    screen.blit(self.exp3,pos)
                elif 7 < self.explosionDur <=9:
                    screen.blit(self.exp4,pos)
                elif 9 < self.explosionDur <=11:
                    screen.blit(self.exp5,pos)
                elif 11 < self.explosionDur <=13:
                    screen.blit(self.exp6,pos)
                elif 13 < self.explosionDur <=15:
                    screen.blit(self.exp7,pos)
                elif 15 < self.explosionDur <=17:
                    screen.blit(self.exp8,pos)
                elif 20<self.explosionDur:
                    screen.blit(self.exp9,pos)

                if self.explosionDur>22:
                    self.explosionDur = 0
                    self.player.trueX = SCREEN_WIDTH//2
                    self.player.trueY = SCREEN_HEIGHT//2
                    self.player.target = None
                    self.isExplosion_player = False

            if self.VERSION==2:
                if self.renderA and self.fontRenderTime<self.fontRenderRemoval:
                    font = pygame.font.Font(None, 20)
                    text = font.render("Crelch", True, WHITE)
                    screen.blit(self.enemy.image, [self.enemy.rect.x,self.enemy.rect.y])
                    screen.blit(text, [self.enemy.rect.x+5,self.enemy.rect.y+80])
                    self.fontRenderTime+=1.0
                    if self.fontRenderTime>=self.fontRenderRemoval:
                        self.renderA = False
                        self.fontRenderTime = 0.0
                elif self.renderB and self.fontRenderTime<self.fontRenderRemoval:
                    font = pygame.font.Font(None, 20)
                    text = font.render("Foove", True, WHITE)
                    screen.blit(self.enemy.image, [self.enemy.rect.x,self.enemy.rect.y])
                    screen.blit(text, [self.enemy.rect.x+5, self.enemy.rect.y+80])
                    self.fontRenderTime+=1.0
                    if self.fontRenderTime>=self.fontRenderRemoval:
                        self.renderB = False
                        self.fontRenderTime = 0.0

            if self.VERSION==3:
                if self.renderA and self.fontRenderTime<self.fontRenderRemoval:
                    font = pygame.font.Font(None, 20)
                    text = font.render("Foove", True, WHITE)
                    screen.blit(self.enemy.image, [self.enemy.rect.x,self.enemy.rect.y])
                    screen.blit(text, [self.enemy.rect.x+5,self.enemy.rect.y+80])
                    self.fontRenderTime+=1.0
                    if self.fontRenderTime>=self.fontRenderRemoval:
                        self.renderA = False
                        self.fontRenderTime = 0.0
                elif self.renderB and self.fontRenderTime<self.fontRenderRemoval:
                    font = pygame.font.Font(None, 20)
                    text = font.render("Crelch", True, WHITE)
                    screen.blit(self.enemy.image, [self.enemy.rect.x,self.enemy.rect.y])
                    screen.blit(text, [self.enemy.rect.x+5, self.enemy.rect.y+80])
                    self.fontRenderTime+=1.0
                    if self.fontRenderTime>=self.fontRenderRemoval:
                        self.renderB = False
                        self.fontRenderTime = 0.0

            elif self.VERSION==4:            
                if self.render and self.renderTime<self.renderRemoval:
                    screen.blit(self.enemy.image, [self.enemy.rect.x,self.enemy.rect.y])
                    self.renderTime+=1.0
                    if self.renderTime>=self.renderRemoval:
                        self.render = False
                        self.renderTime = 0.0
             
        pygame.display.flip()