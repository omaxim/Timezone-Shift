import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt

countries = glob.glob('*.npy')
country_names = [countries[i][-7:-5] for i in range(len(countries))]

controlable_data = {country_names[i]:np.load(countries[i])[1,:] for i in range(len(countries))}
uncontrolable_data = {country_names[i]:np.load(countries[i])[2,:] for i in range(len(countries))}

controlable = pd.DataFrame(controlable_data)/1000 # in GW
uncontrolable = pd.DataFrame(uncontrolable_data)/1000 # in GW

time_shift_dict = {'MK':0, 'FR':-1, 'SE':0, 'UK':-1, 'FI':0, 'RS':0, 'AT':0, 'IT':0, 'NO':0, 'RO':0, 'DE':0, 'NL':-1, 'ME':0, 'CZ':0, 'LV':0, 'CH':0, 'PT':-1, 'BE':-1, 'IE':-1, 'SI':0, 'SK':0, 'ES':-1, 'PL':0, 'EE':0, 'LT':0, 'HR':0, 'GR':-1, 'HU':0, 'DK':0, 'BG':0, 'BA':0}

hours_in_day = 24
fig, ax = plt.subplots(figsize=(9, 7))
hours_x = np.arange(hours_in_day)
#ax.plot(hours_x, controlable.sum(axis=1), label='controlable sources before')
#ax.plot(hours_x, uncontrolable.sum(axis=1), label='uncontrolable sources')

total_before = uncontrolable.sum(axis=1) + controlable.sum(axis=1)
for country, time_shift in time_shift_dict.items():
    # this if statement is kinda reduntant
    # if country in controlable.columns:
    controlable[country] = controlable[country].reindex(index=np.roll(controlable[country].index, time_shift))
    controlable[country] = np.roll(controlable[country], time_shift)
total_after = uncontrolable.sum(axis=1) + controlable.sum(axis=1)

#ax.plot(hours_x, controlable.sum(axis=1), label='controlable sources after')
ax.plot(hours_x, total_before, label='total before')
ax.plot(hours_x, total_after, label='total after')
ax.set_xbound(0, hours_in_day - 1)
ax.set_xticks(np.arange(0, hours_in_day, step=1))


ax.set(xlabel='Time [Hours]', ylabel='Net Generation (MW)',
       title='Winter energy production during the day in Europe')
ax.grid()
ax.legend(loc=2)
ax2 = ax.twinx()
ax2.plot(hours_x,100*(total_after/total_before-1),label = 'percentage change',color='grey',alpha=0.5,linewidth=3)
ax2.legend(loc=1)

plt.tight_layout()
plt.show()

