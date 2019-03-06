import numpy as np
import pandas as pd



def devide_year(fpath, year, availcols):
    '''
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

if __name__ == "__main__":
    filepath = 'C:\\Users\\XZ\\ECE143Proj\\parking-citations.csv'
    availcols = ['Issue Date', 'Issue time', 'RP State Plate', 'Make', 'Body Style',
             'Color', 'Violation Description', 'Fine amount', 'Latitude', 'Longitude']
    devide_year(filepath, '2015', availcols)
    devide_year(filepath, '2016', availcols)
    devide_year(filepath, '2017', availcols)
    devide_year(filepath, '2018', availcols)
           
    
