#!/usr/bin/python2
import pygame, pygame.locals
import random, sys
import options, objects

class Game:
    def __init__(self):
        pygame.init()
        self.enemymodels = []
        for i in options.Enemies:
            self.enemymodels.append(i)
        self.enemydelay = options.Options['Game']['enemydelay']
        self.powerupdelay = options.Options['Game']['powerupdelay']
        self.newenemycount = 0
        self.powerupcount = 0
        self.screensize = options.Options['Game']['screensize']
        self.screen  = pygame.display.set_mode(self.screensize, 32, 0)
        boffset = options.Options['Game']['boundsoffset']
        self.bounds  = pygame.Rect(-boffset['left'], -boffset['top'],
                                   boffset['left'] +self.screensize[0]+ boffset['right'],
                                   boffset['top'] +self.screensize[1]+ boffset['bottom'])
        self.clock   = pygame.time.Clock()
        self.FPS     = options.Options['Game']['FPS']
        self.running = True
        # visuals:
        self.objects = {
            'player': [objects.Player(options.Player, options.Player['startposition'])],
            'enemies':[],
            'bullets':[],
            'stuff':  [], # things without collision
            'static': [],
            'power':  []  # powerups
            }
        self.objqueue = ['stuff', 'static', 'bullets', 'enemies', 'power']

    def terminate(self):
        pygame.quit()
        sys.exit()
    def quit(self):
        #ask if really quit, credits or whatevs
        self.terminate()
    def gameover(self):
        
        while True:
            
            self.terminate()

    def pause(self):
        #self.paused = True
        while True:#self.paused:
            for _e in pygame.event.get():
                if _e.type in options.Options['Keys']['pause']:
                    #self.paused = False
                    break
            self.clock.tick(self.FPS)

    def changemode(self, nextmode):
        if nextmode == 'killed':
            self.terminate()
        elif nextmode == 'quit':
            self.quit()
        elif nextmode == 'gameover':
            self.gameover()
        elif nextmode == 'paused':
            self.pause()
    
    def start(self):
        self.objects['static'].append(objects.Basic(
                                        options.Stuff['sun'], (70, 60), 'static',
                                                    ['bullets', 'enemies']))
        while self.running:
            self.cycle()

    def updateobjects(self, list):
        ''' get a reversed range object of len of list '''
        nums = range(len(list))
        nums.reverse()
        for i in nums:
            if not list[i].update(self.bounds, self.objects, self.screen):
                list.pop(i)

    def cycle(self):
        mode = self.objects['player'][0].control(self.objects)
        if not mode == 'continue': self.changemode(mode)

        self.newenemycount += 1
        self.powerupcount += 1

        if self.newenemycount >= self.enemydelay:
            model = self.enemymodels[random.randint(0, (len(self.enemymodels) -1))]
            self.objects['enemies'].append(objects.Thinking(
                                        options.Enemies[model],
                                        (random.randint(0, self.screensize[1]), -16),
                                        None, 'enemies',
                                        ['bullets', 'player', 'enemies', 'static']))
            self.newenemycount = 0
        if self.powerupcount >= self.powerupdelay:
            self.powerupcount = 0

        self.screen.fill( options.Options['Game']['bgcolour'] )

        self.objects['player'][0].update1(self.bounds, self.objects, self.screen)

        for i in range(len(self.objqueue)):
            self.updateobjects(self.objects[self.objqueue[i]])

        if not self.objects['player'][0].update2(self.bounds, self.objects, self.screen):
            self.gameover()

        pygame.display.update()
        self.clock.tick(self.FPS)

if __name__ == '__main__':
    Main = Game()
    Main.start()
