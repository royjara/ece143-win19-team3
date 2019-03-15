import numpy as np
import pandas as pd
import pyproj
'''
    Split big dataset to several csv by year.
    Author: Xu Zhu

'''



def split_year(fpath, year, availcols):
    '''
    Resave raw data into csv by Issue Year
    '''
    loop = True
    rfile = pd.read_csv(fpath, usecols = availcols, iterator=True)
    empty_df = pd.DataFrame(columns = availcols)
    empty_df.to_csv(year + 'parking-citations.csv', mode = 'w', header = True) #initialize, write a header
    while loop:
        try:
            sel = []
            chunk = rfile.get_chunk(100000)
            for row in range(len(chunk)):
                if isinstance(chunk.iloc[row,0], str) and len(chunk.iloc[row,0]) == 19:
                    if chunk.iloc[row,0][0:4] == year:
                        sel = sel + [row]
            if len(sel) > 0:
                chunk.iloc[sel].to_csv(year + 'parking-citations.csv', mode = 'a', header = False)
        except StopIteration:
            loop = False
    print(year + 'parking-citations finished')

def convert_position():
    '''
    Convert the coordinate into universal Latitude and Longitude
    '''
    for year in [2015, 2016, 2017, 2018]:
        df=pd.read_csv(str(year) + 'parking-citations.csv', parse_dates = ['Issue Date'])
        df=df[~df['Latitude'].isin([99999])]
        ESRI102645=pyproj.Proj("+proj=lcc +lat_1=34.03333333333333 +lat_2=35.46666666666667 +lat_0=33.5 +lon_0=-118 +x_0=2000000 +y_0=500000.0000000002 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",preserve_units = True)
        WGS84=pyproj.Proj("+init=EPSG:4326")
        x,y=df['Latitude'],df['Longitude']
        df['Longitude_WGS'],df['Latitude_WGS']=pyproj.transform(ESRI102645, WGS84, np.array(x), np.array(y))
        df = df[df['Latitude_WGS'] > 33]
        df.to_csv(str(year) + 'gmaps.csv', mode = 'w', header = True, columns = ['Fine amount', 'Longitude_WGS', 'Latitude_WGS', 'Issue Date'])
    print('Convert done!')

if __name__ == "__main__":
    filepath = 'parking-citations.csv'
    availcols = ['Issue Date', 'Issue time', 'RP State Plate', 'Make', 'Body Style',
             'Color', 'Violation Description', 'Fine amount', 'Latitude', 'Longitude']
    #split_year(filepath, '2015', availcols)
    #split_year(filepath, '2016', availcols)
    #split_year(filepath, '2017', availcols)
    #split_year(filepath, '2018', availcols)
    convert_position()
           
    
