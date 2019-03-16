import pandas as pd
import numpy as np
import gmaps
from IPython.display import display
import time

'''
    Author: Xu Zhu
    Animation of gmaps
'''

gmaps.configure(api_key='AIzaSyBCkXSNL58obNihjx6WUR5zqQUZYBcFP0E')

#a class of Heatmap Animation
class HeatmapAnimation(object):
    
    def __init__(self, datasets, weights):
        self._datasets = datasets
        self._weights = weights
        self._figure = gmaps.figure(center = (34.0522, -118.2437), zoom_level = 11)
        self._current_index = 0
        self._heatmap = gmaps.heatmap_layer(datasets[self._current_index], weights = weights[self._current_index])
        self._figure.add_layer(self._heatmap)
        
    def render(self):
        return display(self._figure)
    
    def start_animation(self):
        while True:
            self._current_index = (self._current_index + 1) % len(self._datasets)
            self._render_current_dataset()
            time.sleep(1)
    
    def _render_current_dataset(self):
        self._heatmap.locations = self._datasets[self._current_index] # update the locations drawn on the heatmap

def weekdata(year):

    datasets = []
    weights = []
    assert year in [2015, 2016, 2017, 2018]
    df = pd.read_csv(str(year) + 'gmaps.csv', parse_dates = ['Issue Date'])
    gp = df[['Latitude_WGS','Longitude_WGS','Fine amount']].groupby(df['Issue Date'].dt.weekday)
    for i in range(7):
        day = gp.get_group(i)
        location = day.groupby(['Latitude_WGS','Longitude_WGS']).count()
        datasets.append(list(location.index))
        weights.append(np.concatenate(location.values.tolist()))
    return (datasets, weights)

def showfig(datasets, weights, weekday):
    '''
    '''
    assert weekday in range(7)
    fig = gmaps.figure(center = (34.0522, -118.2437), zoom_level=11)
    fig.add_layer(gmaps.heatmap_layer(datasets[weekday], weights = weights[weekday]))
    return fig
    
