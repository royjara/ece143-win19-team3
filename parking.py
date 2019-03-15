import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gmaps

'''
    Parking lots annotated in gmaps
    Author: Yifan Huang
    Edited and Modified by Xu Zhu in 3/15
'''

gmaps.configure(api_key='AIzaSyBCkXSNL58obNihjx6WUR5zqQUZYBcFP0E')
los_angeles_coordinates = (34.0522, -118.2437)


def clean_data(file_in):
    df=pd.read_csv(file_in,usecols=['X','Y','Zipcode','Lat','Lon','Type','Hours','HourlyCost','DailyCost','MonthlyCost','SpecialFeatures','Spaces'],low_memory=True)
    return df

def park():
    '''
    Annocate parking lots
    '''
    df=pd.read_csv('parking-citations-processed.csv',usecols=['Latitude_WGS', 'Longitude_WGS'],low_memory=True)
    dfmark=clean_data('City_Owned_Parking_Lots.csv')
    parking_locations = dfmark[['Y','X']].loc[:1e6]
    
    locationsh = df[['Latitude_WGS','Longitude_WGS']]
    locationsh=locationsh.groupby(['Latitude_WGS','Longitude_WGS'])
    freq1=df.groupby(['Latitude_WGS','Longitude_WGS']).size().reset_index(name='freq')
    locationsh=freq1[['Latitude_WGS','Longitude_WGS']]
    

    fig=gmaps.figure(center=los_angeles_coordinates, zoom_level=12)

    markers = gmaps.marker_layer(parking_locations)
    fig.add_layer(markers)
    fig.add_layer(gmaps.heatmap_layer(locationsh,weights=freq1['freq']))
    # fig.add_layer(gmaps.traffic_layer())
    return(fig)
