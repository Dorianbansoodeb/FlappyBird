# Dorian Bansoodeb FlappyBird Game
# Developped using the python libraries

import random
import pygame
import pygame as pg
import sys
import time
import copy
import os



# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 94, 0)
YELLOW = (242, 255, 0)
GREEN = (4, 255, 0)
BLUE = (0, 234, 255)
PURPLE = (119, 0, 255)
PINK = (255, 125, 231)

# DIMENSIONS
WIDTH = 800
HEIGHT = 600

# PHYSICS
GRAVITY = 0.8
JUMP_VELOCITY = -10
FALL_MULTIPLIER = 0.2
STARTING_VEL = 0

# BIRD
STARTING_Y = HEIGHT // 2
STARTING_X = 100
BIRD_SIZE = 35

# FRAME CAP
FPS = 60

OBJ_SPEED = 1

OBJ_WIDTH = 100
OBJ_HEIGHT = 50

#SOUNDS
pg.mixer.init()
pg.mixer.music.set_volume(0.1)
JUMP_SOUND = pygame.mixer.Sound("jump_sound.mp3")
DEATH_SOUND = pygame.mixer.Sound("death_sound.mp3")



brick_maptemp = [
    ["B"],
    ["B"],
    ["B"],
    ["B"],
    ["B"],
    ["B"],
    ["B"],
    ["B"],
    ["B"],
    ["B"],
    ["B"],
    ["B"],
]

play_button = pg.image.load("play_button.png")
exit_button = pg.image.load("exit_button.png")
retry_button = pg.image.load("retry_button.png")
menu_button = pg.image.load("menu_button.png")
lb_button = pg.image.load("lb_button.png")
left_button = pg.image.load("left_button.png")
right_button = pg.image.load("right_button.png")
select_button = pg.image.load("select_button.png")
skins_button = pg.image.load("skins_button.png")
share_button = pg.image.load("share_button.png")



class Button():

    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def render_button(self):
        action = False

        pos = pg.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# MAIN CLASS
class Game():

    def __init__(self):
        pg.display.set_caption('Flappy Bird')
        pg.init()
        self.stack_of_skins = ["Bird_1.png", "Bird_2.png", "Bird_3.png"]
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.Background=pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()
        self.bird_v = STARTING_VEL
        self.bird_y = STARTING_Y
        self.in_menu = True
        self.in_idle = False
        self.in_skins = False
        self.in_lb = False
        self.in_share = False
        self.dead = False
        self.score = 0
        self.active_rectangles = []
        self.column = 0
        self.combined_object = pg.Rect(700, 0, OBJ_WIDTH, 0)
        self.scored = False

        #TYPING

        #OBJECTS
        self.g_brick = pg.image.load("g_brick.png")
        self.brickmap_obj = []

        #TITLES
        self.getready = pg.image.load("getready.png")
        self.getready = pg.transform.scale(self.getready, (self.getready.get_width() * 3.5, self.getready.get_height() * 3.5))
        self.pressspace = pg.image.load("press_space.png")
        self.pressspace = pg.transform.scale(self.pressspace, (self.pressspace.get_width() * 3.5, self.pressspace.get_height() * 3.5))
        self.gameover = pg.image.load("gameover.png")
        self.gameover = pg.transform.scale(self.gameover, (self.gameover.get_width() * 4.3, self.gameover.get_height() * 4.3))
        self.score_bg = pg.image.load("score_button.png")
        self.score_bg = pg.transform.scale(self.score_bg, (self.score_bg.get_width() * 4.3, self.score_bg.get_height() * 4.3))
        self.lb_bg = pg.image.load("lb_bg.png")
        self.lb_bg = pg.transform.scale(self.lb_bg , (self.lb_bg .get_width() * 4.3, self.lb_bg .get_height() * 4.3))
        self.text_box = pg.image.load("text_box.png")
        self.text_box = pg.transform.scale(self.text_box , (self.text_box .get_width() * 10.5, self.text_box .get_height() * 10.5))

        #BACKGROUNDS
        self.bg_main = pg.image.load("bg_main.png")
        self.bg_main = pg.transform.scale(self.bg_main, (800, 600))
        self.bg_play = pg.image.load("bg_play.png")
        self.bg_play = pg.transform.scale(self.bg_play, (801, 601))
        self.bg_dead = pg.image.load("bg_dead.png")
        self.bg_dead = pg.transform.scale(self.bg_dead, (801, 601))

        #BIRD SKINS
        self.bird_img = pg.image.load("Bird_1.png")
        self.bird_img = pg.transform.scale(self.bird_img, (BIRD_SIZE * 1.3, BIRD_SIZE))

        self.bird_img2 = pg.image.load("Bird_2.png")
        self.bird_img = pg.transform.scale(self.bird_img, (BIRD_SIZE * 1.3, BIRD_SIZE))

        self.bird_img3 = pg.image.load("Bird_3.png")
        self.bird_img = pg.transform.scale(self.bird_img, (BIRD_SIZE * 1.3, BIRD_SIZE))
        

        #BUTTONS
        self.play_button = Button(WIDTH // 2 - play_button.get_width() // 4, 330, play_button, 0.5)

        self.exit_button = Button(WIDTH // 2 - exit_button.get_width() // 4, 405, exit_button, 0.5)

        self.retry_button = Button(WIDTH // 2 - retry_button.get_width() // 4, 450, retry_button, 0.5)

        self.menu_button = Button(WIDTH // 2 - menu_button.get_width() // 2 - 66, 385, menu_button, 4.3)

        self.idle_menu_button = Button(WIDTH // 2 - menu_button.get_width() // 2 - 66, 450, menu_button, 4.3)

        self.menu_lb_button = Button(WIDTH // 2 - lb_button.get_width() // 2 - 98, 480, lb_button, 4.3)

        self.death_lb_button = Button(WIDTH // 2 - lb_button.get_width() // 2 - 98, 520, lb_button, 4.3)


        self.left_button = Button(100 - left_button.get_width() // 2, HEIGHT // 2, left_button, 4.3)

        self.right_button = Button((WIDTH - 147) - right_button.get_width() // 2, HEIGHT // 2, right_button, 4.3)


        self.select_button = Button(WIDTH // 2 - select_button.get_width() // 2 - 66, 420, select_button, 4.3)

        self.skins_button = Button(WIDTH // 8 + 50 - skins_button.get_width() // 2 - 66, 430, skins_button, 4.3)

        self.share_button = Button(WIDTH // 2 + 190 - share_button.get_width() // 2 - 66, 320, share_button, 4.3)

        pg.display.set_icon(self.bird_img)


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            # KEYSTROKES
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE and not self.in_menu and not self.dead and not self.in_idle and not self.in_skins and not self.in_lb and not self.in_share:
                    self.bird_v = JUMP_VELOCITY
                    JUMP_SOUND.play()

                elif event.type == pg.KEYDOWN and self.in_share:
                    if event.key == pg.K_BACKSPACE:
                        text_type = text_type[:-1]
                    else:
                        text_type += event.unicode 

                elif event.key == pg.K_SPACE and self.in_idle:
                    self.in_idle = False

                elif event.key == pg.K_ESCAPE:
                    self.quit()
                    

    def update(self):
        if not self.in_menu and not self.dead and not self.in_idle and not self.in_skins and not self.in_lb and not self.in_share:
            self.bird_y += self.bird_v
            self.bird_v += GRAVITY

            # Bottom Border
            if self.bird_y >= 540:
                self.bird_y = 600
                self.bird_v = 0
                self.dead = True
                DEATH_SOUND.play()

            # Top Border
            if self.bird_y <= 0:
                self.bird_y = 0

            # Check collision with gaps
            for rect in self.active_rectangles:
                if rect.colliderect(self.bird_rect):
                    self.active_rectangles = []
                    self.column = 0
                    self.dead = True 
                    DEATH_SOUND.play()


    def mapgen(self):
        brick_map2 = [["B"],["B"],["B"],["B"],["B"],["B"],["B"],["B"],["B"],["B"],["B"],["B"]]

        gap_height = random.randint(3, 5)

        if gap_height == 3:
            gap_loc = random.randint(1, 8)
            for i in range(gap_height):
                brick_map2[gap_loc][0] = "A"
                gap_loc += 1

        elif gap_height == 4:
            gap_loc = random.randint(1, 7)
            for i in range(gap_height):
                brick_map2[gap_loc][0] = "A"
                gap_loc += 1

        elif gap_height == 5:
            gap_loc = random.randint(1, 6)
            for i in range(gap_height):
                brick_map2[gap_loc][0] = "A"
                gap_loc += 1
        
        return brick_map2


    def writelb(self, initials, val):
        file = open("leaderboard", "w")
        file.write(initials, val)


    def quit(self):
        pg.quit()
        sys.exit()


    def render(self):
        self.screen.fill(WHITE)

        if self.dead:
            self.render_death()
        elif self.in_menu:
            self.render_menu()
        elif self.in_skins:
            self.render_skins()
        elif self.in_idle:
            self.render_idle_fly()
        elif self.in_lb:
            self.render_lb()
        elif self.in_share:
            self.render_share()
        else:
            self.render_main()
            self.render_obj()
            self.render_text()

        pg.display.update()


    def text(self, text, colour, font, pos):
        font = pg.font.SysFont(font, 40)
        chars = font.render(text, 1, colour)
        text_rect = chars.get_rect(center=pos)
        self.screen.blit(chars, text_rect)


    def render_menu(self):
        self.Background.blit(self.bg_play, (-1, -1))

        if self.play_button.render_button() == True:
            self.active_rectangles = []
            self.column = -1
            self.bird_v = 0
            self.score = 0
            self.in_idle = True
            self.in_menu = False
            self.bird_y = STARTING_Y

        if self.exit_button.render_button() == True:
            pass

        if self.menu_lb_button.render_button() == True:
            self.in_menu = False
            self.in_lb = True
            
        if self.skins_button.render_button() == True:
            self.in_idle = False
            self.dead = False
            self.in_menu = False
            self.in_skins = True

        self.bird_select = pg.image.load("Bird_2.png")
        self.bird_select = pg.transform.scale(self.bird_img, (BIRD_SIZE * 2.6, BIRD_SIZE * 2))

        rect = self.bird_select.get_rect()
        rect.center = (WIDTH // 8 + 50, HEIGHT // 3 * 2 - 20)
        self.screen.blit(self.bird_select, rect)

        logo = pg.image.load("logo.png")
        logo = pg.transform.scale(logo, (logo.get_width() * 0.5, logo.get_height() * 0.5))

        rect = logo.get_rect()
        rect.center = (WIDTH // 2, 200)


        self.screen.blit(logo, rect)


    def render_lb(self):
        self.Background.blit(self.bg_play, (-1, -1))

        rect = self.lb_bg.get_rect()
        rect.center = (WIDTH // 2, 220)
        self.screen.blit(self.lb_bg, rect)

        scores_list = []

        with open("leaderboard.txt", 'r') as file:
            file = file.readlines()

        for lines in file:
            score = lines.strip()
            scores_list.append(int(score))

        for i in range(len(scores_list)-1, 0, -1):
            min_loc = i
            for j in range(i):
                if scores_list[j] < scores_list[min_loc]:
                    min_loc = j
            temp = scores_list[i]
            scores_list[i] = scores_list[min_loc]
            scores_list[min_loc] = temp

        #print(scores_list)

        title = "| High Scores |"
        line_1 = scores_list[0]
        line_2 = scores_list[1]
        line_3 = scores_list[2]
        line_4 = scores_list[3]
        line_5 = scores_list[4]

        font = pg.font.Font(None, 45)
        text = font.render(str(title), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 90) 
        self.screen.blit(text, text_rect)

        font = pg.font.Font(None, 45)
        text = font.render(str(line_1), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 140) 
        self.screen.blit(text, text_rect)

        font = pg.font.Font(None, 45)
        text = font.render(str(line_2), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 190) 
        self.screen.blit(text, text_rect)

        font = pg.font.Font(None, 45)
        text = font.render(str(line_3), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 240) 
        self.screen.blit(text, text_rect)

        font = pg.font.Font(None, 45)
        text = font.render(str(line_4), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 290) 
        self.screen.blit(text, text_rect)

        font = pg.font.Font(None, 45)
        text = font.render(str(line_5), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 340) 
        self.screen.blit(text, text_rect)

        if self.menu_button.render_button() == True:
            self.in_skins = False
            self.in_idle = False
            self.dead = False
            self.in_lb = False
            self.in_menu = True

        
    def render_share(self):
        self.Background.blit(self.bg_play, (-1, -1))

        rect = self.text_box.get_rect()
        rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
        self.screen.blit(self.text_box, rect)

        message1 = "Your Score of " + str(self.score) + " Has Been"
        message2 = "Added to the Leaderboard!"

        font = pg.font.Font(None, 45)
        text = font.render(str(message1), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 220) 
        self.screen.blit(text, text_rect)
        
        font = pg.font.Font(None, 45)
        text = font.render(str(message2), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 270) 
        self.screen.blit(text, text_rect)

        player_name = "Anonymous"

        if self.menu_button.render_button() == True:
            with open("leaderboard.txt", "a") as file:
                file.write(f'{self.score}\n')
            self.in_skins = False
            self.in_idle = False
            self.dead = False
            self.in_lb = False
            self.in_share = False
            self.in_menu = True


    def render_skins(self):
        self.Background.blit(self.bg_play, (-1, -1))

        self.stack_of_skins

        if self.right_button.render_button() == True:
            current_skin = self.stack_of_skins.pop(0)  # Pop the first element from the list
            self.stack_of_skins.append(current_skin)  # Push the value to the end of the list

        if self.left_button.render_button() == True:
            current_skin = self.stack_of_skins.pop()  # Pop the last element from the list
            self.stack_of_skins.insert(0, current_skin)  # Insert the value at the beginning of the list

        if self.select_button.render_button() == True:
            self.bird_img = pg.image.load(self.stack_of_skins[0])
            self.bird_img = pg.transform.scale(self.bird_img, (BIRD_SIZE * 1.3, BIRD_SIZE))
            self.in_skins = False
            self.in_idle = False
            self.dead = False
            self.in_menu = True

        self.bird_select_skins = pg.image.load(self.stack_of_skins[0])
        self.bird_select_skins = pg.transform.scale(self.bird_select_skins, (BIRD_SIZE * 3.9, BIRD_SIZE * 3))
        rect = self.bird_select_skins.get_rect()
        rect.center = (WIDTH // 2, HEIGHT // 2)
        self.screen.blit(self.bird_select_skins, rect)


    def render_idle_fly(self):
        self.Background.blit(self.bg_play, (-1, -1))

        rect = self.getready.get_rect()
        rect.center = (WIDTH // 2, 200)
        self.screen.blit(self.getready, rect)

        rect = self.pressspace.get_rect()
        rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
        self.screen.blit(self.pressspace, rect)

        rect = self.bird_img.get_rect()
        rect.center = (STARTING_X, HEIGHT // 2)
        self.screen.blit(self.bird_img, rect)

        if self.idle_menu_button.render_button() == True:
            self.active_rectangles = []
            self.column = 0
            self.score = 0
            self.in_menu = True
            self.bird_y = STARTING_Y


    def render_death(self):
        #Render Bakcground
        self.Background.blit(self.bg_play, (-1, -1))


        rect = self.gameover.get_rect()
        rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
        self.screen.blit(self.gameover, rect)

        rect = self.score_bg.get_rect()
        rect.center = (WIDTH // 2, 350)
        self.screen.blit(self.score_bg, rect)

        #SCORE VALUE
        font = pg.font.Font(None, 50)
        text = font.render(str(self.score), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2 + 50, 350) 
        self.screen.blit(text, text_rect)


        #BUTTON
        if self.death_lb_button.render_button() == True:
            self.dead = False
            self.in_lb = True

        if self.share_button.render_button() == True:
            self.dead = False
            self.in_share = True

        if self.retry_button.render_button() == True:
            self.active_rectangles = []
            self.column = -1
            self.bird_v = 0
            self.score = 0
            self.dead = False
            self.bird_y = STARTING_Y

        if self.menu_button.render_button() == True:
            self.active_rectangles = []
            self.column = 0
            self.score = 0
            self.dead = False
            self.in_menu = True
            self.bird_y = STARTING_Y


    def render_main(self):
        self.Background.blit(self.bg_main, (0, 0))
        self.bird_rect = self.bird_img.get_rect(center=(STARTING_X, int(self.bird_y)))
        bird_rect = self.bird_img.get_rect(center=(STARTING_X, int(self.bird_y)))
        self.screen.blit(self.bird_img, bird_rect)


    def render_obj(self):
        # Move the combined object to the left

        # Check if the combined object has moved past the halfway mark
        self.scored = False

        for rect in self.active_rectangles: 
            if rect.right == 100 and self.scored == False:
                self.score += 1
                self.scored = True

            if rect.right != 100:
                self.scored = False

        if self.combined_object.right < WIDTH // 2 + 100:
            self.brickmap_obj = self.mapgen()
            self.combined_object.x = WIDTH
            self.combined_object.height = 0

        # Draw each object in the list
        for row in range(len(self.brickmap_obj)):
            if self.brickmap_obj[row][0] == "B":
                obj_y = row * OBJ_HEIGHT
                obj_rect = pygame.Rect(self.combined_object.x, obj_y, OBJ_WIDTH, OBJ_HEIGHT)
                self.active_rectangles.append(obj_rect)

        # Move and draw each active rectangle
        for rect in self.active_rectangles:
            rect.move_ip(-4, 0)
            self.screen.blit(self.g_brick, rect)

        self.combined_object = self.combined_object.move(-4, 0)

        self.active_rectangles = [rect for rect in self.active_rectangles if rect.right > 0]


    def render_text(self):

        bg_score = pg.image.load("bgscore.png")
        bg_score = pg.transform.scale(bg_score, (60, 60))

        rect = bg_score.get_rect()
        rect.center = (WIDTH // 2, 35)

        self.screen.blit(bg_score, rect)

        font = pg.font.Font(None, 50)
        text = font.render(str(self.score), True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 35) 

        self.screen.blit(text, text_rect)

        # Update the display
        pygame.display.update()
        pygame.time.delay(1)
 
 
    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.render()
            self.clock.tick(FPS)

flappy_bird = Game()
flappy_bird.run()