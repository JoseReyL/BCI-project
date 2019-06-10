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


def injectERP(amp=1,host="localhost",port=8300):
    """Inject an erp into a simulated data-stream, sliently ignore if failed, e.g. because not simulated"""
    import socket
    try:
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0).sendto(bytes(amp),(host,port))
    except: # sliently igore any errors
        pass

# Base on: Just added a bunch of pygame.
# https://www.pygame.org/project-AAfilledRoundedRect-2349-.html
def AAfilledRoundedRect(surface, rect, color, radius=0.4):
    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)

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


def select_icon_initial_screen(position, menu):
    initial_screen(position, yellow)
    while True:
        if position > 4:
            position = 1
            initial_screen(position, yellow)
        if position < 1:
            position = 4
            initial_screen(position, yellow)

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
                    sleep(1)
                    events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                    if events == []:
                        print("Error! no predictions, continuing")
                        evt = []
                    else:
                        if len(events) > 1:
                            print("Warning: multiple predictions. Some ignored.")
                        evt = events[-1]  # only use the last event
                    if evt !=[]:
                        if int(evt.value) == 1:
                            menu = menu_dict(position, menu)
                            menu_selecter(menu)
                            break
                        elif int(evt.value) ==0:
                            initial_screen(position, yellow)
                if position == 2:
                    initial_screen(position, green)
                    sleep(1)
                    events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                    if events == []:
                        print("Error! no predictions, continuing")
                        evt = []
                    else:
                        if len(events) > 1:
                            print("Warning: multiple predictions. Some ignored.")
                        evt = events[-1]  # only use the last event
                    if evt != []:
                        if int(evt.value) == 1:
                            menu = menu_dict(position, menu)
                            menu_selecter(menu)
                            break
                        elif int(evt.value) == 0:
                            initial_screen(position, yellow)
                if position == 3:
                    initial_screen(position, green)
                    sleep(1)
                    events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                    if events == []:
                        print("Error! no predictions, continuing")
                        evt = []
                    else:
                        if len(events) > 1:
                            print("Warning: multiple predictions. Some ignored.")
                        evt = events[-1]  # only use the last event
                    if evt != []:
                        if int(evt.value) == 1:
                            menu = menu_dict(position, menu)
                            menu_selecter(menu)
                            break
                        elif int(evt.value) == 0:
                            initial_screen(position, yellow)
                if position == 4:
                    initial_screen(position, green)
                    sleep(1)
                    events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                    if events == []:
                        print("Error! no predictions, continuing")
                        evt = []
                    else:
                        if len(events) > 1:
                            print("Warning: multiple predictions. Some ignored.")
                        evt = events[-1]  # only use the last event
                    if evt != []:
                        if int(evt.value) == 1:
                            menu = menu_dict(position, menu)
                            menu_selecter(menu)
                            break
                        elif int(evt.value) == 0:
                            initial_screen(position, yellow)
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
            if int(eve.value) == 2:

                if menu["tv"]:

                    if position == 1:
                        phone_tv_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('tv', 1)
                            elif int(evt.value) == 0:
                                select_icon_phone_tv_screen(position, yellow)

                    if position == 2:
                        phone_tv_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('tv', 2)
                            elif int(evt.value) == 0:
                                select_icon_phone_tv_screen(position, yellow)

                    if position == 3:
                        phone_tv_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('tv', 3)
                            elif int(evt.value) == 0:
                                select_icon_phone_tv_screen(position, yellow)
                elif menu['phone']:

                    if position == 1:
                        phone_tv_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('call', 1)
                            elif int(evt.value) == 0:
                                select_icon_phone_tv_screen(position, yellow)

                    if position == 2:
                        phone_tv_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('call', 2)
                            elif int(evt.value) == 0:
                                select_icon_phone_tv_screen(position, yellow)

                    if position == 3:
                        phone_tv_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('call', 3)
                            elif int(evt.value) == 0:
                                select_icon_phone_tv_screen(position, yellow)

                if position == 4:
                    phone_tv_screen(position, green)
                    sleep(1)
                    events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                    if events == []:
                        print("Error! no predictions, continuing")
                        evt = []
                    else:
                        if len(events) > 1:
                            print("Warning: multiple predictions. Some ignored.")
                        evt = events[-1]  # only use the last event
                    if evt != []:
                        if int(evt.value) == 1:
                            menu = menu_dict(4, menu)
                            menu_selecter(menu)
                            break
                        elif int(evt.value) == 0:
                            select_icon_phone_tv_screen(position, yellow)

                if position == 5:
                    phone_tv_screen(position, green)
                    sleep(1)
                    events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                    if events == []:
                        print("Error! no predictions, continuing")
                        evt = []
                    else:
                        if len(events) > 1:
                            print("Warning: multiple predictions. Some ignored.")
                        evt = events[-1]  # only use the last event
                    if evt != []:
                        if int(evt.value) == 1:
                            bufhelp.sendEvent('sos', 'on')
                            menu = menu_dict(4, menu)
                            menu_selecter(menu)
                            break
                        elif int(evt.value) == 0:
                            select_icon_navigation_screen(position, yellow)
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
                    # home selected
                    if position == 1:
                        sos_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('sos', 'pain')
                                menu = menu_dict(4, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                select_icon_sos_screen(position, yellow)
                    if position == 2:
                        sos_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('sos', 'food')
                                menu = menu_dict(4, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                select_icon_sos_screen(position, yellow)
                    if position == 3:
                        sos_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('sos', 'wc')
                                menu = menu_dict(4, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                select_icon_sos_screen(position, yellow)
                    if position == 4:
                        sos_screen(position, green)
                        sleep(1)
                        menu = menu_dict(0, menu)
                        menu_selecter(menu)
                        break
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
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('navigate', 'up')
                                menu = menu_dict(4, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                navigation_screen(position, yellow)
                    if position == 2:
                        navigation_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('navigate', 'down')
                                menu = menu_dict(4, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                navigation_screen(position, yellow)
                    if position == 3:
                        navigation_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('navigate', 'left')
                                menu = menu_dict(4, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                navigation_screen(position, yellow)
                    if position == 4:
                        navigation_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('navigate', 'right')
                                menu = menu_dict(4, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                navigation_screen(position, yellow)
                    # home selected
                    if position == 5:
                        navigation_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                menu = menu_dict(0, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                navigation_screen(position, yellow)
                    # sos selected
                    if position == 6:
                        navigation_screen(position, green)
                        sleep(1)
                        events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
                        if events == []:
                            print("Error! no predictions, continuing")
                            evt = []
                        else:
                            if len(events) > 1:
                                print("Warning: multiple predictions. Some ignored.")
                            evt = events[-1]  # only use the last event
                        if evt != []:
                            if int(evt.value) == 1:
                                bufhelp.sendEvent('sos', 'on')
                                menu = menu_dict(4, menu)
                                menu_selecter(menu)
                                break
                            elif int(evt.value) == 0:
                                navigation_screen(position, yellow)
                if int(evt.value) == 3:
                    pass



# updates the disctionary which says in which screen we are
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


# CONFIGURABLE VARIABLES EXPERIMENT
verb = 0
nSymbols = 2
nSequences = 2 # a bit more data to be on the safe side
nBlock = 1  # 10; # number of stim blocks to use
trialDuration = 3
feedbackDuration = 2
baselineDuration = 1
intertrialDuration = 2

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

# create a surface object, image is drawn on it.
up_arr = pygame.image.load('icons/up_arrow.png')
down_arr = pygame.image.load('icons/down_arrow.png')
left_arr = pygame.image.load('icons/left_arrow.png')
right_arr = pygame.image.load('icons/right_arrow.png')

tv = pygame.image.load('icons/tv.png')
phone = pygame.image.load('icons/phone.png')
navigate = pygame.image.load('icons/wheel.png')

sos = pygame.image.load('icons/sos.png')
# sos sub menu choice
pain = pygame.image.load('icons/pain.png')
food = pygame.image.load('icons/food.png')
wc = pygame.image.load('icons/wc.png')

# put this for going back:
home = pygame.image.load('icons/house.png')

# for phone and tv:
one = pygame.image.load('icons/one.png')
two = pygame.image.load('icons/two.png')
three = pygame.image.load('icons/three.png')




# navigate: pygame.draw.circle(display_surface, yellow, (200, Y//2), 200)
# phone:  pygame.draw.circle(display_surface, yellow, (600, Y//2), 200)
# tv:  pygame.draw.circle(display_surface, yellow, (1025, Y//2), 200)
# sos: pygame.draw.circle(display_surface, yellow, (1400, Y//2), 200)





# connect to the buffer
ftc, hdr = bufhelp.connect()

### Navigation menu ###

initial_screen(1, yellow)

# position on the screen
# position 1 - navigate, 2 - phone, 3 - tv, 4 - sos

# classifier: # 0 - left, 1 - right, 2 - both, 3 - none (no movement)
initial_position = 1

while True:

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
    if evt!= []:
        if initial_position > 4:
            initial_position = 1
            select_icon_initial_screen(initial_position, menu)
        if initial_position < 1:
            initial_position = 4
            select_icon_initial_screen(initial_position, menu)

        # if left movement is predicted
        if int(evt.value) == 0:
            initial_position = initial_position - 1
            select_icon_initial_screen(initial_position, menu)
        # if right movement is predicted
        if int(evt.value) == 1:
            initial_position = initial_position + 1
            select_icon_initial_screen(initial_position, menu)
        # if both hands movement is predicted - select this option
        if int(evt.value) == 2:
            initial_screen(initial_position, green)
            sleep(1)
            events, state = bufhelp.buffer_newevents('errp.trigger', 1000, state=None)
            if events == []:
                print("Error! no predictions, continuing")
                evt = []
            else:
                if len(events) > 1:
                    print("Warning: multiple predictions. Some ignored.")
                evt = events[-1]  # only use the last event
            if evt != []:
                if int(evt.value) == 1:
                    menu = menu_dict(initial_position, menu)
                    menu_selecter(menu)
                    break
                elif int(evt.value) == 0:
                    initial_screen(position, yellow)
        if int(evt.value) == 3:
            pass


