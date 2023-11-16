import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data = pd.read_csv(r"P:\research\experiments\QCM\data\2023_07_12_LED_response\2023_07_14_LED_responses.csv")
data = pd.read_csv(r"P:\research\experiments\QCM\data\2023_04_13_LIM_O3_4BBA\2023_04_17_LIM_O3_photo.csv")
data = pd.read_csv(r"P:\research\experiments\QCM\data\2023_05_31_LIM_O3_RH\2023_05_31_LIM_O3_StartDry.csv")


time_hours = data['Relative_time'].to_numpy()/3600
frequency = data['Resonance_Frequency'].to_numpy()
temperature = data['Temperature'].to_numpy()
sample_mass = 80
sense_factor = 30

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


print("Max: ",np.log10(max(np.abs(d2fdt2[np.where(np.isinf(d2fdt2)==False)]))))
print("Mean: ",np.log10(np.abs(d2fdt2[np.where((np.isnan(d2fdt2)==False) & (np.isinf(d2fdt2)==False))]).mean()))


max_change = max(np.abs(d2fdt2[np.where(np.isinf(d2fdt2)==False)]))
mean_d2fdt2 = np.abs(d2fdt2[np.where((np.isnan(d2fdt2)==False) & (np.isinf(d2fdt2)==False))]).mean()
for i in range(1,len(time_hours)-10):
    if d2fdt2[i] > max_change/100:
        dfdt[i] = dfdt[i]/1e4
        dfdt[i+1] = dfdt[i+1]/1e4
        dfdt[i+2] = dfdt[i+2]/1e4
        dfdt[i+3] = dfdt[i+3]/1e4
        dfdt[i+4] = dfdt[i+4]/1e4
        dfdt[i+5] = dfdt[i+5]/1e4
        dfdt[i+6] = dfdt[i+6]/1e4
        dfdt[i+7] = dfdt[i+7]/1e4
        dfdt[i+8] = dfdt[i+8]/1e4
    if d2fdt2[i] < -max_change/100:
        dfdt[i] = dfdt[i]/1e4
        dfdt[i+1] = dfdt[i+1]/1e4
        dfdt[i+2] = dfdt[i+2]/1e4
        dfdt[i+3] = dfdt[i+3]/1e4
        dfdt[i+4] = dfdt[i+4]/1e4
        dfdt[i+5] = dfdt[i+5]/1e4
        dfdt[i+6] = dfdt[i+6]/1e4
        dfdt[i+7] = dfdt[i+7]/1e4
        dfdt[i+8] = dfdt[i+8]/1e4

mlr = (1/sense_factor)*dfdt
fmlr = mlr/sample_mass


plt.plot(time_hours,fmlr)
#plt.plot(time_hours,d2fdt2/1000,c='r')
plt.ylim(0,1.5)
#plt.xlim(0,0.7)
plt.show()

