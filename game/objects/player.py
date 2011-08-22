import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP

from local import asciisprites

from basic import Basic
from stuff import Bullet

from options import Options as Game


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
            new = Bullet(s._game, s._game.OPTIONS.Bullets['bullet'],
                         (s.rect.centerx, s.rect.top),
                         s._game.images['bullet'])
            s._game.objects['bullets'][new] = 0
            s._ammo -= 1
            s._shootcooldown = 0
        if s._bombkey and s._bombs:
            new = Bullet(s._game, s._game.OPTIONS.Bullets['rocket'],
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
