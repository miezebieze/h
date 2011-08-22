import random

import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP

from local import asciisprites

from options import Options as Game
from options import Enemies
from options import Bullets



class Basic(object):

    def __init__(s, game, options, position, image, group = None,
                 course = None, colliders = []):
        s._game = game
        # Visual data:
        s.image = image
        #print s.image
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
            for key in Game['Directions']:
                s._moves[key] = False
            if bool(course):
                if isinstance(course, list):
                    for direction in course:
                        s._moves[direction]
                else:   s._moves[course] = True
            s._speed = options['speed']
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
            for object in s._game.objects[s.colliders[i]]:
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
                if s.dead(): break
            if s.dead(): break

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
        dirs = ['left', 'right', 'up', 'down']
        nums = [[0,2,3], [1,2,3], [2,0,1], [3,0,1]]
        offset = [0, 0, 0, 0]
        for i, j1, j2 in nums:
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



class Pickup(Basic):

    def __init__(s, game, options, position, image, group = 'power',
                 initdirection = None, colliders = ['player']):
        Basic.__init__(s, game, options, position, group,
                       initdirection, colliders)
        if options['type'] == 'money':
            s.value = options['value']
            s.halflife = options['halflife']
        elif options['type'] == 'powerup':
           pass 



class Bullet(Basic):

    def __init__(s, game, options, position, image, group = 'bullets',
                 course = 'up', colliders = ['static', 'enemies']):
        Basic.__init__(s, game, options, position,
                       image, group, course, colliders)



class Player(Basic):

    ''' is not s.update()'d! '''
    def __init__(s, game, options, position, image, group = 'player',
                 colliders = ['enemies', 'static', 'power']):
        Basic.__init__(s, game, options, position,
                       image, group, None, colliders)
        s._power = options['power']
        s._shootspeed = options['shootspeed']
        s._shootcooldown = 0
        s._shootkey = False
        s._bombkey = False
        s._ammo = options['ammo']
        s._bombs = options['bombs']
        s._lives = options['lives']
        s.money = 0
        s.stats = {
            'ammo': s._ammo, 'bombs': s._bombs, 'lives': s._lives,
            'shootspeed': s._shootspeed, 'power': s._power,
            'speed': s._speed, 'speedmax': s._speedmax, 'health': s.health,
            'speedmin': s._speedmin, 'damage': s.damage,
            'money': s.money}
        s._maxstats = {
            'ammo': options['maxammo'], 'bombs': options['maxbombs'],
            'lives': options['maxlives'],
            'shootspeed': options['maxshootspeed'],
            'power': options['maxpower'], 'speed': options['maxspeed'],
            'speedmax': options['maxspeedmax'], 'health': s.maxhealth,
            'speedmin': options['maxspeedmin'], 'damage': options['maxdamage']}

    def update(s, num):
        #s._game.state = s._control()
        if num == 1:
            s._update1()
        elif num == 2:
            s._update2()

    def _update1(s):
        ''' used before AI '''
        if s.dead():
            s._respawn()
        else:
            s._move()
            s._shoot()

    def _update2(s):
        ''' used after AI '''
        s.draw(s._game.screen)

    def _move(s):
        ''' convert screen to player visible bounds. '''
        bounds = s._game.screen.get_rect()
        s.move_internal(bounds)

    def pickup(s, type, value):
        s.stats[type] += value
        try:
            s.stats[type] > s._maxstats[type]
        #except KeyError:
        finally:
            s.stats[type] = s._maxstats[type]
        return
        if item.type == 'money':
            s.money += item.value
        elif item.type == 'ammo':
            s._ammo += item.value
        elif item.type == 'health':
            s.life += item.value
            if s.life > s._maxhealth:
                s._life = s._maxhealth
        elif item.type == 'bomb':
            s._bombs += item.value
        elif item.type == 'life':
            s._lives += item.value
        elif item.type == 'powerup':
            if item.effect == 'power':
                s._power += item.value
            elif item.effect == 'shootspeed':
                s._shootspead += item.value

    def _respawn(s):
        ''' dummy '''
        s._lives -= 1
        s.health = s.maxhealth
        print 'bam'

    def _shoot(s):
        ''' Append a bullet to the game. '''
        s._shootcooldown += 1
        if s._shootkey and s._shootcooldown >= s._shootspeed and s._ammo:
            new = Bullet(s._game, Bullets['bullet'],
                         (s.rect.centerx, s.rect.top),
                         s._game.images['bullet'])
            s._game.objects['bullets'][new] = 0
            s._ammo -= 1
            s._shootcooldown = 0
        if s._bombkey and s._bombs:
            new = Bullet(s._game, Bullets['rocket'],
                         (s.rect.centerx, s.rect.top),
                         s._game.images['rocket'])
            s._game.objects['bullets'][new] = 0
            s._bombs -= 1
            s._bombkey = False # It stops and bombs aren't wasted.

    def _control(s):
        ''' Controls the Player(object) with pygame.event '''
        if s._lives == 0:
            return 'gameover'

        for event in pygame.event.get():
            if event.type == QUIT:
                return 'killed'

            if event.type == KEYUP:
                if event.key in Game['Keys']['quit']:
                    return 'quit'

                elif event.key in Game['Keys']['pause']:
                    return 'paused'

                for dir_ in s._moves:
                    if event.key in Game['Keys'][dir_]: s._moves[dir_] = False
                if event.key in Game['Keys']['shoot']:  s._shootkey = False
                if event.key in Game['Keys']['bomb']:   s._bombkey = False

            if event.type == KEYDOWN:
                for dir_ in s._moves:
                    if event.key in Game['Keys'][dir_]: s._moves[dir_] = True
                if event.key in Game['Keys']['shoot']:  s._shootkey = True
                if event.key in Game['Keys']['bomb']:   s._bombkey = True
        return 'continue'



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



"""
class Group(object):

    def __init__(s):
        s.objects = {}

    def add(s, object):
        s.objects[object] = 0
        object.groups[s] = 0

    def remove(s, object):
        s.remove_int(object)
        object.remove_int(s)

    def remove_int(s, object):
        s.objects.pop(object)

    def update(s):
        dels = {}
        for i in s.objects:
            if not i.update()
                dels[i] = 0
        for i in dels:
            s.remove(i)
"""
