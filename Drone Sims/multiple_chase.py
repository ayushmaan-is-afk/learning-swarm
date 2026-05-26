# This is a simulation for quadcopters pursuing a target while avoiding obstacles and maintaining flocking behavior by following Boids rules.

import math
import random
from turtle import speed
import pygame as pg

pg.init()

WIDTH, HEIGHT = 1920, 1080
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Multiple Drones Pursuit Simulation")
DRONE_RADIUS = 20
WHITE = (0,0,0)
RED = (255, 0, 0)
MAX_SPEED = 6

class Drone: 
    
    def __init__(self, x, y, DRONE_RADIUS, MAX_SPEED, perception_radius=100, separation_radius=40):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.perception_radius = perception_radius
        self.radius = DRONE_RADIUS
        self.max_speed = MAX_SPEED
        self.neighbours = []
        self.separation_radius = separation_radius
        self.leader = None
        self.is_leader = False
  
    
    def avoidance(self, obstacle):
        dx = self.x - obstacle.x
        dy = self.y - obstacle.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < obstacle.radius + 100 and distance > 0:
            force_away = (1 / distance**2)
            self.vx += (dx / distance) * force_away * 6000
            self.vy += (dy / distance) * force_away * 6000
    
    
    def separation(self, drones):
        for drone in drones:
            if drone != self:
                dx = self.x - drone.x
                dy = self.y - drone.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < self.perception_radius and distance > 0:
                    force_away = (1/ distance**2) 
                    self.vx += (dx / distance) * force_away * 1200
                    self.vy += (dy / distance) * force_away * 1200


    def alignment(self, drones):
        self.neighbours = []
        for drone in drones:
            if drone != self:
                dx = drone.x - self.x
                dy = drone.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < self.perception_radius and distance > 0:
                    self.neighbours.append((drone, distance))
    
        if self.neighbours:
            total_weight = sum(1 / dist for drone, dist in self.neighbours)
            avg_vx = sum(drone.vx * (1 / dist) for drone, dist in self.neighbours) / total_weight
            avg_vy = sum(drone.vy * (1 / dist) for drone, dist in self.neighbours) / total_weight
    
            self.vx += (avg_vx - self.vx) * 0.05
            self.vy += (avg_vy - self.vy) * 0.05
    
    
    def cohesion(self, drones):
        if self.neighbours:
            avg_x = sum(drone.x for drone, dist in self.neighbours) / len(self.neighbours)
            avg_y = sum(drone.y for drone, dist in self.neighbours) / len(self.neighbours)
            
            dx = avg_x - self.x
            dy = avg_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                self.vx += (dx / distance) * 0.05
                self.vy += (dy / distance) * 0.05
            
            
    def pursuit(self, target_x, target_y):
        
        if not self.is_leader and self.leader is not None:
            dx = self.leader.x - self.x
            dy = self.leader.y - self.y        
        else:
            dx = target_x - self.x
            dy = target_y - self.y
            
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            if self.is_leader:
                desired_vx = (dx / distance) * self.max_speed
                desired_vy = (dy / distance) * self.max_speed
            else:
                desired_vx = (dx / distance) * self.max_speed * 0.8
                desired_vy = (dy / distance) * self.max_speed * 0.8
            self.vx += (desired_vx - self.vx) * 0.5
            self.vy += (desired_vy - self.vy) * 0.5
    
    
    def update(self, drones):
        self.separation(drones)
        self.alignment(drones)
        self.cohesion(drones)
        self.x += self.vx
        self.y += self.vy
        
        if self.x <= 0 or self.x >= WIDTH:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= HEIGHT:
            self.vy = -self.vy
            
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > self.max_speed:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed
        
            
    def draw(self):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
  
  
def update_pursuit(drones, target_x, target_y):
    closest = min(drones, key=lambda d: math.sqrt((d.x - target_x)**2 + (d.y - target_y)**2))
    for drone in drones:
        drone.is_leader = (drone == closest)
        drone.leader = closest 
  
       
       
class Obstacle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        
    def draw(self):
        pg.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), self.radius)
        
         
Drones = [Drone(random.uniform(20, WIDTH-20), random.uniform(20, HEIGHT-20), DRONE_RADIUS, MAX_SPEED) for _ in range(6)]
obstacles = [Obstacle(random.uniform(100, WIDTH-100), random.uniform(100, HEIGHT-100), 50) for _ in range(5)]
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    screen.fill(WHITE)
    
    for obstacle in obstacles:
        obstacle.draw()
            
    mouse_x, mouse_y = pg.mouse.get_pos()
    update_pursuit(Drones, mouse_x, mouse_y)
    
    for drone in Drones:
        drone.update(Drones)
        drone.draw()
        drone.pursuit(mouse_x, mouse_y)
        for obstacle in obstacles:     
            drone.avoidance(obstacle)
        
    pg.display.flip()
    clock.tick(60)
    
pg.quit()