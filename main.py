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

SIZE = 40

class Snake:
    def __init__(self, surface,length):
        self.length=length
        self.parent_screen = surface #As we need something to draw upon!
        self.block = pygame.image.load("resources/block.jpg").convert() #Method for loading the image.
        self.x=[SIZE]*length #x co-ordinates #to ensure having multiple blocks.
        self.y=[SIZE]*length #y co-ordinates #to ensure having multiple blocks.
        self.direction = 'down'
    
    def draw(self): #Function to draw a block
        self.parent_screen.fill((165, 224, 242)) #to fill the background with some color; 255,255,255 is white color; will also ensure before drawing the block, the screen is clear.

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i])) #blit draws the image
        pygame.display.flip() #updating the screen with changes we did!
    
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
        if self.direction == 'left':
            self.x-=10
        if self.direction == 'right':
            self.x+=10
        if self.direction == 'up':
            self.y-=10
        if self.direction == 'down':
            self.y+=10       

        self.draw()

class Game:
    def __init__(self):
        pygame.init() #initializes the pygame module,
        self.surface = pygame.display.set_mode((500,500)) #initializes game window size!
        self.surface.fill((165, 224, 242))
        self.snake = Snake(self.surface) #Since snake would be within a Game, creating snake object here
        self.snake.draw()


    def run(self):
            
            running=True #Variable controlling running window on screen

            while running: #To keep the window open until conditio is met!
                for event in pygame.event.get(): #To get all kinds of pygame events

                    if event.type == KEYDOWN:
                        
                        if event.key == K_ESCAPE: #to exit game by escape
                            running=False

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

                self.snake.walk()
                time.sleep(0.2)


if __name__== "__main__":

    game = Game() #object of Game class
    game.run()



