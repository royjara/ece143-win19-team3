import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import pyproj
from uszipcode import Zipcode
import gmaps
from collections import Counter


'''
    Author: Yeqing Huang
    Geographical Analysis
    Func:
    MedianHousehold()
    PopulationDensity()
    heatmap_all()
    street()
    hl_street
    
    Edit and Modified by Xu Zhu 3/15
'''

gmaps.configure(api_key='AIzaSyBCkXSNL58obNihjx6WUR5zqQUZYBcFP0E')
los_angeles_coordinates = (34.0522, -118.2437)


def MedianHousehold():
    df = pd.read_csv('parking-citations-extended.csv')
    df = df[df['Number of Parking Citations'] < 150000]
    sns.set_style('white')
    gridobj = sns.lmplot(x = 'Median Household Income', y = 'Number of Parking Citations', data = df)

def PopulationDensity():
    df = pd.read_csv('parking-citations-extended.csv')
    df = df[df['Number of Parking Citations'] < 150000]
    sns.set_style('white')
    gridobj = sns.lmplot(x = 'Population Density', y = 'Number of Parking Citations', data = df)

def heatmap_all():
    '''
    plot the heatmap of all citation place
    '''
    df=pd.read_csv('parking-citations-processed.csv',usecols=['Latitude_WGS', 'Longitude_WGS'],low_memory=True)
    locations = df[['Latitude_WGS','Longitude_WGS']]
    locations=locations.groupby(['Latitude_WGS','Longitude_WGS'])
    freq=df.groupby(['Latitude_WGS','Longitude_WGS']).size().reset_index(name='freq')
    locations=freq[['Latitude_WGS','Longitude_WGS']]
    fig=gmaps.figure(center=los_angeles_coordinates, zoom_level=11)
    fig.add_layer(gmaps.heatmap_layer(locations,weights=freq['freq']))
    fig.add_layer(gmaps.traffic_layer())
    return fig

def street():
    '''
    Which streets have the most parking citations
    Generate a horizontal bar plot
    '''
    df=pd.read_csv('parking-citations-processed.csv',usecols=['Latitude_WGS', 'Longitude_WGS','Street Name'],low_memory=True)
    freq=df.groupby(['Street Name']).size().reset_index(name='freq').sort_values(by=['freq'],ascending=False)
    most_streetslist=list(freq['Street Name'])[0:20]
    ypos=np.arange(len(most_streetslist))
    fig, ax = plt.subplots(figsize=(20,15))
    ax.barh(ypos,freq['freq'][0:20])
    ax.set_yticks(ypos)
    ax.set_yticklabels(most_streetslist)
    ax.invert_yaxis()
    ax.yaxis.set_tick_params(labelsize=18)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.set_xlim(left=1e4,auto=True)
    ax.set_title('Streets with the most parking citations',size=30)
    for i, v in enumerate(freq['freq'][0:20]):
        ax.text(v + 500, i+0.1 , str(v), color='black', fontweight='bold',size=20)
    plt.show()

def hl_street():
    '''
    highlight streets with the most parking citations on Google map
    '''
    df=pd.read_csv('parking-citations-processed.csv',usecols=['Latitude_WGS', 'Longitude_WGS','Street Name'],low_memory=True)
    freq=df.groupby(['Street Name']).size().reset_index(name='freq').sort_values(by=['freq'],ascending=False)
    most_streetslist=list(freq['Street Name'])[0:20]
    freq=df.groupby(['Street Name','Latitude_WGS','Longitude_WGS']).size().reset_index(name='freq').sort_values(by=['freq'],ascending=False)
    freq=freq.set_index('Street Name')
    most_streetpoint=freq.loc[most_streetslist]
    most_points=list(zip(list(most_streetpoint['Latitude_WGS']),list(most_streetpoint['Longitude_WGS'])))
    most_points=list(set(most_points))

    fig=gmaps.figure(center=los_angeles_coordinates, zoom_level=12)

    most = gmaps.symbol_layer(most_points[::20],fill_color='blue', stroke_color='blue', scale=3,stroke_opacity=0)
    fig.add_layer(most)
    # fig.add_layer(gmaps.traffic_layer())
    return(fig)

