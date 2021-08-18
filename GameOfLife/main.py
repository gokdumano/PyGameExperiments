from random import choices
import pygame
pygame.init()

HCELLNUM    = 250
VCELLNUM    = 150
CELLSIZE    = 3
PERCALIVE   = 0.075

DISPLAYSIZE = (CELLSIZE*HCELLNUM, CELLSIZE*VCELLNUM)
DISPLAYSURF = pygame.display.set_mode(DISPLAYSIZE)
pygame.display.set_caption("Game of Life")

PLAY  = True
FPS   = 12
CLOCK = pygame.time.Clock()

class Cell(pygame.sprite.Sprite):
    def __init__(self,iCol,iRow,CellSize,percAlive,**pos):
        super().__init__()
        self.iCol      = iCol
        self.iRow      = iRow
        self.isAlive,  = choices([True, False], [percAlive, 1-percAlive])
        self.image     = pygame.Surface([CellSize, CellSize])
        self.rect      = self.image.get_rect(**pos)
        
    def __str__(self):
        return '+' if self.isAlive else ' '
        
    def numAlive(self, grid):
        dirs = {'N':(0,-1),'NE':(1,-1),'E':(1,0),'SE':(1,1),'S':(0,1),'SW':(-1,1),'W':(-1,0),'NW':(-1,-1)}
        num  = 0
        for dCol, dRow in dirs.values():
            index = self.iCol + dCol, self.iRow + dRow
            jCell = grid.get(index)
            if jCell is not None and jCell.isAlive: num += 1
        return num
    
    def update(self, grid):
        num  = self.numAlive(grid)
        if   self.isAlive and num in [2, 3]: self.isAlive = True ; self.image.fill(0xffffff)
        elif not self.isAlive and num == 3 : self.isAlive = True ; self.image.fill(0xffffff)
        else                               : self.isAlive = False; self.image.fill(0x000000)
            

cells = pygame.sprite.Group()
grid  = {}

for Row in range(VCELLNUM):
    for Col in range(HCELLNUM):
        topleft = (Col*CELLSIZE,Row*CELLSIZE)
        cell    = Cell(Col,Row,CELLSIZE,PERCALIVE,topleft=topleft)
        cells.add(cell)
        grid[(Col,Row)] = cell

while PLAY:
    for EVENT in pygame.event.get():
        if EVENT.type == pygame.QUIT:
            PLAY = False
    
    cells.update(grid)
    cells.draw(DISPLAYSURF)
    
    pygame.display.update()
    CLOCK.tick(FPS)    

pygame.quit()
