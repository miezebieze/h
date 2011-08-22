import pygame
from options import Options as Game
from options import Enemies
from options import Bullets
import Sprites
from pygame.locals import QUIT, KEYDOWN, KEYUP

class Basic(object):
    ''' Basic non moving object. '''
    def __init__(self, game, options, position, group={}, colliders=[]):
        ''' position is the middle of the object '''
        #self.team  = options['team'] # for collisions
        self.game = game
        self.sprite = Sprites.getsprite( options['sprite'],
                                         options['colours'],
                                         Game['Game']['bgcolour'] )
        self.rect = pygame.Rect( (0,0), self.sprite.get_size() )
        self.rect.center = position # Much easier! :3
        self.life = options['life'] # <=0 == dead, None == invincible
        self.damage = options['damage'] # collision damage done to other, None == instadeath
        self.colliders = colliders
        self.group = group

    def update(self):
        ''' Every update contains bounds, objects and surface for easier useability. '''
        if self.dead():
            return False

        self.collide_ip()
        self.draw(self.game.screen)
        return True

    def draw(self, surface):
        surface.blit(self.sprite, self.rect.topleft)
    def dead(self):
        if not self.life == None:
            if self.life <= 0 or not self.inbounds(self.game.bounds):
                return True
        return False

    def inbounds(self, bounds):
        return bounds.contains(self.rect)

    def collide_ip(self):
        ''' Collide self.rect with all objects in self.colliders lists. '''
        for i in range(len(self.colliders)):
            for object in self.game.objects[self.colliders[i]]:
                if not self == object: # it could happen
                    if self.collide(object):
                        if not object.dead():
                            if not self.life == None: # invincible
                                if object.damage == None: # almighty
                                    self.life = 0
                                else:
                                    self.life -= object.damage
                            if not object.life == None:
                                if self.damage == None:
                                    object.life = 0
                                else:
                                    object.life -= self.damage

    def collide(self, object):
        ''' Collide self.rect only with one object. '''
        return self.rect.colliderect(object.rect)

    def shoot(self):
        ''' Space for the shooting stuff. '''
        pass

class Money(Basic):
    def __init__(self, game, options, position, group='money', colliders=['player']):
        Basic.__init__(self, game, options, position, group, colliders)
        self.value = options['value']
        self.halflife = options['halflife']
        self.animation = Sprites.Animation( options['sprites'], options['fps'],
                                            options['timeline'], options['colours'])
    def update(self):
        if self.halflife:
            self.collide_ip()
            if self.game.frame % self.animation.fps:
            self.animation.update()
            self.draw(self.game.screen)
            return True
        return False

class Moving(Basic):
    ''' Basic moving object. '''
    def __init__(self, game, options, position, group, initdirection, colliders=[]):
        Basic.__init__(self, game, options, position, group, colliders)
        self.moves = {}
        for _dir in Game['Directions']:
            self.moves[_dir] = None
        if not initdirection == None:
            self.moves[initdirection] = True
        self.speed = options['speed']
    def update(self):
        if not self.dead():
            self.collide_ip()
            self.move()
            self.draw(self.game.screen)
            return True
        return False

    def move(self):
        ''' Move the item by self.speed in self.moves['direction'].
            AI controlled objects have extended bounds,
            where Player has only on-screen visible bounds. (With it's own method.)'''
        self.move_internal(self.game.bounds)
    def control(self):
        ''' Space for the AI or the player controls. '''
        pass

    def move_internal(self, bounds):
        ''' Internal used - move it!'''
        offset = [0, 0]
        if self.moves['up']:
            if self.rect.top >= bounds.top:
                if self.moves['left'] and self.moves['right']:
                    offset[1] -= (self.speed * 1.25)
                elif self.moves['left'] or self.moves['right']:
                    offset[1] -= (self.speed * 0.75)
                else:
                    offset[1] -= self.speed
        if self.moves['down']:
            if self.rect.bottom <= bounds.bottom:
                if self.moves['left'] and self.moves['right']:
                    offset[1] += (self.speed * 1.25)
                elif self.moves['left'] or self.moves['right']:
                    offset[1] += (self.speed * 0.75)
                else:
                    offset[1] += self.speed
        if self.moves['left']:
            if self.rect.left >= bounds.left:
                if self.moves['up'] and self.moves['down']:
                    offset[0] -= (self.speed * 1.25)
                elif self.moves['up'] or self.moves['down']:
                    offset[0] -= (self.speed * 0.75)
                else:
                    offset[0] -= self.speed
        if self.moves['right']:
            if self.rect.right <= bounds.right:
                if self.moves['up'] and self.moves['down']:
                    offset[0] += (self.speed * 1.25)
                elif self.moves['up'] or self.moves['down']:
                    offset[0] += (self.speed * 0.75)
                else:
                    offset[0] += self.speed
        self.rect.move_ip(offset)

class Player(Moving):
    ''' is not self.update()'d! '''
    def __init__(self, game, options, position, group='player', colliders=[]):
        Moving.__init__(self, game, options, position, group, None, colliders)
        self.power = options['power']
        self.shootspeed = options['shootspeed']
        self.shootcooldown = 0
        self.shootkey = False
        self.shootcount = options['shootspeed']
        self.bombkey = False
        self.bombs = options['bombs']
        self.lives = 2
    def update1(self):
        ''' used before AI '''
        if self.dead():
            self.respawn()
        else:
            self.move()
            self.shoot()
    def update2(self):
        ''' used after AI '''
        self.draw(self.game.screen)

    def respawn(self):
        ''' dummy '''
        self.lives -= 1
        self.life = 10
        print 'respawn'

    def move(self):
        ''' convert screen to player visible bounds. '''
        bounds = self.game.screen.get_rect()
        self.move_internal(bounds)
        
    def shoot(self):
        self.shootcooldown += 1
        if self.shootkey or self.bombkey:
            bullets = self.game.objects['bullets']
        if self.shootkey and self.shootcooldown >= self.shootspeed:
            bullets[Moving(self.game, Bullets['normal'],
                           (self.rect.centerx, self.rect.top),
                           'bullets', 'up', ['static', 'enemies'])] = 0
            self.shootcooldown = 0
        if self.bombkey and self.bombs > 0:
            bullets[Moving(self.game, Bullets['rocket'],
                           (self.rect.centerx, self.rect.top),
                           'bullets', 'up', ['static', 'enemies'])] = 0
            self.bombs -= 1
            self.bombkey = False # It stops and bombs aren't wasted.

    def control(self):
        # objects is for consistency with AI.control()
        if self.lives < 0:
            return 'gameover'
        for _e in pygame.event.get():
            if _e.type == QUIT:
                return 'killed'
            if _e.type == KEYUP:
                if _e.key in Game['Keys']['quit']:
                    return 'quit'
                elif _e.key in Game['Keys']['pause']:
                    return 'paused'

                for _dir in Game['Directions']:
                    if _e.key in Game['Keys'][_dir]: self.moves[_dir] = False
                if _e.key in Game['Keys']['shoot']:  self.shootkey    = False
                if _e.key in Game['Keys']['bomb']:   self.bombkey     = False

            if _e.type == KEYDOWN:
                for _dir in Game['Directions']:
                    if _e.key in Game['Keys'][_dir]: self.moves[_dir] = True
                if _e.key in Game['Keys']['shoot']:  self.shootkey    = True
                if _e.key in Game['Keys']['bomb']:   self.bombkey     = True

        return 'continue'

class Thinking(Moving):
    def __init__(self, game, options, position, group, initdirection=None, colliders=[]):
        Moving.__init__(self, game, options, position, group, initdirection, colliders)
        self.behaviour = options['behaviour']
        self.target = self.game.subject
    def update(self):
        if not self.dead():
            self.collide_ip()
            self.control()
            self.move()
            self.shoot()
            self.draw(self.game.screen)
            return True
        return False

    def control(self):
        newdirections = self.think()
        for i in self.moves:
            self.moves[i] = False
        for i in range(len(newdirections)):
            self.moves[newdirections[i]] = True

    def think(self):
        directions = []
        if 'dumbdown' in self.behaviour:
            directions.append('down')
        if 'followx' in self.behaviour:
            if not self.rect.top > self.target.rect.bottom:
                if self.rect.left > self.target.rect.centerx:
                    directions.append('left')
                elif self.rect.right < self.target.rect.centerx:
                    directions.append('right')
        return directions
"""
class Group(object):
    def __init__(self):
        self.objects = {}

    def add(self, object):
        self.objects[object] = 0
        object.groups[self] = 0

    def remove(self, object):
        self.remove_int(object)
        object.remove_int(self)

    def remove_int(self, object):
        self.objects.pop(object)

    def update(self):
        dels = {}
        for i in self.objects:
            if not i.update()
                dels[i] = 0
        for i in dels:
            self.remove(i)
"""
