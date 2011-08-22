import pygame.locals
from data import *

Options = {
    'Game': {
        'screensize': (128, 128),
        'boundsoffset': {
            'top': 32,
            'left': 16,
            'right': 16,
            'bottom': 8
            },
        'FPS':        30,
        'enemydelay': 100,
        'powerupdelay': 300,
        'bgcolour':   Colours['transblack']
        },
    'Keys': {
        'left': [pygame.locals.K_LEFT,  pygame.locals.K_a],
        'right':[pygame.locals.K_RIGHT, pygame.locals.K_d],
        'down': [pygame.locals.K_DOWN,  pygame.locals.K_s],
        'up':   [pygame.locals.K_UP,    pygame.locals.K_w],
        'shoot':[pygame.locals.K_z,     pygame.locals.K_j],
        'bomb' :[pygame.locals.K_x,     pygame.locals.K_k],
        'quit': [pygame.locals.K_ESCAPE],
        'pause':[pygame.locals.K_p]
        },
    'Directions': {
        'left':  4,
        'right': 6,
        'up':    8,
        'down':  2
        }
    }
Player = {
    'startposition': (56, 120),
    'life':     7,
    'power':    0,
    'speed':    2,
    'team':     'player',
    'shootspeed': 5,
    'bombs':    2,
    'damage':   1,
    'sprite':   Sprites['Ship1'],
    'colours':  {
        'X': Colours['white']
        }
    }

Enemies = {
    'dumb': {
        'life':     2,
        'speed':    1,
        'damage':   3,
        'team':     'enemy',
        'behaviour':['dumbdown'],
        'sprite':   Sprites['Ship2'],
        'colours':  {
            'X': Colours['white']
            }
        },
    'followx': {
        'life':     5,
        'speed':    2,
        'damage':   5,
        'team':     'enemy',
        'behaviour':['dumbdown', 'followx'],
        'sprite':   Sprites['Ship3'],
        'colours':  {
            'X': Colours['white']
            }
        }
    }

Bullets = {
    'normal': {
        'life':     1,
        'speed':    8,
        'damage':   1,
        'team':     None,
        'sprite':   Sprites['Bullet'],
        'colours':  {
            'X': Colours['white']
            }
        },
    'rocket': {
        'life':     1,
        'speed':    8,
        'damage':   5,
        'team':     None,
        'sprite':   Sprites['Rocket'],
        'colours':  {
            'X': Colours['white']
            }
        }
    }

Stuff = {
    'sun': {
        'life':     None,
        'damage':   None,
        'sprite':   Sprites['Sun'],
        'colours':  {
            'X': Colours['yellowd']
            }
        },
    'star': {
        'life':     None,
        'damage':   0,
        'sprite':   Sprites['Star'],
        'colours':  {
            'X': Colours['yellowb']
            }
        },
    'paused': {
        'life':     None,
        'damage':   0,
        'sprite':   Sprites['Paused'],
        'colours':  {
            'X': Colours['white']
            }
        },
    'game': {
        'life':     None,
        'damage':   0,
        'sprite':   Sprites['Game'],
        'colours':  {
            'X': Colours['white']
            }
        },
    'over': {
        'life':     None,
        'damage':   0,
        'sprite':   Sprites['Over'],
        'colours':  {
            'X': Colours['white']
            }
        }
    }

