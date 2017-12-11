from pygame import *
import pygame, sys, random, math
from os import path

pygame.init()
pygame.mixer.init()

display_width = 900;    #setup the width of the display
display_height = 451;
HS_file = 'highscore.txt'
gamefont = pygame.font.SysFont(None, 30)
velocity_index = 0
velocity = [-8.5,-8,-7.5,-7,-6.0, -5.9000000000000004, -5.8000000000000007, -5.7000000000000011,
 -5.6000000000000014, -5.5000000000000018, -5.4000000000000021, -5.3000000000000025,
  -5.2000000000000028, -5.1000000000000032, -5.0000000000000036, -4.9000000000000039, -4.8000000000000043, -4.7000000000000046, -4.600000000000005, -4.5000000000000053, -4.4000000000000057, -4.300000000000006, -4.2000000000000064, -4.1000000000000068, -4.0000000000000071, -3.9000000000000075, -3.8000000000000078, -3.7000000000000082, -3.6000000000000085, -3.5000000000000089, -3.4000000000000092, -3.3000000000000096, -3.2000000000000099, -3.1000000000000103, -3.0000000000000107, -2.900000000000011, -2.8000000000000114,
   -2.7000000000000117, -2.6000000000000121, -2.1000000000000139, -2.0000000000000142, -1.9000000000000146, -1.8000000000000149, -1.7000000000000153, -1.6000000000000156, -1.500000000000016, -1.4000000000000163, -1.3000000000000167, -1.2000000000000171, -1.1000000000000174, -1.0000000000000178, -0.90000000000001812, -0.80000000000001847, -0.70000000000001883, -0.60000000000001918, -0.50000000000001954, -0.4000000000000199, -0.30000000000002025,
   -0.20000000000002061, -0.10000000000002096,
   -2.1316282072803006e-14,  0.6999999999999762, 0.79999999999997584, 0.89999999999997549, 0.99999999999997513, 1.0999999999999748,  1.2999999999999741, 1.3999999999999737, 1.4999999999999734, 1.599999999999973, 1.6999999999999726, 1.7999999999999723, 1.8999999999999719, 1.9999999999999716, 2.0999999999999712, 2.1999999999999709, 2.2999999999999705, 2.3999999999999702,  2.8999999999999684, 2.999999999999968, 3.0999999999999677, 3.1999999999999673,
   3.299999999999967, 3.3999999999999666, 3.4999999999999662, 3.5999999999999659, 3.6999999999999655, 3.7999999999999652, 3.8999999999999648, 3.9999999999999645, 4.0999999999999641, 4.1999999999999638, 4.2999999999999634, 4.3999999999999631, 4.4999999999999627, 4.5999999999999623,
  4.699999999999962,  4.7999999999999616,4.8999999999999613,4.9999999999999609, 5.0999999999999606,5.1999999999999602,5.2999999999999599, 5.3999999999999595, 5.4999999999999591, 5.5999999999999588, 5.6999999999999584, 5.7999999999999581, 5.8999999999999577,6,7,7.5,8,8.5]

arrow_img = image.load('arrow.png')
background = image.load('game_background.png')
giraf_img = image.load('baby_giraf.png')
go_img = image.load('gameover.png')
lion_img = image.load('lion.png')
con_img = image.load('cong.png')

class lion(pygame.sprite.Sprite):

    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load("lion.png")
        self.rect = self.image.get_rect()
        self.rect.x = (display_width *0.85) +300
        self.rect.y = (display_height * 0.58)
        self.speedx = random.uniform(4.5,5.9)

    def update(self):
        self.rect.x -= self.speedx;
        if self.rect.x < -600:
            self.rect.x = (display_width *0.85)+300
            self.rect.y = (display_height * 0.58)
            self.speedx = random.uniform(4.5,8.63)

class Player(pygame.sprite.Sprite):

    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = giraf_img
        self.rect = self.image.get_rect()
        self.rect.x = (900 * 0.15)
        self.rect.y = (451 * 0.58)
        self.velocity_index = 0
        self.jumping = False

    def do_jump(self):
        global velocity
        if self.jumping:
            self.rect.y += velocity[self.velocity_index];
            self.velocity_index +=1;
            if self.velocity_index >= len(velocity) -1:
                self.velocity_index = len(velocity) -1;
                if self.rect.y > (display_height * 0.58):
                    self.rect.y = (display_height * 0.58);
                    self.jumping = False;
                    self.velocity_index = 0

clock = pygame.time.Clock()
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.back_x =0
        self.FPS = 60
        self.display_width = 900;
        self.display_height = 451;

        # clock = pygame.time.Clock()
        self.display_game =  display.set_mode((self.display_width, self.display_height))
        self.display_game.blit(background, (0,0));
        title_game = display.set_caption("Save the baby giraffe!")
        self.clock =pygame.time.Clock()
        self.running = True

        # self.font_name = pygame.font.match_font(gamefont)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir,HS_file),'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        self.timer =0
        self.all_sprites = pygame.sprite.Group()
        self.lionsgroup = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.lions = lion(self)
        self.all_sprites.add(self.lions)
        self.lionsgroup.add(self.lions)
        self.run()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick()/1000
            self.events()
            self.update()
            self.player.do_jump()
            self.draw()
            self.tik()


    def update(self):
        self.all_sprites.update()

        #stop game when lion hits giraffe
        hit = pygame.sprite.spritecollide(self.player,self.lionsgroup, False, pygame.sprite.collide_mask)
        if hit:
            self.playing = False;



    def events(self):

        # Game Loop - events
        for event in pygame.event.get():

            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.jumping == False:
                    self.player.jumping = True



    def draw(self):

        # Roll the screen infinitely
        rel_x = self.back_x % background.get_rect().width
        self.display_game.blit(background,(rel_x - background.get_rect().width  ,0));
        if rel_x < display_width:
            self.display_game.blit(background, (rel_x, 0))
            self.back_x -=2;

        # draw all the sprites
        self.all_sprites.draw(self.display_game)

        # get the timer on to run the score
        self.display_timer = math.trunc(self.timer)
        self.timer_text = gamefont.render('Your score: ' +str(self.display_timer), 1, [105,0,105])
        boxsize = self.timer_text.get_rect()
        timerXpos = (self.display_width-boxsize[2])/1.13 + 80
        self.display_game.blit(self.timer_text, [timerXpos, 20])

        # show the highscore
        scorefont = pygame.font.SysFont('Arial black',20)
        score_end = scorefont.render('High score: ' +str(self.highscore), 1, [105,0,105])
        self.display_game.blit(score_end, (570,13))

        pygame.display.update()

    def tik(self):

        #let the score tik with each second
        seconds = self.clock.tick()/1000;
        self.timer+=seconds

    def start_screen(self):

        #layout screen
        myfont = pygame.font.SysFont(None,45)
        myfont1 = pygame.font.SysFont('comicsansms',19)
        label = myfont.render("Welcome to the world of our baby giraffe.",1,(155,0,150))
        scorefont = pygame.font.SysFont('Arial black',20)
        score_end = scorefont.render('High score: ' +str(self.highscore), 1, [105,0,105])
        self.display_game.blit(score_end, (700,12))
        self.display_game.blit(label,(150,100))
        label1 = myfont.render("Can you save the giraffe from the mean lions?",1,(155,0,150))
        self.display_game.blit(label1,(130,135))
        label2 = myfont1.render("> Enter SPACE and TAB to play",1,(125,0,0))
        self.display_game.blit(label2,(350,377))
        self.display_game.blit(giraf_img, (200,(451 * 0.58)))
        self.display_game.blit(arrow_img,(400,175))
        # start_sound.play()
        pygame.display.flip()
        #wait for space to run while loop
        self.wait_for_key()

    def game_over_screen(self):
        # if playing and quit is clicked on
        if not self.running:
            return

        #layout screen
        self.display_game.blit(background, (0,0));
        myfont1 = pygame.font.SysFont('comicsansms',19)
        label1 = myfont1.render("> Enter SPACE and TAB to try again",1,(125,0,0))
        self.display_game.blit(label1,(330,377))
        self.display_game.blit(go_img, (300,30))
        scorefont = pygame.font.SysFont('Arial black',30)
        score_end = scorefont.render('Your Final score: ' +str(self.display_timer), 1, [105,0,105])
        self.display_game.blit(score_end, (300,280))
        if self.display_timer >= self.highscore:
            self.highscore = self.display_timer
            labelh = scorefont.render("NEW HIGH SCORE!!!",1,(105,0,105))
            self.display_game.blit(labelh,(285,240))
            self.display_game.blit(con_img,(750,340))
            self.display_game.blit(con_img,(750,20))
            self.display_game.blit(con_img,(20,20))
            self.display_game.blit(con_img,(20,340))
            with open(path.join(self.dir,HS_file),'w') as f:
                f.write(str(self.highscore))

        pygame.display.update()

        #wait for space to play the game// run the while loop again
        self.wait_for_key()

    # function: pressing space will bring you to g.new()/ game loop
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick()/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and keys[pygame.K_TAB]:
                # if event.type == pygame.KEYUP:
                    # if event.key == pygame.K_SPACE: #and event.key == pygame.K_TAB:
                    waiting = False
                    pygame.event.pump()
#Running the game
g = Game()
g.start_screen()

while g.running:
    g.new()
    g.game_over_screen()
pygame.quit()
