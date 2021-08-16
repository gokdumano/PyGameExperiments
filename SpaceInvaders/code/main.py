# -*- coding: utf-8 -*-

from players import Player, Enemy
import pygame, sys

"""
Created on Sat Aug  7 19:15:05 2021

@author: gokdumano

https://towardsdatascience.com/building-simulations-in-python-a-complete-walkthrough-3965b2d3ede0
https://towardsdatascience.com/simulation-structures-and-modelling-in-simpy-6503833b79f6
https://medium.com/@plaha.roshan/creating-a-simple-train-simulator-with-pygame-182204df7f04
https://github.com/RoshyPlaha/python_train_simulator
https://www.youtube.com/watch?v=o-6pADy5Mdg
https://kidscancode.org/blog/tags/pygame/

"""
class Game:
    def __init__(self, display_width, display_height, framerate, bgcolor):
        pygame.init()
        
        display_size        = (display_width, display_height)
        self.display_surf   = pygame.display.set_mode(display_size)
        self.display_rect   = self.display_surf.get_rect()
        
        self.tv_surf        = pygame.image.load('../graphics/tv.png').convert_alpha()
        self.tv_rect        = self.tv_surf.get_rect(topleft=self.display_rect.topleft)
        
        self.music          = pygame.mixer.Sound('../audio/music.wav')
        self.music.set_volume(0.1)
        self.music.play(-1)
        
        self.hit_sound      = pygame.mixer.Sound('../audio/explosion.wav')
        self.hit_sound.set_volume(0.5)
                
        self.framerate      = framerate
        self.clock          = pygame.time.Clock()
        
        self.bgcolor        = bgcolor
        
        player              = Player(5, -5, 4, 750, midbottom=self.display_rect.midbottom)
        self.player         = pygame.sprite.GroupSingle(player)
        
        font_path           = '../font/Pixeled.ttf'
        font                = pygame.font.Font(font_path, 30)
        self.text_surf      = font.render("Press SPACE to start!", True, '#FFFFFF')
        self.text_rect      = self.text_surf.get_rect(center=self.display_rect.center)
        
        self.player_lasers  = pygame.sprite.Group()
        self.enemy_lasers   = pygame.sprite.Group()
        self.create_enemies()
        self.create_blocks()
        
        self.curr_screen    = self.start_screen
    
    def create_enemies(self):
        self.enemies    = pygame.sprite.Group()
        EnemyPerRow     =  self.display_rect.width // 50 - 2
        EnemyTypes      = ["red", "yellow", "green"]
        
        for RowIndx, EnemyType in enumerate(EnemyTypes):
            for ColIndx in range(EnemyPerRow):
                enemy_x = ColIndx *  50 + 50
                enemy_y = RowIndx * 100 + 50
                enemy   = Enemy(EnemyType, enemy_x, enemy_y)
                self.enemies.add(enemy)        
    
    def create_blocks(self):
        self.blocks         = pygame.sprite.Group()
        
    def check_hit(self):
        for player_laser in self.player_lasers:
            self.player_lasers.remove(player_laser)
            if pygame.sprite.spritecollide(player_laser, self.enemies, True): self.hit_sound.play()
            else : self.player_lasers.add(player_laser)
            
        pygame.sprite.spritecollide(self.player.sprite, self.enemy_lasers, True)
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def game_screen(self):
        self.display_surf.fill(self.bgcolor)
        
        self.player.draw(self.display_surf)
        self.player_lasers.draw(self.display_surf)
        
        self.enemies.draw(self.display_surf)
        self.enemy_lasers.draw(self.display_surf)
        
        self.player.update(self.display_rect, self.player_lasers)
        self.player_lasers.update(self.display_rect, self.player_lasers)
        
        self.enemies.update(self.display_rect, self.enemy_lasers)
        self.enemy_lasers.update(self.display_rect, self.enemy_lasers)
        
        #self.display_surf.blit(self.tv_surf, self.tv_rect)
        
        pygame.display.update()
        self.clock.tick(self.framerate)
        
    def start_screen(self):
        self.display_surf.fill(self.bgcolor)
        self.player.draw(self.display_surf)
        self.enemies.draw(self.display_surf)
        self.display_surf.blit(self.text_surf, self.text_rect)
        
        pygame.display.update()
        self.clock.tick(self.framerate)
        
        if pygame.key.get_pressed()[pygame.K_SPACE]: 
            self.curr_screen = self.game_screen
            self.music.set_volume(0.07)
        
    def run(self):
        while True:
            self.check_events()
            self.curr_screen()
            self.check_hit()
            
DISPLAYWIDTH    = 600
DISPLAYHEIGHT   = 720
FRAMERATE       = 120
BGCOLOR         = '#000a12'
game            = Game(DISPLAYWIDTH, DISPLAYHEIGHT, FRAMERATE, BGCOLOR)
game.run()