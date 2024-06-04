import pygame
from dataclasses import dataclass
import pygame, random

@dataclass
class Paddle:
    pos: pygame.Vector2
    size: tuple
    color: tuple = (255, 128, 255)
    speed: int = 12
    
    def __post_init__(self):
        self.movement = dict(Up = False, Down = False)
        self.score: int = 0
        
    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def render(self, surf):
        pygame.draw.rect(surf, self.color, self.rect())
        return True
    
    def update(self, height):
        self.pos.y = self.pos.y + self.speed * (self.movement["Down"] - self.movement["Up"])
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > height - self.size[1]:
            self.pos.y = height - self.size[1]
    
    def dir(self):
        return pygame.Vector2(0, self.movement["Down"] - self.movement["Up"])
    
@dataclass
class Ball:
    startPos: pygame.Vector2
    size: tuple
    color: tuple = (255,255,255)
    
    def __post_init__(self):
        flip = random.choice([-1,1])
        self.direction = pygame.Vector2(flip, 0)
        self.screenSize = pygame.display.get_window_size()
        self.pos = self.startPos
        self.speed = 5
    
    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def update(self, paddles: list[Paddle]):
        
        self.pos.x = self.pos.x + self.direction.x * self.speed
        # Paddle collsion in X
        for paddle in paddles:
            if self.rect().colliderect(paddle):
                self.speed = 12
                if self.direction.x > 0 : 
                    self.pos.x = paddle.pos.x - self.size[0]
                else:
                    self.pos.x = paddle.pos.x + paddle.size[0]
                self.direction.x = self.direction.x * -1
                if not paddle.dir().y == 0:
                    self.direction = self.direction.lerp(paddle.dir(), 0.5)
                    self.direction.y = pygame.math.lerp(self.direction.y, 0, 0.4)
                    self.direction = self.direction.normalize()
                self.pos = self.pos + self.direction * self.speed
        
        if self.pos.x < 0:
            paddles[0].score += 1
            self.__post_init__()
            self.pos = pygame.Vector2(self.screenSize[0]/2, self.screenSize[1]/2)
        if self.pos.x >  self.screenSize[0] - self.size[0]:
            paddles[1].score += 1
            self.__post_init__()
            self.pos = pygame.Vector2(self.screenSize[0]/2, self.screenSize[1]/2)
        
        self.pos.y = self.pos.y + self.direction.y * self.speed
        # Paddle collision in Y
        for paddle in paddles:
            if self.rect().colliderect(paddle):
                self.speed = 12
                if self.direction.y == 1: 
                    self.pos.y = paddle.pos.y - self.size[1]
                if self.direction.x == -1:
                    self.pos.y = paddle.pos.y + paddle.size[1]                  
                self.direction.y = self.direction.y * -1
        
        if self.pos.y < 0:
            self.pos.y = 0
            self.direction.y = self.direction.y * -1
            
        if self.pos.y >  self.screenSize[1] - self.size[1]:
            self.pos.y =  self.screenSize[1] - self.size[1]
            self.direction.y = self.direction.y * -1
        
        self.direction = self.direction.normalize()
        
    def changeAngle(self, intersection):
        self.angle = intersection * 180
    
    def render(self, surf):
        pygame.draw.rect(surf, self.color, self.rect())
        return True