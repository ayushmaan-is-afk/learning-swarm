import pygame as pg
import random
import math
pg.init()

width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Multiple Bouncing Balls with collision physics")
clock = pg.time.Clock()
BALL_RADIUS = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Ball:
    def __init__(self, color):
        self.x = random.uniform(BALL_RADIUS, width - BALL_RADIUS)
        self.y = random.uniform(BALL_RADIUS, height - BALL_RADIUS)
        self.vx = random.randint(2,6) 
        self.vy = random.randint(2,6)
        self.radius = BALL_RADIUS
        self.color = color
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x - self.radius <= 0 or self.x + self.radius >=width:
            self.vx = -self.vx
            self.x = max(self.radius, min(self.x, width - self.radius))
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.vy = -self.vy
            self.y = max(self.radius, min(self.y, height - self.radius))
    
    def draw(self):
        pg.draw.circle(screen, self.color, (int(self.x), (int(self.y))), BALL_RADIUS)
        
    def check_collisions(self, other_ball):
        dx = self.x - other_ball.x
        dy = self.y - other_ball.y
        
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance <2 * 20:
            normal_vector = pg.math.Vector2(dx, dy).normalize()
            relative_velocity = pg.math.Vector2(self.vx -other_ball.vx, self.vy - other_ball.vy)
            velocity_along_normal = relative_velocity.dot(normal_vector)
            
            
            if velocity_along_normal > 0:return
            
            impulse = velocity_along_normal
            self.vx -= impulse * normal_vector.x
            self.vy -= impulse * normal_vector.y
            other_ball.vx += impulse * normal_vector.x
            other_ball.vy += impulse * normal_vector.y

balls = [Ball((random.randint(0,255), random.randint(0,255), random.randint(0,255))) for _ in range(7)]

running = True 
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    for ball in balls:
        ball.update()
        
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            balls[i].check_collisions(balls[j])
            
    screen.fill((255,255,255))
    
    for ball in balls:
        ball.draw()
        
    pg.display.flip()
    clock.tick(90)
    
pg.quit()