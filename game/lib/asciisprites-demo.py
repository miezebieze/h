import sys, pygame
from pygame.locals import KEYUP, QUIT, K_ESCAPE, K_q, SRCALPHA, \
                          K_LEFT, K_RIGHT, K_SPACE, K_DOWN

from asciisprites import Image, Animation


### Data:
# Setup a test image:
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

# Setup Frames for animation:
animation = [
        """
 XXX 
XXXXX
XXOXX
XXXXX
 XXX 
""",    """
  X  
 XXX 
 XXX 
 XXX 
  X  
""",    """
  X  
  X  
  X  
  X  
  X  
""",    """
  X  
 XXX 
 XOX 
 XXX 
  X  
""",    """
 XXX 
XXOXX
XOXOX
XXOXX
 XXX 
"""]
# Define Timelines:
backwards = [0, 1, 2, 3, 4, 3, 2, 1]
forewards = [4, 3, 2, 1, 0, 1, 2, 3]

# Define Colours:
coloursI = [(255, 0, 0, 255),
            (0, 255, 0, 255),
            (255, 255, 0, 255),
            (0, 0, 255, 255)
    ]
coloursB = [(64, 64, 64, 255),
            (128, 128, 128, 255),
            (192, 192, 192, 255),
            (255, 255, 255, 255)
    ]
# Assign Colours to letters: colours[n] uses coloursX[n]
colours = ['T', 'E', 'S', 'A']

Gold = {'X': (200, 150, 0, 255),
        'O': (255, 255, 0, 255)
    }
Silver={'X': (200, 200, 200, 255),
        'O': (100, 100, 100, 255)
    }
Bronze={'X': (150, 50, 0, 255),
        'O': (200, 75, 0, 255)
    }

gold = True
blind = False

def swapcolours(forward=True):
    if forward: colours.append(colours.pop(0))
    else:       colours.insert(0, colours.pop(3))

def getcolourdict():
    # Make a dict for 'Image'
    dict = {}
    for i in range(4):
        if blind: dict[colours[i]] = coloursB[i]
        else:     dict[colours[i]] = coloursI[i]
    return dict

# Setup pygame:
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((66, 18), SRCALPHA, 32)

# Setup the objects:
image = Image(image, getcolourdict())
print ('ani1')
ani1  = Animation(animation, backwards, Gold)
print ('ani2')
ani2  = Animation(animation, forewards, Gold)

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit() # needed by users of idle.
            sys.exit()
        if e.type == KEYUP:
            if e.key == K_ESCAPE or e.key == K_q:
                pygame.quit()
                sys.exit()

            if e.key == K_RIGHT:
                # one way to change the colours of the image
                swapcolours()
                image.colours = getcolourdict()
                #image.update_colours()
            if e.key == K_LEFT:
                # and the other way...
                swapcolours(False)
                image.colours = getcolourdict()
                #image.update_colours()

            if e.key == K_SPACE:
                # print the asciis stored in ani1 and switch colour blind mode!
                #print ani1.get_asciis()
                if blind:
                    blind = False
                    image.set_colours(getcolourdict())
                    if gold:
                        ani1.set_colours(Gold)
                        ani2.set_colours(Gold)
                    else:
                        ani1.set_colours(Bronze)
                        ani2.set_colours(Bronze)
                else:
                    image.set_colours(getcolourdict())
                    ani1.set_colours(Silver)
                    ani2.set_colours(Silver)
                    blind = True

                #image.update_colours()

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


'''
Make a library, for playing animations:
    Animation would have a switch to end it after n iterations.
    Another one to show if it's done with n.
    Daemonizing would be accomplished with something like:
        ani = Animation(args)

Animation: ([asciis], [timeline], {colours})
    frames:
        [Image objects in order of asciis]
    timeline:
        [indexes of frames]
    surface:
        surface of current frame
'''
