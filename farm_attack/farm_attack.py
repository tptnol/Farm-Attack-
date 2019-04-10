# Imports
import pygame
import random
import xbox360_controller

# Initialize game engine
pygame.init()

'''
things to do 
 - share lol

things i have actually done
 - edit the display_stats so that you due the rectangle thingy majigy
 - pixel perfect collision resolution
 - different background music
 - shield / health bar??
'''

# Window
WIDTH = 1600
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Farm Attack!"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)
FPS = 60

# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/orange juice 2.0.ttf", 96)
TITLE_FONT = pygame.font.Font("assets/fonts/kimberly-geswein_kg-small-town-southern-girl/KGSmallTownSouthernGirl.ttf", 200)
SMALL_TITLE_FONT = pygame.font.Font("assets/fonts/kimberly-geswein_kg-small-town-southern-girl/KGSmallTownSouthernGirl.ttf", 100)

# Images
ship_img = pygame.image.load('assets/animals/PNG/Round/narwhal.png').convert_alpha()
damaged_img = pygame.image.load('assets/animals/PNG/Round/gorilla.png').convert_alpha()

laser_img = pygame.image.load('assets/emotes/PNG/Pixel/Style 1/emote_heart.png').convert_alpha()

''' enemies '''
middle_enemy_img = pygame.image.load('assets/animals/PNG/Round/frog.png').convert_alpha()
back_enemy_img = pygame.image.load('assets/animals/PNG/Round/buffalo.png').convert_alpha()
front_enemy_img = pygame.image.load('assets/animals/PNG/Round/parrot.png').convert_alpha()

bomb_img = pygame.image.load('assets/images/evilman.png').convert_alpha()

powerup_img = pygame.image.load('assets/animals/PNG/Round/sloth.png').convert_alpha()

# background
farm_background = pygame.image.load('assets/images/Background/farm_background.jpg').convert()

# Sounds
laser_music = pygame.mixer.Sound('assets/sounds/yay.ogg')
boom_music = pygame.mixer.Sound('assets/sounds/boomfromfrog.ogg')
ouch_music = pygame.mixer.Sound('assets/sounds/ouch.ogg')

start_theme = 'assets/sounds/playingbackground.ogg'
main_theme = 'assets/sounds/startbackground.ogg'
end_theme = None


# Stages
stage = 69

START = 0
PLAYING = 1
BAD_END = 2
GOOD_END = 3

# make a controller
controller = xbox360_controller.Controller(0)

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()

        self.speed = 10

        self.lives = 5

        #self.shot_timer = 0
        
    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
        global shots_taken
        
        laser_music.play()
        print('sound for laser')

        laser = Laser(laser_img)
        
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top

        lasers.add(laser)

        shots_taken += 1
        
        #ship.shot_timer = 20
        
    def update(self):
        global stage
        global lives, score
        
        ''' check if ship feels like a mexican trying to cross the border / edge detection'''
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        ''' remove the cooldown on the shooting '''
        #self.shot_timer -= 1
        
        ''' check if i am loved or not (powerups) '''
        hit_list = pygame.sprite.spritecollide(self, powerups, True,
                                               pygame.sprite.collide_mask)

        for hit in hit_list:
            print('yay sloth hug')
            hit.apply(self)
            
        ''' check if hiroshima merked me or not'''
        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)
        
        for hit in hit_list:
            ouch_music.play()
            print("an enemy bomb has hit me")
            self.lives -= 1
            score -= 1000
            lives -= 1

        ''' check if mob touched me like my uncle '''
        mob_hit_list = pygame.sprite.spritecollide(self, mobs, True,
                                                   pygame.sprite.collide_mask)

        if len(mob_hit_list) > 0:
            self.lives = 0
            self.kill

        ''' change to end when i lose lives ''' 
        if self.lives == 0:
            stage = BAD_END
            set_music(end_theme)

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()

        self.speed = 8

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 6
        
    def drop_bomb(self):
        print('i am currently shooting a bomb')

        bomb = Bomb(bomb_img)
        
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom

        bombs.add(bomb)
        
    def update(self):
        global score
        
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
                                               
        if len(hit_list) > 0:
            boom_music.play()
            print("yeet")
            self.kill()

            score += 100
           
class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()

        self.speed = 3
        
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class HealthPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 6

    def apply(self, ship):
        global lives, score
        
        ship.lives = 5
        lives = 5
        score += 1000

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill
        
class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 1
        self.drop = 5
        self.moving_right = True
        self.bomb_rate = 10

    def move(self):
        hits_edge = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH + 50:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= -50:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        global stage
        
        self.move()
        self.choose_bomber()
        
        mob_list = mobs.sprites()

        ''' game looks to see how many mobs are left and changes speed '''
        if 20 >= len(mob_list) >= 10:
            self.speed = 2
        elif 10 > len(mob_list) > 0:
            self.speed = 5
        elif len(mob_list) == 0:
            stage = GOOD_END
            set_music(end_theme)
            
# Game helper functions
def show_title_screen():

    screen.fill(RED)

    ''' random clouds '''
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGHT)
    
    pygame.draw.ellipse(screen, GREEN, [x, y + 20, 40 , 40])
    pygame.draw.ellipse(screen, GREEN, [x + 60, y + 20, 40 , 40])
    pygame.draw.ellipse(screen, GREEN, [x + 20, y + 10, 25, 25])
    pygame.draw.ellipse(screen, GREEN, [x + 35, y, 50, 50])
    pygame.draw.rect(screen, GREEN, [x + 20, y + 20, 60, 40])

    ''' actual text title '''
    title_text = TITLE_FONT.render("Farm Attack!", 1, WHITE)
    w1 = title_text.get_width()
    h1 = title_text.get_height()
    screen.blit(title_text, [WIDTH/2 - w1/2, HEIGHT/2 - h1/2])

    ''' press button to start '''
    small_title_text = SMALL_TITLE_FONT.render("Press SPACE / START to play", True, WHITE)
    sw = small_title_text.get_width()
    screen.blit(small_title_text, [WIDTH/2 - sw/2, 650])

    ''' now including [insert annoying thing lol] '''
    now_including_text = SMALL_TITLE_FONT.render("CONTROLLER COMPATIBLE!", 1, WHITE)
    w1 = now_including_text.get_width()
    screen.blit(now_including_text, [WIDTH/2 - w1/2, 800])
    
def show_lose_end_screen():
    
    screen.fill(BLACK)

    ''' random clouds '''
    draw_clouds()

    ''' end title text '''
    title_text = TITLE_FONT.render("YOU WERE SLAIN", 1, WHITE)
    w1 = title_text.get_width()
    screen.blit(title_text, [WIDTH/2 - w1/2, 450])

    ''' press space to restart lol '''
    small_title_text = SMALL_TITLE_FONT.render("Press R / X to restart", True, WHITE)
    sw = small_title_text.get_width()
    screen.blit(small_title_text, [WIDTH/2 - sw/2, 650])

def show_win_end_screen():
    
    screen.fill(BLACK)

    ''' random clouds '''
    draw_clouds()

    ''' end title text '''
    title_text = TITLE_FONT.render("YOU WIN!", 1, WHITE)
    w1 = title_text.get_width()
    screen.blit(title_text, [WIDTH/2 - w1/2, 450])

    ''' press r to restart lol '''
    small_title_text = SMALL_TITLE_FONT.render("Press R / X to restart", True, WHITE)
    sw = small_title_text.get_width()
    screen.blit(small_title_text, [WIDTH/2 - sw/2, 650])
    
def show_acc():
    global acc
    
    acc = ((32 / shots_taken) * 100) // 1
    acc_txt = FONT_XL.render('Accuracy: ' + str(acc) + '%', True, WHITE)
    w1 = acc_txt.get_width()
    screen.blit(acc_txt, [WIDTH/2 - w1/2, 800])

def check_acc():
    global score, bonus_points
    
    if acc == 100:
        bonus_points = 1800
    elif acc >= 90:
        bonus_points = 1400
    elif acc >= 80:
        bonus_points = 800
    elif acc >= 50:
        bonus_points = 400
    else:
        bonus_points = 0

def display_end_stats():
    global score, bonus_points
    
    ''' show original score '''
    score_txt = FONT_XL.render(str(score), 1, WHITE)
    score_rect = score_txt.get_rect()
    score_rect.left = 25
    score_rect.top = 100
    screen.blit(score_txt, score_rect)

    ''' bonus points for acc '''
    bonus_points_txt = FONT_XL.render(str(bonus_points), 1, WHITE)
    bonus_points_rect = bonus_points_txt.get_rect()
    bonus_points_rect.left = score_rect.right + 200
    bonus_points_rect.top = 100
    screen.blit(bonus_points_txt, bonus_points_rect)
    
    ''' do the actual final score itself '''
    final_score = score + bonus_points

    final_score_txt = FONT_XL.render(str(final_score), 1, WHITE)
    final_score_rect = final_score_txt.get_rect()
    final_score_rect.left = bonus_points_rect.right + 200
    final_score_rect.top = 100
    screen.blit(final_score_txt, final_score_rect)

    ''' score subtext '''
    score_subtxt = FONT_MD.render('Actual Score!', True, WHITE)
    scores_subtxt_rect = score_subtxt.get_rect()
    scores_subtxt_rect.left = score_rect.left
    scores_subtxt_rect.bottom = score_rect.top - 10
    screen.blit(score_subtxt, scores_subtxt_rect)

    ''' bonus points subtext '''
    bonus_score_subtxt = FONT_MD.render('Bonus Points!', True, WHITE)
    bonus_scores_subtxt_rect = bonus_score_subtxt.get_rect()
    bonus_scores_subtxt_rect.left = bonus_points_rect.left
    bonus_scores_subtxt_rect.bottom = bonus_points_rect.top - 10
    screen.blit(bonus_score_subtxt, bonus_scores_subtxt_rect)
    
    ''' final score subtext  '''
    final_score_subtxt = FONT_MD.render('Final Score!', True, WHITE)
    final_scores_subtxt_rect = final_score_subtxt.get_rect()
    final_scores_subtxt_rect.left = final_score_rect.left
    final_scores_subtxt_rect.bottom = final_score_rect.top - 10
    screen.blit(final_score_subtxt, final_scores_subtxt_rect)

    ''' extra info underneath the bonus points '''
    score_extrainfo_subtxt = FONT_MD.render('Get a higher accuracy to get more points!', True, WHITE)
    scores_extrainfo_subtxt_rect = score_extrainfo_subtxt.get_rect()
    scores_extrainfo_subtxt_rect.centerx = bonus_points_rect.centerx
    scores_extrainfo_subtxt_rect.top = bonus_points_rect.bottom + 20
    screen.blit(score_extrainfo_subtxt, scores_extrainfo_subtxt_rect)

def display_stats():
    global stage
    
    ''' score '''
    score_subtxt = SMALL_TITLE_FONT.render('Score', True, WHITE)
    scores_subtxt_rect = score_subtxt.get_rect()
    scores_subtxt_rect.left = 25
    scores_subtxt_rect.top = 0
    screen.blit(score_subtxt, scores_subtxt_rect)
    
    score_txt = FONT_XL.render(str(score), 1, WHITE)
    score_rect = score_txt.get_rect()
    score_rect.left = 25
    score_rect.top = 100
    screen.blit(score_txt, score_rect)

    if stage == GOOD_END:
        ''' Lives ''' 
        lives_subtxt = SMALL_TITLE_FONT.render('Health', True, WHITE)
        lives_subtxt_rect = lives_subtxt.get_rect()
        lives_subtxt_rect.right = WIDTH - 20
        lives_subtxt_rect.top = 0
        screen.blit(lives_subtxt, lives_subtxt_rect)

    ''' replaced by the health bar '''
    #lives_txt = FONT_XL.render(str(lives), 1, WHITE)
    #lives_rect = lives_txt.get_rect()
    #lives_rect.right = WIDTH - 50
    #lives_rect.top = 100
    #screen.blit(lives_txt, lives_rect)

def set_music(track):

    if track != None:  
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)
        
def setup():
    global stage, done
    global score, lives, shots_taken
    global player, ship, lasers, mobs, fleet, bombs, powerups
    
    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30
    

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    lasers = pygame.sprite.Group()

    ''' first row '''
    mob1 = Mob(0, 0, back_enemy_img)
    mob2 = Mob(200, 0, back_enemy_img)
    mob3 = Mob(400, 0, back_enemy_img)
    mob4 = Mob(600, 0, back_enemy_img)
    mob5 = Mob(800, 0, back_enemy_img)
    mob6 = Mob(1000, 0, back_enemy_img)
    mob7 = Mob(1200, 0, back_enemy_img)
    mob8 = Mob(1400, 0, back_enemy_img)

    '''second row'''
    mob9 = Mob(100, 50, middle_enemy_img)
    mob10 = Mob(300, 50, middle_enemy_img)
    mob11 = Mob(500, 50, middle_enemy_img)
    mob12 = Mob(700, 50, middle_enemy_img)
    mob13 = Mob(900, 50, middle_enemy_img)
    mob14 = Mob(1100, 50, middle_enemy_img)
    mob15 = Mob(1300, 50, middle_enemy_img)
    mob16 = Mob(1500, 50, middle_enemy_img)

    '''third row'''
    mob17 = Mob(0, 100, front_enemy_img)
    mob18 = Mob(200, 100, front_enemy_img)
    mob19 = Mob(400, 100, front_enemy_img)
    mob20 = Mob(600, 100, front_enemy_img)
    mob21 = Mob(800, 100, front_enemy_img)
    mob22 = Mob(1000, 100, front_enemy_img)
    mob23 = Mob(1200, 100, front_enemy_img)
    mob24 = Mob(1400, 100, front_enemy_img)

    '''fourth row'''
    mob25 = Mob(100, 150, back_enemy_img)
    mob26 = Mob(300, 150, back_enemy_img)
    mob27 = Mob(500, 150, back_enemy_img)
    mob28 = Mob(700, 150, back_enemy_img)
    mob29 = Mob(900, 150, back_enemy_img)
    mob30 = Mob(1100, 150, back_enemy_img)
    mob31 = Mob(1300, 150, back_enemy_img)
    mob32 = Mob(1500, 150, back_enemy_img)

    mobs = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    
    mobs.add(mob1, mob2, mob3, mob4,
             mob5, mob6, mob7, mob8,
             mob9, mob10, mob11, mob12,
             mob13, mob14, mob15, mob16,
             mob17, mob18, mob19, mob20,
             mob21, mob22, mob23, mob24,
             mob25, mob26, mob27, mob28,
             mob29, mob30, mob31, mob32)

    powerup1 = HealthPowerUp(200, -2000, powerup_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1)
    
    fleet = Fleet(mobs)
    
    shots_taken = 0
    
    score = 0
    lives = 5
    
    ''' set stage '''
    stage = START
    done = False

    ''' music '''
    set_music(start_theme)

# draw functions

def draw_background():
    screen.blit(farm_background, [0, 0])

def draw_clouds():
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGHT)
    
    pygame.draw.ellipse(screen, GREEN, [x, y + 20, 40 , 40])
    pygame.draw.ellipse(screen, GREEN, [x + 60, y + 20, 40 , 40])
    pygame.draw.ellipse(screen, GREEN, [x + 20, y + 10, 25, 25])
    pygame.draw.ellipse(screen, GREEN, [x + 35, y, 50, 50])
    pygame.draw.rect(screen, GREEN, [x + 20, y + 20, 60, 40])
    
def draw_health_bar():
    # the size of the screen is 1600 wide by 1000 height
    ''' 100 down, 50 from the right '''
    pygame.draw.rect(screen, BLACK, [1370, 95, 210, 60])
    pygame.draw.rect(screen, WHITE, [1375, 100, 200, 50])

    if lives == 5:
        pygame.draw.rect(screen, GREEN, [1375, 100, 200, 50])
    if lives == 4:
        pygame.draw.rect(screen, YELLOW, [1375, 100, 160, 50])
    if lives == 3:
        pygame.draw.rect(screen, YELLOW, [1375, 100, 120, 50])
        ship.image = damaged_img
    if lives == 2:
        pygame.draw.rect(screen, RED, [1375, 100, 80, 50])
    if lives == 1:
        pygame.draw.rect(screen, RED, [1375, 100, 40, 50])
        
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                
            if stage == START:
                if event.key == pygame.K_SPACE:
                    set_music(main_theme)
                    stage = PLAYING
                    
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                if event.key == pygame.K_k:
                    stage = BAD_END
                    set_music(end_theme)
                if event.key == pygame.K_l:
                    stage = GOOD_END
                    set_music(end_theme)
        
            elif stage == BAD_END:
                if event.key == pygame.K_r:
                    setup()

            elif stage == GOOD_END:
                if event.key == pygame.K_r:
                    setup()

        ''' more controller crap yay '''
        if event.type == pygame.JOYBUTTONDOWN:
            if stage == START:
                if event.button == xbox360_controller.START:
                    set_music(main_theme)
                    stage = PLAYING
                    
            elif stage == PLAYING:
                if event.button == xbox360_controller.A:
                    ship.shoot()
                    
            elif stage == BAD_END:
                if event.button == xbox360_controller.X:
                    setup()
            elif stage == GOOD_END:
                if event.button == xbox360_controller.X:
                    setup()
                    
    pressed = pygame.key.get_pressed()
    
    # joystick stuff                

    left_x, left_y = controller.get_left_stick()
        
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        
        if pressed[pygame.K_a]:
            ship.move_left()
        elif pressed[pygame.K_d]:
            ship.move_right()

        if pressed[pygame.K_w]:
            ship.move_up()
        elif pressed[pygame.K_s]:
            ship.move_down()

        ''' controller things '''
        #if a_btn == 1:
            #ship.shoot()

        ''' controller movement ''' 
        ship.rect.x += int(left_x * 15)
        ship.rect.y += int(left_y * 15)
        

        ''' updates ''' 
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        powerups.update()
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == PLAYING:
        
        draw_background()
        lasers.draw(screen)
        bombs.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        powerups.draw(screen)

        display_stats()
        draw_health_bar()
    
    if stage == START:
        show_title_screen()
        
    if stage == BAD_END:
        show_lose_end_screen()
        display_stats()
        
    if stage == GOOD_END:
        show_win_end_screen()
        show_acc()
        check_acc()
        display_end_stats()
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()
