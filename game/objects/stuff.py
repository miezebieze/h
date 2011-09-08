import random

#from local import asciisprites

from basic import Basic

#from options import Options as Game
#from options import Bullets



class Pickup(Basic):

    instances = []

    def __init__(s, game, options, position, image, group = 'power',
                 initdirection = None, colliders = ['player']):
        Basic.__init__(s, game, options, position, group,
                       initdirection, colliders)
        s.instances.append(s)
        if options['type'] == 'money':
            s.value = options['value']
            s.halflife = options['halflife']
        elif options['type'] == 'powerup':
           pass 



class Bullet(Basic):

    instances = []

    def __init__(s, game, options, position, image, group = 'bullets',
                 course = 'up', colliders = ['static', 'enemies']):
        Basic.__init__(s, game, options, position,
                       image, group, course, colliders)
        s.instances.append(s)


'''
class Animated(Basic):

    def __init__(s, game, options, position, image, group, colliders = []):
        Basic.__init__(s, game, options, position, image, group, colliders)
        s.fps = options['fps']
        s.animation = asciisprites.Animation(options['sprites'],
                                        options['timeline'],
                                        options['colours'])
        s.image = s.animation.surface
    def update(s):
        if s.out_of_game():
            return False

        if s.frame >= float(s._game.fps) / s.animation.fps:
            s.animation.update()
        s.draw(s._game.screen)
        return True
'''
