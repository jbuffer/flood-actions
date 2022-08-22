import requests
import pandas as pd
import numpy as np
from datetime import datetime

def get_data():
    '''create a dataframe from
    the flood api call'''
    dict_temp = {}
    data = []

    url = 'http://environment.data.gov.uk/flood-monitoring/id/floods'

    r = requests.get(url)
    if r.status_code == 200:
        print('Success')
        r = r.json()
        for i in range(len(r['items'])):
            print(r.keys)
            dict_temp['date'] = datetime.today()
            dict_temp['data_status'] = 'Data available'
            dict_temp['flood_area_id']= r['items'][i]['floodAreaID']
            dict_temp['county'] = r['items'][i]['floodArea']['county']
            dict_temp['severity'] = r['items'][i]['severity']
            dict_temp['severity_level'] = r['items'][i]['severityLevel']
            dict_temp['time_changed'] = r['items'][i]['timeSeverityChanged']
            dict_temp['flood_id'] = r['items'][i]['floodArea']['@id']
            dict_temp['polygon_url'] = r['items'][i]['floodArea']['polygon']
            dict_temp['riverorsea'] = r['items'][i]['floodArea']['riverOrSea']
            data.append(dict_temp)
        df = pd.DataFrame.from_dict(data)
    else:
        print('Cannot connect to server')
    
    if df.empty:
        df = pd.DataFrame({
                'date': datetime.today(),
                'data_status': 'No Flood Data',
                'flood_area_id': np.nan,
                'county': np.nan,
                'severity': np.nan,
                'severity_level': np.nan,
                'time_changed': np.nan,
                'flood_id': np.nan,
                'polygon_url': np.nan,
                'riverorsea': np.nan
                },
                index=[0])
    return (df)

def get_polys(df):
    '''take dataframe created 
    by `get_data` function and 
    append additional columns'''
    df['lat'] = np.nan
    df['long'] = np.nan
    df['coords'] = np.nan
    df['description']= np.nan
    df['CTY19NM'] = np.nan
    if df['flood_area_id'].hasnans==False:
        for i in range(len(df['polygon_url'])):
            if i % 10 == 0:
                print('{} of {} urls processed.\r'.format(i, len(df)))
            r2 = requests.get(df['polygon_url'].iloc[i]).json()
            df['long'].iloc[i] = r2['features'][0]['geometry']['coordinates'][0][0][i][0]
            df['lat'].iloc[i] = r2['features'][0]['geometry']['coordinates'][0][0][i][1]

            r3 = requests.get(df['polygon_url'].iloc[i]).json()
            df['description'].iloc[i] =r3['features'][0]['properties']['DESCRIP']
            df['CTY19NM'].iloc[i] = r3['features'][0]['properties']['LA_NAME']
    else:
        print('No new records')
    return(df)

# return dataframe derived from functions
df = get_data()
df = get_polys(df)

# read in data and append
df_historical = pd.read_csv('data/flood-data.csv')
df_historical = pd.concat([df_historical,df])
df_historical['date'] = pd.to_datetime(df_historical['date'])
df_historical.sort_values('date', ascending=False, inplace=True)
df_historical.drop_duplicates(inplace=True)

# save updated file 
df_historical.to_csv('data/flood-data.csv', index = False)