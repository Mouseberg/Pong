import pygame, sys

from entities import Paddle, Ball

pygame.init()
pygame.font.init

pygame.display.set_caption("Fractal Trees")
width = 1200
height = 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
text = pygame.font.SysFont("Consolas", 100)
paddleHeight = 100
paddleWidth = 20
margin = 50
segments = 12
segLength = height/(segments*2)

leftPaddle = Paddle(pygame.Vector2(margin, height/2-paddleHeight/2),(paddleWidth, paddleHeight))
rightPaddle = Paddle(pygame.Vector2(width - margin - paddleWidth, height/2 - paddleHeight),(paddleWidth,paddleHeight))
ball = Ball(pygame.Vector2(width/2,height/2),(30,30))

while True:
    screen.fill((0, 0, 0))
    for i in range(segments * 2):
        if i % 2:
            pygame.draw.line(screen, (255,255,255), (width/2, i * segLength), (width/2, (i + 1) * segLength), paddleWidth)
    
    leftPaddle.render(screen)
    rightPaddle.render(screen)
    ball.render(screen)
    ball.update([rightPaddle, leftPaddle])
    
    leftScore = text.render(str(leftPaddle.score), False, (255,255,255))
    screen.blit(leftScore, (width/2-leftScore.get_width()-margin, 25))
    
    rightScore = text.render(str(rightPaddle.score), False, (255,255,255))
    screen.blit(rightScore, (width/2 + margin, 25))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                leftPaddle.movement["Down"] = True
            if event.key == pygame.K_w:
                leftPaddle.movement["Up"] = True
            if event.key == pygame.K_DOWN:
                rightPaddle.movement["Down"] = True
            if event.key == pygame.K_UP:
                rightPaddle.movement["Up"] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                leftPaddle.movement["Down"] = False
            if event.key == pygame.K_w:
                leftPaddle.movement["Up"] = False
            if event.key == pygame.K_DOWN:
                rightPaddle.movement["Down"] = False
            if event.key == pygame.K_UP:
                rightPaddle.movement["Up"] = False
            
                
        
    rightPaddle.update(height)
    leftPaddle.update(height)            
    
            
    pygame.display.update()
    clock.tick(60) #60fps


    
    