# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 00:37:41 2021

@author: gokdumano

https://rkhive.com/guitar.html
https://material.io/resources/color/#!/

http://bspaans.github.io/python-mingus/index.html
https://github.com/FelixGSE/pypiano
"""
# http://freepats.zenvoid.org
from mingus.containers.note import Note
from mingus.midi import fluidsynth
import pygame, sys

#fluidsynth.init('soundfonts/FreePatsGM-SF2-20210329/FreePatsGM-20210329.sf2')
#fluidsynth.init('soundfonts/schinchr/Schinchr.sf2')
#fluidsynth.init('soundfonts/neoorgan/Neoorgan.sf2')
#fluidsynth.init('soundfonts/multigit/Multigit.sf2')
fluidsynth.init('soundfonts/aggorg/Aggorg.sf2')

pygame.init()

OCTAVE, CHANNEL = 4, 1
MIN_OCTAVE      = 2
MAX_OCTAVE      = 8

BUTTONWIDTH     = 100
BUTTONHEIGHT    = 400

SCALEWIDTH      = 1.5
SCALEHEIGHT     = 2
SHARPWIDTH      = BUTTONWIDTH  // SCALEWIDTH
SHARPHEIGHT     = BUTTONHEIGHT // SCALEHEIGHT

DISPLAYWIDTH    = BUTTONWIDTH * 7
DISPLAYHEIGHT   = BUTTONHEIGHT

DISPLAYSURF     = pygame.display.set_mode((DISPLAYWIDTH,DISPLAYHEIGHT))
DISPLAYRECT     = DISPLAYSURF.get_rect()

CLOCK           = pygame.time.Clock()
FRAMERATE       = 60

FONT            = pygame.font.SysFont(None, 30)

class Button(pygame.sprite.Sprite):
    def __init__(self,text,mode,key,**pos):
        super().__init__()
        
        if   mode == 'normal'   : self.colors = {'on_click':'#bcbcbc', 'on_button':'#eeeeee', 'on_normal':'#ffffff'}; SIZE = (BUTTONWIDTH, BUTTONHEIGHT)
        elif mode == 'sharp'    : self.colors = {'on_click':'#4f5b62', 'on_button':'#263238', 'on_normal':'#000a12'}; SIZE = (SHARPWIDTH , SHARPHEIGHT )
        else                    : raise NameError('Unknown button mode')
        self.ready2play = pygame.time.get_ticks()
        self.cooldown   = 5
        self.channel    = CHANNEL
        self.pressed    = False
        
        self.text       = text
        self.key        = key
        self.note       = Note(self.text, OCTAVE)
        
        self.image      = pygame.Surface(SIZE)
        self.rect       = self.image.get_rect(**pos)
        
        self.color      = self.colors['on_normal']
        self.image.fill(self.color)
        
        self.text_color = 'black' if mode=='normal' else 'white'
        
        #self.text_rect  = self.text_surf.get_rect(midtop=self.rect.center)
        self.text_surf  = FONT.render(self.text, True, self.text_color)
        self.text_rect  = self.text_surf.get_rect(midtop=self.image.get_rect().center)
        self.image.blit(self.text_surf, self.text_rect)
        
    def play(self):
        fluidsynth.play_Note(self.note, self.channel, 100)
        
    def update(self):
        now     = pygame.time.get_ticks()
        keys    = pygame.key.get_pressed()
        if now > self.ready2play +  50 and keys[self.key] : self.play(); self.color = self.colors['on_click']; self.ready2play = now + self.cooldown
        if now > self.ready2play + 100 : self.color = self.colors['on_normal']            
        if now > self.ready2play + 500 : fluidsynth.stop_Note(self.note, self.channel)
        
        self.image.fill(self.color)      
        self.image.blit(self.text_surf, self.text_rect)
        pygame.draw.rect(self.image, 'black', self.image.get_rect(), width=3)
        
Buttons     = pygame.sprite.Group()

C           = Button('C' , mode='normal', key=pygame.K_q, topleft=DISPLAYRECT.topleft)
C_          = Button('C#', mode='sharp' , key=pygame.K_w, midtop =C.rect.topright)
D           = Button('D' , mode='normal', key=pygame.K_e, topleft=C.rect.topright)
D_          = Button('D#', mode='sharp' , key=pygame.K_a, midtop =D.rect.topright)
E           = Button('E' , mode='normal', key=pygame.K_s, topleft=D.rect.topright)
F           = Button('F' , mode='normal', key=pygame.K_d, topleft=E.rect.topright)
F_          = Button('F#', mode='sharp' , key=pygame.K_g, midtop =F.rect.topright)
G           = Button('G' , mode='normal', key=pygame.K_h, topleft=F.rect.topright)
G_          = Button('G#', mode='sharp' , key=pygame.K_j, midtop =G.rect.topright)
A           = Button('A' , mode='normal', key=pygame.K_b, topleft=G.rect.topright)
A_          = Button('A#', mode='sharp' , key=pygame.K_n, midtop =A.rect.topright)
B           = Button('B' , mode='normal', key=pygame.K_m, topleft=A.rect.topright)


Buttons.add(C,D,E,F,G,A,B,C_,D_,F_,G_,A_)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    Buttons.draw(DISPLAYSURF)
    Buttons.update()
    pygame.display.update()
    CLOCK.tick(FRAMERATE)
    