# This program is a simple matplotlib simulation of a bouncing ball.

import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

ball1, = ax.plot([], [], 'o', markersize=35)

x1, y1 = 50, 50
vx1, vy1 = 15, 10

def update(frame):
    global x1,y1,vx1,vy1
    x1 += vx1
    y1 += vy1


    if x1 <= 0 or x1 >= 100:
        vx1 = -vx1
    if y1 <= 0 or y1 >= 100:
        vy1 = -vy1

    ball1.set_data([x1], [y1])
    return ball1,

ani = animation.FuncAnimation(fig, update, frames=240, interval=35, blit=True)
plt.show()