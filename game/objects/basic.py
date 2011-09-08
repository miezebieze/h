import pygame

#from local import asciisprites

#from options import GAME, DIRECTIONS
#from options import Enemies
#from options import Bullets


class Basic(object):

    instances = None # List with instances of the Class. Only subclasses
                     # may contain an actual list.

    def __init__(s, game, options, position, image, group = None,
                 course = None, colliders = []):
        s._game = game
        s.GAME = s._game.OPTIONS.GAME
        # Visual data:
        s.image = image
        s.rect = pygame.Rect((0,0), s.image.surface.get_size())
        s.move_to(position)
        # Gaming data:
        try:
            s.team = options['team']
        except KeyError:
            s.team = None
        s.health = options['health']
        s.maxhealth = options['health']
        s.damage = options['damage']
        s.colliders = colliders
        s.group = group
        # For movement:
        try:
            s._moves = options['moving']
        except KeyError:
            s._moves = False
        if s._moves:
            #s._moved = True
            s._thrust = 1
            s._moves = {}
            for i in s._game.OPTIONS.DIRECTIONS:
                s._moves[i] = False
            if bool(course):
                if isinstance(course, list):
                    for direction in course:
                        s._moves[direction]
                else:   s._moves[course] = True
            s._speed = 1.0 * options['speed'] / s._game.fps
            try:             s._speedmin = options['speedmin']
            except KeyError: s._speedmin = 1
            try:             s._speedmax = options['speedmax']
            except KeyError: s._speedmax = 1

    def update(s):
        if s.out_of_game():
            return False
        s.collide_ip()
        if s._moves:
            s._move()
        #if s.group == 'static_stuff':
         #   s.draw(s._game.background)
        #else:
        s.draw(s._game.screen)
        return True

    def move_to(s, position):
        (s.x, s.y) = position
        s.adjust_position()

    def adjust_position(s):
        ''' Update s.rect.center to [s.x, s.y].
        This is needed, so while 'pygame.Rect' can
        only store ints, the position can be in floats.'''
        s.rect.center = (s.x, s.y)

    def draw(s, surface):
        surface.blit(s.image.surface, s.rect.topleft)

    def collide_ip(s):
        ''' Collide s.rect with all objects in s.colliders lists. '''
        for i in range(len(s.colliders)):
            if s.dead(): break
            for j in range(len(s._game.objects[s.colliders[i]])):
                if s.dead(): break
                object = s._game.objects[s.colliders[i]][j]
                if not s == object: # it could happen
                    if s.collides_with(object):
                        if not object.out_of_game():
                            if not s.health == None: # invincible
                                if object.damage == None: # almighty
                                    s.health = 0
                                else:
                                    s.health -= object.damage
                            if not object.health == None:
                                if s.damage == None:
                                    object.health = 0
                                else:
                                    object.health -= s.damage



    def _move(s):
        ''' Move the item by s.speed in s.moves['direction'].
            AI controlled objects have extended bounds,
            where Player has only on-screen visible bounds.i
            With it's own method.)'''
        s.move_internal(s._game.bounds)

    def _shoot(s):
        ''' Space for the shooting stuff. '''
        pass
    def _control(s):
        ''' Space for the AI or the player controls. '''
        pass

    def in_bounds(s, bounds):
        return bounds.contains(s.rect)

    def moves_out_of_bounds(s, direction, bounds):
        if direction is 'left':
            return s.rect.left <= bounds.left
        if direction is 'right':
            return s.rect.right >= bounds.right
        if direction is 'up':
            return s.rect.top <= bounds.top
        if direction is 'down':
            return s.rect.bottom >= bounds.bottom
        
    def vulnerable(s):
        return s.health is not None

    def dead(s):
        return s.vulnerable() and s.health <= 0

    def out_of_game(s):
        return not s.in_bounds(s._game.bounds) or s.dead()

    def collides_with(s, object):
        return s.rect.colliderect(object.rect)

    def move_internal(s, bounds):
        dirs = s._game.OPTIONS.DIRECTIONS # l, r, u, d
        NUMS = [[0,2,3], [1,2,3], [2,0,1], [3,0,1]]
        offset = [0, 0, 0, 0]
        for i, j1, j2 in NUMS:
            if s._moves[dirs[i]]:
                if not s.moves_out_of_bounds(dirs[i], bounds):
                    if s._moves[dirs[j1]] and s._moves[dirs[j2]]:
                        offset[i] += (s._speed * s._speedmax) * s._thrust
                    elif s._moves[dirs[j1]] or s._moves[dirs[j2]]:
                        offset[i] += (s._speed * s._speedmin) * s._thrust
                    else:
                        offset[i] += s._speed * s._thrust
        s.x -= offset[0]
        s.x += offset[1]
        s.y -= offset[2]
        s.y += offset[3]
        s.adjust_position()
