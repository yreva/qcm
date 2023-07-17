import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


data = pd.read_csv(r"P:\research\experiments\QCM\data\2023_07_12_LED_response\2023_07_14_LED_responses.csv")

time_hours = data['Relative_time'].to_numpy()/3600
frequency = data['Resonance_Frequency'].to_numpy()
temperature = data['Temperature'].to_numpy()

frequency_1st_derivative = np.empty(len(frequency))
for i in range(1,len(frequency)-1):
    frequency_1st_derivative[i] = (frequency[i+1] - frequency[i-1]) / (time_hours[i+1] - time_hours[i-1])


gs_kw = dict(width_ratios=[1],height_ratios=[1,2.5])
fig1, ax1 = plt.subplots(2,1,gridspec_kw=gs_kw,sharex=True)


ax1[0].plot(time_hours,(frequency-frequency[0]),lw=2,c='#0f0f0f')
ax1[0].set_ylim(50,250)

ax1[1].plot(time_hours,(frequency-frequency[0]),lw=2,c='#0f0f0f')
ax1[1].set_ylim(-1,34)

# hide the spines between ax and ax1[1]
ax1[0].spines.bottom.set_visible(False)
ax1[1].spines.top.set_visible(False)
ax1[0].xaxis.tick_top()
ax1[0].tick_params(labeltop=False)  # don't put tick labels at the top
ax1[1].xaxis.tick_bottom()

d = .5  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=8,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1[0].plot([0, 1], [0, 0], transform=ax1[0].transAxes, **kwargs)
ax1[1].plot([0, 1], [1, 1], transform=ax1[1].transAxes, **kwargs)


ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>0.09) & (time_hours<0.175),
    color='#5928ed',
    alpha=0.3)

ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>0.26) & (time_hours<0.356),
    color='#5928ed',
    alpha=0.15)

ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>0.522) & (time_hours<0.594),
    color='#2546f0',
    alpha=0.3)

ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>0.661) & (time_hours<0.736),
    color='#2546f0',
    alpha=0.15)

ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>0.846) & (time_hours<0.982),
    color='#0073e6',
    alpha=0.3)

ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>1.04) & (time_hours<1.138),
    color='#0073e6',
    alpha=0.15)

ax1[0].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>1.202) & (time_hours<1.28),
    color='#00b4c5',
    alpha=0.3)
ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>1.202) & (time_hours<1.28),
    color='#00b4c5',
    alpha=0.3)

ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>1.324) & (time_hours<1.393),
    color='#00b4c5',
    alpha=0.15)

ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>1.425) & (time_hours<1.45),
    color='#00bf7d',
    alpha=0.3)

ax1[1].fill_between(
    x=time_hours,
    y1=(frequency-frequency[0]),
    y2=-2,
    where=(time_hours>1.51) & (time_hours<1.519),
    color='r',
    alpha=0.3)


# Set axes parameters
ax1[1].set_ylabel('$\Delta f$ / Hz',fontsize=14)
ax1[1].set_xlabel('time / hours',fontsize=14)
ax1[0].tick_params(labelsize=14)
ax1[1].tick_params(labelsize=14)

# Add color legend for LEDS
custom_lines = [Line2D([0], [0], color='#5928ed', alpha=0.3, lw=4),
                Line2D([0], [0], color='#2546f0', alpha=0.3, lw=4),
                Line2D([0], [0], color='#0073e6', alpha=0.3, lw=4),
                Line2D([0], [0], color='#00b4c5', alpha=0.3, lw=4),
                Line2D([0], [0], color='#00bf7d', alpha=0.3, lw=4),
                Line2D([0], [0], color='r', alpha=0.3, lw=4)]

ax1[0].legend(custom_lines,['285 nm','300 nm','340 nm','400 nm','532 nm','633 nm'],fontsize=12,loc=0,ncol=2,edgecolor='none')

plt.tight_layout()
plt.subplots_adjust(hspace=0.03)

plt.savefig('QCM_LED_response.png',dpi=700)
plt.show()
