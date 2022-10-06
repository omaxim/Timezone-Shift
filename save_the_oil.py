import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

controlable = ['Biomass  - Actual Aggregated [MW]',
    'Fossil Brown coal/Lignite  - Actual Aggregated [MW]',
    'Fossil Coal-derived gas  - Actual Aggregated [MW]',
    'Fossil Gas  - Actual Aggregated [MW]',
    'Fossil Hard coal  - Actual Aggregated [MW]',
    'Fossil Oil  - Actual Aggregated [MW]',
    'Fossil Oil shale  - Actual Aggregated [MW]',
    'Fossil Peat  - Actual Aggregated [MW]',
    'Hydro Pumped Storage  - Actual Aggregated [MW]',
    'Hydro Pumped Storage  - Actual Consumption [MW]',
    'Hydro Water Reservoir  - Actual Aggregated [MW]',
    'Nuclear  - Actual Aggregated [MW]',
    'Waste  - Actual Aggregated [MW]'
]

uncontrolable = [
    'Geothermal  - Actual Aggregated [MW]',
    'Hydro Run-of-river and poundage  - Actual Aggregated [MW]',
    'Marine  - Actual Aggregated [MW]',
    'Other  - Actual Aggregated [MW]',
    'Other renewable  - Actual Aggregated [MW]',
    'Solar  - Actual Aggregated [MW]',
    'Wind Offshore  - Actual Aggregated [MW]',                         
    'Wind Onshore  - Actual Aggregated [MW]'
]

countries_datafiles = glob.glob('countries/*')
dataframes = []

for file in countries_datafiles:
  df = pd.read_csv(file, )
  dataframes.append(df)

num_countries = 32
#num_countries = 1
for i in range(num_countries):
    df = dataframes[i]
    countryname = str(df['Area'][0])
    df = df.replace('n/e', 0.0)

    print(countryname)
    print('\n\n')
    print(df.head())

    hours_in_day = 24
    days_in_year = 365

    num_samples_in_hour = round(len(df.index) / days_in_year / hours_in_day)
    print(num_samples_in_hour)

    n = round(len(df.index) / days_in_year)
    print(n)

    df = df.groupby(df.index // num_samples_in_hour).sum()

    # I take 0, 24, 48, 72, 96 ...
    # I take 1, 25, 49, 73, 97 ...
        # I take 2, 26, 50, 74, 98 ...

    result = []

    winter_period = 60 # first 2 months: jan, feb
    for i in range(hours_in_day):
        end = winter_period * hours_in_day + i
        # grab every 24'th row and take the mean of it
        result.append(df.iloc[i:end:hours_in_day, :].mean())

    
    for i in range(hours_in_day):
        result[i] = result[i].to_frame().transpose()


    result_df = result[0]
    result = result[1:]
    for res in result:
        result_df = pd.concat([result_df, res])

    print(result_df.head())

    controlable_sum = 0.0
    for column in controlable:
        if column in result_df.columns:
            controlable_sum = controlable_sum + result_df[column]
  
    uncontrolable_sum = 0.0 
    for column in uncontrolable:
        if column in result_df.columns:
            uncontrolable_sum = uncontrolable_sum + result_df[column]


    fig, ax = plt.subplots(figsize=(18, 8))
    hours_x = np.arange(24)
    ax.plot(hours_x, controlable_sum, label='controlable sources')
    ax.plot(hours_x, uncontrolable_sum, label='uncontrolable sources')
    ax.plot(hours_x, uncontrolable_sum + controlable_sum, label='total')
    ax.set_xbound(0, 23)
    ax.set_ybound(0)
    ax.set_xticks(np.arange(0, 24, step=1))


    savearray = np.array([hours_x,controlable_sum,uncontrolable_sum])
    np.save("Consumption_data/" + str(countryname)+".npy",savearray)

    ax.set(xlabel='Day-time (h)', ylabel='Energy usage (MWh)',
       title='Winter energy consumption during the day in '+ str(countryname))
    ax.grid()
    ax.legend()
    plt.show()



# %%
# we want to average by the hour over the period (of winter)


# for each column I want to add every n'th row for 60 days and then div by 60
# n = num_rows / 365
# granularity = n / 24
# then we should add up n + granularity rows i.e.

# for each column
#   for row in range(0, num_rows, n)
#     for time_step in range(granularity)


