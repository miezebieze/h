#!/usr/bin/python2
import pygame
from pygame.locals import SRCALPHA
import random, sys
import options, objects

class Game:
    def __init__(self, state):
        pygame.init()
        self.enemymodels = []
        for i in options.Enemies:
            self.enemymodels.append(i)
        self.options = options
        self.enemydelay = options.Options['Game']['enemydelay']
        self.powerupdelay = options.Options['Game']['powerupdelay']
        self.newenemycount = 0
        self.powerupcount = 0
        self.screensize = options.Options['Game']['screensize']
        self.screen = pygame.display.set_mode(self.screensize, SRCALPHA, 32)
        boffset = options.Options['Game']['boundsoffset']
        self.bounds = pygame.Rect(-boffset['left'], -boffset['top'],
                                   boffset['left'] +self.screensize[0]+ boffset['right'],
                                   boffset['top'] +self.screensize[1]+ boffset['bottom'])
        self.clock  = pygame.time.Clock()
        self.fps    = options.Options['Game']['FPS']
        self.frame  = 0
        self.on     = None
        self.state  = state
        self.subject = None
        # visuals:
        self.objects = {
            'player':   {},
            'enemies':  {},
            'bullets':  {},
            'stuff':    {}, # things without collision
            'static':   {},
            'power':    {}, # powerups
            'tmp':      {}  # 'game over', 'paused' and such sprites
            }
        self.queue = ['stuff', 'static', 'bullets', 'enemies', 'power'] # for objects

    def setup(self):
        self.subject = objects.Player(self, options.Player,
                                            options.Player['startposition'])
        self.objects['player'][self.subject] = 0
        sun = objects.Basic(self, options.Stuff['sun'], (70, 60), 'stuff')
        self.objects[sun.group][sun] = 0

    def run(self):
        self.on = True
        self.frame = 0
        while self.on:
            self.frame += 1
            if self.state == 'start':
                self.setup()
            self.state = self.subject.control()
            if self.state == 'continue':
                self.cycle()
            elif self.state == 'paused':
                self.pause()
            elif self.state == 'gameover':
                self.gameover()
            elif self.state == 'quit':
                self.quit()
            elif self.state == 'killed':
                self.on = False

            pygame.display.update()
            self.clock.tick(self.fps)
            if self.frame == self.fps: self.frame = 0

        self.terminate()

    def cycle(self):
        self.spawnstuff()
        self.screen.fill( options.Options['Game']['bgcolour'] )

        self.subject.update1()

        for i in range(len(self.queue)):
            self.updateobjects(self.objects[self.queue[i]])

        self.subject.update2()
        self.updateobjects(self.objects['tmp'])

    def pause(self):
        for _e in pygame.event.get():
            if _e.type in options.Options['Keys']['pause']:
                self.state = 'continue'
        # show 'paused'
    def gameover(self):
        self.on = False
        # show 'game' 'over'
    def quit(self):
        #ask if really quit, credits or whatevs
        self.on = False
    def terminate(self):
        pygame.quit()
        sys.exit()

    def spawnstuff(self):
        self.newenemycount += 1
        self.powerupcount += 1

        if self.newenemycount >= self.enemydelay:
            model = self.enemymodels[random.randint(0, (len(self.enemymodels) -1))]
            self.objects['enemies'][objects.Thinking( self, options.Enemies[model],
                                        (random.randint(0, self.screensize[1]), -16),
                                        'enemies', None,
                                        ['bullets', 'player', 'enemies', 'static'])
                                        ] = 0
            self.newenemycount = 0
        if self.powerupcount >= self.powerupdelay:
            self.powerupcount = 0
        
    def updateobjects(self, list):
        dels = {}
        for i in list:
            if not i.update():
                dels[i] = 0
        for i in dels:
            list.pop(i)

if __name__ == '__main__':
    Main = Game('start')
    Main.run()
