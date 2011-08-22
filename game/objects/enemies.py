import random

from local import asciisprites

from basic import Basic

from options import Enemies


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
        s._control()
        s._move()
        s._shoot()
        s.draw(s._game.screen)
        return True

    def _control(s):
        course = s._think()
        if s._moves:
            for i in s._moves:
                s._moves[i] = False
            for i in range(len(course)):
                s._moves[course[i]] = True

    def _think(s):
        directions = []
        if 'dumbdown' in s._behaviour:
            directions.append('down')
        if 'followx' in s._behaviour:
            if not s.rect.top > s._target.rect.bottom:
                s._thrust = 1
                s._blah = True
                if s.rect.left > s._target.rect.centerx:
                    directions.append('left')
                elif s.rect.right < s._target.rect.centerx:
                    directions.append('right')
                else:
                    directions.append('left')
                    directions.append('right')
            elif s._blah:
                s._thrust = random.randint(30, 100) / 100.0
                s._blah = False
        return directions
