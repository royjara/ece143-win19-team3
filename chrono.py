import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

pd.plotting.register_matplotlib_converters()

def plot_num_avg(x_axis, xlab, num, numlab, avg, avglab, title, isweek = False):
    '''
    lab for label
    '''
    dayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig = plt.figure()
    
    ax_num = fig.add_subplot(111)
    ln1 = ax_num.plot(x_axis, num, 'r--o', label='num')
    ax_num.set_xlabel(xlab)
    ax_num.set_ylabel(numlab)
    ax_num.set_title(title)
    ax_num.set_ylim([min(num)*0.95, max(num)*1.05])

    ax_avg = ax_num.twinx()
    ln2 = ax_avg.plot(x_axis, avg, 'b--o', label='avg_fine')
    ax_avg.set_ylabel(avglab)
    ax_avg.set_ylim([65, 75])

    ln = ln1 + ln2
    labels = [l.get_label() for l in ln]
    ax_num.legend(ln, labels, loc = 0)

    #annotate
    for a,b in zip(x_axis, num):
        ax_num.annotate(str(b), xy=(a,b), xytext=(a-0.05, b*1.0015))
    for a,b in zip(x_axis, avg):
        ax_avg.annotate(str("{:.2f}".format(b)), xy=(a,b), xytext=(a-0.03, b*1.0015))

    if isweek == True:
        plt.xticks(x_axis, dayname)
    else:
        plt.xticks(x_axis)
    plt.show()

def plot_num(x_axis, xlab, num, numlab, title, isweek = False):
    '''
    lab for label
    '''
    dayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig = plt.figure()
    
    ax_num = fig.add_subplot(111)
    ln1 = ax_num.plot(x_axis, num, 'r--o', label='num')
    ax_num.set_xlabel(xlab)
    ax_num.set_ylabel(numlab)
    ax_num.set_title(title)
    ax_num.set_ylim([min(num)*0.95, max(num)*1.05])


    #annotate
    for a,b in zip(x_axis, num):
        ax_num.annotate(str(b), xy=(a,b), xytext=(a-0.05, b*1.0015))

    if isweek == True:
        plt.xticks(x_axis, dayname)
    else:
        plt.xticks(x_axis)
    plt.show()



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
    plot_num_avg(x_axis = years, xlab = 'Years', num = num, numlab = 'Number of Citations per Year', avg = avg_fine, avglab = 'Average Fine Amount', title = 'Num. and Avg. Fine vs Year')

def num_month(year):
    '''
    '''
    assert year in [2015, 2016, 2017, 2018]
    
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])

    gp = df['Fine amount'].groupby(df['Issue Date'].dt.month)
    print(gp.count())
    print(gp.mean())

    #plot
    plot_num_avg(x_axis = range(1,13), xlab = 'Months', num = gp.count(), numlab = 'Number of Citations per Month', avg = gp.mean(), avglab = 'Average Fine Amount', title = str(year) + '  ' + 'Num. and Avg. Fine vs Month')
    

def num_weekday(month, year):
    assert month in range(1,13) or month == 'all'
    assert year in [2015, 2016, 2017, 2018]

    import calendar
    dayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    if month == 'all':
        gp = df['Fine amount'].groupby(df['Issue Date'].dt.weekday)
        plot_num(x_axis = range(7), xlab = 'Months', num = gp.count(), numlab = 'Number of Citations per Weekday', title = str(year) + '  ' + 'Number of Fine vs Weekday', isweek = True)
    else:
        gp = df.loc[df['Issue Date'].dt.month == month]['Fine amount'].groupby(df['Issue Date'].dt.weekday)
        plot_num(x_axis = range(7), xlab = 'Months', num = gp.count(), numlab = 'Number of Citations per Weekday', title = str(year) + ' ' + calendar.month_name[month]+ ' Number of Fine vs Month', isweek = True)

def dayofyear(year):
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    gp = df['Fine amount'].groupby(df['Issue Date'])
    print(gp)
    fig = plt.figure()
    x_axis = gp.count().index
    ax_num = fig.add_subplot(111)
    ax_num.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
    ax_num.plot(x_axis, gp.count(), 'r-', label='num')
    ax_num.set_xlabel('Date')
    ax_num.set_ylabel('Number of Citations per Day')
    ax_num.set_title(str(year) + '  ' + 'Number of Citations vs Date')
    ax_num.set_ylim([min(gp.count())*0.95, max(gp.count())*1.2])


    plt.xticks(pd.date_range(x_axis[0], x_axis[-1], freq = 'M'), rotation = 45)
    plt.show()

def bar_month():

    df15 = pd.read_csv('2015parking-citations.csv', parse_dates = ['Issue Date'])
    gp15 = df15['Fine amount'].groupby(df15['Issue Date'].dt.month)
    df16 = pd.read_csv('2016parking-citations.csv', parse_dates = ['Issue Date'])
    gp16 = df16['Fine amount'].groupby(df16['Issue Date'].dt.month)
    df17 = pd.read_csv('2017parking-citations.csv', parse_dates = ['Issue Date'])
    gp17 = df17['Fine amount'].groupby(df17['Issue Date'].dt.month)
    df18 = pd.read_csv('2018parking-citations.csv', parse_dates = ['Issue Date'])
    gp18 = df18['Fine amount'].groupby(df18['Issue Date'].dt.month)


    x_axis = range(2,26,2)
    bar1 = plt.bar(x = [i - 0.1 for i in x_axis], height = gp15.count(), width = 0.2, color = 'red', label = '2015')
    bar2 = plt.bar(x = [i + 0.1 for i in x_axis], height = gp16.count(), width = 0.2, color = 'green', label = '2016')
    bar3 = plt.bar(x = [i + 0.3 for i in x_axis], height = gp17.count(), width = 0.2, color = 'pink', label = '2017')
    bar4 = plt.bar(x = [i + 0.5 for i in x_axis], height = gp18.count(), width = 0.2, color = 'purple', label = '2018')

    plt.ylabel('Number of Citations per Month')
    plt.xticks([i + 0.2 for i in x_axis], range(1,13))
    plt.xlabel('Month')
    plt.title('Number of Citations vs Month in Each Year')
    plt.legend()

    plt.show()
    
    
if __name__ == "__main__":
    bar_month()
        

