import pygame
from options import Options as Game
from options import Enemies
from options import Bullets
import Sprites
from pygame.locals import QUIT, KEYDOWN, KEYUP

class Basic(object):
    ''' Basic non moving object. '''
    def __init__(self, options, position, group, colliders=[]):
        ''' position is the middle of the object '''
        #self.team  = options['team'] # for collisions
        self.sprite = Sprites.getsprite( options['sprite'],
                                         options['colours'],
                                         Game['bgcolour'])
        self.rect = pygame.Rect( (0,0), self.sprite.get_size() )
        self.rect.center = position # Much easier :3
        self.life = options['life'] # <=0 == dead, None == invincible
        self.damage = options['damage'] # collision damage done to other, None == almighty
        self.colliders = colliders
        self.group = group
    def update(self, bounds, objects, surface):
        ''' Every update contains bounds, objects and surface for easier useability. '''
        if self.dead(bounds):
            return False
        else:
            self.collide_ip(objects, bounds)
            self.draw(surface)
            return True

    def draw(self, surface):
        surface.blit(self.sprite, self.rect.topleft)
    def dead(self, bounds):
        if not self.life == None:
            if self.life <= 0 or not bounds.contains(self.rect):
                return True
        return False

    def collide_ip(self, objects, bounds):
        ''' Collide self.rect with all objects in self.colliders lists. '''
        for i in range(len(self.colliders)):
            for object in objects[self.colliders[i]]:
                if not self == object: # it could happen
                    if self.rect.colliderect(object.rect):
                        if not object.dead(bounds):
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
        if self.rect.colliderect(object.rect):
            return True
        return False

    def shoot(self, objects):
        ''' Space for the shooting stuff. '''
        pass


class Moving(Basic):
    ''' Basic moving object. '''
    def __init__(self, options, position, initdirection, group, colliders=[]):
        Basic.__init__(self, options, position, group, colliders)
        self.moves = {}
        for _dir in Game['Directions']:
            self.moves[_dir] = None
        if not initdirection == None:
            self.moves[initdirection] = True
        self.speed = options['speed']
    def update(self, bounds, objects, screen):
        if not self.dead(bounds):
            self.collide_ip(objects, bounds)
            self.move(bounds)
            self.draw(screen)
            return True
        return False

    def move(self, bounds):
        ''' Move the item by self.speed in self.moves['direction'].
            AI controlled objects have extended bounds,
            where Player has only on-screen visible bounds. (With it's own method.)'''
        self._move(bounds)
    def control(self, objects):
        ''' Space for the AI or the player controls. '''
        pass

    def _move(self, bounds):
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
    def __init__(self, options, position, group='player', colliders=[]):
        Moving.__init__(self, options, position, False, group, colliders)
        self.power = options['power']
        self.shootspeed = options['shootspeed']
        self.shootcooldown = 0
        self.shootkey = False
        self.shootcount = options['shootspeed']
        self.bombkey = False
        self.bombs = options['bombs']
        self.lives = 2
    def update1(self, bounds, objects, screen):
        ''' used before AI '''
        if self.dead(bounds):
            self.respawn()
        else:
            self.move(screen)
            self.shoot(objects)
    def update2(self, bounds, objects, screen):
        ''' used after AI '''
        self.draw(screen)

    def respawn(self):
        ''' dummy '''
        self.lives -= 1
        self.life = 10
        print 'respawn'

    def move(self, screen):
        ''' convert screen to player visible bounds. '''
        bounds = screen.get_rect()
        self._move(bounds)
        
    def shoot(self, objects):
        self.shootcooldown += 1
        if self.shootkey and self.shootcooldown >= self.shootspeed:
            objects['bullets'].append(Moving(Bullets['normal'],
                                             (self.rect.centerx, self.rect.top),
                                             'up', 'bullets', ['static', 'enemies']))
            self.shootcooldown = 0
        if self.bombkey and self.bombs > 0:
            objects['bullets'].append(Moving(Bullets['rocket'],
                                             (self.rect.centerx, self.rect.top),
                                             'up', 'bullets', ['static', 'enemies']))
            self.bombs -= 1
            self.bombkey = False # It stops and bombs aren't wasted.

    def control(self, objects):
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
    def __init__(self, options, position, group, initdirection=None, colliders=[]):
        Moving.__init__(self, options, position, initdirection, group, colliders)
        self.behaviour = options['behaviour']
    def update(self, bounds, objects, screen):
        if not self.dead(bounds):
            self.collide_ip(objects, bounds)
            self.control(objects)
            self.move(bounds)
            self.shoot(objects)
            self.draw(screen)
            return True
        return False

    def control(self, objects):
        newdirections = self.think(objects)
        for i in self.moves:
            self.moves[i] = False
        for i in range(len(newdirections)):
            self.moves[newdirections[i]] = True

    def think(self, objects):
        directions = []
        if 'dumbdown' in self.behaviour:
            directions.append('down')
        if 'followx' in self.behaviour:
            if not self.rect.top > objects['player'][0].rect.bottom:
                if self.rect.left > objects['player'][0].rect.centerx:
                    directions.append('left')
                elif self.rect.right < objects['player'][0].rect.centerx:
                    directions.append('right')
        return directions
