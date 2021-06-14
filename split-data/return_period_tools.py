import numpy as np
import pandas as pd

def get_main_dir():
    return '/home/jmframe/frequency-analysis/'

def read_ri(ri_file, ris=None):
    with open(ri_file) as f:
        ri = pd.read_csv(f)
        if ris:
            ris = ['ri_'+str(i) for i in ris]
            ris.insert(0,'gauge_id')
            return(ri.loc[:,ris])
        else:
            return(ri)

#main_dir = '/att/nobackup/jframe/frequency-analysis/'
#ri_file = main_dir+"ri-calc.csv"
#print(read_ri(ri_file, [5,50]))


def read_b17(gauge_id: str):
    b17_dir = get_main_dir() + 'b17-out/txt/'
    file_path = b17_dir + gauge_id + '.txt'
    with open(file_path) as f:
        column_names = ['ri', 'p', 'q', 'q_high', 'q_low', 'delete1', 'delete2']
        ri = pd.read_csv(f, sep='\t', names=column_names, index_col=0)
        ri = ri.iloc[:,1]
        ri_low = ri[50.0]
        slope = (ri[100.0] - ri_low)/(100-50)
        ri[75.0] = ri_low + 25*slope
        ri[80.0] = ri_low + 30*slope
        ri[90.0] = ri_low + 40*slope
        ri[95.0] = ri_low + 45*slope
    return(ri.sort_values())

def read_peak_flows(gauge_id: str):
    peak_dir = get_main_dir() + 'usgs-peak/tight/'
    file_path = peak_dir + gauge_id + '.csv'
    with open(file_path) as f:
        peaks = pd.read_csv(f, header=None)
    return(peaks)

def gauge_id_str(gauge_id):
    return str(gauge_id).zfill(8)

def get_water_year(year, month):
    if month > 9:
        return(year+1)
    else:
        return(year)

def closest_value(value, df_index):
    min_diff = 1000000
    loc_diff = np.nan
    for i, r in enumerate(df_index):
        diff = np.abs(value-r)
        if diff < min_diff:
            min_diff = diff
            loc_diff = r
    return(loc_diff)

def mm_to_cfs(basin, mm):
    return(0)

def interpolate_ri(flow, b17):
    df = pd.DataFrame(b17)
    ris = list(df.index.values)
    for i in range(b17.shape[0]):
        if flow > df.iloc[i,0] and flow < df.iloc[i+1,0]:
            slope = (ris[i+1]-ris[i])/(df.iloc[i+1,0] - df.iloc[i,0])
            diff = flow - df.iloc[i,0]
            interpolated_value = ris[i] + diff * slope
            return(interpolated_value)

# Use neuralhydrology metrics instead
#def nse(obs, sim) -> float:
#
#    for i in range(obs.shape[0]):
#
#        denominator = ((obs - obs.mean())**2).sum()
#        numerator = ((sim - obs)**2).sum()
#    
#        value = 1 - numerator / denominator
#    
#        return float(value)
#
