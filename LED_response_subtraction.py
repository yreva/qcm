import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


data = pd.read_csv(r"P:\research\experiments\QCM\data\2023_07_12_LED_response\2023_07_14_LED_responses.csv")

time_hours = data['Relative_time'].to_numpy()/3600
frequency = data['Resonance_Frequency'].to_numpy()
temperature = data['Temperature'].to_numpy()

dfdt = np.empty(len(frequency))
d2fdt2 = np.empty(len(frequency))
for hour in time_hours:
    loc = np.where(time_hours==hour)[0]
    try:
        dfdt[loc] = (frequency[loc+1] - frequency[loc-1]) / (time_hours[loc+1] - time_hours[loc-1])
    except IndexError:
        dfdt[loc]=0

for i in range(1,len(time_hours)-1):
    d2fdt2[i] = (dfdt[i+1] - dfdt[i-1]) / (time_hours[i+1]-time_hours[i-1])


for i in range(1,len(time_hours)-10):
    if d2fdt2[i] > 1e4:
        dfdt[i] = dfdt[i]/1e4
        dfdt[i+1] = dfdt[i+1]/1e4
        dfdt[i+2] = dfdt[i+2]/1e4
        dfdt[i+3] = dfdt[i+3]/1e4
        dfdt[i+4] = dfdt[i+4]/1e4
        dfdt[i+5] = dfdt[i+5]/1e4
        dfdt[i+6] = dfdt[i+6]/1e4
        dfdt[i+7] = dfdt[i+7]/1e4
        dfdt[i+8] = dfdt[i+8]/1e4

plt.scatter(time_hours,dfdt)
plt.plot(time_hours,d2fdt2/1000,c='r')
plt.ylim(-10000,10000)
#plt.xlim(0.84,0.88)
plt.show()

