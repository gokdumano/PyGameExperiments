# https://www.101computing.net/pygame-how-tos/
# https://www.101computing.net/flowchart/
# https://www.101computing.net/breakout-tutorial-using-pygame-adding-the-paddle/
# http://programarcadegames.com/index.php
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
# https://fiftyexamples.readthedocs.io
# https://github.com/kennycason/art
# https://kennycason.com/posts/2018-10-01-quad-tree-images.html
# https://www.cs.cmu.edu/afs/cs/academic/class/15850c-s96/www/nbody.html#p3m
# https://en.wikipedia.org/wiki/Barnes–Hut_simulation
# https://www.ifa.hawaii.edu/~barnes/treecode/treeguide.html
# https://fas.org/sgp/othergov/doe/lanl/pubs/00326635.pdf
# https://arhiv.djs.si/proc/nene2011/pdf/311.pdf
# https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/#determining-margin-and-padding-sizes
# https://opengameart.org/content/planets-and-stars-set-high-res
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
# https://nssdc.gsfc.nasa.gov/planetary/planetfact.html
# http://www.scholarpedia.org/article/N-body_simulations#Tree_codes
# http://www.scholarpedia.org/article/Computational_celestial_mechanics
# https://arhiv.djs.si/proc/nene2011/pdf/311.pdf
# MANY-BODY TREE METHODS IN PHYSICS - SUSANNE PFALZNER
# The gravitational constant: G
# Assumed scale: 100 pixels = 1 AU

import numpy as np
import pygame
pygame.init()

SIZE       = (WIDTH, HEIGHT) = (512, 512)
SCREENSURF = pygame.display.set_mode(SIZE)
SCREENRECT = SCREENSURF.get_rect()

CLOCK      = pygame.time.Clock()
STOP       = False

class Body(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.image = pygame.Surface([5,5])
        self.image.fill(0xff5d00)
        self.rect  = self.image.get_rect(center=center)
        
        self.Vx, self.Vy = np.random.randint(-1,1,2)
        
    def update(self, others):
        if self.rect.left + self.Vx < SCREENRECT.left or self.rect.right  + self.Vx > SCREENRECT.right : self.Vx *= -1
        if self.rect.top  + self.Vy < SCREENRECT.top  or self.rect.bottom + self.Vy > SCREENRECT.bottom: self.Vy *= -1
        self.rect.move_ip(self.Vx, self.Vy)
        
class Border(pygame.sprite.Sprite):
    def __init__(self, size, **pos_abs):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(0xffffff)
        self.image.set_colorkey(0xffffff)
        self.rect  = self.image.get_rect(**pos_abs)
        
        topleft       = self.image.get_rect().topleft
        self.rect_abs = pygame.Rect(topleft, size)
        
        self.type     = 'undefined'
        self.childs   = pygame.sprite.Group()
        
    def isInside(self, sprite1, sprite2):
        return pygame.Rect.collidepoint(sprite1.rect, sprite2.rect.center)
    
    def update(self, bodies, borders):
        pygame.draw.rect(self.image, 0x000000, self.rect_abs, width=1)
        if self.type == 'undefined':
            self.bodies = pygame.sprite.spritecollide(self, bodies, False, collided=self.isInside)
            if len(self.bodies) > 1:
                self.type = 'twig'
                self.image.fill(0x9a7943)
                childs    = Quadrants(self)
                self.childs.add(childs)
            elif len(self.bodies) == 1:
                self.type = 'leaf'
                self.image.fill(0xccffcc)
            else:
                borders.remove(self)
                
        self.childs.draw(SCREENSURF)
        self.childs.update(bodies, borders)
                
        
def Quadrants(border00):
    rect = border00.rect
    w, h = rect.size
    size = w/2, h/2
    
    border01 = Border(size, topleft=rect.topleft)
    border02 = Border(size, topleft=rect.midtop )
    border03 = Border(size, topleft=rect.midleft)
    border04 = Border(size, topleft=rect.center )
    return border01, border02, border03, border04

def Sample(num, dim1_max=WIDTH, dim2_max=HEIGHT, r=20):
    def inRange(sprite1, sprite2):
        dx   = sprite2.rect.x-sprite1.rect.x
        dy   = sprite2.rect.y-sprite1.rect.y
        dist = np.hypot(dx, dy)
        if dist < r: return True
        else       : return False
        
    bodies  = pygame.sprite.Group()
    while len(bodies) < num:
        center  = np.random.randint(0, dim1_max, 2)
        body    = Body(center)
        if pygame.sprite.spritecollideany(body, bodies, collided=inRange) is None:
            bodies.add(body)
    return bodies
        
        
        
