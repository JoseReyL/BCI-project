#!/usr/bin/env python3
# Set up imports and paths
import sys, os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pygame
from time import sleep, time
from random import shuffle

# Add the buffer bits to the search path
try:
    pydir = os.path.dirname(__file__)
except:
    pydir = os.getcwd()
sigProcPath = os.path.join(os.path.abspath(pydir), '../../python/signalProc')
sys.path.append(sigProcPath)
import bufhelp

DEBUG = False  # True #


def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

# initiate pygame
pygame.init()

# define colours:
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0,0,255)

X =1600
Y = 800

display_surface = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
pygame.display.set_caption('Imagined Movement Calibration')

icons_path = os.path.join(pydir, 'icons') # The icons folder path

left_arr    =  pygame.image.load(os.path.join(icons_path,'left_arrow.png'))
right_arr   =  pygame.image.load(os.path.join(icons_path,'right_arrow.png'))
up_arr      =  pygame.image.load(os.path.join(icons_path,'up_arrow.png'))
down_arr    =  pygame.image.load(os.path.join(icons_path,'down_arrow.png'))

state = []

# HELPER FUNCTIONS FOR PYGAME

# copied from stackoverflow:
# https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame

# No easy or nice way to render text in pygame. This looks wavy
def blit_text(surface, text, pos, font, color):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def display_message():
    display_surface.fill(white)
    font = pygame.font.Font('freesansbold.ttf', 32)
    message = "Welcome to our imagined moved brain-computer interface! \n " \
              + "Before you can fully enjoy the benefits of our interface, we need to calibrate the system \n" \
              + "\n" \
              + "Following you will see a screen with a circle in the middle and two arrows (left and right) \n" \
              + "First, the circle will turn red. This is an indication for you to prepare. Then an arrow turns yellow, indicating that you need to imagine a movement from the corresponding arm \n" \
              + "\n" \
              + "If both arrows are marked in yellow - you are asked to imagine movement of your both hands \n" \
              + "\n" \
              + "If no arrows are marked in yellow - you are asked to not imagine any movement, just remain concentrated on the central point \n" \
              + "\n" \
              + "If the target then turns green you did good, red for bad. Easy! Good luck."

    blit_text(display_surface, message, (20, 50), font, black)
    pygame.display.update()

    pygame.draw.circle(display_surface, yellow, (535, 600), 100)
    display_surface.blit(left_arr, (471, 536))
    display_surface.blit(right_arr, (1001, 536))
    pygame.draw.circle(display_surface, black, [X // 2, 600], 40)
    pygame.display.flip()

    message = "Press ENTER to start"
    blit_text(display_surface, message, (1200, 670), font, black)
    pygame.display.update()

def injectERP(amp=1,host="localhost",port=8300):
    """Inject an erp into a simulated data-stream, sliently ignore if failed, e.g. because not simulated"""
    import socket
    try:
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0).sendto(bytes(amp),(host,port))
    except: # sliently igore any errors
        pass


def initial_display():
    display_surface.fill(white)
    pygame.display.update()
    display_surface.blit(left_arr, (471, 336))
    display_surface.blit(right_arr, (1001, 336))
    pygame.draw.circle(display_surface, black, [X // 2, Y // 2], 40)
    pygame.display.flip()


def run_feedback(nSequences, nBlock, trialDuration, feedbackDuration, intertrialDuration, baselineDuration, state=None):
    # Display fixation circle and two arows (left and right)
    initial_display()
    # pygame.time.delay(intertrialDuration)

    # make the target sequence
    nSymbols = 4
    targetSequence = list(range(nSymbols)) * int(nSequences / nSymbols + 1)  # sequence in sequential order
    last_trial_id = len(targetSequence)
    shuffle(targetSequence)  # N.B. shuffle works in-place!

    # 0 - left, 1 - right, 2 - both, 3 - none (no movement) 
    it = 0
    for target in targetSequence:
        it +=1
        sleep(intertrialDuration)

        # show the baseline
        pygame.draw.circle(display_surface, blue, [X // 2, Y // 2], 40)
        pygame.display.update()
        bufhelp.sendEvent('stimulus.baseline', 'start')
        sleep(baselineDuration)
        bufhelp.sendEvent('stimulus.baseline', 'end')

       # initial_display()


        # show the target in yellow

        if target == 0:
            pygame.draw.circle(display_surface, yellow, [X // 2, Y // 2], 40) # fixation yellow
            pygame.draw.circle(display_surface, yellow, (535, 400), 100) # mark target
            display_surface.blit(left_arr, (471, 336))
            pygame.display.update()
        elif target == 1:
            pygame.draw.circle(display_surface, yellow, [X // 2, Y // 2], 40)  # fixation yellow
            pygame.draw.circle(display_surface, yellow, (1065, 400), 100) # mark target
            display_surface.blit(right_arr, (1001, 336))
            pygame.display.update()
        elif target == 2:
            pygame.draw.circle(display_surface, yellow, [X // 2, Y // 2], 40)  # fixation yellow
            pygame.draw.circle(display_surface, yellow, (535, 400), 100)  # mark target
            pygame.draw.circle(display_surface, yellow, (1065, 400), 100)  # mark target
            display_surface.blit(left_arr, (471, 336))
            display_surface.blit(right_arr, (1001, 336))
            pygame.display.update()
        else:
            pygame.draw.circle(display_surface, yellow, [X // 2, Y // 2], 40)  # fixation yellow
            pygame.display.update()

        bufhelp.sendEvent('stimulus.trial', 'start')
        if it == last_trial_id :
            bufhelp.sendEvent('stimulus.last_target', target)
        else:
            bufhelp.sendEvent('stimulus.target', target)
        injectERP(amp=1)
        

        sleep(trialDuration)

        bufhelp.sendEvent('stimulus.end_target', 'end')
    
        #catch the prediction
        # N.B. use state to track which events processed so far
        events,state = bufhelp.buffer_newevents('classifier.prediction',3000,state)
        if events == []:
            print("Error! no predictions, continuing")
        else:
            if len(events)>1:
                print("Warning: multiple predictions. Some ignored.") 
            evt=events[-1] # only use the last event

        print(evt.value == target)
        if evt.value == target: 
            bufhelp.sendEvent('stimulus.start_feedback', "1")
        else:
            bufhelp.sendEvent('stimulus.start_feedback', "0")
            
        # show prediction (user feedback)
        if evt.value == target :    # good prediction !
            # Turn the target green
            if target == 0:
                pygame.draw.circle(display_surface, green, [X // 2, Y // 2], 40) 
                pygame.draw.circle(display_surface, green, (535, 400), 100) 
                display_surface.blit(left_arr, (471, 336))
                pygame.display.update()
            elif target == 1:
                pygame.draw.circle(display_surface, green, [X // 2, Y // 2], 40)  
                pygame.draw.circle(display_surface, green, (1065, 400), 100) 
                display_surface.blit(right_arr, (1001, 336))
                pygame.display.update()
            elif target == 2:
                pygame.draw.circle(display_surface, green, [X // 2, Y // 2], 40)  
                pygame.draw.circle(display_surface, green, (535, 400), 100)  
                pygame.draw.circle(display_surface, green, (1065, 400), 100)  
                display_surface.blit(left_arr, (471, 336))
                display_surface.blit(right_arr, (1001, 336))
                pygame.display.update()
            else:
                pygame.draw.circle(display_surface, green, [X // 2, Y // 2], 40) 
                pygame.display.update()
        else :  # wrong prediction !
            # Turn target red
            if target == 0:
                pygame.draw.circle(display_surface, red, [X // 2, Y // 2], 40) 
                pygame.draw.circle(display_surface, red, (535, 400), 100)
                display_surface.blit(left_arr, (471, 336))
                pygame.display.update()
            elif target == 1:
                pygame.draw.circle(display_surface, red, [X // 2, Y // 2], 40)  
                pygame.draw.circle(display_surface, red, (1065, 400), 100) 
                display_surface.blit(right_arr, (1001, 336))
                pygame.display.update()
            elif target == 2:
                pygame.draw.circle(display_surface, red, [X // 2, Y // 2], 40)  
                pygame.draw.circle(display_surface, red, (535, 400), 100)  
                pygame.draw.circle(display_surface, red, (1065, 400), 100)  
                display_surface.blit(left_arr, (471, 336))
                display_surface.blit(right_arr, (1001, 336))
                pygame.display.update()
            else:
                pygame.draw.circle(display_surface, red, [X // 2, Y // 2], 40)  
                pygame.display.update()

        injectERP(amp=1)
        sleep(feedbackDuration)
        bufhelp.sendEvent('stimulus.end_feedback', "end")
        
        

        bufhelp.sendEvent('stimulus.trial', 'end')
        # reset the display
        initial_display()
        sleep(1)
        


# CONFIGURABLE VARIABLES EXPERIMENT

verb = 0
nSymbols = 2
nSequences = 2 # a bit more data to be on the safe side
nBlock = 1  # number of stim blocks to use
trialDuration = 3
feedbackDuration = 2
baselineDuration = 1
intertrialDuration = 2






crashed = False
clock = pygame.time.Clock()

# Display instructions first:
display_message()


while True:

    clock.tick(10)

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            pygame.display.update()
        if event.type == pygame.KEYDOWN:
            if event.key == 13: # this is ENTER
                ftc, hdr = bufhelp.connect();
                bufhelp.sendEvent('stimulus.training', 'start');
                run_feedback(nSequences, nBlock, trialDuration, feedbackDuration, intertrialDuration, baselineDuration)
                bufhelp.sendEvent('stimulus.training', 'end')





pygame.quit()
quit()
