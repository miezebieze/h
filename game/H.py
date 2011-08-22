#!/usr/bin/python2
import random
import sys

import pygame
from pygame.locals import SRCALPHA, KEYUP

from local import asciisprites

import objects
import options


class Game:

    def __init__(s, state):
        pygame.init()
        s.OPTIONS = options
        s.enemydelay = s.OPTIONS.Options['Game']['enemydelay']
        #s.powerupdelay = s.OPTIONS.Options['Game']['powerupdelay']
        s._newenemycount = 0
        #s._powerupcount = 0
        s.screensize = s.OPTIONS.Options['Game']['screensize']
        s.screen = pygame.display.set_mode(s.screensize, SRCALPHA, 32)
        # Setup some bounds, where the objects can live in:
        _boffset = s.OPTIONS.Options['Game']['boundsoffset']
        _bsize = [_boffset['left'] + s.screensize[0] + _boffset['right'],
                  _boffset['top'] + s.screensize[1] + _boffset['bottom']]
        s.bounds = pygame.Rect(_boffset['left'] * -1 , _boffset['top'] * -1,
                               _bsize[0], _bsize[1])

        # Stuff:
        s._clock = pygame.time.Clock()
        s.fps = s.OPTIONS.Options['Game']['FPS']
        s.frame = 0
        s._on = True
        s.state = state
        s.subject = None
        # Visuals:
        s.objects = {
            'player':   {},
            'enemies':  {},
            'bullets':  {},
            'stuff':    {}, # things without collision
            'static':   {},
            'power':    {}, # powerups
            'tmp':      {}  # 'game over', 'paused' and such sprites
            }
        # update order of object groups:
        s.queue = ['stuff', 'static', 'bullets', 'enemies', 'power']

    def setup(s):
        # parse images
        s.images = {}
        for i in s.OPTIONS.Images:
            s.images[i] = asciisprites.Image(s.OPTIONS.Images[i]['sprite'],
                                             s.OPTIONS.Images[i]['colours'])
        s.subject = objects.Player(s, s.OPTIONS.Player,
                                   s.OPTIONS.Player['startposition'],
                                   s.images['player'])
        s.objects['player'][s.subject] = 0
        # TODO: blit 'stuff' on the game.surface at beginning forever
        sun = objects.Basic(s, s.OPTIONS.Stuff['sun'], (70, 60),
                            s.images['sun'], 'stuff')
        s.objects[sun.group][sun] = 0
        for i in range(s.OPTIONS.Options['Game']['startstars']):
            s.objects['stuff'][objects.Basic(s, s.OPTIONS.Stuff['stars'],
                                (random.randint(10, s.screensize[0] -10),
                                 random.randint(10, s.screensize[1] -10)),
                                 s.images['stars'], 'stuff')] = 0
        for i in range(s.OPTIONS.Options['Game']['startenemies']):
            s.objects['enemies'][objects.Thinking(s, s.OPTIONS.Enemies['blue'],
                                    (random.randint(0, s.screensize[0]),
                                     random.randint(-10, s.screensize[1] - 50)),
                                     s.images['blue'], 'enemies', None, 
                            ['bullets', 'player', 'enemies', 'static'])] = 0

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
            s._clock.tick(s.fps)
            if s.frame == s.fps: s.frame = 0

        s.terminate()

    def cycle(s):
        s.spawn()
        s.screen.fill(s.OPTIONS.Options['Game']['bgcolour'])

        s.subject.update(1)

        for i in range(len(s.queue)):
            s._update_objects(s.objects[s.queue[i]])

        s.subject.update(2)
        s._update_objects(s.objects['tmp'])

    def pause(s):
        while s.state == 'paused':
            for event in pygame.event.get():
                if (event.type == KEYUP and
                event.key in s.OPTIONS.Options['Keys']['pause']):
                    s.state = 'continue'
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
            if random.randint(0, 10) < 4:
                model = 'red'
            else:
                model = 'blue'
            #model = s.enemymodels[random.randint(0, (len(s.enemymodels) -1))]
            colgroups = ['bullets', 'player', 'enemies', 'static']
            coords = (random.randint(0, s.screensize[0]), -16)
            newenemy = objects.Thinking(s, s.OPTIONS.Enemies[model], coords,
                                         s.images[model], 'enemies',
                                        None, colgroups)

            s.objects['enemies'][newenemy] = 0
            s._newenemycount = 0
        
    def _update_objects(s, list):
        dels = {}
        for i in list:
            if not i.update():
                dels[i] = 0
        for i in dels:
            list.pop(i)


if __name__ == '__main__':
    Main = Game('start')
    Main.run()
