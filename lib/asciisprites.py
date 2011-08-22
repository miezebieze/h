""" Inspirated and partly taken from the game Gorillas.py by Al Sweigart.
Visit him (and learn programming games) at:

        http://inventwithpython.com
"""
import pygame
from pygame.locals import SRCALPHA

class Image:
    def __init__(self, ascii, colours={'X': (255, 255, 255, 255)}):
        self.ascii      = ascii
        self.colours    = {}
        for colour in colours:
            self.colours[colour] = colours[colour]
        self.update()

    def update(self):
        ''' Update everything. '''
        self.update_ascii()
        self.update_colours()

    def update_ascii(self):
        ''' Call this after You changed self.ascii. '''
        self.asciilist  = self.ascii.split('\n')[1:-1]
        self.width      = max([len(x) for x in self.asciilist])
        self.height     = len(self.asciilist)
        self.surface    = pygame.Surface((self.width, self.height), SRCALPHA, 32)
        try: self.surface.fill(self.colours['bg'])
        except KeyError: self.surface.fill((0,0,0,0))
        self.update_colours()

    def update_colours(self):
        ''' Call this after You changed self.colours. '''
        for colour in self.colours:
            self.update_colour(colour)

    def update_colour(self, colour):
        ''' Update a single colour. Used internally. '''
        if colour in self.colours:
            for y in range(self.height):
                for x in range(self.width):
                    if self.asciilist[y][x] == colour:
                        self.surface.set_at((x, y), self.colours[colour])
        
    def set_colour(self, key, value):
        ''' Set the colour of any byte in self.colours.'''
        self.colours[key] = value
        self.update_colour(key)

    def set_colours(self, colours):
        for i in colours:
            self.colours[i] = colours[i]
        self.update_colours()

    def set_ascii(self, ascii):
        self.ascii = ascii
        self.update_ascii()

    def get_surface(self):
        return self.surface

class Animation:
    ''' self.frames are the indexes in self.timeline of self.images,
        which are the Image(object)s. '''
    def __init__(self, asciis, timeline=['0'], colours={'X': (255, 255, 255, 255)}):
        self.frames     = {}
        self.timeline   = timeline
        for i in asciis:
            self.frames[i] = Image(asciis[i], colours)
        self.curframe   = 0
        self.update_curframe()
        self.update_frames()

    def update_curframe(self):
        ''' Update current shown Image. '''
        self.curimage = self.frames[self.timeline[self.curframe]]
        self.surface = self.curimage.surface

    def update_frames(self):
        for i in self.frames:
            self.frames[i].update()

    def set_colours(self, colours):
        for i in self.frames:
            self.frames[i].set_colours(colours)

    def set_colour(self, key, value):
        for i in self.frames:
            self.frames[i].set_colour(key, value)

    def swap(self, amount = 1):
        if self.curframe + amount > len(self.timeline) -1:
            self.curframe = 0
        else:
            self.curframe += amount
        self.update_curframe()

    def get_image(self):
        frames = []
        for i in self.timeline:
            frames.append(self.frames[i])
        return frames

    def get_frames(self):
        images = []
        for i in self.timeline:
            images.append(self.frames[i].surface)
        return images

    def get_asciis(self):
        asciis = {}
        for i in self.frames:
            asciis[i] = self.frames[i].ascii
        return asciis



### Example time:

# Data:
image = """
TTTTTTTT  EEEEEEE   SSSSSS  AAAAAAAA
TTTTTTTT  EEEEEEE  SSSSSSS  AAAAAAAA
   TT     EE       SS          AA   
   TT     EEEEE    SSSSSS      AA   
   TT     EEEEE     SSSSSS     AA   
   TT     EE            SS     AA   
   TT     EEEEEEE  SSSSSSS     AA   
   TT     EEEEEEE  SSSSSS      AA   
"""

animation = {
        '0': """
 XXX 
XXXXX
XXOXX
XXXXX
 XXX 
""",    '1': """
  X  
 XXX 
 XXX 
 XXX 
  X  
""",    '2': """
  X  
  X  
  X  
  X  
  X  
""",    '3': """
  X  
 XXX 
 XOX 
 XXX 
  X  
""",    '4': """
 XXX 
XXOXX
XOXOX
XXOXX
 XXX 
"""}
backwards = ['0','1','2','3','4','3','2','1']
forewards = ['4','3','2','1','0','1','2','3']

coloursI = {'T': (255, 0, 0, 255),
            'E': (0, 255, 0, 255),
            'S': (255, 255, 0, 255),
            'A': (0, 0, 255, 255)
    }
coloursB = {'T': (64, 64, 64, 255),
            'E': (128, 128, 128, 255),
            'S': (192, 192, 192, 255),
            'A': (255, 255, 255, 255)
    }
Gold = {'X': (200, 150, 0, 255),
        'O': (255, 255, 0, 255)
    }
Silver={'X': (200, 200, 200, 255),
        'O': (100, 100, 100, 255)
    }
Bronze={'X': (150, 50, 0, 255),
        'O': (200, 75, 0, 255)
    }

import sys#, pygame
from pygame.locals import KEYUP, QUIT, K_ESCAPE, K_q, \# SRCALPHA, \
                          K_LEFT, K_RIGHT, K_SPACE, K_DOWN

# I made a symlink 'local' from some directory into the python libs,
# put an empty '__init__.py' file in it and have now a place, to easyly
# use my custom libs globally in all my projects:
#from local.asciisprites import *


# setup pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((66, 18), SRCALPHA, 32)

# setup the objects
image = Image(image, coloursI)
ani1  = Animation(animation, backwards, Gold)
ani2  = Animation(animation, forewards, Gold)

gold = True
blind = False

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            # pygame.quit() is needed by idle users.
            pygame.quit()
            sys.exit()
        if e.type == KEYUP:
            if e.key == K_ESCAPE or e.key == K_q:
                pygame.quit()
                sys.exit()
            if e.key == K_RIGHT:
                # one way to change the colours of the image
                temp = image.colours['S']
                image.colours['S'] = image.colours['E']
                image.colours['E'] = image.colours['T']
                image.colours['T'] = image.colours['A']
                image.colours['A'] = temp
                image.update_colours()
            if e.key == K_LEFT:
                # and another way...
                temp = image.colours['S']
                image.set_colour('S', image.colours['A'])
                image.set_colour('A', image.colours['T'])
                image.set_colour('T', image.colours['E'])
                image.set_colour('E', temp)
            if e.key == K_SPACE:
                # print the asciis stored in ani1 and switch colour blind mode!
                #print ani1.get_asciis()
                if blind:
                    blind = False
                    image.set_colours(coloursI)
                    if gold:
                        ani1.set_colours(Gold)
                        ani2.set_colours(Gold)
                    else:
                        ani1.set_colours(Bronze)
                        ani2.set_colours(Bronze)
                else:
                    image.set_colours(coloursB)
                    ani1.set_colours(Silver)
                    ani2.set_colours(Silver)
                    blind = True

            if e.key == K_DOWN:
                if gold:
                    gold = False
                    if not blind:
                        ani1.set_colours(Bronze)
                        ani2.set_colours(Bronze)
                else:
                    gold = True
                    if not blind:
                        ani1.set_colours(Gold)
                        ani2.set_colours(Gold)
            
    # fill the window with a grey to show off the transparency, that bugged around so long
    screen.fill((88, 88, 88, 255))

    # update and draw ani1
    ani1.swap()
    screen.blit(ani1.surface, (56, 7))
    # update and draw ani2
    ani2.swap()
    screen.blit(ani2.surface, (5,7))
    # draw the TEST-image
    screen.blit(image.surface, (15, 5))

    pygame.display.flip()
    clock.tick(6)
