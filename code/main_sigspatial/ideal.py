import numpy as np
import matplotlib.pyplot as plt
import random    

# 24 hours
t = range(0,25)        
wobble = lambda x: x + x*((random.random()*2 -1)*0.005)              

# data: pre-fetch
s1 = [1,1,1,1,1,1,1,0.7,0.3,0,0,0,0,0,0,0,0,0.3,0.7,1,1,1,1,1,1]
s1 = map(wobble, s1)

# data: cache-miss
s2 = map(lambda x: 1-x, s1)
        
ideal_load = 0.44           
s1 = map(lambda x: x*ideal_load, s1)
s2 = map(lambda x: x*ideal_load, s2)

# data: latency
s3 = [200]*len(t)
s3 = map(wobble, s3)

ar = (1.61803399, 1)
factor = 2.5
fig = plt.figure(figsize=(ar[0]*factor, ar[1]*factor))
ax1 = fig.add_subplot(111)                     
ax1.plot(t, s1, 'b', t, s2, 'b--')
#ax1.set_xlabel('Time (h)')
# Make the y-axis label and tick labels match the line color.
#ax1.set_ylabel('Load', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
ax1.axis((0,24,0,0.88))

ax2 = ax1.twinx()
ax2.plot(t, s3, 'g')
#ax2.set_ylabel('Average latency (ms)', color='k')
for tl in ax2.get_yticklabels():
    tl.set_color('g')
ax2.axis((0,24,0,360))
plt.savefig("ideal.png")