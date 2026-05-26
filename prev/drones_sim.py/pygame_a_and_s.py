import pygame as pg
import math
import random

pg.init()

WIDTH, HEIGHT = 800,600
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Drone Target Seeking Simulation with alignment and separation")
DRONE_SIZE = 20
perception_radius = 100
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Drone:
    def __init__(self, x, y, color, DRONE_SIZE=20, perception_radius=100, max_speed=10):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.size = DRONE_SIZE
        self.max_speed = max_speed
        self.color = color
        self.perception_radius = perception_radius
        self.neighbours = []

    def separation(self, drones, separation_radius=40):
        
        for other in drones:
            if other != self:
                dx = self.x - other.x
                dy = self.y - other.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < separation_radius:
                    force_away = (separation_radius - distance) 
                    self.vx += (dx / distance) * force_away * 0.05
                    self.vy += (dy / distance) * force_away * 0.05
                    other.vx -= (dx / distance) * force_away * 0.05
                    other.vy -= (dy / distance) * force_away * 0.05
                    
                    
    def alignment(self, drones):
        for drone in drones:
            if drone !=self:
                dx = drone.x - self.x
                dy = drone.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < self.perception_radius:
                    self.neighbours.append(drone)
        
        if self.neighbours:
            avg_vx = sum(drone.vx for drone in self.neighbours) / len(self.neighbours)
            avg_vy = sum(drone.vy for drone in self.neighbours) / len(self.neighbours)
            
            self.vx += (avg_vx - self.vx) * 0.05
            self.vy += (avg_vy - self.vy) * 0.05
            
    
    def cohesion(self, others):
        if self.neighbours:
            avg_x = sum(drone.x for drone in self.neighbours) / len(self.neighbours)
            avg_y = sum(drone.y for drone in self.neighbours) / len(self.neighbours)
            
            self.vx += (avg_x - self.x) * 0.01
            self.vy += (avg_y - self.y) * 0.01
            
    
    def update(self, drones):
        self.separation(drones)
        self.alignment(drones)
        self.cohesion(drones)

        # move
        self.x += self.vx
        self.y += self.vy

        # speed cap
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > self.max_speed:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed

        # boundary
        if self.x <= 0 or self.x >= WIDTH:
            self.vx = -self.vx
            self.x = max(0, min(self.x, WIDTH))
        if self.y <= 0 or self.y >= HEIGHT:
            self.vy = -self.vy
            self.y = max(0, min(self.y, HEIGHT))
            
    def draw(self):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        
drones = [Drone(random.randint(0, WIDTH), random.randint(0, HEIGHT), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), DRONE_SIZE, perception_radius) for _ in range(5)]
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    screen.fill(WHITE)
    
    for drone in drones:
        drone.update(drones)
        drone.draw()    
        
    pg.display.flip()
    clock.tick(60)
        
        
pg.quit()