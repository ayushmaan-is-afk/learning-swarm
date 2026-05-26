import pygame as pg

#Initialization
pg.init()

#Dimensions
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Bouncing Ball Sim")

#Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#Ball properties
g = 9.81
cor = 0.8
dt = 0.05
x,y = WIDTH//4, HEIGHT//2
radius = 20
vx, vy = 15,10

#Controls the frame rate
clock = pg.time.Clock()

#Update Ball Position
def update_ball(t=0):
    global x,y,vx,vy
    
    while x<WIDTH:
        t+=dt
        x+=vx*dt
        y+=vy*dt
        vy+=g*dt
        if y+radius>HEIGHT:
            y=HEIGHT-radius
            vy = -vy*cor
        yield x,y
ball = update_ball()

#Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    x,y = next(ball)
    screen.fill(WHITE)
    pg.draw.circle(screen, RED, (int(x), int(y)), radius)
    
    pg.display.flip()
    clock.tick(90)
    
pg.quit()


