from utils import *
import pygame
pygame.init()

border00 = Border(SIZE, center=(SCREENRECT.center))
borders  = pygame.sprite.GroupSingle(border00)
bodies   = Sample(100)

while not STOP:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            STOP = True
    borders.draw(SCREENSURF)
    borders.update(bodies, borders)
    
    bodies.draw(SCREENSURF)
    #bodies.update(bodies)
    
    pygame.display.update()
    CLOCK.tick(60)
pygame.quit()



