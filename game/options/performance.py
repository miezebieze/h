from random import randint
import pygame.locals
from data import *

GAME = {
        'screensize': (70, 150),
        'bounds_offset': {
            'top': 32,
            'left': 16,
            'right': 16,
            'bottom': 8
            },
        'fps':        30,
        'enemy_p_sec': 50,
        'start_enemies': 30,
        'start_stars': 30,
        'bg_colour':   Colours['transblack'],
        'prob': {
            'red': 20,
            'green': 10
        }
    }

KEYS = {
        'left':  [pygame.locals.K_LEFT,  pygame.locals.K_a],
        'right': [pygame.locals.K_RIGHT, pygame.locals.K_d],
        'up':    [pygame.locals.K_UP,    pygame.locals.K_w],
        'down':  [pygame.locals.K_DOWN,  pygame.locals.K_s],
        'shoot': [pygame.locals.K_z,     pygame.locals.K_j],
        'bomb':  [pygame.locals.K_x,     pygame.locals.K_k],
        'quit':  [pygame.locals.K_ESCAPE],
        'pause': [pygame.locals.K_p]
        }
 
DIRECTIONS = ['left', 'right', 'up', 'down']

### class Player(Moving):
## game.group = 'player; game.player
# also legend of properties

PLAYER = {
    # everything:
    'health':       7,  # health. if==None: self.invincible
    'damage':       1,  # collision damage to others, if==None: other.instadeath
    'team':     'player', # TODO: idk
    'moving':     True, # if it can move
    # Moving only:
    'speed':       60,  # speed in pixels/second
    'speedmin':   0.75, # speedmod when moving diagonal
    'speedmax':   1.25, # speedmod with booster
    # player only:
    'start_position': (GAME['screensize'][0] / 2, GAME['screensize'][1] - 20),
    'power':        0,  # TODO: (upgradeable) shotpower
    'shootspeed':  10, # delay of normal shot, in times/second
    'ammo':         100, # TODO: amount of normal ammo
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


Images = {
    'player': {
        'colours': {'X': Colours['magenta']},
        'sprite': Sprites['player']},
    'blue': {
        'colours': {'X': Colours['cyan'],
                    'O': Colours['yellow'],
                    'o': Colours['cyantr']},
        'sprite': Sprites['blue']},
    'red': {
        'colours': {'X': Colours['red']},
        'sprite': Sprites['red']},
    'green': {
        'colours': {'X': Colours['greend']},
        'sprite': Sprites['green']},
    #'yellow': {},
    #'boss': {},
    'bullet': {
        'colours': {'X': Colours['white']},
        'sprite': Sprites['bullet']},
    #'ebullet': {},
    #'bbullet': {},
    'rocket': {
        'colours': {'X': Colours['green']},
        'sprite': Sprites['rocket']},
    'money': {
        'colours': {'X': Colours['yellowb'],
                    'O': Colours['yellowd']},
        'sprite': Sprites['money']['1']},
    'bullets': {
        'colours': Sprites['bullets']['colours'],
        'sprite': Sprites['bullets']['sprite']},
    'planet': {
        'colours': {'X': Colours['yellowd']},
        'sprite':   Sprites['planet']},
    'stars': {
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['pixel']},
    'starm': {
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['bullet']},
    'starl': {
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['star']},
    'paused': {
        'colours': {'X': Colours['white']},
        'sprite': Sprites['paused']},
    'game': {
        'colours': {'X': Colours['white']},
        'sprite': Sprites['game']},
    'over': {
        'colours': {'X': Colours['white']},
        'sprite': Sprites['over']}
    }

        
### class Thinking(Moving):
# game.group = 'enemies'
Enemies = {
    'blue': {
        'health':   1,
        'damage':   2,
        'speed':    30,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['dumb']
        },
    'red': {
        'health':   2,
        'damage':   4,
        'speed':    90,
        'speedmin': 0.7,
        'speedmax': 1.8,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['dumb', 'follow_fast']
        },
    'green': {
        'health':   9,
        'damage':   4,
        'speed':    60,
        'speedmin': 0.3,
        'speedmax': 1.2,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['smart', 'follow_slow', 'shooting']
        }
    }

### class Thinking(Moving):
## game.group = 'bullets'
Bullets = {
    'bullet': {
        'health':   1,
        'damage':   2,
        'speed':    300,
        'team':     None,
        'moving':   True,
        },
    'rocket': {
        'health':   1,
        'damage':   5,
        'speed':    240,
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
    'planet': {
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

