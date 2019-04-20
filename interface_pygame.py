import pygame 
import time


'''
configuration_file = 'config.txt'

def read(configuration_file):
    f = open(configuration_file,'r')
    content = f.readlines()
    f.close()
    variables = {}
    for i in content:
        variables[i.split(':')[0]] = i.split(':')[1].replace('\n','')
    return variables

vari = read(configuration_file)
'''

#Base on: Just added a bunch of pygame.
#https://www.pygame.org/project-AAfilledRoundedRect-2349-.html
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


# activate the pygame library . 
# initiate pygame and give permission 
# to use pygame's functionality. 
pygame.init() 
  
# define the RGB value 
# for white colour 
white = (255, 255, 255) 
  
# assigning values to X and Y variable 
X = 1600
Y = 800
  
# create the display surface object 
# of specific dimension..e(X, Y). 
display_surface = pygame.display.set_mode((X, Y )) 
  
# set the pygame window name 
pygame.display.set_caption('Image') 
  
# create a surface object, image is drawn on it. 
up_arr      =  pygame.image.load('icons/up_arrow.png')
down_arr    =  pygame.image.load('icons/down_arrow.png')
left_arr    =  pygame.image.load('icons/left_arrow.png')
right_arr   =  pygame.image.load('icons/right_arrow.png') 

tv        =  pygame.image.load('icons/tv.png')
phone     =  pygame.image.load('icons/phone.png')
navigate  =  pygame.image.load('icons/wheel.png')


loop = True

left = 0 
enter_pressed = False
rec_color = (0,0,0)


'''
if not loop:
        pygame.draw.circle(display_surface, (0,255,0,), (400,170), 100)  

        pygame.draw.circle(display_surface, (0,255,0,), (135,400), 100) 

        pygame.draw.circle(display_surface, (0,255,0,), (400,630), 100) 

        pygame.draw.circle(display_surface, (0,255,0,), (665,400), 100) 
'''


# infinite loop 
while True : 

    display_surface.fill(white) 
    

    if not enter_pressed: 
        rect_color = (255,255,0)

    if enter_pressed: 
        rect_color = (0,255,0)

    

    if left%3 == 0:
        AAfilledRoundedRect(display_surface, (296,252,296,296), rect_color)

    if left%3 == 1:
        AAfilledRoundedRect(display_surface, (652,252,296,296), rect_color)
    
    if left%3 == 2:
        AAfilledRoundedRect(display_surface, (1008,252,296,296), rect_color)



    display_surface.blit(tv, (316,272)) 
    display_surface.blit(phone, (672,272)) 
    display_surface.blit(navigate, (1028,272)) 

    ''' 
    display_surface.blit(up_arr, (337,100)) 
    display_surface.blit(down_arr, (,)) 
    display_surface.blit(left_arr, (337,100)) 
    display_surface.blit(right_arr, (337,100))
    '''

  

    pygame.display.update()


    # iterate over the list of Event objects 
    # that was returned by pygame.event.get() method. 

    if enter_pressed: time.sleep(2)

    enter_pressed = False
 
    for event in pygame.event.get() : 
  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE :
                print("Space bar pressed down.")
                left = left+1

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN :
                print("Enter bar pressed down.")
                enter_pressed = True

        if event.type == pygame.QUIT : 
            pygame.quit() 
            quit() 
  
    

