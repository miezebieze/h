#!/usr/bin/python2
import random
import sys

import pygame
from pygame.locals import SRCALPHA, KEYUP

from lib import Image
#from lib import asciisprites

import objects


class Game:

    def __init__(s, options, state = 'start'):
        pygame.init()
        s.OPTIONS = options
        s.enemydelay = 1.0 * s.OPTIONS.GAME['fps'] / s.OPTIONS.GAME['enemy_p_sec'] 
        s.screensize = s.OPTIONS.GAME['screensize']
        s.screen = pygame.display.set_mode(s.screensize, SRCALPHA, 32)
        # Setup some bounds, where the objects can live in:
        _boffset = s.OPTIONS.GAME['main_bounds_offset']
        _bsize = [_boffset[0] + s.screensize[0] + _boffset[1],
                  _boffset[2] + s.screensize[1] + _boffset[3]]
        s.bounds = pygame.Rect(_boffset[0] * -1 , _boffset[2] * -1,
                               _bsize[0], _bsize[1])
        # Stuff:
        s._clock = pygame.time.Clock()
        s.fps = s.OPTIONS.GAME['fps']
        s.mspf = 1000 / s.fps
        s.frame = 0
        s._on = True
        s.state = state
        s.subject = None
        # Visuals:
        s.objects = {}
        for group in s.OPTIONS.GROUPS:
            s.objects[group] = []
        # update order of object groups:
        s.queue = s.OPTIONS.QUEUE

    def setup(s):
        s._newenemycount = 0
        # Parse images: Could be a wrapper, that makes an Image, when
        # first asked for and otherwise just returns the Image.
        # But this will only be necessary, when there are very many.
        s.images = {}
        for i in s.OPTIONS.OBJECTS:
            s.images[i] = Image(s.OPTIONS.OBJECTS[i]['prototype']['sprite'],
                                s.OPTIONS.OBJECTS[i]['prototype']['colours'])
        # setup Player:
        s.subject = objects.Player(s, s.OPTIONS.OBJECTS['player'],
                                   s.OPTIONS.OBJECTS['player']['start_position'],
                                   s.images['player'])
        s.objects['player'].append(s.subject)

        # Make a random background: TODO: Multiple layers, that move.
        objects_ = []
        objects_.append(objects.Basic(s, s.OPTIONS.OBJECTS['planet'], (70, 60),
                               s.images['planet'], 'static_stuff'))
        stars = ['stars', 'stars', 'stars', 'stars', 'stars', 'stars',
                 'starm', 'starm', 'starm', 'starl']
        for i in range(s.OPTIONS.GAME['start_stars']):
            star = random.choice(stars)
            position = (random.randint(2, s.screensize[0] -2),
                        random.randint(2, s.screensize[1] -2))
            objects_.append(objects.Basic(s, s.OPTIONS.OBJECTS[star],
                                   position, s.images[star], 'static_stuff'))

        s.screen.fill(s.OPTIONS.GAME['bg_colour'])
        s._update_objects(objects_)
        s.background = s.screen.copy()

        # Fill in some enemies:
        colliders = ['bullets', 'player', 'enemies', 'static']
        for i in range(s.OPTIONS.GAME['start_enemies']):
            position = (random.randint(4, s.screensize[0] + 4),
                        random.randint(-4, s.screensize[1] - 50))
            s.objects['enemies'].append(objects.Thinking(
                                    s, s.OPTIONS.OBJECTS[s.OPTIONS.GAME['default_enemy']],
                                    position, s.images[s.OPTIONS.GAME['default_enemy']],
                                    'enemies', None, colliders))
        #print (objects.Thinking.instances

    def run(s):
        s.frame = 0
        while s._on:
            s.frame += 1
            if s.state == 'start':
                s.setup()

            s.state = s.subject._control()
            if s.state == 'continue':
                s.cycle()
            elif s.state == 'paused':
                s.pause()
            elif s.state == 'gameover':
                s.gameover()
            elif s.state == 'quit':
                s.quit()
            elif s.state == 'killed':
                s._on = False
            pygame.display.update()
            #pygame.time.delay(s.mspf)
            s._clock.tick(s.fps)
            if s.frame == s.fps: s.frame = 0

        s.terminate()

    def cycle(s):
        s.spawn()

        s.screen.blit(s.background, (0, 0))
        s.subject.update(1)

        for i in range(len(s.queue)):
            s._update_objects(s.objects[s.queue[i]])

        if s.frame == 1:
            count = 0
            for i in s.objects:
                count += len(s.objects[i])
            #print 'objects:', count
        s.subject.update(2)
        s._update_objects(s.objects['tmp'])

    def pause(s):
        while s.state == 'paused':
            for event in pygame.event.get():
                if (event.type == KEYUP and
                event.key in s.OPTIONS.KEYS['pause']):
                    s.state = 'continue'
            #s.time.delay(s.mspf)
            s._clock.tick(s.fps)
        # show 'paused'

    def gameover(s):
        s._on = False
        # show 'game' + 'over'

    def quit(s):
        #ask if really quit, credits or whatevs
        s._on = False

    def terminate(s):
        pygame.quit()
        sys.exit()

    def spawn(s):
        ''' Test, if it's time and put new stuff to the game. '''
        s._newenemycount += 1

        if s._newenemycount >= s.enemydelay:
            val = random.randint(0, 100)
            colgroups = ['bullets', 'player', 'enemies', 'static']
            if val < s.OPTIONS.GAME['prob']['red']:
                model = 'red'
            elif val > (100 - s.OPTIONS.GAME['prob']['green']):
                model = 'green'
            else:
                #colgroups = ['bullets', 'player', 'static']
                model = s.OPTIONS.GAME['default_enemy']
            #model = s.enemymodels[random.randint(0, (len(s.enemymodels) -1))]

            coords = (random.randint(4, s.screensize[0] - 4),
                      s.OPTIONS.GAME['main_bounds_offset'][3] / 2)
            newenemy = objects.Thinking(s, s.OPTIONS.OBJECTS[model], coords,
                                         s.images[model], 'enemies',
                                        None, colgroups)

            s.objects['enemies'].append(newenemy)
            s._newenemycount = 0
        
    def _update_objects(s, list_):
        dels = []
        for i in list_:
            if not i.update():
                dels.append(i)
        for i in dels:
            list_.pop(list_.index(i))

    def _update_objects_alt(s, list_):
        # depreceated. I don't know anymore, why I needed it this complex.
        for i in range(len(list_)):
            if not list_[i].update():
                dels.append(list_[i])
        for i in range(len(dels)):
            list_.pop(list_.index(dels[i]))
