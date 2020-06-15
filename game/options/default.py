import pygame.locals
from .data import Colours, Prototypes

# For moving of objects: ESSENTIAL! Don't change, unless You know what Your doing
DIRECTIONS = ['left', 'right', 'up', 'down']

GAME = {
        'screensize': (300, 400),
        'main_bounds_offset': [16, 16, 16, 16],
        'fps': 30, # All times in game are counted in ms.
                   # I don't know, what this means?
        'enemy_p_sec': 20, # enemies per second
        'default_enemy': 'blue', # Which enemy shall be spammed on screen,
                                 # before the game begins. TODO Multiple with percents
        'start_enemies': 100,    # How much of them
        'start_stars': 200,  # How much stars should be generated at startup.
                             # They are then put on a big surface, so add like you like.
        'bg_colour':   Colours['transblack'], # background colour; trans for transparent
        'prob': {       # What model the next spawned enemy will be in percent.
            'red': 35,   # Only not default have to be listed.
            'green': 10  # For not using the default, fill the percents, or TODO: None
        }
    }

# Groups of objects in game: For collision mainly.
GROUPS = ['player', 'enemies', 'bullets', 'stuff', 'static', 'power', 'tmp']

# Queue for updating the object groups:
# Player is updated separately. Don't add it here!
QUEUE = ['stuff', 'static', 'bullets', 'enemies', 'power']

KEYS = {
        'left':  [pygame.locals.K_LEFT,  pygame.locals.K_h],
        'right': [pygame.locals.K_RIGHT, pygame.locals.K_l],
        'up':    [pygame.locals.K_UP,    pygame.locals.K_k],
        'down':  [pygame.locals.K_DOWN,  pygame.locals.K_j],
        'shoot': [pygame.locals.K_z,     pygame.locals.K_d],
        'bomb':  [pygame.locals.K_x,     pygame.locals.K_f],
        'quit':  [pygame.locals.K_ESCAPE],
        'pause': [pygame.locals.K_p]
        }
 
### class Player(Moving):
## game.group = 'player; game.player
# also legend of properties

OBJECTS = {
    'player': {
        # also legend of object properties.
        # everything: (class Basic)
        'health':       7,  # health. if==None: self.invincible
        'damage':       1,  # collision damage to others, if==None: other.instadeath
        'team':     'player', # TODO: idk
        'moving':     True, # if it can move
        'bounds_offset': None, # Coordinates considered out of bounds None = default
        # Moving only:
        'speed':       120,  # speed in pixels/second
        'speedmin':   0.75, # speedmod when moving diagonal
        'speedmax':   1.25, # speedmod with booster
        # player only: (class Player)
        'start_position': (GAME['screensize'][0] / 2, GAME['screensize'][1] - 20),
        'power':        0,  # TODO: (upgradeable) shotpower
        'shootspeed':   3, # delay of normal shot, in times/second
        'ammo':         100, # TODO: amount of normal ammo
        'bombs':        2,  # amount of special ammo
        'lives':        4,  # amount of lives at start
        # more player stuff: upgrade-/collectable maximums
        'maxpower':     0,
        'maxshootspeed': 5,
        'maxammo':      31,
        'maxbombs':     7,
        'maxlives':     7,
        'maxspeed':     2,
        'maxspeedmax':  2,
        'maxspeedmin':  1,
        'maxdamage':    1,
        # AI only: (class Thinking)
        'behaviour':    [],  # what the AI does with 'self'
        # visual data:
        'prototype':    Prototypes['player']
        #'animated':  False   # whether the sprite is animated
        },
    # enemies (class Thinking)
    #'yellow': {}, TODO
    #'boss': {}, TODO
    'blue': {
        'health':   2,
        'damage':   2,
        'speed':    60,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['dumb'],
        'prototype':Prototypes['blue']
        },
    'red': {
        'health':   2,
        'damage':   4,
        'speed':    180,
        'speedmin': 0.7,
        'speedmax': 1.8,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['dumb', 'follow_fast'],
        'prototype':Prototypes['red']
        },
    'green': {
        'health':   9,
        'damage':   4,
        'speed':    120,
        'speedmin': 0.3,
        'speedmax': 1.2,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['smart', 'follow_slow', 'shooting'],
        'prototype':Prototypes['green']
        },
    # projectiles (class Bullet)
    'bullet': {
        'health':   1,
        'damage':   2,
        'speed':    200,
        'team':     None,
        'moving':   True,
        'prototype':Prototypes['bullet']
        },
    'rocket': {
        'health':   1,
        'damage':   5,
        'speed':    160,
        'team':     None,
        'moving':   True,
        'prototype':Prototypes['rocket']
        },
    'ebullet': {
        'health':   1,
        'damage':   3,
        'speed':    160,
        'team':     None,
        'moving':   True,
        'prototype':Prototypes['bullet']
        },
    'bbullet': {
        'health':   None,
        'damage':   None,
        'speed':    120,
        'team':     None,
        'moving':   True,
        'prototype':Prototypes['bullet']
        },
    # stuff
    'money': {
        'health':   None,
        'damage':   0,
        'prototype':Prototypes['money']
        },
    'planet': {
        'health':   None,
        'damage':   None,
        'prototype':Prototypes['planet']
        },
    'stars': {
        'health':   None,
        'damage':   0,
        'prototype':Prototypes['stars']
        },
    'starm': {
        'health':   None,
        'damage':   0,
        'prototype':Prototypes['starm']
        },
    'starl': {
        'health':   None,
        'damage':   0,
        'prototype':Prototypes['starl']
        },
    'paused': {
        'health':   None,
        'damage':   0,
        'prototype':Prototypes['paused']
        },
    'game': {
        'health':   None,
        'damage':   0,
        'prototype':Prototypes['game']
        },
    'over': {
        'health':   None,
        'damage':   0,
        'prototype':Prototypes['over']
        }
    }
