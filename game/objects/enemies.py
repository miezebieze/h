import random

from local import asciisprites

from basic import Basic

#from options import Enemies


class Thinking(Basic):

    def __init__(s, game, options, position, image, group,
                 initdirection = None, colliders = []):
        Basic.__init__(s, game, options, position, image, group,
                       initdirection, colliders)
        s._behaviour = options['behaviour']
        s._target = s._game.subject

    def update(s):
        if s.out_of_game():
            return False
        s.collide_ip()
        if s._control():
            s._move()
        s._shoot()
        s.draw(s._game.screen)
        return True

    def _control(s):
        if s._moves:
            course = s._think()
            for i in s._moves:
                s._moves[i] = False
            for i in range(len(course)):
                s._moves[course[i]] = True
            return True
        return False

    def _think(s):
        directions = []
        if 'dumb' in s._behaviour:
            directions.append('down')
        elif 'smart' in s._behaviour:
            # placeholder:
            directions.append('down')
        if 'follow_fast' in s._behaviour:
            if not s.rect.top > s._target.rect.bottom:
                # not below player ship
                s._thrust = 0.8
                s._followswitch = True
                if s.rect.left > s._target.rect.centerx:
                    directions.append('left')
                elif s.rect.right < s._target.rect.centerx:
                    directions.append('right')
                else:
                    directions.append('left')
                    directions.append('right')
            elif s._followswitch:
                # thing will only happen once until the target
                # is in 'sight' again.
                s._thrust = random.randint(30, 100) / 100.0
                s._followswitch = False
        if 'follow_slow' in s._behaviour:
            if not s.rect.top > s._target.rect.bottom:
                if s.rect.left > s._target.rect.centerx:
                    directions.append('left')
                elif s.rect.right < s._target.rect.centerx:
                    directions.append('right')
                
                
        return directions
