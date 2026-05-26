import pygame as pg
import math
import random

pg.init()

WIDTH, HEIGHT = 1920, 1080
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Object Tracking Simulation with Pursuit Behavior")
DRONE_RADIUS = 20
WHITE = (0, 0, 0)
RED = (255, 0, 0)

class Drone:
    def __init__(self, x,y,DRONE_RADIUS=20, max_speed=10):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.radius = DRONE_RADIUS
        self.max_speed = max_speed

    def pursuit(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            desired_vx = (dx/ distance) * self.max_speed
            desired_vy = (dy/ distance) * self.max_speed
            self.vx += (desired_vx - self.vx) * 0.5
            self.vy += (desired_vy - self.vy) * 0.5
            
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x <= 0:
            self.vx = -self.vx
        if self.y <= 0:
            self.vy = -self.vy
            
    def draw(self):
        pg.draw.circle(screen, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), (int(self.x), int(self.y)), self.radius)
        

Drone1 = Drone(WIDTH//4, HEIGHT//2)

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    screen.fill(WHITE)
    
    Drone1.update()
    Drone1.draw()
    
    mouse_x, mouse_y = pg.mouse.get_pos()
    Drone1.pursuit(mouse_x, mouse_y)
    
    pg.display.flip()
    clock.tick(60)

pg.quit()