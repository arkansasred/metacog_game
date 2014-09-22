from os import mkdir, path, listdir
import pygame 
from psychopy import core
import pyo
from bullet import Bullet
from enemy import Enemy
from player import Player
from global_variables import *
from random import shuffle

"""No labels training stage"""

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    # --- Class attributes. 
     
    # Sprite lists
    enemyA_list = None
    enemyB_list = None
<<<<<<< HEAD
    numberEnemies = 6 #number of enemies for each group
=======
    numberEnemies = 10 #number of enemies for each group
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
    A1Enemies = ['A1' for i in range (numberEnemies)]
    A2Enemies = ['A2' for i in range (numberEnemies)]
    A3Enemies = ['A3' for i in range (numberEnemies)]
    A4Enemies = ['A4' for i in range (numberEnemies)]
    A5Enemies = ['A5' for i in range (numberEnemies)]
    A6Enemies = ['A6' for i in range (numberEnemies)]
    A7Enemies = ['A7' for i in range (numberEnemies)]
    A8Enemies = ['A8' for i in range (numberEnemies)]
    B1Enemies = ['B1' for i in range(numberEnemies)]
    B2Enemies = ['B2' for i in range(numberEnemies)]
    B3Enemies = ['B3' for i in range(numberEnemies)]
    B4Enemies = ['B4' for i in range(numberEnemies)]
    B5Enemies = ['B5' for i in range(numberEnemies)]
    B6Enemies = ['B6' for i in range(numberEnemies)]
    B7Enemies = ['B7' for i in range(numberEnemies)]
    B8Enemies = ['B8' for i in range(numberEnemies)]
    enemies_list = A1Enemies + A2Enemies + A3Enemies + A4Enemies + A5Enemies + A6Enemies + A7Enemies + A8Enemies + B1Enemies + B2Enemies + B3Enemies + B4Enemies + B5Enemies + B6Enemies + B7Enemies + B8Enemies
    bullet_list = None
    all_sprites_list = None
    player = None
    #Time measurements
    shotTime = []
    captureTime = []
    enemyAKillTime = []
    enemyBKillTime = []
    enemyAWrongHitTime = []
<<<<<<< HEAD
    enemyBWrongHitTime = []
=======
    enembyBWrongHitTime = []
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
    #record when player does not hit the enemy at all (enemy hits player)
    enemyAHitPlayerTime = []
    enemyBHitPlayerTime = []
    # Other data
    score = 0
    maxTrials = 40 #maximum number of enemies to play through
    enemy_live = False #bool to tell us if there is a live enemy
    elapsedTime = 0.0 #keep track of elapsed time via frame rate changes
    enemySpawnTime= 120.0 # of frames between enemy death and next enemy spawn
    ammo = 100
    renderTime = 0.0
    renderRemoval = 120.0
    render = None
    isExplosion_center = False
    isExplosion_enemy = False
    isExplosion_player = False
    explosion_img = pygame.image.load('images/explosion1.bmp')
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
     
    # --- Class methods
    # Set up the game
    def __init__(self):
        shuffle(self.enemies_list)
        print self.enemies_list
        self.score = 0
        self.game_over = False
        self.game_start = True
         
        # Create sprite lists
        self.enemyA_list = pygame.sprite.Group()
        self.enemyB_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()

         
         
        # Create the player
        self.player = Player()
        #shot sound
        self.shot_sound = pyo.SfPlayer("Sounds/laser_shot.aif", mul=0.4)
        #wrong button sound
        self.wrong_button = pyo.SfPlayer("Sounds/wrong_hit.wav")
<<<<<<< HEAD
        self.explosionSound = pyo.SfPlayer("Sounds/explosion.wav", speed=[1,1], mul=0.5)
 
=======
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
 
    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

<<<<<<< HEAD
        def shoot(color, target, degree, origin):
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
=======
        def shoot(color, target, degree):
            self.bullet = Bullet(color, target, degree)
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
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.turnLeft = True
                elif event.key == pygame.K_RIGHT:
                    self.player.turnRight = True
                elif event.key == pygame.K_RETURN:
<<<<<<< HEAD
                    shoot(RED, self.player.currTarget, self.player.degree, (self.player.trueX,self.player.trueY))
=======
                    shoot(RED, self.player.currTarget, self.player.degree)
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
                elif event.key == pygame.K_SPACE:
                    if self.game_start:
                        self.game_start = False
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
        updates positions and checks for collisions.
        """

        def kill_enemy(enemy_type):
            font = pygame.font.Font(None, 25)
            time = core.getTime()
            if enemy_type=='A':
                self.enemyAKillTime.append(time)
                self.render = True
            elif enemy_type=='B':
                self.enemyBKillTime.append(time)
                self.render = True
            self.enemy.pop.out()
            self.score += 20
            self.elapsedTime = 0
            self.enemy_live = False

        if not self.game_start and not self.game_over:
            #create enemy sprites
            if not self.enemy_live and self.elapsedTime==self.enemySpawnTime:
                self.enemy_type = self.enemies_list.pop()
                self.enemy = Enemy(self.enemy_type)
                self.enemy.generate()
                self.all_sprites_list.add(self.enemy)
<<<<<<< HEAD
                if self.enemy_type=='A1' or self.enemy_type=='A2' or self.enemy_type=='A3' or self.enemy_type=='A4' or self.enemy_type=='A5' or self.enemy_type=='A6' or self.enemy_type=='A7' or self.enemy_type=='A8' or self.enemy_type=='A9' or self.enemy_type=='A10' or self.enemy_type=='A11' or self.enemy_type=='A12':
                    self.enemyA_list.add(self.enemy)
                
                elif self.enemy_type=='B1' or self.enemy_type=='B2' or self.enemy_type=='B3' or self.enemy_type=='B4' or self.enemy_type=='B5' or self.enemy_type=='B6' or self.enemy_type=='B7' or self.enemy_type=='B8'or self.enemy_type=='B9' or self.enemy_type=='B10' or self.enemy_type=='B11' or self.enemy_type=='B12':
=======
                if self.enemy_type=='A1' or self.enemy_type=='A2' or self.enemy_type=='A3' or self.enemy_type=='A4' or self.enemy_type=='A5' or self.enemy_type=='A6' or self.enemy_type=='A7' or self.enemy_type=='A8':
                    self.enemyA_list.add(self.enemy)
                
                elif self.enemy_type=='B1' or self.enemy_type=='B2' or self.enemy_type=='B3' or self.enemy_type=='B4' or self.enemy_type=='B5' or self.enemy_type=='B6' or self.enemy_type=='B7' or self.enemy_type=='B8':
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
                    self.enemyB_list.add(self.enemy)
                
                """for every 20 enemies killed/captured, increase speed"""

<<<<<<< HEAD
                if len(self.enemies_list)<(self.numberEnemies*16-1) and (len(self.enemyAKillTime)+len(self.enemyBKillTime))%20 == 0:
=======
                if len(self.enemies_list)<159 and (len(self.enemyAKillTime)+len(self.enemyBKillTime))%20 == 0:
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
                    self.player.rotationSpeed+=1
                    Enemy.speed+=1
                    self.player.speed+=1
                self.enemy_live = True
                
            if self.enemy_live:
                #when enemy enters screen, decrease score    
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
<<<<<<< HEAD
                    self.enemyBWrongHitTime.append(time)
=======
                    self.enembyBWrongHitTime.append(time)
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
                    self.enemy.wrong_hit()
                    self.score -= 20
                    self.isExplosion_enemy = True
                    self.elapsedTime = 0
                    self.enemy_live = False
<<<<<<< HEAD
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
            
 
=======
                    self.render = True
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)

>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea

            if self.player.atCenter:
                if pygame.sprite.spritecollide(self.player, self.enemyB_list, True):
                    time = core.getTime()
                    self.enemyBHitPlayerTime.append(time)
                    self.enemy_live = False
                    self.elapsedTime = 0
                    self.score -= 20
                    self.enemy.wrong_hit()
                
                if pygame.sprite.spritecollide(self.player, self.enemyA_list, True):
<<<<<<< HEAD
                    time = core.getTime()
=======
                    time = core.getTime
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
                    self.enemyAHitPlayerTime.append(time)
                    self.enemy_live = False
                    self.elapsedTime = 0
                    self.score -= 20
                    self.isExplosion_center=True
                    self.explosionSound.out()
            
            elif not self.player.atCenter and self.enemy_live:
                
                if pygame.sprite.spritecollide(self.player, self.enemyB_list, True):
                    if not self.enemy.targetReached:
                        kill_enemy('B')
                        self.player.targetReached = True
                    else:
                        time = core.getTime()
                        self.enemyBHitPlayerTime.append(time)
                        self.enemy_live = False
<<<<<<< HEAD
                        self.enemy.wrong_hit()
=======
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
                        self.elapsedTime = 0
                        self.score -= 20
                
                if pygame.sprite.spritecollide(self.player, self.enemyA_list, True):
<<<<<<< HEAD
                    if not self.enemy.targetReached:
                        time = core.getTime
                        self.enemyAHitPlayerTime.append(time)
                        self.enemy.wrong_hit()
                        self.enemy_live = False
                        self.elapsedTime = 0
                        self.score -= 10
                        self.isExplosion_enemy=True
                        self.player.targetReached=True

                    else:
=======
                    if self.enemy.targetReached:
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
                        time = core.getTime()
                        self.enemyAWrongHitTime.append(time)
                        self.explosionSound.out()
                        self.score -= 20
                        self.isExplosion_player = True
                        self.elapsedTime = 0
                        self.enemy_live = False

<<<<<<< HEAD
=======
                    else:
                        time = core.getTime
                        self.enemyAHitPlayerTime.append(time)
                        self.enemy.wrong_hit()
                        self.enemy_live = False
                        self.elapsedTime = 0
                        self.score -= 10
                        self.isExplosion_center=True

>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea


            """define end of level"""
            if len(self.enemies_list)==0 and not self.enemy_live:
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
<<<<<<< HEAD
=======
        def display_enemies():
            A = pygame.image.load(Enemy.enemyA_images[0])
            A = pygame.transform.scale(A, [75,75])
            A.set_colorkey(WHITE)
            B = pygame.image.load(Enemy.enemyB_images[1])
            B = pygame.transform.scale(B, [75,75])
            B.set_colorkey(WHITE)
            screen.blit(A, [420,420])
            screen.blit(B, [520,420])
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea

        if self.game_over:  
            font = pygame.font.Font(None, 25)
            text2 = font.render("You successfully killed "+ str(len(self.enemyAKillTime)+len(self.enemyBKillTime)) +
<<<<<<< HEAD
                                " out of 96 enemies, for a score of {:.0f}".format(self.score),
=======
                                " out of 16 enemies, for a score of {:.0f}".format(self.score),
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
                                True, GREEN)
            center_x = (SCREEN_WIDTH // 2) - (text2.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) + (text2.get_height() // 2) + 2
            screen.blit(text2, [center_x, center_y])

            
        if self.game_start:
            font = pygame.font.Font(None, 25)
            text = font.render("Hello, thank you for participating in this experiment! You will be using the following buttons for the first level:",
                               True, WHITE)
            text2 = font.render("Space:            Enter:", True, WHITE)
            text3 = font.render ("Press the Space bar to begin", True, WHITE)
<<<<<<< HEAD
            shoot = font.render("SHOOT",True, RED)
            capture = font.render("CAPTURE", True, GREEN)
            center_text(text)
            next_line(text2, 40)
            next_line(text3, 140)
            screen.blit(shoot, [420,420])
            screen.blit(capture, [520,420])
=======
            center_text(text)
            next_line(text2, 40)
            next_line(text3, 140)
            display_enemies()
>>>>>>> 6d046b60d7c3ac6be4a3c27d1a07691d0e6fdfea
            
         
        if not self.game_over and not self.game_start:
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
  

            if self.isExplosion_enemy:
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


            if self.isExplosion_player:
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

            if self.render and self.renderTime<self.renderRemoval:
                screen.blit(self.enemy.image, [self.enemy.rect.x,self.enemy.rect.y])
                self.renderTime+=1.0
                if self.renderTime>=self.renderRemoval:
                    self.render = False
                    self.renderTime = 0.0

                
             
        pygame.display.flip()