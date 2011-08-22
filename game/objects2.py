import pygame
from options import Enemies, Bullets, Options as Game
import Sprites
from pygame.locals import QUIT, KEYDOWN, KEYUP

class Basic(pygame.sprite.Sprite):
    def __init__(self, game, options, position, *groups, colliders=[]):
        pygame.sprite.Sprite.__init__(self, *groups):
        self.game   = game
        self.image  = Sprites.getsprite( options['sprite'], options['colours'],
                                         Game['Game']['bgcolour'] )
        self.rect   = pygame.Rect( (0,0), self.sprite.get.size() )
        self.rect.center = position # Much easier than calculating all that stuff out! :3
        self.life   = options['life'] # <=0: dead, None: invincible
        self.damage = options['damage'] # collision damage done to other, None:instadeath
        self.colliders = colliders
