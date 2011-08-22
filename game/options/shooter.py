import pygame.locals
from data import *

GAME = {
        'screensize': (70, 150),
        'bounds_offset': {
            'top': 32,
            'left': 16,
            'right': 16,
            'bottom':8 
            },
        'fps': 30, # All times in game are counted in ms.
        'enemy_p_sec': 100,
        'start_enemies': 0,
        'start_stars': 30,
        'bg_colour':   Colours['transblack'],
        'prob': {
            'red': 20,
            'green': 10
        }
    }

# Groups of objects in game: For collision mainly.
GROUPS = ['player', 'enemies', 'bullets', 'stuff', 'static', 'power', 'tmp']

# Queue for updating the object groups:
# Player is updated separately. Don't add it here!
QUEUE = ['stuff', 'static', 'bullets', 'enemies', 'power']

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

OBJECTS = {
    'player': {
        # also legend of object properties.
        # everything: (class Basic)
        'health':       7,  # health. if==None: self.invincible
        'damage':       1,  # collision damage to others, if==None: other.instadeath
        'team':     'player', # TODO: idk
        'moving':     True, # if it can move
        # Moving only:
        'speed':       60,  # speed in pixels/second
        'speedmin':   0.75, # speedmod when moving diagonal
        'speedmax':   1.25, # speedmod with booster
        # player only: (class Player)
        'start_position': (GAME['screensize'][0] / 2, GAME['screensize'][1] - 20),
        'power':        0,  # TODO: (upgradeable) shotpower
        'shootspeed':  10, # delay of normal shot, in times/second
        'ammo':         10000, # TODO: amount of normal ammo
        'bombs':        20,  # amount of special ammo
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
        'colours': {'X': Colours['magenta']},
        'sprite': Sprites['player']
        #'animated':  False   # whether the sprite is animated
        },
    # enemies (class Thinking)
    #'yellow': {}, TODO
    #'boss': {}, TODO
    'blue': {
        'health':   1,
        'damage':   2,
        'speed':    10,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['dumb'],
        'colours': {'X': Colours['cyan'],
                    'O': Colours['yellow'],
                    'o': Colours['cyantr']},
        'sprite': Sprites['blue']
        },
    'red': {
        'health':   2,
        'damage':   4,
        'speed':    60,
        'speedmin': 0.7,
        'speedmax': 1.8,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['dumb', 'follow_fast'],
        'colours': {'X': Colours['red']},
        'sprite': Sprites['red']
        },
    'green': {
        'health':   9,
        'damage':   4,
        'speed':    40,
        'speedmin': 0.3,
        'speedmax': 1.2,
        'team':     'enemy',
        'moving':   True,
        'behaviour':['smart', 'follow_slow', 'shooting'],
        'colours': {'X': Colours['greend']},
        'sprite': Sprites['green']
        },
    # projectiles (class Bullet)
    'bullet': {
        'health':   1,
        'damage':   2,
        'speed':    300,
        'team':     None,
        'moving':   True,
        'colours': {'X': Colours['white']},
        'sprite': Sprites['bullet']
        },
    'rocket': {
        'health':   1,
        'damage':   5,
        'speed':    240,
        'team':     None,
        'moving':   True,
        'colours': {'X': Colours['green']},
        'sprite': Sprites['rocket']
        },
    'ebullet': {
        'health':   1,
        'damage':   3,
        'speed':    160,
        'team':     None,
        'moving':   True,
        'colours': {'X': Colours['red']},
        'sprite': Sprites['bullet']
        },
    'bbullet': {
        'health':   None,
        'damage':   None,
        'speed':    120,
        'team':     None,
        'moving':   True,
        'colours': {'X': Colours['red']},
        'sprite': Sprites['star']
        },
    # stuff
    'money': {
        'health':   None,
        'damage':   0,
        'colours': {'X': Colours['yellowb'],
                    'O': Colours['yellowd']},
        'sprite': Sprites['money']['1']
        },
    'planet': {
        'health':   None,
        'damage':   None,
        'colours': {'X': Colours['yellowd']},
        'sprite':   Sprites['planet'],
        },
    'stars': {
        'health':   None,
        'damage':   0,
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['pixel'],
        },
    'starm': {
        'health':   None,
        'damage':   0,
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['bullet'],
        },
    'starl': {
        'health':   None,
        'damage':   0,
        'colours': {'X': Colours['yellowb']},
        'sprite': Sprites['star'],
        },
    'paused': {
        'health':   None,
        'damage':   0,
        'colours': {'X': Colours['white']},
        'sprite': Sprites['paused'],
        },
    'game': {
        'health':   None,
        'damage':   0,
        'colours': {'X': Colours['white']},
        'sprite': Sprites['game'],
        },
    'over': {
        'health':   None,
        'damage':   0,
        'colours': {'X': Colours['white']},
        'sprite': Sprites['over'],
        }
    }
