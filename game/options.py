from random import randint
import pygame.locals
from data import *
from data import Sprites

Options = {
    'Game': {
        'screensize': (200, 600),
        'boundsoffset': {
            'top': 32,
            'left': 16,
            'right': 16,
            'bottom': 8
            },
        'FPS':        30,
        'enemydelay': 1,
        'startenemies': 120,
        'powerupdelay': 300,
        'startstars': 200,
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
        'left':  0,
        'right': 1,
        'up':    2,
        'down':  3
        }
    }
### class Player(Moving):
## game.group = 'player; game.player
# also legend of properties

Player = {
    # everything:
    'health':       7,  # health. if==None: self.invincible
    'damage':       1,  # collision damage to others, if==None: other.instadeath
    'team':     'player', # TODO: idk
    'moving':     True, # if it can move
    # Moving only:
    'speed':        2,  # speed in pixels per frame TODO: pixels/second
    'speedmin':   0.75, # speedmod when moving diagonal
    'speedmax':   1.25, # speedmod with booster
    # player only:
    'startposition': (Options['Game']['screensize'][0] / 2,
                      Options['Game']['screensize'][1] - 20),
    'power':        0,  # TODO: (upgradeable) shotpower
    'shootspeed':   5,  # delay of normal shot, in frames/shot TODO: times/second
    'ammo':         10, # TODO: amount of normal ammo
    'bombs':        2,  # amount of special ammo
    'lives':        4,  # amount of lives at start
    # more player: upgrade-/collectable maximums
    'maxpower':     0,
    'maxshootspeed': 5,
    'maxammo':      31,
    'maxbombs':     7,
    'maxlives':     7,
    'maxspeed':     2,
    'maxspeedmax':  2,
    'maxspeedmin':  1,
    'maxdamage':    1,
    # AI only:
    'behaviour':    [],  # what the AI does with 'self'
    # visual data:
    'animated':  False   # whether the sprite is animated
    }
### class Thinking(Moving):
# game.group = 'enemies'
Images = {
    'blue': {
        'colours': {'X': Colours['cyan'],
                    'O': Colours['yellow'],
                    'o': Colours['cyantr']},
        'sprite': Sprites['Ship2']},
    'red': {
        'colours': {'X': Colours['red']},
        'sprite': Sprites['Ship3r']},
    #'green': {},
    #'yellow': {},
    #'boss': {},
    'player': {
        'colours': {'X': Colours['magenta']},
        'sprite': Sprites['Ship1']},
    'bullet': {
        'colours': {'X': Colours['white']},
        'sprite': Sprites['Bullet']},
    'rocket': {
        'colours': {'X': Colours['green']},
        'sprite': Sprites['Rocket']},
    'money': {
        'colours': {'X': Colours['yellowb'],
                    'O': Colours['yellowd']},
        'sprite': Sprites['Money']['1']},
    'sun': {
        'colours': {'X': Colours['yellowd']},
        'sprite':   Sprites['Sun']},
    'stars': {
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['Bullet']},
    'starm': {
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['Starm']},
    'starl': {
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['Starl']},
    'paused': {
        'colours': {'X': Colours['white']},
        'sprite': Sprites['Paused']},
    'game': {
        'colours': {'X': Colours['white']},
        'sprite': Sprites['Game']},
    'over': {
        'colours': {'X': Colours['white']},
        'sprite': Sprites['Over']}
    }

        
Enemies = {
    'blue': {
        'health':   1,
        'damage':   3,
        'speed':    1,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['dumbdown']
        },
    'red': {
        'health':   2,
        'damage':   5,
        'speed':    3,
        'speedmin': 0.7,
        'speedmax': 1.8,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['dumbdown', 'followx']
        }

    }

### class Thinking(Moving):
## game.group = 'bullets'
Bullets = {
    'bullet': {
        'health':   1,
        'damage':   2,
        'speed':    10,
        'team':     None,
        'moving':   True,
        },
    'rocket': {
        'health':   1,
        'damage':   5,
        'speed':    8,
        'team':     None,
        'moving':   True
        }

    }

### class Powerup(Moving):
## game.group = <<power>>
### class Basic
## game.group = <<several>>
Stuff = {
    'money': {
        'health':   None,
        'damage':   0,
        },
    'sun': {
        'health':   None,
        'damage':   None,
        },
    'stars': {
        'health':   None,
        'damage':   0,
        },
    'starm': {
        'health':   None,
        'damage':   0,
        },
    'starl': {
        'health':   None,
        'damage':   0,
        },
    'paused': {
        'health':   None,
        'damage':   0,
        },
    'game': {
        'health':   None,
        'damage':   0,
        },
    'over': {
        'health':   None,
        'damage':   0,
        }
    }

