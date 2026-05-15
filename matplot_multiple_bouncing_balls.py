import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
fig,ax = plt.subplots()
ax.set_xlim(0,500)
ax.set_ylim(0,500)

drones = []

for i in range(10):
    x = random.uniform(1,500)
    y = random.uniform(1,500)
    vx = random.uniform(-20,20)
    vy = random.uniform(-10,20) 
    # vx = random.uniform(-1,10)
    # vy = random.uniform(-1,10)
    
    drone, = ax.plot([], [], 'o', markersize=10)
    drones.append([x,y,vx,vy,drone])
    
    
def update(frame):
    for drone in drones:
        drone[0] += drone[2]
        drone[1] += drone[3]
        
        if drone[0] <= 0 or drone[0] >= 500:
            drone[2] = -drone[2]
        if drone[1] <= 0 or drone[1] >= 500:
            drone[3] = -drone[3]
            
        drone[4].set_data([drone[0]], [drone[1]])
    return [d[4] for d in drones]
    
ani = animation.FuncAnimation(fig, update, frames=240, interval=50, blit=True)

plt.show()