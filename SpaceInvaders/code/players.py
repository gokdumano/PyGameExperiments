# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 20:26:33 2021

@author: Punisher_12
https://material.io/resources/color/#!/?view.left=0&view.right=0&primary.color=9FA8DA

"""

from random import choices
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, enemy_x, enemy_y):
        super().__init__()
        if   enemy_type == 'green' : self.image  = pygame.image.load('../graphics/green.png' ).convert_alpha(); self.hitrate = 0.05;
        elif enemy_type == 'yellow': self.image  = pygame.image.load('../graphics/yellow.png').convert_alpha(); self.hitrate = 0.10;
        elif enemy_type == 'red'   : self.image  = pygame.image.load('../graphics/red.png'   ).convert_alpha(); self.hitrate = 0.15;
        self.rect   = self.image.get_rect(topleft=(enemy_x, enemy_y))
        
        self.Ready4Action   = pygame.time.get_ticks()
        self.CoolDownIntv   = 300
        self.dx, self.dy    = 25, 50
    
    def move(self, display_rect):
        now = pygame.time.get_ticks()
        if self.Ready4Action < now:
            if  self.rect.right + self.dx > display_rect.right or self.rect.left + self.dx < display_rect.left: 
                self.rect.move_ip(0, self.dy)
                self.dx *= -1;
            else: 
                self.rect.move_ip(self.dx, 0)
    
    def shoot(self, lasers):
        now = pygame.time.get_ticks()
        if self.Ready4Action < now:
            action,   = choices(["shoot", "pass"], [self.hitrate, 1 - self.hitrate])
            if action == "shoot":
                laser = Laser(4, 5, midtop = self.rect.midbottom)
                lasers.add(laser)
            self.Ready4Action   = now + self.CoolDownIntv
            
    
    def update(self, display_rect, lasers):
        self.move(display_rect)
        self.shoot(lasers)
        
        
class Player(pygame.sprite.Sprite):
    def __init__(self, player_speed, laser_speed, laser_width, cooldown, **pos):
        super().__init__()
        self.image  = pygame.image.load('../graphics/player.png').convert_alpha()
        self.rect   = self.image.get_rect(**pos)
        
        self.dx, self.dy    = player_speed, 0
        
        self.laser_sound    = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.4)
        self.laser_speed    = laser_speed
        self.laser_width    = laser_width
        
        self.Ready2ShootAt  = pygame.time.get_ticks()
        self.CoolDownIntv   = cooldown
        
    def move(self, keys, display_rect):        
        if keys[pygame.K_d] and self.rect.right + self.dx < display_rect.right: self.rect.move_ip( self.dx, self.dy)
        if keys[pygame.K_a] and self.rect.left  - self.dx > display_rect.left : self.rect.move_ip(-self.dx, self.dy)
        
    def shoot(self, keys, lasers):
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and self.Ready2ShootAt < now: 
            self.Ready2ShootAt = now + self.CoolDownIntv
            laser = Laser(self.laser_width, self.laser_speed, midbottom = self.rect.midtop)
            lasers.add(laser)
            self.laser_sound.play()
        
    def update(self, display_rect, lasers):
        keys    = pygame.key.get_pressed()
        self.move(keys, display_rect)
        self.shoot(keys, lasers)
        
class Laser(pygame.sprite.Sprite):
    def __init__(self, laser_width, laser_speed, **pos):
        super().__init__()
        self.image          = pygame.Surface((laser_width, 20)); self.image.fill('White');
        self.rect           = self.image.get_rect(**pos)
        
        self.dx, self.dy    = 0, laser_speed
        
    def update(self, display_rect, lasers):
        self.move(display_rect, lasers)
        
    def move(self, display_rect, lasers):
        self.rect.move_ip(self.dx, self.dy)
        if self.rect.bottom < display_rect.top: lasers.remove(self)
    
    def check_collision(self, mobs):
        pass

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size)); self.image.fill(color);
        self.rect  = self.image.get_rect(topleft = (x,y))
        
Obstacle_Shape = [
    '     x     ',
    '    xxx    ',
    '   xxxxx   ',
    '  xxxxxxx  ',
    ' xxxxxxxxx ',
    'xxx     xxx',
    'xx       xx']