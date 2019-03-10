#!/Users/rjara/anaconda3/bin/python

#----------Package + function imports
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# import seaborn as sns
# from scipy import stats

import os.path
from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

import plotly
plotly.tools.set_credentials_file(username='rjara224', api_key='ch7E3BaYLVKVYNmTLX1m')
import plotly.plotly as py
import plotly.graph_objs as go

from past_assignments import split_count

#------------------------Importing Data---------------------------------
# change path name for global use
fullpath = '/Users/rjara/Dropbox/UCSD/Classes/ECE/143/project/parking-citations.csv'
cleanedpath = '/Users/rjara/Dropbox/UCSD/Classes/ECE/143/project/cleaned_data.csv'

if os.path.isfile(cleanedpath) :
    df=pd.read_csv(cleanedpath,nrows=400, low_memory=True)
else :
    df=pd.read_csv(fullpath,nrows=400, low_memory=True)

new_df = df[['Issue Date', 'RP State Plate', 'Plate Expiry Date', 'Make', 'Body Style', 'Color', 'Location', 'Violation code', 'Violation Description', 'Fine amount']].copy()
essential_df = df[['Make', 'Body Style', 'Color', 'Violation Description']].copy()

#------------------Word Cloud--------------------------------------------
#show wordcloud? Change value to True
show_wordcloud = False

# Show Word Cloud
if show_wordcloud :
    mpl.rcParams['font.size']=12                #10
    mpl.rcParams['savefig.dpi']=100             #72
    mpl.rcParams['figure.subplot.bottom']=.1

    stopwords = set(STOPWORDS)
    data = essential_df

    wordcloud = WordCloud(
                              background_color='white',
                              stopwords=stopwords,
                              max_words=200,
                              max_font_size=40,
                              random_state=42
                             ).generate(str(data['Violation Description']))

    print(wordcloud)
    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    fig.savefig("word1.png", dpi=900)

#---------------------------Plot of pie charts--------------------------------
# First color, then (make, body style, location)

# Goes from df to counts of entries of a specific column
color_data_to_plot = essential_df.iloc[:,2]
color_data_to_plot = color_data_to_plot.dropna()
color_data_to_plot = split_count(color_data_to_plot)

# Separate Series data:     labels = colors, values = counts
labels = list(color_data_to_plot.index)
values = []
for i in range(color_data_to_plot.size):
    values.append(int(color_data_to_plot.iloc[i]))

# Make graph object with values/labels
trace = go.Pie(labels=labels, values=values)
# Plot pie chart using plotly
py.iplot([trace], filename='basic_pie_chart')

# works Fine ---- Check plot in: https://plot.ly/~rjara224/0

# Next steps;
#       1) make interactive widget to select the data to plot in pie chart
#       2) Add dictionary to translate two letters to full color names
#       3) Match name color with actual color of in pie chart
