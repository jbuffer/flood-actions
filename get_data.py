from datetime import datetime
import numpy as np
import pandas as pd
import requests


def get_data():
    '''create a dataframe from
    the flood api call'''
    dict_temp = {}
    data = []

    url = 'http://environment.data.gov.uk/flood-monitoring/id/floods'

    r = requests.get(url)
    if r.status_code == 200:
        print('Successfully made the request')
        r = r.json()
        for i, value in enumerate(r['items']):
            dict_temp['date'] = datetime.today()
            dict_temp['data_status'] = 'Data available'
            dict_temp['flood_area_id'] = r['items'][i]['floodAreaID']
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
        # create empty dataframe
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

    # get further information from url
    poly_dict_temp = {}
    poly_data = []

    for i, value in enumerate(df['flood_area_id']):
        url = df['polygon_url'][i]
        if df['flood_area_id'][i] != np.nan:
            print('Flood area included')
            r_poly = requests.get(url).json()
            poly_dict_temp['coords'] = r_poly['features'][0]['geometry']
            poly_dict_temp['long'] = r_poly['features'][0]['geometry']['coordinates'][0][0][0][0] # noqaE501
            poly_dict_temp['lat'] = r_poly['features'][0]['geometry']['coordinates'][0][0][0][1] # noqaE501
            poly_dict_temp['description'] = r_poly['features'][0]['properties']['DESCRIP'] # noqaE501
            poly_dict_temp['CTY19NM'] = r_poly['features'][0]['properties']['LA_NAME'] # noqaE501
            poly_data.append(poly_dict_temp)           
        else:
            poly_dict_temp['coords'] = np.nan
            poly_dict_temp['long'] = np.nan
            poly_dict_temp['lat'] = np.nan
            poly_dict_temp['description'] = np.nan
            poly_dict_temp['CTY19NM'] = np.nan

            poly_data.append(poly_dict_temp)

    df_poly = pd.DataFrame.from_dict(poly_data)
    df_final = pd.concat([df, df_poly], axis=1)

    df_final.drop_duplicates(subset=['flood_area_id'], inplace=True)

    # read in data and append
    df_historical = pd.read_csv('data/flood-data.csv')
    df_historical = pd.concat([df_historical, df_final])
    df_historical['date'] = pd.to_datetime(df_historical['date'])
    df_historical.sort_values('date', ascending=False, inplace=True)
    # save updated file
    df_historical.to_csv('data/flood-data.csv', index=False)
    print('Updated dataset')


if __name__ == "__main__":
    get_data()
