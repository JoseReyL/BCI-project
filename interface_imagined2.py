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

DEBUG = False 


def injectERP(amp=1,host="localhost",port=8300):
    """Inject an erp into a simulated data-stream, sliently ignore if failed, e.g. because not simulated"""
    import socket
    try:
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0).sendto(bytes(amp),(host,port))
    except: # sliently igore any errors
        pass


# menu dictionary
menu = {
  "home": True,
  "navigation": False,
  "phone": False,
  "tv": False,
  "sos": False
}


# draw original screen menu
def initial_screen(position, colour):
    display_surface.fill(white)
    if position == 1:
        pygame.draw.circle(display_surface, colour, (225, Y // 2), 200)
    if position == 2:
        pygame.draw.circle(display_surface, colour, (625, Y // 2), 200)
    if position == 3:
        pygame.draw.circle(display_surface, colour, (1025, Y // 2), 200)
    if position == 4:
        pygame.draw.circle(display_surface, colour, (1400, Y // 2), 200)

    display_surface.blit(navigate, (100, Y // 2 - icon_height / 2))
    display_surface.blit(phone, (500, Y // 2 - icon_height / 2))
    display_surface.blit(tv, (900, Y // 2 - icon_height / 2))
    display_surface.blit(sos, (1280, Y // 2 - icon_height / 2))
    pygame.display.update()

# draw phone screen, call 1, call 2, call 3, home, sos
def phone_tv_screen(position, colour):
    display_surface.fill(white)
    if position == 1:
        pygame.draw.circle(display_surface, colour, (100 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 2:
        pygame.draw.circle(display_surface, colour, (500 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 3:
        pygame.draw.circle(display_surface, colour, (900 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 4:
        pygame.draw.circle(display_surface, colour, (1300 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 5:
        pygame.draw.circle(display_surface, colour, (X // 2, Y // 2 + icon_height // 2 + icon_height // 4), 200)

    display_surface.blit(one, (100, Y // 2 - icon_height))
    display_surface.blit(two, (500, Y // 2 - icon_height))
    display_surface.blit(three, (900, Y // 2 - icon_height))
    display_surface.blit(home, (1300, Y // 2 - icon_height))
    display_surface.blit(sos, (X // 2 - icon_width // 2, Y // 2 + icon_height // 4))
    pygame.display.update()

# draw navigation screen menu
def navigation_screen(position, colour):
    display_surface.fill(white)
    if position == 1:
        pygame.draw.circle(display_surface, colour, (100 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 2:
        pygame.draw.circle(display_surface, colour, (500 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 3:
        pygame.draw.circle(display_surface, colour, (900 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 4:
        pygame.draw.circle(display_surface, colour, (1300 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 5:
        pygame.draw.circle(display_surface, colour, (500 + icon_width // 2, Y // 2 + icon_height//2 + icon_height//4), 200)
    if position == 6:
        pygame.draw.circle(display_surface, colour, (900 + icon_width // 2, Y // 2 + icon_height//2 + icon_height//4), 200)

    display_surface.blit(up_arr, (100, Y // 2 - icon_height))
    display_surface.blit(down_arr, (500, Y // 2 - icon_height))
    display_surface.blit(left_arr, (900, Y // 2 - icon_height))
    display_surface.blit(right_arr, (1300, Y // 2 - icon_height))
    display_surface.blit(home, (500, Y // 2 + icon_height // 4))
    display_surface.blit(sos, (900, Y // 2 + icon_height // 4))
    pygame.display.update()

# draw sos screen
def sos_screen(position, colour):
    display_surface.fill(white)
    if position == 1:
        pygame.draw.circle(display_surface, colour, (225, Y // 2), 200)
    if position == 2:
        pygame.draw.circle(display_surface, colour, (625, Y // 2), 200)
    if position == 3:
        pygame.draw.circle(display_surface, colour, (1025, Y // 2), 200)
    if position == 4:
        pygame.draw.circle(display_surface, colour, (1400, Y // 2), 200)
    display_surface.blit(pain, (100, Y // 2 - icon_height / 2))
    display_surface.blit(food, (500, Y // 2 - icon_height / 2))
    display_surface.blit(wc, (900, Y // 2 - icon_height / 2))
    display_surface.blit(home, (1280, Y // 2 - icon_height / 2))
    pygame.display.update()


# helper function to send events to the error potential classifier
def errp_communicate(menu, position):
    selected = False
    while True:
        events_errp, state_errp = bufhelp.buffer_newevents('errp.prediction', 1000, state=None)
        if events_errp == []:
            print("Error! no predictions, continuing")
            evt_errp = []
        else:
            if len(events_errp) > 1:
                print("Warning: multiple predictions. Some ignored.")
            evt_errp = events_errp[-1]  # only use the last event
        if evt_errp != []:
            if int(evt_errp.value) == 1:
                if menu['tv'] and position < 4:
                    bufhelp.sendEvent('tv', position)
                    phone_tv_screen(position, blue)
                    break
                if menu['phone'] and position < 4:
                    bufhelp.sendEvent('call', position)
                    phone_tv_screen(position, blue)
                    break
                if (menu['phone'] or menu['tv']) and position > 3:
                    if menu['tv']: bufhelp.sendEvent('tv', 'end')
                    if position == 4:
                        menu = menu_dict(4, menu)
                        selected = True
                        menu_selecter(menu)
                        break
                    if position == 5:
                        bufhelp.sendEvent('sos', 'on')
                        menu = menu_dict(4, menu)
                        selected = True
                        menu_selecter(menu)
                        break
                if menu['sos']:
                    if position == 1:
                        bufhelp.sendEvent('sos', 'pain')
                        sos_screen(position, blue)
                        break
                    if position == 2:
                        bufhelp.sendEvent('sos', 'food')
                        sos_screen(position, blue)
                        break
                    if position == 3:
                        bufhelp.sendEvent('sos', 'wc')
                        sos_screen(position, blue)
                        break
                    if position == 4:
                        selected = True
                        menu = menu_dict(0, menu)
                        menu_selecter(menu)
                        break
                if menu['navigation']:
                    if position == 1:
                        bufhelp.sendEvent('navigate', 'up')
                        navigation_screen(position, blue)
                        break
                    if position == 2:
                        bufhelp.sendEvent('navigate', 'down')
                        navigation_screen(position, blue)
                        break
                    if position == 3:
                        bufhelp.sendEvent('navigate', 'left')
                        navigation_screen(position, blue)
                        break
                    if position == 4:
                        bufhelp.sendEvent('navigate', 'right')
                        navigation_screen(position, blue)
                        break
                    if position == 5:
                        selected = True
                        menu = menu_dict(0, menu)
                        menu_selecter(menu)
                        break
                    if position == 6:
                        bufhelp.sendEvent('sos', 'on')
                        selected = True
                        menu = menu_dict(4, menu)
                        menu_selecter(menu)
                        break
                if menu['home']:
                    selected = True
                    menu = menu_dict(position, menu)
                    menu_selecter(menu)
                    break
            elif int(evt_errp.value) == 0:
                if menu['tv']:phone_tv_screen(position, yellow)
                if menu['home']: initial_screen(position, yellow)
                if menu['navigation']:navigation_screen(position, yellow)
                if menu['sos']:sos_screen(position, yellow)
                if menu['phone']:phone_tv_screen(position, yellow)
                break
    return selected


def select_icon_initial_screen(position, menu):
    initial_screen(position, yellow)
    while True:
        if position > 4:
            position = 1
            initial_screen(position, yellow)
        if position < 1:
            position = 4
            initial_screen(position, yellow)

        bufhelp.sendEvent('stimulus.target', "hey")
        if not DEBUG: sleep(3)

        events, state = bufhelp.buffer_newevents('classifier.prediction', 3000, state=None)
        if events == []:
            print("Error! no predictions, continuing")
            evt = []
        else:
            if len(events) > 1:
                print("Warning: multiple predictions. Some ignored.")
            evt = events[-1]  # only use the last event

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if evt!=[]:
            if int(evt.value) == 0:
                position = position - 1
                initial_screen(position, yellow)
            if int(evt.value) == 1:
                position = position + 1
                initial_screen(position, yellow)
            if int(evt.value) == 2:
                if position == 1:
                    initial_screen(position, green)
                    bufhelp.sendEvent('errp.trigger', 'start')
                    if not DEBUG: sleep(1)
                    selected = errp_communicate(menu, position)
                    if selected:break
                if position == 2:
                    initial_screen(position, green)
                    bufhelp.sendEvent('errp.trigger', 'start')
                    if not DEBUG: sleep(1)
                    selected = errp_communicate(menu, position)
                    if selected:break
                if position == 3:
                    initial_screen(position, green)
                    bufhelp.sendEvent('errp.trigger', 'start')
                    if not DEBUG: sleep(1)
                    selected = errp_communicate(menu, position)
                    if selected:break
                if position == 4:
                    initial_screen(position, green)
                    bufhelp.sendEvent('errp.trigger', 'start')
                    if not DEBUG: sleep(1)
                    selected = errp_communicate(menu, position)
                    if selected:break

            if int(evt.value) == 3:
                pass


# phone and tv have the same screens
def select_icon_phone_tv_screen(position, menu):
    phone_tv_screen(position, yellow)

    while True:
        if position > 5:
            position = 1
            phone_tv_screen(position, yellow)
        if position < 1:
            position = 5
            phone_tv_screen(position, yellow)

        bufhelp.sendEvent('stimulus.target', "hey")
        if not DEBUG: sleep(3)

        events, state = bufhelp.buffer_newevents('classifier.prediction', 3000, state=None)
        if events == []:
            print("Error! no predictions, continuing")
            evt = []
        else:
            if len(events) > 1:
                print("Warning: multiple predictions. Some ignored.")
            evt = events[-1]  # only use the last event

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if evt!=[]:
            if int(evt.value) == 0:
                position = position - 1
                phone_tv_screen(position, yellow)
            if int(evt.value) == 1:
                position = position + 1
                phone_tv_screen(position, yellow)
            if int(evt.value) == 2:
                if menu["tv"]:
                    if position == 1:
                        phone_tv_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected: break
                    if position == 2:
                        phone_tv_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected: break
                    if position == 3:
                        phone_tv_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected: break
                elif menu['phone']:
                    if position == 1:
                        phone_tv_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected: break
                    if position == 2:
                        phone_tv_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected: break
                    if position == 3:
                        phone_tv_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected: break
                if position == 4:
                    phone_tv_screen(position, green)
                    bufhelp.sendEvent('errp.trigger', 'start')
                    if not DEBUG: sleep(1)
                    selected = errp_communicate(menu, position)
                    if selected:break
                if position == 5:
                    phone_tv_screen(position, green)
                    bufhelp.sendEvent('errp.trigger', 'start')
                    if not DEBUG: sleep(1)
                    selected = errp_communicate(menu, position)
                    if selected:break
            if int(evt.value) == 3:
                pass


def select_icon_sos_screen(position, menu):
    sos_screen(position, yellow)

    while True:

        if position > 4:
            position = 1
            sos_screen(position, yellow)
        if position < 1:
            position = 4
            sos_screen(position, yellow)

        bufhelp.sendEvent('stimulus.target', "hey")
        if not DEBUG: sleep(3)

        events, state = bufhelp.buffer_newevents('classifier.prediction', 3000, state=None)
        if events == []:
            print("Error! no predictions, continuing")
            evt = []
        else:
            if len(events) > 1:
                print("Warning: multiple predictions. Some ignored.")
            evt = events[-1]  # only use the last event

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if evt!=[]:
                if int(evt.value) == 0:
                    position = position - 1
                    sos_screen(position, yellow)
                    # if right movement is predicted
                if int(evt.value) == 1:
                    position = position + 1
                    sos_screen(position, yellow)
                    # if both hands movement is predicted - select this option
                if int(evt.value) == 2:
                    if position == 1:
                        sos_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected:break
                    if position == 2:
                        sos_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected:break
                    if position == 3:
                        sos_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected:break
                    if position == 4:
                        sos_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected:break
                if int(evt.value) == 3:
                    pass


def select_icon_navigation_screen(position, menu):
    navigation_screen(position, yellow)

    while True:

        if position > 6:
            position = 1
            navigation_screen(position, yellow)
        if position < 1:
            position = 6
            navigation_screen(position, yellow)

        bufhelp.sendEvent('stimulus.target', "hey")
        if not DEBUG: sleep(3)

        events, state = bufhelp.buffer_newevents('classifier.prediction', 3000, state=None)
        if events == []:
            print("Error! no predictions, continuing")
            evt = []
        else:
            if len(events) > 1:
                print("Warning: multiple predictions. Some ignored.")
            evt = events[-1]  # only use the last event

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if evt!=[]:
                if int(evt.value) == 0:
                    position = position - 1
                    navigation_screen(position, yellow)
                # if right movement is predicted
                if int(evt.value) == 1:
                    position = position + 1
                    navigation_screen(position, yellow)
                # if both hands movement is predicted - select this option
                if int(evt.value) == 2:
                    if position == 1:
                        navigation_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected:break
                    if position == 2:
                        navigation_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected:break
                    if position == 3:
                        navigation_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected:break
                    if position == 4:
                        navigation_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected:break
                    # home selected
                    if position == 5:
                        navigation_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected: break
                    # sos selected
                    if position == 6:
                        navigation_screen(position, green)
                        bufhelp.sendEvent('errp.trigger', 'start')
                        if not DEBUG: sleep(1)
                        selected = errp_communicate(menu, position)
                        if selected: break
                if int(evt.value) == 3:
                    pass


# updates the dictionary which says in which screen we are
def menu_dict(position, menu):
    # enter navigation menu
    if position ==0:
        menu = {key: False for key in menu}
        menu["home"] = True
        menu.update(menu)
    if position == 1:
        menu = {key: False for key in menu}
        menu["navigation"] = True
        menu.update(menu)
    if position == 2:
        menu = {key: False for key in menu}
        menu["phone"] = True
        menu.update(menu)
    if position == 3:
        menu = {key: False for key in menu}
        menu["tv"] = True
        menu.update(menu)
    if position == 4:
        menu = {key: False for key in menu}
        menu["sos"] = True
        menu.update(menu)
    return menu


# initiates the right menu
def menu_selecter(menu):
    if menu["home"] : select_icon_initial_screen(1, menu)
    if menu["navigation"] : select_icon_navigation_screen(1, menu)
    if menu["phone"] : select_icon_phone_tv_screen(1, menu)
    if menu["tv"] : select_icon_phone_tv_screen(1, menu)
    if menu["sos"] : select_icon_sos_screen(1, menu)


# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# define the RGB value for colours
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0,0,255)


# assigning values to X and Y variable (resolution)
X = 1600
Y = 800
icon_width = 256
icon_height = 256

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Brain-Computer Interface Imagined Movement')

#################### ICONS ###########################################
icons_path = os.path.join(pydir, 'icons') # The icons folder path
up_arr = pygame.image.load(os.path.join(icons_path,'up_arrow.png'))
down_arr = pygame.image.load(os.path.join(icons_path,'down_arrow.png'))
left_arr    =  pygame.image.load(os.path.join(icons_path,'left_arrow.png'))
right_arr = pygame.image.load(os.path.join(icons_path,'right_arrow.png'))

tv = pygame.image.load(os.path.join(icons_path,'tv.png'))
phone = pygame.image.load(os.path.join(icons_path,'phone.png'))
navigate = pygame.image.load(os.path.join(icons_path,'wheel.png'))

sos = pygame.image.load(os.path.join(icons_path,'sos.png'))
# sos sub menu choice
pain = pygame.image.load(os.path.join(icons_path,'pain.png'))
food = pygame.image.load(os.path.join(icons_path,'food.png'))
wc = pygame.image.load(os.path.join(icons_path,'wc.png'))

# put this for going back:
home = pygame.image.load(os.path.join(icons_path,'house.png'))

# for phone and tv:
one = pygame.image.load(os.path.join(icons_path,'one.png'))
two = pygame.image.load(os.path.join(icons_path,'two.png'))
three = pygame.image.load(os.path.join(icons_path,'three.png'))

#################### MAIN PROGRAM ###################################

# connect to the buffer
ftc, hdr = bufhelp.connect()

### Navigation menu ###
initial_screen(1, yellow)
position = 1

while True:
    bufhelp.sendEvent('stimulus.target', "hey")
    if not DEBUG: sleep(3)

    events, state = bufhelp.buffer_newevents('classifier.prediction', 3000, state=None)
    if events == []:
        print("Error! no predictions, continuing")
        evt = []
    else:
        if len(events) > 1:
            print("Warning: multiple predictions. Some ignored.")
        evt = events[-1]  # only use the last event

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # do not let the position get out of bounds and not showing which menu item is selected
    if evt != []:
        # to keep the position within the interface
        if position > 4:
            position = 1
            select_icon_initial_screen(position, menu)
        if position < 1:
            position = 4
            select_icon_initial_screen(position, menu)
        # if left movement is predicted
        if int(evt.value) == 0:
            position = position - 1
            select_icon_initial_screen(position, menu)
        # if right movement is predicted
        if int(evt.value) == 1:
            position = position + 1
            select_icon_initial_screen(position, menu)
        # if both hands movement is predicted - select this option
        if int(evt.value) == 2:
            initial_screen(position, green)
            if not DEBUG: sleep(1)
            bufhelp.sendEvent('errp.trigger', 'start')
            injectERP(amp=1)
            sleep(1)
            selected = errp_communicate(menu, position)
            if selected: break

        if int(evt.value) == 3:
            pass

