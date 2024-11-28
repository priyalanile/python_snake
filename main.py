"""
Note: Pygame Documentation

Pygame is a set of Python modules designed for writing games

Event Loop: Every UI application has it to suspend the screen for sometime and awaits for mouse or keyboard input.
import time #just to freeze the window to check

pygame.event.get() => 
"""
#pip install pygame

import pygame #To import Python game module
from pygame.locals import * #To get all kinds of pygame events
import time
import random #to move apple at random position

SIZE = 40 #as size of block is 40 blocks
BACKGROUND_COLOR = (110,110,5)

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen #As we need something to draw upon!
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE*3 
        self.y = SIZE*3 #Should be multiple of 40 as 40 blocks of snake block size!
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x,self.y)) #blit draws the image
        pygame.display.flip() #updating the screen with changes we did!

    def move(self):
        '''
        Note: Horizontal window size limit =1000, vertical window size limit=800,
        with 40 SIZe i.e. pixel size of apple, 1000/40 i.e. 25 possible increments in horizontal space possible &
        same 800/40 i.e. 20 possible increments in vertical space possible (in order to not exceed apple outside the window)
        Note: Kept the value little bit low by 1, just to avoid apple going out of the window.
        '''
        self.x = random.randint(1,24)*SIZE #1000 (horizontal window size)/40 i.e. 25 possible increments
        self.y = random.randint(1,19)*SIZE #800(vertical window size)/40=20 i.e. 20 possible increments as we have 

class Snake:
    def __init__(self, parent_screen,length):
        self.length=length
        self.parent_screen = parent_screen #As we need something to draw upon!
        self.block = pygame.image.load("resources/block.jpg").convert() #Method for loading the image.
        self.x=[SIZE]*length #x co-ordinates #to ensure having multiple blocks.
        self.y=[SIZE]*length #y co-ordinates #to ensure having multiple blocks.
        self.direction = 'down'
    
    def draw(self): #Function to draw a block
        #self.parent_screen.fill(BACKGROUND_COLOR) #to fill the background with some color; 255,255,255 is white color; will also ensure before drawing the block, the screen is clear.

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i])) #blit draws the image
        pygame.display.flip() #updating the screen with changes we did!
    
    def increase_length(self):
        self.length+=1
        self.x.append(-1) #putting random value of -1 for now, as we can deal with it in walk() function
        self.y.append(-1) #putting random value of -1 for now, as we can deal with it in walk() function


    def move_left(self):
        self.direction = 'left'
        self.draw()
    
    def move_right(self):
        self.direction = 'right'
        self.draw()

    def move_up(self):
        self.direction = 'up'
        self.draw()

    def move_down(self):
        self.direction = 'down'
        self.draw()
    
    def walk(self):

        #For other blocks, to put blocks at the position of previous blocks using for loop running in reverse.

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        #For Head of snake i.e. x[0]
        if self.direction == 'left':
            self.x[0]-=SIZE
        if self.direction == 'right':
            self.x[0]+=SIZE
        if self.direction == 'up':
            self.y[0]-=SIZE
        if self.direction == 'down':
            self.y[0]+=SIZE       

        self.draw()

class Game:
    def __init__(self):
        pygame.init() #initializes the pygame module,

        pygame.display.set_caption("Author: Priyal Nile & Inspiration: Code Basics YouTube")

        pygame.mixer.init() #initializing the sound module of pygame
        self.play_background_music() #playing background music as soon as the game starts

        
        self.surface = pygame.display.set_mode((1000,800)) #initializes game window size!
        self.surface.fill((110, 110, 5))

        self.snake = Snake(self.surface, 1) #Since snake would be within a Game, creating snake object here
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self,x1,y1,x2,y2):
        '''
        #Collission detection logic. Snake(x1,y1) & apple(x2,y2)
        '''
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1< y2 + SIZE:
                return True
        return False
        
    def display_score(self):
        self.font = pygame.font.SysFont('aerial',30)
        self.score = self.font.render(f"Score:{self.snake.length}", True, (255,255,255))
        self.surface.blit(self.score,(900,10))

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3") #Note: music is longer, sound is shorter duration.
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound=pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0)) #the image is bigger in pixel(can be checked in image properties), so setting from 0,0 should cover everything

    def play(self):
            self.render_background() #The place where we are drawing everything!
            self.snake.walk()
            self.apple.draw()
            self.display_score()
            pygame.display.flip()

            #Snake Eating/colliding with Apple:
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
                #We would check collision of x[0] & y[0] only i.e. snake head!

                #to play ding music when Snake ate an Apple!
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()
                print("Collision Occured!")
            
            #Snake Colliding with itself! i.e. finding collision of head with remaining blocks.
            for i in range(2,self.snake.length): #3 as 2 blocks of its body,the snake won't be hitting anyways.
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i],self.snake.y[i]):
                    #to play crash music when Snake hits itself!
                    self.play_sound("crash")
                    raise "Game Over" #as Game over is interruption, better to handle it like this!

            # snake colliding with the boundries of the window
            if not (0 <= self.snake.x[0] <= 960 and 0 <= self.snake.y[0] <= 760):
                self.play_sound('crash')
                raise "Hit the boundry error!"

    def show_game_over(self):
        #self.surface.fill(BACKGROUND_COLOR) #clearing the surface
        self.render_background() #to get the background image of our interest
        self.font = pygame.font.SysFont('aerial',30)
        self.line1 = self.font.render(f"Game is Over! Your Score is:{self.snake.length}", True, (255,255,255))
        self.surface.blit(self.line1,(200,300)) #200,300 ~middle of screen!

        self.line2 = self.font.render("To play again Press Enter. To exit press Escape!",True,(255,255,255))
        self.surface.blit(self.line2,(200,350)) #200,350 ~middle of screen!
        pygame.display.flip() #refreshing UI
        pygame.mixer.music.pause() #To pause the music when game is over.

    def reset(self): #i.e. We reinitialize our Snake & Apple objects.

        self.snake = Snake(self.surface, 1) #Since snake would be within a Game, creating snake object here
        self.apple = Apple(self.surface)


    def run(self):
            
            running=True #Variable controlling running window on screen
            pause=False

            while running: #To keep the window open until conditio is met!
                for event in pygame.event.get(): #To get all kinds of pygame events

                    if event.type == KEYDOWN:
                        
                        if event.key == K_ESCAPE: #to exit game by escape
                            running=False

                        if event.key == K_RETURN:
                            pygame.mixer.music.play() #To start music when user is replaying the game!
                            pause=False

                        if not pause:

                            if event.key == K_UP: #based on X,Y co-ordinates of this game window! X doesn't affect!
                                self.snake.move_up()

                            if event.key == K_DOWN:
                                self.snake.move_down()

                            if event.key == K_LEFT: #Y doesn't affect!
                                self.snake.move_left()

                            if event.key == K_RIGHT:
                                self.snake.move_right()

                    elif event.type == QUIT: #to exit game by closing the sign
                        running=False

                try:
                    if not pause:
                        self.play()
                except Exception as e: #as Game over is like interruption. So handling here.
                    self.show_game_over() 
                    pause=True
                    self.reset() #to reset the game when someone wants to replay the game again.

                time.sleep(0.3)



if __name__== "__main__":

    game = Game() #object of Game class
    game.run()

