import numpy as np
import matplotlib.pyplot as plt

# First create some toy data:
x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)

# Create just a figure and only one subplot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Simple plot')
plt.show()

# Create two subplots and unpack the output array immediately
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(x, y)
ax1.set_title('Sharing Y axis')
ax2.scatter(x, y)
plt.show()

# Create four polar axes and access them through the returned array
fig, axs = plt.subplots(2, 2, subplot_kw=dict(projection="polar"))
axs[0, 0].plot(x, y)
axs[1, 1].scatter(x, y)
plt.show()

x = []
y1 = []
y2 = []
fig, ax1 = plt.subplots(1)
def plottt():
    ax1.plot(x, y1, color='r', label='Current')
    ax1.set_xlabel('Measurement number')
    ax1.set_ylabel('Current (A)', color='red')
    ax2 = ax1.twinx()
    ax2.plot(x, y2, color='b', label='Voltage')
    ax2.set_ylabel('Voltage (V)', color='blue')
    fig.show()
plottt()
for i in range(10):
    x.append(i)
    y1.append(i)
    y2.append(i*2)
    plottt()
    fig.show()
