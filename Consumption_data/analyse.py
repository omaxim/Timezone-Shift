import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt

countries = glob.glob('*.npy')
controlable_data = {countries[i][-7:-5]:np.load(countries[i])[1,:] for i in range(len(countries))}
uncontrolable_data = {countries[i][-7:-5]:np.load(countries[i])[2,:] for i in range(len(countries))}


controlable = pd.DataFrame(controlable_data)
uncontrolable = pd.DataFrame(uncontrolable_data)

#plt.plot(controlable.sum(axis=1)+uncontrolable.sum(axis=1))
#plt.plot(controlable['AT']+uncontrolable['AT'])
austria = np.load('Austria (AT).npy')
plt.plot(austria[1,:]+austria[2,:])
#plt.plot(uncontrolable.sum(axis=1))
plt.show()
print(controlable)
