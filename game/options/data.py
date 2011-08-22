Colours = {
    'white':    (255, 255, 255, 255),
    'black':    (0, 0, 0, 255),
    'red':      (255, 0, 0, 255),
    'green':    (0, 255, 0, 255),
    'blue':     (0, 0, 255, 255),
    'yellow':   (255, 255, 0, 255),
    'magenta':  (255, 0, 255, 255),
    'cyan':     (0, 255, 255, 255),
    'orange':   (255, 127, 0, 255),
    'yellowb':  (255, 255, 100, 255),
    'yellowd':  (200, 150, 0, 255),
   'transwhite':(255, 255, 255, 0),
   'transblack':(0, 0, 0, 0),
    'cyantr':   (0, 255, 255, 175),
    'greend':   (40, 200, 20, 255)
    }

Blueprints = {
    'r0':
"""
   XX   
   XX   
  XXXX  
  XXXX  
 XXXXXX 
XXXXXXXX
XX XX XX
X  XX  X
X XXXX X
""",
    'f0':
"""
  XXXX  
 XooooX 
 XooooX 
 XooooX 
XXXXXXXX
XOOOOOOX
XXXXXXXX
 XXXXXX 
""",
    'f1':
"""
   XX   
  XXXX  
XXXXXXXX
XXXXXXXX
 XXXXXX 
  XXXX  
  XXXX  
   XX   
""",
    'r1':
"""
X  XX  X
X  XX  X
XX XX XX
XXXXXXXX
 XXXXXX 
  XXXX  
   XX   
  XXXX  
""",
    'f2':
"""
  XXXX  
   XX   
  XXXX  
 XXXXXX 
XXXXXXXX
XX XX XX
X  XX  X
X  XX  X
""",
    'b0':
"""
       XX       
      XXXX      
      XXXX      
      XXXX      
     XXXXXX     
   XXXXXXXXXX   
   XXXXXXXXXX   
  XXXXXXXXXXXX  
 XXXXXXXXXXXXXX 
XXXXXXXXXXXXXXXX
XXXX   XX   XXXX
XXX    XX    XXX
XXX    XX    XXX
XX    XXXX    XX
XX   XXXXXX   XX
X   XXX  XXX   X
""",
    'bullet':
"""
XX
XX
""",
    'rocket':
"""
 XX 
XXXX
XXXX
XXXX
 XX 
XXXX
""",
    'planet':
"""
      XXXX      
    XXXXXXXX    
   XXXXXXXXXX   
  XXXXXXXXXXXX  
 XXXXXXXXXXXXXX 
 XXXXXXXXXXXXXX 
XXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXX
 XXXXXXXXXXXXXX 
 XXXXXXXXXXXXXX 
  XXXXXXXXXXXX  
   XXXXXXXXXX   
    XXXXXXXX    
      XXXX      
""",
    'star':
"""
X X X
 XXX 
XXXXX
 XXX 
X X X
""",
    'pixel':
"""
X
""",
    'money': {
     '1':
"""
 XXX 
XXOXX
XOOOX
XXOXX
 XXX 
""",
    '2':
"""
  X  
 XXX 
 XXX 
 XXX 
  X  
""",
    '3':
"""
  X  
  X  
  X  
  X  
  X  
"""
    }
}


Prototypes = {
    'player': {
        'sprite': Blueprints['r0'],
        'colours': {'X': Colours['magenta']}
    },
    'blue': {
        'sprite': Blueprints['f0'],
        'colours': {'X': Colours['blue'],
                    'o': Colours['cyan'],
                    'O': Colours['yellow']}
    },
    'green': {
        'sprite': Blueprints['f1'],
        'colours': {'X': Colours['green']}
    },
    'redr': {
        'sprite': Blueprints['r1'],
        'colours': {'X': Colours['red']}
    },
    'red': {
        'sprite': Blueprints['f2'],
        'colours': {'X': Colours['red']}
    },
    'boss': {
        'sprite': Blueprints['b0'],
        'colours': {'X': Colours['orange']}
    },
    'bullet': {
        'sprite': Blueprints['bullet'],
        'colours': {'X': Colours['yellow']}
    },
    'rocket': {
        'sprite': Blueprints['rocket'],
        'colours': {'X': Colours['white']}
    },
    'planet': {
        'sprite': Blueprints['planet'],
        'colours': {'X': Colours['orange']}
    },
    'stars': {
        'sprite': Blueprints['pixel'],
        'colours': {'X': Colours['yellow']}
    },
    'starm': {
        'sprite': Blueprints['bullet'],
        'colours': {'X': Colours['yellow']}
    },
    'starl': {
        'sprite': Blueprints['star'],
        'colours': {'X': Colours['yellow']}
    },
    'money': {
        'sprite': Blueprints['money']['1'],
        'colours': {'X': Colours['yellowb'],
                    'O': Colours['yellowd']}
    },
    'bullets': {
        'sprite':
"""
 XXXXXXXXXX 
X          X
X AB AB AB X
X CD CD CD X
X ED ED ED X
X ED ED ED X
X ED ED ED X
X EF EF EF X
X          X
 XXXXXXXXXX 
""",
        'colours': {'X': (106, 120, 10, 255),
                    'A': (82, 65, 37, 255),
                    'B': (200, 156, 88, 255),
                    'C': (125, 98, 56, 255),
                    'D': (236, 150, 16, 255),
                    'E': (120, 77, 10, 255),
                    'F': (138, 91, 17, 255)}
    },
    'paused': {
        'sprite':
"""
XXXXXXXXXX      XXXXX     XX       XX   XXXXXXXXXX  XXXXXXXXXXX  XXXXXXXXXX 
XXXXXXXXXXX    XXXXXXX    XX       XX  XXXXXXXXXXX  XXXXXXXXXXX  XXXXXXXXXXX
XX       XX    XX   XX    XX       XX  XX           XX           XX       XX
XX       XX   XX     XX   XX       XX  XX           XX           XX       XX
XXXXXXXXXXX   XX     XX   XX       XX  XXXXXXXXXX   XXXXXXXXX    XX       XX
XXXXXXXXXX    XXXXXXXXX   XX       XX   XXXXXXXXXX  XXXXXXXXX    XX       XX
XX           XXXXXXXXXXX  XX       XX           XX  XX           XX       XX
XX           XX       XX  XX       XX           XX  XX           XX       XX
XX           XX       XX  XXXXXXXXXXX  XXXXXXXXXXX  XXXXXXXXXXX  XXXXXXXXXXX
XX           XX       XX   XXXXXXXXX   XXXXXXXXXX   XXXXXXXXXXX  XXXXXXXXXX 
""",
        'colours': {'X': Colours['white']}
    },
    'game': {
        'sprite':
"""
 XXXXXXXXX      XXXXX      XXXXXXXXX   XXXXXXXXXXX
XXXXXXXXXXX    XXXXXXX    XXXXXXXXXXX  XXXXXXXXXXX
XX             XX   XX    XXX XXX XXX  XX         
XX            XX     XX   XX   X   XX  XX         
XX    XXXX    XX     XX   XX   X   XX  XXXXXXXXX  
XX    XXXXX   XXXXXXXXX   XX   X   XX  XXXXXXXXX  
XX       XX  XXXXXXXXXXX  XX   X   XX  XX         
XX       XX  XX       XX  XX   X   XX  XX         
XXXXXXXXXXX  XX       XX  XX   X   XX  XXXXXXXXXXX
 XXXXXXXXX   XX       XX  XX   X   XX  XXXXXXXXXXX
""",
        'colours': {'X': Colours['white']}
    },
    'over': {
        'sprite':
"""
 XXXXXXXXX   XX       XX  XXXXXXXXXXX  XXXXXXXXXX 
XXXXXXXXXXX  XX       XX  XXXXXXXXXXX  XXXXXXXXXXX
XXX     XXX   XX     XX   XX           XX       XX
XX       XX   XX     XX   XX           XX       XX
XX       XX    XX   XX    XXXXXXXXX    XXXXXXXXXXX
XX       XX    XX   XX    XXXXXXXXX    XXXXXXXXXX 
XX       XX     XX XX     XX           XX     XX  
XXX     XXX     XX XX     XX           XX     XX  
XXXXXXXXXXX      XXX      XXXXXXXXXXX  XX      XX 
 XXXXXXXXX       XXX      XXXXXXXXXXX  XX      XX 
""",
        'colours': {'X': Colours['white']}
    }
}
