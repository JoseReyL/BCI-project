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
def initial_screen():
    display_surface.fill(white)
    pygame.draw.circle(display_surface, yellow, (200, Y // 2), 200)
    display_surface.blit(navigate, (100, Y // 2 - icon_height / 2))
    display_surface.blit(phone, (500, Y // 2 - icon_height / 2))
    display_surface.blit(tv, (900, Y // 2 - icon_height / 2))
    display_surface.blit(sos, (1280, Y // 2 - icon_height / 2))
    pygame.display.update()


# draw navigation screen menu
def navigation_screen():
    display_surface.fill(white)
    pygame.draw.circle(display_surface, yellow, (100 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    display_surface.blit(up_arr, (100, Y // 2 - icon_height))
    display_surface.blit(down_arr, (500, Y // 2 - icon_height))
    display_surface.blit(left_arr, (900, Y // 2 - icon_height))
    display_surface.blit(right_arr, (1300, Y // 2 - icon_height))
    display_surface.blit(home, (500, Y // 2 + icon_height // 4))
    display_surface.blit(sos, (900, Y // 2 + icon_height // 4))
    pygame.display.update()

# draw sos screen
def sos_screen():
    display_surface.fill(white)
    pygame.draw.circle(display_surface, yellow, (200, Y // 2), 200)
    display_surface.blit(pain, (100, Y // 2 - icon_height / 2))
    display_surface.blit(food, (500, Y // 2 - icon_height / 2))
    display_surface.blit(wc, (900, Y // 2 - icon_height / 2))
    display_surface.blit(home, (1280, Y // 2 - icon_height / 2))
    pygame.display.update()

# taken the initial screen, this function marks the selected icon
def select_icon_initial_screen(position):
    display_surface.fill(white)
    if position == 1:
        pygame.draw.circle(display_surface, yellow, (200, Y // 2), 200)
    if position == 2:
        pygame.draw.circle(display_surface, yellow, (600, Y // 2), 200)
    if position == 3:
        pygame.draw.circle(display_surface, yellow, (1025, Y // 2), 200)
    if position == 4:
        pygame.draw.circle(display_surface, yellow, (1400, Y // 2), 200)

    display_surface.blit(navigate, (100, Y // 2 - navigate.get_rect().size[1] / 2))
    display_surface.blit(phone, (500, Y // 2 - phone.get_rect().size[1] / 2))
    display_surface.blit(tv, (900, Y // 2 - tv.get_rect().size[1] / 2))
    display_surface.blit(sos, (1280, Y // 2 - sos.get_rect().size[1] / 2))
    pygame.display.update()

def select_icon_navigation_screen(position):
    display_surface.fill(white)
    if position == 1:
        pygame.draw.circle(display_surface, yellow, (100 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 2:
        pygame.draw.circle(display_surface, yellow, (500 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 3:
        pygame.draw.circle(display_surface, yellow, (900 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 4:
        pygame.draw.circle(display_surface, yellow, (1300 + icon_width // 2, Y // 2 - icon_height // 2), 200)
    if position == 5:
        pygame.draw.circle(display_surface, yellow, (500 + icon_width // 2, Y // 2 - icon_height // 8), 200)
    if position == 6:
        pygame.draw.circle(display_surface, yellow, (900 + icon_width // 2, Y // 2 - icon_height // 8), 200)
    display_surface.blit(up_arr, (100, Y // 2 - icon_height))
    display_surface.blit(down_arr, (500, Y // 2 - icon_height))
    display_surface.blit(left_arr, (900, Y // 2 - icon_height))
    display_surface.blit(right_arr, (1300, Y // 2 - icon_height))
    display_surface.blit(home, (500, Y // 2 + icon_height // 4))
    display_surface.blit(sos, (900, Y // 2 + icon_height // 4))
    pygame.display.update()
    navigation_screen(position)


def navigate_navigation_screen(position):
    for event in pygame.event.get():
        # print(event)
        if position > 6:
            position = 1
            select_icon_navigation_screen(position)
        if position < 1:
            position = 6
            select_icon_navigation_screen(position)

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # key 275 is right
        if event.type == pygame.KEYDOWN and event.key == 275:
            position = position + 1
            select_icon_navigation_screen(position)
        # key 276 is left
        if event.type == pygame.KEYDOWN and event.key == 276:
            position = position - 1
            select_icon_navigation_screen(position)



# updates the disctionary which says in which screen we are
def menu_dict(position, menu):
    # enter navigation menu
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
    if menu["home"] : initial_screen()
    if menu["navigation"] : navigation_screen()
    # if menu["phone"] : phone_screen()
    # if menu["tv"] : tv_screen()
    if menu["sos"] : sos_screen()


# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# define the RGB value
# for white colour
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
pygame.display.set_caption('Image')

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




# navigate: pygame.draw.circle(display_surface, yellow, (200, Y//2), 200)
# phone:  pygame.draw.circle(display_surface, yellow, (600, Y//2), 200)
# tv:  pygame.draw.circle(display_surface, yellow, (1025, Y//2), 200)
# sos: pygame.draw.circle(display_surface, yellow, (1400, Y//2), 200)





# connect to the buffer
# ftc, hdr = bufhelp.connect()

### Navigation menu ###

initial_screen()

# position on the screen
# position 1 - navigate, 2 - phone, 3 - tv, 4 - sos

initial_position = 1

while True:

   # events, state = bufhelp.buffer_newevents('classifier.prediction', 3000, state)

    for event in pygame.event.get():

       # print(event)

        if initial_position > 4:
            initial_position = 1
            select_icon_initial_screen(initial_position)
        if initial_position < 1:
            initial_position = 4
            select_icon_initial_screen(initial_position)

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # key 275 is right
        if event.type == pygame.KEYDOWN and event.key == 275:
            initial_position = initial_position + 1
            select_icon_initial_screen(initial_position)
        # key 276 is left
        if event.type == pygame.KEYDOWN and event.key == 276:
            initial_position = initial_position - 1
            select_icon_initial_screen(initial_position)
        if event.type == pygame.KEYDOWN and event.key == 13:
            # update the menu disctionary
            menu = menu_dict(initial_position, menu)

            # enter the appropriate menu
            menu_selecter(menu)
            if menu["navigation"] :
                navigation_position = 1
                select_icon_initial_screen(navigation_position)