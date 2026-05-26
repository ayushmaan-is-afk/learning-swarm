import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = 9.81
dt = 0.05
cor = 0.45
x,y = 0,4
vx,vy = 2,0

def get_pos(t=0):
    global x,y,vx,vy
    
    while x<5:
        t+=dt
        x+=vx*dt
        y+=vy*dt
        vy-=g*dt
        if y<0:
            y=0
            vy = -vy*cor
        yield x,y
        
fig, ax = plt.subplots()
ax.set_xlim(0,5)
ax.set_ylim(0,5)
ball = plt.Circle((x,y),0.2,fc='r')
ax.add_patch(ball)

def animate(pos):
    x,y = pos
    ball.set_center((x,y))
    return ball,

ani = animation.FuncAnimation(fig, animate, get_pos, blit=True, interval=dt*1000)
plt.show()
    