# importing mplot3d toolkits, numpy and matplotlib
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

def generate_data():
    # defining all 3 axes
    z = np.linspace(0, 1, 100)
    x = z * np.sin(25 * z)
    y = z * np.cos(25 * z)
    return (x,y,z)


def get_data_for_itr(i,x,y,z):
    return (x[i],y[i],z[i])

def animate(i):
    global x,y,z
    xi,yi,zi=get_data_for_itr(i,x,y,z)
    tempx.append(xi)
    tempy.append(yi)
    tempz.append(zi)
    
    
    # if i >40:
    #     '''
    #     This helps in keeping the graph fresh and refreshes values after every 40 timesteps
    #     '''
    #     tempx.pop(0)
    #     tempy.pop(0)
    #     tempz.pop(0)
    #     #counter = 0
    #     plt.cla() # clears the values of the graph
        
      # syntax for 3-D projection
    ax = plt.axes(projection ='3d')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    # plotting
    ax.plot3D(tempx, tempy, tempz, 'green')
    ax.set_title('3D line plot')
    
    time.sleep(0.02) # keep refresh rate of 0.25 seconds

tempx=[]
tempy=[]
tempz=[]

x=[]
y=[]
z=[]

def main():
    global x,y,z
    x,y,z=generate_data()
    #fig = plt.figure()
    
  

    ani = FuncAnimation(plt.gcf(), animate, 100,interval=1)
    plt.tight_layout()
    plt.show()


if __name__=='__main__':
    main()
