import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def num_year():
    '''
    '''
    years = [2015, 2016, 2017, 2018]
    num = []
    avg_fine = []
    for year in years:
        df = pd.read_csv(str(year)+'parking-citations.csv')
        num.append(len(df))
        avg_fine.append(df.loc[:,'Fine amount'].mean())
    #plot
    fig = plt.figure()
    
    ax_num = fig.add_subplot(111)
    ax_num.plot(years, num, 'r--o', label='num')
    ax_num.set_xlabel('Years')
    ax_num.set_ylabel('Number of Citations each year')
    ax_num.set_title('Num. and Avg. Fine vs Year')
    ax_num.set_ylim([min(num)-10000, max(num)+10000])

    ax_avg = ax_num.twinx()
    ax_avg.plot(years, avg_fine, 'b--o', label='avg_fine')
    ax_avg.set_ylabel('Average Fine Amount')
    ax_avg.set_ylim([65, 75])

    #annotate
    for a,b in zip(years, num):
        ax_num.annotate(str(b), xy=(a,b), xytext=(a-0.05, b+5000))
    for a,b in zip(years, avg_fine):
        ax_avg.annotate(str("{:.2f}".format(b)), xy=(a,b), xytext=(a-0.03, b+0.1))

    plt.xticks(years)
    plt.show()    
    print(num)
    print(avg_fine)

def num_month(year):
    '''
    '''
    assert year in [2015, 2016, 2017, 2018]
    
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    print(df['Issue Date'][0])

    gp = df['Fine amount'].groupby(df['Issue Date'].dt.month)
    print(gp.count())
    print(gp.mean())
    
    

if __name__ == "__main__":
    num_month(2015)
        

