#----------Package + function imports
import numpy as np
from math import pi
import pandas as pd
import os.path
from wordcloud import WordCloud, STOPWORDS
import custom_funcs

from bokeh.io import show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.io import output_notebook

import matplotlib as mpl
import matplotlib.pyplot as plt
'''
    Author: Roy Jara
    Edited by Xu Zhu
'''

#------------------------Importing Data---------------------------------
# define path name depending on location of data
df = pd.read_csv('all-citations.csv')
essential_df = df[['Make', 'Color', 'Violation Description','Violation code', 'Fine amount']].copy().dropna()

#------------------Word Cloud--------------------------------------------

def Wcloud():
    description_data = custom_funcs.split_count(essential_df['Violation Description'])
    description_dictio = description_data['count'].to_dict()
    wordcloud = WordCloud(
                              width = 1400,
                              height = 700,
                              background_color='white',
                              scale = 2,
                              min_font_size=10,
                              relative_scaling = 0.4
                             ).generate_from_frequencies(description_dictio)
    fig = plt.figure(1)
    plt.tight_layout(pad=0)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
#---------------------------Plot of pie charts--------------------------------
# Data to make pie chart for colors:
def pie_color():
    color_data_to_plot = essential_df['Color'].dropna()
    color_data_to_plot = custom_funcs.split_count(color_data_to_plot)
    color_data_to_plot = custom_funcs.group_top_and_other(color_data_to_plot, 12)
    white2 = color_data_to_plot.loc['WH']
    color_data_to_plot = color_data_to_plot.drop(['WH'])
    color_data_to_plot.loc['WT'] += white2
    color_data_to_plot = color_data_to_plot.sort_values(by = 'count', axis = 0)
    color_codes = list(color_data_to_plot.index)
    color_hex = {'BK':'#000000','WT':'#FFFFFF', 'GY':'#808080', 'SL':'#C0C0C0', 'BL':'#00008B',
                 'RD':'#FF0000', 'GN':'#2E8B57', 'WH':'#FFFFFF', 'BN':'#654321', 'GO':'#ffd700',
                 'MR':'#800000', 'SI':'#708090', 'Other':'#FFB6C1', 'TN':'#D2B48C'}

    color_names = {'BK':'Black','WT':'White', 'GY':'Grey', 'SL':'Silver', 'BL':'Blue',
                   'RD':'Red', 'GN':'Green', 'WH':'White2', 'BN':'Brown', 'GO':'Gold',
                   'MR':'Maroon', 'Other':'Other', 'TN':'Tan', 'BG':'Beige'}
    
    list_of_col_hex = [color_hex[i] for i in color_codes]
    list_of_col_names = [color_names[i] for i in color_codes]
    values = []
    for i in range(color_data_to_plot.size):
        values.append(int(color_data_to_plot.iloc[i]))
    x = dict(zip(list_of_col_names, values))

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'Color'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = list_of_col_hex
    data['percentage'] = data['value']/data['value'].sum()*100
    data['percentage'] = data['percentage'].round(2)

    p = figure(plot_width = 1600, plot_height=1200, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@Color: @value",x_range=(-0.7, 0.8))

    p.title.text = 'Car Colors and Infractions'
    p.title.text_font_size = '40pt'
    p.wedge(x=0, y=1, radius=0.5,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), name ='percentage',
            line_color="grey", fill_color='color', legend='Color', source=data)
    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    p.legend.label_text_font_size = '28pt'
    show(p)

#-------------------------------------------------------------------------
#Pie chart for 'make':
#clean and organize data
def pie_make():
    make_data_to_plot = essential_df['Make'].dropna()
    make_data_to_plot = custom_funcs.split_count(make_data_to_plot)
    make_data_to_plot = custom_funcs.group_top_and_other(make_data_to_plot, 20)
    make_data_to_plot = make_data_to_plot.sort_values(by = 'count', axis = 0)
    make_codes = list(make_data_to_plot.index)
    make_names = {'ACUR':'Acura','INFI':'Infinity','CHRY':'Chrysler', 'GMC':'GMC', 'MAZD':'Mazda', 'AUDI':'Audi',
                  'KIA':'KIA', 'JEEP':'Jeep', 'DODG':'Dodge', 'LEXS':'Lexus', 'HYUN':'Hyundai',
                  'VOLK':'Volkswagen', 'MERZ':'Mercedes-Benz', 'BMW':'BMW', 'CHEV':'Chevrolet',
                  'NISS':'Nissan', 'FORD':'Ford', 'HOND':'Honda', 'TOYT':'Toyota','OTHR':'Other','Other':'Other'}
    list_of_make_names = [make_names[i] for i in make_codes]
    values = []
    for i in range(make_data_to_plot.size):
        values.append(int(make_data_to_plot.iloc[i]))
    y = dict(zip(list_of_make_names, values))
#---------make figure, plot and save:
    data = pd.Series(y).reset_index(name='value').rename(columns={'index':'Make'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(y)]
    data['percentage'] = data['value']/data['value'].sum()*100
    data['percentage'] = data['percentage'].round(2)
    
    p = figure(plot_width = 1600, plot_height=1200, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@Make: @value", x_range=(-0.7, 0.9))
    p.title.text = 'Brands and Citations'
    p.title.text_font_size = '40pt'
    p.wedge(x=0, y=1, radius=0.5,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="grey", fill_color='color', legend='Make', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    p.legend.label_text_font_size = '28pt'
    show(p)
#------------------------------------------------------
# Separate brands into luxury vs non luxury and compare citation numbers
brand_level = {'luxury':['ACUR', 'BMW', 'MBNZ', 'MASE', 'PONT', 'TESL','INFI', 'CADI',
                         'BUIC', 'LINC', 'LEXU','AUDI', 'MERZ', 'BENZ','JAGR', 'PORS',
                         'TSMR', 'LEXS', 'JAGU', 'LROV', 'RROV','LNDR','BENT', 'ROL',
                         'HUMM','FERR','BUGA', 'ASTO','RANG','LAMO','MENZ','ALFA','MUST',
                         'LAND','LRVR','ROS', 'ROV','ROVE','PORC'],
               'non-luxury': ['HOND', 'GMC', 'NISS', 'CHEV','MAZD','TOYO', 'FORD', 'CHRY',
                              'STRN','HYUN', 'DODG', 'SUBA','MERC', 'SCIO', 'KIA','MITS',
                              'VOLK','JEEP','VOLV','SATU','SUZU','FIAT','TOYT','SAA','ISU',
                              'SUZI','SMRT', 'DATS', 'DAEW','ACC', 'MINI', 'ISUZ','BOUN',
                              'IND','VW', 'SAAB','MH','DAT', 'SMAR','MIDA','MITZ','SUB',
                              'MER', 'EGLE','DAIH', 'EAGL'],
               'trucks/busses': ['PTRB','FREI','KW', 'HINO','MACK','HNO','NEOP','FLGH',
                                 'IVEC','GILL','FRTL'],
               'misc':['LIND','OLDS','MNNI','UNK','CHEC','OTHR','STLG','PLYM','HD','INTL',
                       'JENS','UNK','ESTB','KAWK','GEO','TRIU','YAMA','GRUM','FSKR','MERK',
                       'HARL','SABU','WNBG', 'KAWA','DUES','HYTR','COOP','CNQS','AURO',
                       'LIEB','WHIT','UTIL','ZERO','SWMD','PRRO','THT','STU','WABA','AMER',
                       'FBAL', 'FLGH','IVEC','BRHM','BUDR', 'LNCI', 'FIRE', 'VANS','IRAC',
                       'TRLR', 'SPCN', 'WRAN', 'FLEX','STOU','SUV','EXPL','LOOK','INTE',
                       'APR','VN','CROS','CIMC','LODC','AUBU','DORS','LASE', 'CHNK','WNBN',
                       'APPL']}

def percent():
    list_brands = list(essential_df['Make'].dropna().unique())
    
# Get ratios for percentage of infractions being 'No park/street clean'/total # of infractions
# for each car group:
    split_brand_levels = custom_funcs.split_count(essential_df['Make'].dropna())
    all_lux = int(split_brand_levels.loc[brand_level['luxury']].sum())
    all_nlux = int(split_brand_levels.reindex(brand_level['non-luxury']).sum())
    all_truck = int(split_brand_levels.reindex(brand_level['trucks/busses']).sum())
    all_misc = int(split_brand_levels.reindex(brand_level['misc']).sum())
    no_park_df = essential_df[essential_df['Violation Description']=='NO PARK/STREET CLEAN']
    split_brand_levels_nopark = custom_funcs.split_count(no_park_df['Make'].dropna())
    nopark_lux = int(split_brand_levels_nopark.reindex(brand_level['luxury']).sum())
    nopark_nlux = int(split_brand_levels_nopark.reindex(brand_level['non-luxury']).sum())
    nopark_truck = int(split_brand_levels_nopark.reindex(brand_level['trucks/busses']).sum())
    nopark_misc = int(split_brand_levels_nopark.reindex(brand_level['misc']).sum())

    ratios_nopark = {'Luxury Brands':float(nopark_lux/all_lux)*100,
                     'Non-Luxury Brands': float(nopark_nlux/all_nlux)*100,
                     'Truck/Bus Brands':float(nopark_truck/all_truck)*100,
                     'Misc. Brand Names':float(nopark_misc/all_misc)*100}
#plot bar chart w above information:
    fig1 = plt.figure(num=None, figsize=(8, 6), dpi=120, facecolor='w', edgecolor='k')
    plt.bar(range(len(ratios_nopark)), list(ratios_nopark.values()), align='center', color='xkcd:sky blue')
    plt.xticks(range(len(ratios_nopark)), list(ratios_nopark.keys()))
    plt.xlabel('Type of Vehicle')
    plt.ylabel('Percentages')
    plt.title('Percentage of Violations that are \n"No Park/Street Clean"')
    plt.show()

# -------------------------------------------------
# now add bool columns to dataframe to identify location of types of brands (lux, non-lux, etc)
def money():
    essential_df['lux?'] = essential_df['Make'].isin(brand_level['luxury'])
    essential_df['non-lux?'] = essential_df['Make'].isin(brand_level['non-luxury'])
    essential_df['truck?'] = essential_df['Make'].isin(brand_level['trucks/busses'])
    essential_df['misc?'] = essential_df['Make'].isin(brand_level['misc'])
# add up money for each group and gather the data together
    tot_money_lux = essential_df.loc[essential_df['lux?'] == True]['Fine amount'].sum()
    tot_money_nonlux = essential_df.loc[essential_df['non-lux?'] == True]['Fine amount'].sum()
    tot_money_truckbus = essential_df.loc[essential_df['truck?'] == True]['Fine amount'].sum()
    tot_money_misc = essential_df.loc[essential_df['misc?'] == True]['Fine amount'].sum()
    
    money_dict = {'Luxury Brands':tot_money_lux/1000000,
                  'Non-Luxury Brands':tot_money_nonlux/1000000,
                  'Truck/Bus Brands':tot_money_truckbus/1000000,
                  'Misc. Brand Names':tot_money_misc/1000000}
# plot:
    fig2 = plt.figure(num=None, figsize=(8, 6), dpi=120, facecolor='w', edgecolor='k')
    plt.bar(range(len(money_dict)), list(money_dict.values()), align='center', color='xkcd:blue')
    plt.xticks(range(len(money_dict)), list(money_dict.keys()))
    plt.xlabel('Type of Vehicle')
    plt.ylabel('Money (in millions)')
    plt.title('Money spent per vehicle type')
    plt.show()
