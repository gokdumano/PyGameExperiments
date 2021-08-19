import pygame
import math
pygame.init()

# The gravitational constant G
# Assumed scale: 100 pixels = 1AU.
# 149.6 million km, in meters.

G          = 6.67408E-11
AU         = 14.96E11   
#AU         = 1.5E11
SCALE      = 250 / AU
TIMESTEP   = 86400
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT) = (1000, 600)
SCREENSURF = pygame.display.set_mode(SCREENSIZE)

font = pygame.font.Font(None, 30)
pygame.display.set_caption("Planets")

RUN    = True
CLOCK  = pygame.time.Clock()

class Body(pygame.sprite.Sprite):
    def __init__(self, x0, y0, vx0, vy0, mass, radius, name='Undefined', color=0x000000):
        super().__init__()
        self.x , self.y  = x0 , y0
        self.vx, self.vy = vx0, vy0
        self.m , self.r  = mass, radius
        self.name        = name
        self.color       = color
        
        self.text        = font.render(self.name, 1, self.color)
        self.x_ = self.x * SCALE + SCREENWIDTH  // 2
        self.y_ = self.y * SCALE + SCREENHEIGHT // 2
        
        self.image       = pygame.Surface([5,5])
        self.image.fill(self.color)
        self.rect        = self.image.get_rect(center=(self.x_, self.y_))
    
    def __repr__(self):
        return f'<{self.name}(Pos:({self.x:.3e},{self.y:.3e})m, PosScaled:({self.x_:.3f},{self.y_:.3f})m, Vel:({self.vx:.3e},{self.vy:.3e})m/s, M:{self.m:.3e}kg, r:{self.r:.3e}m)>'
    
    def __str__(self):
        return self.__repr__()
    
    def acc_on(self, xm=None, ym=None, bodym=None):
        # Acceleration contributed by one mass M of a Body
        # on another Body of mass m at location (x, y)
        # dx   = XM - Xm
        # dy   = YM - Ym
        # dist = (dx^2+dy^2)^.5
        # ax   = GM*dx / dist^3
        # ay   = GM*dy / dist^3
        #
        #Fx = G*self.m*other.m*dx/dist**3      
        #Fy = G*self.m*other.m*dy/dist**3
        
        dx, dy = self.x - xm, self.y - ym
        dist   = math.hypot(dx, dy)
        assert dist != 0, 'Acceleration contributed by one on self is undefined'
        
        a      = G * self.m / dist**3
        ax, ay = a * dx, a * dy
        
        return ax, ay
    
    def step(self, other):
        k1x , k1y  = other.vx, other.vy
        k1vx, k1vy = self.acc_on(other.x, other.y)
        
        k2x  = k1x + TIMESTEP * k1vx / 2
        k2y  = k1y + TIMESTEP * k1vy / 2
        k2vx, k2vy = self.acc_on(other.x + TIMESTEP * k1x / 2,other.y + TIMESTEP * k1y / 2)
        
        k3x  = k1x + TIMESTEP * k2vx / 2
        k3y  = k1y + TIMESTEP * k2vy / 2
        k3vx, k3vy = self.acc_on(other.x + TIMESTEP * k2x / 2, other.y + TIMESTEP * k2y / 2)
        
        k4x  = k1x + TIMESTEP * k3vx / 2
        k4y  = k1y + TIMESTEP * k3vy / 2
        k4vx, k4vy = self.acc_on(other.x + TIMESTEP * k3x / 2, other.y + TIMESTEP * k3y / 2)
        
        other.x  += (k1x  + 2*k2x  + 2*k3x  + k4x ) * TIMESTEP / 6
        other.y  += (k1y  + 2*k2y  + 2*k3y  + k4y ) * TIMESTEP / 6
        
        other.vx += (k1vx + 2*k2vx + 2*k3vx + k4vx) * TIMESTEP / 6
        other.vy += (k1vy + 2*k2vy + 2*k3vy + k4vy) * TIMESTEP / 6
        
        other.x_  = other.x * SCALE + SCREENWIDTH  // 2
        other.y_  = other.y * SCALE + SCREENHEIGHT // 2
        other.rect.center = (other.x_, other.y_)
        SCREENSURF.blit(other.text, (other.x_, other.y_))
    
    def update(self, others):
        for other in others:
            self.step(other)

Sun     = Body(        0, 0, 0,      0, 1.9890E30, 6.957E8, 'Sun'    , 0xffc58a)
Mercury = Body(-4.600E10, 0, 0, -5.9E4, 0.3301E24, 2.440E6, 'Mercury', 0xad9d9d)
Venus   = Body(-1.075E11, 0, 0, -3.5E4, 4.8675E24, 6.052E6, 'Venus'  , 0x450515)
Earth   = Body(-1.471E11, 0, 0, -3.0E4, 5.9720E24, 6.371E6, 'Earth'  , 0x5588a3)
Mars    = Body(-2.066E11, 0, 0, -2.7E4, 6.4171E23, 3.390E6, 'Mars'   , 0xffc58a)
Jupiter = Body(-7.405E11, 0, 0, -1.4E4, 1.8982E27, 7.149E7, 'Jupiter', 0xd9adad)
Saturn  = Body(-1.352E12, 0, 0, -1.0E4, 5.6834E26, 5.436E7, 'Saturn' , 0xfccbcb)
Uranus  = Body(-2.741E12, 0, 0, -7.1E3, 8.6813E25, 2.497E7, 'Uranus' , 0xb9cced)
Neptune = Body(-4.444E12, 0, 0, -5.5E3, 1.0241E26, 2.434E7, 'Neptune', 0x93b5e1)

sun     = pygame.sprite.GroupSingle(Sun)
planets = pygame.sprite.Group((Mercury,Venus,Earth,Mars,Jupiter,Saturn,Uranus,Neptune))
#planets = pygame.sprite.Group((Mercury,Venus,Earth,Mars))

while RUN:
    SCREENSURF.fill(0xffffff)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    
    sun.update(planets)
    sun.draw(SCREENSURF)
    planets.draw(SCREENSURF)
    
    pygame.display.update()
    CLOCK.tick(60)
  
pygame.quit()
