import pandas as pd
import numpy as np
import os
import scipy
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import random
from matplotlib import ticker

def Smoothy(y,width,ends):
    w = int(round(width))
    L = len(y)
    SumPoints = sum(y[1:w])
    out = np.zeros(L)
    halfw = int(round(w/2))
    
    for i in range(L-w-1):
        out[i+halfw-1] = SumPoints
        SumPoints = SumPoints - y[i]
        SumPoints = SumPoints + y[i+w]
    out[i+halfw] = sum(y[L-w:L-1])
    out = out / w
    if ends == 1:
        stpt = round((width+1)/2)
        out[0] = (y[0] + y[1]) / 2
        for i in range(2,stpt-1):
            out[i] = np.mean(y[0:(2*i-1)])
            out[L-i] = np.mean(y[L-2*i+1:L-1])
        out[L-1] = (y[L-1]+y[L-2]) / 2

    return out

def tma(y,width,ends):
    return Smoothy(Smoothy(y,width,ends),width,ends)

def plot_style(ax):
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.set_xlim(xlm)
    plt.xlabel('irradiation time / hours',fontsize='large')
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)


# 2023 Inputs
#path = r"P:\research\experiments\QCM\data\2023_02_01_LIM_O3\2023_02_03_22C_failed.csv"
path = r"P:\research\experiments\QCM\data\2023_02_01_LIM_O3\2023_02_09_25C.csv"
path = r"P:\research\experiments\QCM\data\2023_02_17_aPIN_O3\20230217_Crystal1_23C.csv"
path = r"P:\research\experiments\QCM\data\2023_03_09_LIM_O3_NP\20230309_LIMO3_24DNP.csv"
path = r"P:\research\experiments\QCM\data\2023_03_09_LIM_O3_NP\20230310_LIMO3_2NP.csv"
path = r"P:\research\experiments\QCM\data\2023_03_09_LIM_O3_NP\20230312_LIMO3.csv"
path = r"P:\research\experiments\QCM\data\2023_03_14_LIM_O3_NP\2023_03_14_LIM_O3_24DNP.csv"
path = r"P:\research\experiments\QCM\data\2023_03_14_LIM_O3_NP\2023_03_14_LIM_O3_2NP.csv"
path = r"P:\research\experiments\QCM\data\2023_04_13_LIM_O3_4BBA\2023_04_14_LIM_O3_4BBA_photo.csv"
#path = r"P:\research\experiments\QCM\data\2023_04_13_LIM_O3_4BBA\2023_04_13_LIM_O3_4BBA_dark.csv"
path = r"P:\research\experiments\QCM\data\2023_04_13_LIM_O3_4BBA\2023_04_17_LIM_O3_photo.csv"
#path = r"P:\research\experiments\QCM\data\2023_04_13_LIM_O3_4BBA\2023_04_20_4BBA_photo.csv"
path = r"P:\research\experiments\QCM\data\2023_05_31_LIM_O3_RH\2023_05_31_LIM_O3_StartDry.csv"


z = [x for x in range(len(path)) if '\\' in path[x]][-1]
filename = path[z+1:len(path)].replace('.csv','')

soa_type = 'any'
filt_width = 1001
xlm = [-1,75]

data = pd.read_csv(os.path.normpath(path))
time_hr = (data.Relative_time.to_numpy()/3600)
mass = data.Mass.to_numpy()[0]     # Mass on the crystal in micrograms
freq = data.Resonance_Frequency.to_numpy()
temp = data.Temperature.to_numpy()
t_lights = data.t_lights.to_numpy()[0]
dissipation = data.Dissipation.to_numpy()
try: 
    f_cal = data.f_cal.to_numpy()[0]
    Cf = -(freq[0]-4.999e6)/mass
except: 
    Cf = 50

print(Cf)


filt_freq = signal.savgol_filter(freq,filt_width,3)
filt_diss = signal.savgol_filter(dissipation,filt_width,3)


dfreq = np.empty(len(freq))
ddiss = np.empty(len(dissipation))
for i in range(1,len(freq)-1):
    delta_t = (time_hr[i+1] - time_hr[i-1])
    if (delta_t<0.0005):
        delta_t = 1000
    dfreq[i] = (filt_freq[i+1] - filt_freq[i-1]) / delta_t
    ddiss[i] = (filt_diss[i+1] - filt_diss[i-1]) / delta_t
dfreq[-100:-1] = 'nan'
ddiss[-100:-1] = 'nan'


mlr = (1/Cf)*dfreq  # Mass loss rate in ug/hr
fmlr = mlr / mass   # Mass loss in 1/hr
#fmlr = signal.savgol_filter(fmlr,round(filt_width/2)+1,3)


lost_mass = np.zeros(len(freq))
pml = np.zeros(len(freq))
for i in range(1,len(freq)):
    delta_t = (time_hr[i] == time_hr[i-1])
    if delta_t < 0.005: delta_t = 0.001
    lost_mass[i] = lost_mass[i-1] + fmlr[i]*(time_hr[i] - time_hr[i-1])
    pml[i] = 100*lost_mass[i]


fig = plt.figure(figsize=(5,5.2))
fig.subplots_adjust(left=0.236,right=0.967,bottom=0.098,top=0.936,hspace=0.13)
ax1 = plt.subplot(311)
#plt.plot(time_hr-t_lights,np.ones(len(freq))*4998216*1e-6,linewidth=2.5,color='k',linestyle='dotted',label='Blank Crystal Frequency')
plt.plot(time_hr-t_lights,(freq-freq[0]),linewidth=2.5,color='#0e9e32')
#ax1.set_ylim(4.975e6,5e6)
plt.xticks(color='w')
plot_style(ax1)
plt.ylabel('frequency / MHz',fontsize='large')
ax1.legend(bbox_to_anchor=(0,1,1,0),edgecolor='none',loc='lower right',fontsize='large')
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.4f}"))

ax2 = plt.subplot(312)
line2, = plt.plot(time_hr-t_lights,fmlr,linewidth=2.5,color='#0e9e32')
plt.plot(time_hr-t_lights,fmlr*0,linewidth=1,color='k',linestyle='--')
ax2.set_xlim(xlm)
#ax2.set_ylim(-0.01,0.01)
plt.xticks(color='w')
plot_style(ax2)
plt.ylabel('FMLR / (1/hour)',fontsize='large')

ax4 = plt.subplot(313)
line4, = plt.plot(time_hr-t_lights,pml,linewidth=2.5,color='#0e9e32')
ax4.set_xlim(xlm)
#ax4.set_ylim(0,100)
plot_style(ax4)
plt.ylabel('% mass lost',fontsize='large')


plt.savefig(path.replace('.csv','.png'),dpi=600)
plt.show()



