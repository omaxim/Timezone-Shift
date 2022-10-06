import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt

countries = glob.glob('*.npy')
controlable_data = {countries[i][-7:-5]:np.load(countries[i])[1,:] for i in range(len(countries))}
uncontrolable_data = {countries[i][-7:-5]:np.load(countries[i])[2,:] for i in range(len(countries))}

print([countries[i][-7:-5] for i in range(len(countries))])

controlable = pd.DataFrame(controlable_data)/1000
uncontrolable = pd.DataFrame(uncontrolable_data)/1000

time_shift = {'MK':0, 'FR':-1, 'SE':0, 'UK':-1, 'FI':0, 'RS':0, 'AT':0, 'IT':0, 'NO':0, 'RO':0, 'DE':0, 'NL':-1, 'ME':0, 'CZ':0, 'LV':0, 'CH':0, 'PT':-1, 'BE':-1, 'IE':-1, 'SI':0, 'SK':0, 'ES':-1, 'PL':0, 'EE':0, 'LT':0, 'HR':0, 'GR':-1, 'HU':0, 'DK':0, 'BG':0, 'BA':0}

plt.plot(controlable.sum(axis=1)+uncontrolable.sum(axis=1))
#plt.plot(controlable['AT']+uncontrolable['AT'])
#austria = np.load('Austria (AT).npy')
#plt.plot(austria[1,:]+austria[2,:])
#plt.plot(uncontrolable.sum(axis=1))
plt.show()
print(controlable)
