import pygame as pg
import random
import math

pg.init()

WIDTH, HEIGHT = 800,600
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Drone Target Seeking Simulation")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DRONE_SIZE = 20

class Drone:
    def __init__(self,x,y,color, DRONE_SIZE):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.size = DRONE_SIZE
        self.color = color
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x <= 0 or self.x >= WIDTH:
            self.vx = -self.vx
            self.x = max(0, min(self.x, WIDTH))
        if self.y <= 0 or self.y >= HEIGHT:
            self.vy = -self.vy
            self.y = max(0, min(self.y, HEIGHT))
        
    def draw(self):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        
    def seek_target(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.vx = (dx / distance) * 5
            self.vy = (dy / distance) * 5
                   
            
drones = [Drone(random.randint(0, WIDTH), random.randint(0, HEIGHT), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), DRONE_SIZE) for _ in range(5)]
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    screen.fill(WHITE)
    
    for drone in drones:
        drone.update()
        drone.draw()
                    
    mouse_x, mouse_y = pg.mouse.get_pos()
    for drone in drones:
        drone.seek_target(mouse_x, mouse_y)
        
    
    pg.display.flip()
    clock.tick(60)
    
pg.quit()