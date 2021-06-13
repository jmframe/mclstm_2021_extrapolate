import numpy as np
import pandas as pd
import tools
import pickle

with open(tools.get_main_dir()+'ri-calc.csv') as f:
    df = pd.read_csv(f)

split_years={}
n_train_years_list = []
n_test_years_list = []
train_dates = {}
val_dates = {}
test_dates = {}

for basin in df.gauge_id:
    basin_str = tools.gauge_id_str(basin)
    train_dates[basin_str] = {'start_dates':[], 'end_dates':[]}
    val_dates[basin_str] = {'start_dates':[], 'end_dates':[]}
    test_dates[basin_str] = {'start_dates':[], 'end_dates':[]}
#    print(basin_str)

    ri = tools.read_b17(basin_str)
#    print(ri)

    peakflows = tools.read_peak_flows(basin_str)

    low_flow_cutoff = tools.closest_value(1.1,ri.index.values)

    # Loop through the peaks, and assign the years to either test or train
    split_years[basin_str] = {'test':[], 'val':[], 'train':[]}

    for pf in range(peakflows.shape[0]):

        # Don't include years before 1980
        if int(str(np.array(peakflows.iloc[pf,:])[0]).split('-')[0]) < 1980:
            continue

         #  some of the early months/days are not known, so are input as zero!!!
         #  Just put a month/day so the the water year is the provided calendar year.
        try:
            date_of_peak = pd.to_datetime(np.array(peakflows.iloc[pf,:])[0])
        except:
            if str(np.array(peakflows.iloc[pf,:])[0]).split('-')[1] == '00':
                if str(np.array(peakflows.iloc[pf,:])[0]).split('-')[2] == '00':
                    date_of_peak = pd.to_datetime(str(np.array(peakflows.iloc[pf,:])[0]).split('-')[0]+'-12-31')

        annual_peak = np.array(peakflows.iloc[pf,:])[1]
        
        water_year_of_peak = tools.get_water_year(date_of_peak.year, date_of_peak.month)

        # Now split up the years into train (25-75)
        try:   ### Annual Peak might be NaN or some other non-numeric. So skip...
            if annual_peak < ri[5.0]:
                split_years[basin_str]['train'].append(water_year_of_peak)
        except:
            continue
        
        try:
            if annual_peak >= ri.loc[5] or annual_peak < ri[25.0]:
                split_years[basin_str]['val'].append(water_year_of_peak)
        except:
            continue

        try:
            if annual_peak >= ri[25.0]:
                split_years[basin_str]['test'].append(water_year_of_peak)
        except:
            continue

        # We need to go through both the train and test sets
        # and remove years that cannot maintain a 1 year gap.
        # For instance, we can not train 1980 and test 1981
        for i in split_years[basin_str]['train']:
            if i-1 in split_years[basin_str]['test']:
               split_years[basin_str]['train'].remove(i)
        for i in split_years[basin_str]['test']:
            if i-1 in split_years[basin_str]['train']:
               split_years[basin_str]['test'].remove(i)

    for i in split_years[basin_str]['train']:
        train_dates[basin_str]['start_dates'].append(pd.to_datetime('01/10/{}'.format(i)))
        train_dates[basin_str]['end_dates'].append(pd.to_datetime('30/09/{}'.format(i)))
    for i in split_years[basin_str]['test']:
        test_dates[basin_str]['start_dates'].append(pd.to_datetime('01/10/{}'.format(i)))
        test_dates[basin_str]['end_dates'].append(pd.to_datetime('30/09/{}'.format(i)))
    for i in split_years[basin_str]['val']:
        val_dates[basin_str]['start_dates'].append(pd.to_datetime('01/10/{}'.format(i)))
        val_dates[basin_str]['end_dates'].append(pd.to_datetime('30/09/{}'.format(i)))

    n_train_years_list.append(len(split_years[basin_str]['train']))
    print('Number of train_years', len(split_years[basin_str]['train']))
    print('Train_years', split_years[basin_str]['train'])
    n_test_years_list.append(len(split_years[basin_str]['test']))
    print('Number of test_years', len(split_years[basin_str]['test']))
    print('Test_years', split_years[basin_str]['test'])

print('average number of train years',np.nanmean(n_train_years_list))
print('average number of test years',np.nanmean(n_test_years_list))

with open('per_basin_train_periods_file.plk', 'wb') as fb:
    pickle.dump(train_dates, fb, protocol=pickle.HIGHEST_PROTOCOL)
with open('per_basin_test_periods_file.plk', 'wb') as fb:
    pickle.dump(test_dates, fb, protocol=pickle.HIGHEST_PROTOCOL)
with open('per_basin_val_periods_file.plk', 'wb') as fb:
    pickle.dump(val_dates, fb, protocol=pickle.HIGHEST_PROTOCOL)

