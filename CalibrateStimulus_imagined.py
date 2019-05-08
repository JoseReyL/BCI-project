#!/usr/bin/env python3
# Set up imports and paths
import sys, os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pygame
from time import sleep, time
from random import shuffle


# add the buffer bits to the search path

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

X =1600
Y = 800

display_surface = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
pygame.display.set_caption('Imagined Movement Calibration')

left_arr    =  pygame.image.load('icons/left_arrow.png')
right_arr   =  pygame.image.load('icons/right_arrow.png')
up_arr      =  pygame.image.load('icons/up_arrow.png')
down_arr    =  pygame.image.load('icons/down_arrow.png')

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
              + "Before you can fully enjoy the benefits of our interface, you need to calibrate the system \n" \
              + "\n" \
              + "Following you will see a screen with a circle in the middle and two arrows (left and right) \n" \
              + "When an arrow turns yellow, please, imagine you move the corresponding arm \n" \
              + "\n" \
              + "Press ENTER to start"

    blit_text(display_surface, message, (20, 50), font, black)
    pygame.display.update()



crashed = False
clock = pygame.time.Clock()

# Display instructions first:
display_message()

while not crashed:

    clock.tick(10)

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == 13: # this is ENTER
                display_surface.fill(white)
                pygame.display.update()
                display_surface.blit(left_arr, (471, 336))
                display_surface.blit(right_arr, (1001, 336))
                pygame.draw.circle(display_surface, black, [X//2, Y//2], 40)
                pygame.display.flip()



pygame.quit()
quit()


'''
try:
    pydir = os.path.dirname(__file__)
except:
    pydir = os.getcwd()
sigProcPath = os.path.join(os.path.abspath(pydir), '../../python/signalProc')
sys.path.append(sigProcPath)
import bufhelp

DEBUG = False  # True #


## HELPER FUNCTIONS
def drawnow(fig=None):
    "force a matplotlib figure to redraw itself, inside a compute loop"
    if fig is None: fig = plt.gcf()
    fig.canvas.draw()
    plt.pause(1e-3)  # wait for draw.. 1ms


currentKey = None


def keypressFn(event):
    "wait for keypress in a matplotlib figure, and store in the currentKey global"
    global currentKey
    currentKey = event.key


def waitforkey(fig=None, reset=True, debug=DEBUG):
    "wait for a key to be pressed in the given figure"
    if debug: return
    if fig is None: fig = gcf()
    global currentKey
    fig.canvas.mpl_connect('key_press_event', keypressFn)
    if reset: currentKey = None
    while currentKey is None:
        plt.pause(1e-2)  # allow gui event processing


## CONFIGURABLE VARIABLES
verb = 0
nSymbs = 2
nSeq = 15
nBlock = 2  # 10; # number of stim blocks to use
trialDuration = 3
baselineDuration = 1
intertrialDuration = 2

bgColor = (.5, .5, .5) # gray
tgtColor = (0, 1, 0) # green
fixColor = (1, 0, 0) # red
txtColor = (1, 1, 1) # white

# make the target sequence
tgtSeq = list(range(nSymbs)) * int(nSeq / nSymbs + 1)  # sequence in sequential order
shuffle(tgtSeq)  # N.B. shuffle works in-place!

##--------------------- Start of the actual experiment loop ----------------------------------
# set the display and the string for stimulus
if DEBUG:
    plt.switch_backend('agg')  # N.B. command to work in non-display mode
fig = plt.figure(facecolor=(0, 0, 0))

fig.suptitle('IM-Stimulus', fontsize=14, fontweight='bold', color=txtColor)
ax = fig.add_subplot(111)  # default full-screen ax
ax.set_xlim((-1.5, 1.5))
ax.set_ylim((-1.5, 1.5))
ax.set_axis_off()
txthdl = ax.text(0, 0, 'This is some text', style='italic', color=txtColor)

# setup the targets
stimPos = [];
hdls = [];
stimRadius = .3;
theta = np.linspace(0, np.pi, nSymbs)
stimPos = np.stack((np.cos(theta), np.sin(theta))).T  # [nSymbs x 2]
for hi, pos in enumerate(stimPos):  # N.B. enumerate goes over 1st dim if stimPos is array
    print('%d) stimPos=(%f,%f)' % (hi, pos[0], pos[1]))
    circ = patches.Circle(pos, stimRadius, facecolor=bgColor)
    hhi = ax.add_patch(circ)
    hdls.insert(hi, hhi)
# add symbol for the center of the screen
spos = np.array((0, 0))  # .reshape((1,-1))
stimPos = np.vstack((stimPos, spos))  # [nSymbs+1 x 2]
circ = patches.Circle((0, 0), stimRadius / 4, facecolor=bgColor)
hhi = ax.add_patch(circ)
hdls.insert(nSymbs, hhi)
[_.set(visible=False) for _ in hdls]  # make all invisible

## init connection to the buffer
ftc, hdr = bufhelp.connect();

# wait for key-press to continue
[_.set(facecolor=bgColor) for _ in hdls]
txthdl.set(text='Press key to start')
drawnow()
waitforkey(fig)
txthdl.set(visible=False)

# set stimuli to visible
txthdl.set(visible=False)
[_.set(facecolor=bgColor, visible=True) for _ in hdls]

bufhelp.sendEvent('stimulus.training', 'start');
## STARTING stimulus loop
for si, tgt in enumerate(tgtSeq):
    sleep(intertrialDuration)

    # show the baseline
    hdls[-1].set(facecolor=fixColor)  # fixation cross red
    drawnow()
    bufhelp.sendEvent('stimulus.baseline', 'start')
    sleep(baselineDuration)
    bufhelp.sendEvent('stimulus.baseline', 'end')

    # show the target
    print("%d) tgt=%d :" % (si, tgt))
    hdls[-1].set(facecolor=tgtColor)  # target green
    hdls[tgt].set(facecolor=tgtColor)  # fixation cross green
    drawnow()
    bufhelp.sendEvent('stimulus.target', tgt)
    bufhelp.sendEvent('stimulus.trial', 'start')
    sleep(trialDuration)

    # reset the display
    [_.set(facecolor=bgColor) for _ in hdls]
    drawnow()
    bufhelp.sendEvent('stimulus.trial', 'end');

bufhelp.sendEvent('stimulus.training', 'end')
[_.set(visible=False) for _ in hdls]  # hide all stimuli
txthdl.set(text='Thanks for taking part!' '' 'Press key to finish', visible=True)
drawnow()
waitforkey(fig)
'''