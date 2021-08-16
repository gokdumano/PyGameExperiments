from random import randint
import pygame
pygame.init()
pygame.display.set_caption("Pong!")

class Block(pygame.sprite.Sprite):
    def __init__(self,color,**pos):
        super().__init__()
        default = 'images/green.png'
        path    = {'r':'images/red.png','o':'images/orange.png','b':'images/blue.png','g':'images/green.png'}.get(color,default)

        self.image  = pygame.image.load(path)
        self.rect   = self.image.get_rect(**pos)
        
class Ball(pygame.sprite.Sprite):
    def __init__(self,**pos):
        super().__init__()
        
        path        = 'images/ball.png'
        self.image  = pygame.image.load(path)
        #self.image  = pygame.transform.scale2x(image)
        self.rect   = self.image.get_rect(**pos)
        self.Vx     =  0
        self.Vy     = -5
    
    def update(self, paddle, blocks):
        if self.rect.right + self.Vx > 480 or self.rect.left + self.Vx < 30:
            self.Vx *= -1
            
        if self.rect.top + self.Vy < 30 or pygame.sprite.collide_rect(self, paddle.sprite):
            self.Vx  = randint(-5,5) 
            self.Vy *= -1
            
        if pygame.sprite.spritecollide(self, blocks, True):
            self.Vx  = randint(-5,5) 
            self.Vy *= -1
            
        self.rect.move_ip(self.Vx,self.Vy)
        
class Paddle(pygame.sprite.Sprite):
    def __init__(self,**pos):
        super().__init__()
        
        path        = 'images/paddle.png'
        self.image  = pygame.image.load(path)
        #self.image  = pygame.transform.scale2x(image)
        self.rect   = self.image.get_rect(**pos)
        self.Vx     = 8
        self.Vy     = 0
    
    def update(self):
        keys = pygame.key.get_pressed()
        if   keys[pygame.K_d] and self.rect.right + self.Vx < 480: self.rect.move_ip( self.Vx,self.Vy)
        elif keys[pygame.K_a] and self.rect.left  - self.Vx >  30: self.rect.move_ip(-self.Vx,self.Vy)
        
class Game:
    def __init__(self,displaysize,framerate):
        self.display_surf = pygame.display.set_mode(displaysize)
        self.display_rect = self.display_surf.get_rect()
    
        self.framerate    = framerate
        self.clock        = pygame.time.Clock()
    
        self.play         = True
        self.curr_screen  = self.start_screen
        self.setup()
        
    def setup(self):
        path             = 'images/border.png'
        border_surf      = pygame.image.load(path)
        self.border_surf = pygame.transform.scale2x(border_surf)
        self.border_rect = self.border_surf.get_rect(topleft=self.display_rect.topleft)
        
        paddle           = Paddle(center=(self.display_rect.centerx,450))
        self.paddle      = pygame.sprite.GroupSingle(paddle)
        
        ball             = Ball(midbottom=paddle.rect.midtop)
        self.ball        = pygame.sprite.GroupSingle(ball)
        
        blocks_text      = ['r'*32,'o'*32,'o'*32,'g'*32,'g'*32,'g'*32,'b'*32,]
        self.blocks      = pygame.sprite.Group()
        
        scaleRow, offsetRow = 14, 32*3
        scaleCol, offsetCol = 14, 32
        
        for CoordRow, Row in enumerate(blocks_text):
            for CoordCol, Color in enumerate(Row):
                if Color != ' ':
                    BlockRow = CoordRow * scaleRow + offsetRow
                    BlockCol = CoordCol * scaleCol + offsetCol
                    block    = Block(Color, topleft=(BlockCol, BlockRow))
                    self.blocks.add(block)
        
    def play_screen(self):
        self.display_surf.fill('#000000')
        self.display_surf.blit(self.border_surf, self.border_rect)
        
        self.paddle.draw(self.display_surf)
        self.blocks.draw(self.display_surf)
        self.ball.draw(self.display_surf)
        
        self.paddle.update()
        self.blocks.update()
        self.ball.update(self.paddle, self.blocks)
        
        if self.paddle.sprite.rect.centery < self.ball.sprite.rect.centery:
            self.setup()
        
    def start_screen(self):
        path  = 'images/start_screen.png'
        image = pygame.image.load(path)
        image = pygame.transform.scale2x(image)
        rect  = image.get_rect(topleft=self.display_rect.topleft)
        
        keys  = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.curr_screen = self.play_screen
        self.display_surf.blit(image, rect)
    
    def start(self):
        while self.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.play = False
            self.curr_screen()
            pygame.display.update()
            self.clock.tick(self.framerate)
        pygame.quit()
        
        
        