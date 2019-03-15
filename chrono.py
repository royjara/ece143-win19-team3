import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import calmap

pd.plotting.register_matplotlib_converters()
plt.rcParams['figure.figsize'] = (20.0, 15.0)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 16

def plot_num_avg(x_axis, xlab, num, numlab, avg, avglab, title, isweek = False):
    '''
    Line plot: x = x_axis y = num, avg
    xlab, numlab, avglab for label
    if isweek == True, x will be daynames of aweek
    x, y label fontsize = 20
    title fontsize = 24
    '''
    assert len(x_axis) == len(num) and len(x_axis) == len(avg) #check data length
    assert all(isinstance(x, str) for x in [xlab, numlab, avglab, title])
    
    dayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig = plt.figure()
    
    ax_num = fig.add_subplot(111)
    ln1 = ax_num.plot(x_axis, num, 'r--o', label='num')
    ax_num.set_xlabel(xlab, fontsize = 20)
    ax_num.set_ylabel(numlab, fontsize = 20)
    ax_num.set_title(title, fontsize = 24)
    ax_num.set_ylim([min(num)*0.95, max(num)*1.05])
    ax_num.yaxis.set_ticklabels(['1.8M', '1.9M', '2M', '2.1M', '2.2M', '2.3M'])

    ax_avg = ax_num.twinx()
    ln2 = ax_avg.plot(x_axis, avg, 'b--o', label='avg_fine')
    ax_avg.set_ylabel(avglab, fontsize = 20)
    ax_avg.set_ylim([65, 75])

    ln = ln1 + ln2
    labels = [l.get_label() for l in ln]
    ax_num.legend(ln, labels, loc = 0, fontsize = 16)

    #annotate
    for a,b in zip(x_axis, num):
        ax_num.annotate(str(b), xy=(a,b), xytext=(a-0.15, b*1.002), fontsize = 16)
    for a,b in zip(x_axis, avg):
        ax_avg.annotate(str("{:.2f}".format(b)), xy=(a,b), xytext=(a-0.1, b*1.002), fontsize = 16)

    if isweek == True:
        plt.xticks(x_axis, dayname)
    else:
        plt.xticks(x_axis)
    plt.show()

def plot_num(x_axis, xlab, num, numlab, title, isweek = False):
    '''
    Line plot: x = x_axis y = num
    xlab, numlab for label
    if isweek == True, x will be daynames of aweek
    x, y label fontsize = 20
    title fontsize = 24
    '''
    
    assert len(x_axis) == len(num) #check data length
    assert all(isinstance(x, str) for x in [xlab, numlab, title])
    
    dayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig = plt.figure()
    
    ax_num = fig.add_subplot(111)
    ln1 = ax_num.plot(x_axis, num, 'r--o', label='num')
    ax_num.set_xlabel(xlab, fontsize = 20)
    ax_num.set_ylabel(numlab, fontsize = 20)
    ax_num.set_title(title, fontsize = 24)
    ax_num.set_ylim([min(num)*0.95, max(num)*1.05])


    #annotate
    for a,b in zip(x_axis, num):
        ax_num.annotate(str(b), xy=(a,b), xytext=(a-0.05, b*1.008))

    if isweek == True:
        plt.xticks(x_axis, dayname)
    else:
        plt.xticks(x_axis)
    plt.show()



def num_year():
    '''
    Number and Average Fine versus Years
    x-axis: year in [2015, 2016, 2017, 2018]
    y-axis: num, fine amount
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
    Line chart: Number of citations over month in year [2015, 2016, 2017, 2018]
    x-axis: year in [2015, 2016, 2017, 2018]
    y-axis: num
    '''
    assert year in [2015, 2016, 2017, 2018, 'all']
    
    if year == 'all':
        df15 = pd.read_csv('2015parking-citations.csv', parse_dates = ['Issue Date'])
        gp15 = df15['Fine amount'].groupby(df15['Issue Date'].dt.month)
        df16 = pd.read_csv('2016parking-citations.csv', parse_dates = ['Issue Date'])
        gp16 = df16['Fine amount'].groupby(df16['Issue Date'].dt.month)
        df17 = pd.read_csv('2017parking-citations.csv', parse_dates = ['Issue Date'])
        gp17 = df17['Fine amount'].groupby(df17['Issue Date'].dt.month)
        df18 = pd.read_csv('2018parking-citations.csv', parse_dates = ['Issue Date'])
        gp18 = df18['Fine amount'].groupby(df18['Issue Date'].dt.month)

        x_axis = range(48)
        num = pd.concat([gp15.count(), gp16.count(), gp17.count(), gp18.count()], axis = 0, ignore_index = True)
               
        fig = plt.figure()
        ax_num = fig.add_subplot(111)
        ln1 = ax_num.plot(x_axis, num, 'r--o', label='num')
        ax_num.set_xlabel('Months', fontsize = 20)
        ax_num.set_ylabel('Number of Citations per Month', fontsize = 20)
        ax_num.set_title('Number of citations vs Month Overall', fontsize = 24)
        ax_num.set_ylim([min(num)*0.9, max(num)*1.05])
        ax_num.yaxis.set_ticklabels(['120K', '140K', '160K', '180K', '200K', '220K'])


        #annotate
        tag = []
        for a in range(2015, 2019):
            for b in range(1, 13):
                tag.append(str(a) + '.' + '{:0=2}'.format(b))
        for a in range(2,50,12):
            ax_num.annotate(tag[a] + '  ' + str(num[a]), xy=(a,num[a]), xytext=(a-4, num[a] + 6000), arrowprops=dict(arrowstyle='->', connectionstyle='arc3'), fontsize=15, color='black')
        for a in [10, 22, 34, 46]:
            ax_num.annotate(tag[a] + '  ' + str(num[a]), xy=(a,num[a]), xytext=(a-4, num[a] - 12000), arrowprops=dict(arrowstyle='->', connectionstyle='arc3'), fontsize=15, color='black')
        for a in [1, 25, 37]:
            ax_num.annotate(tag[a] + '  ' + str(num[a]), xy=(a,num[a]), xytext=(a, num[a] - 3000), arrowprops=dict(arrowstyle='->', connectionstyle='arc3'), fontsize=15, color='black')
        plt.xticks([])
        plt.show()
        
        
    else:
        df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
        gp = df['Fine amount'].groupby(df['Issue Date'].dt.month)
        #plot
        plot_num(x_axis = range(1,13), xlab = 'Months', num = gp.count(), numlab = 'Number of Citations per Month', title = str(year) + '  ' + 'Number of citations vs Month')

    
def num_weekday(month, year):
    '''
    Line plot
    '''
    assert month in range(1,13) or month == 'all'
    assert year in [2015, 2016, 2017, 2018]

    import calendar
    dayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    if month == 'all':
        gp = df['Fine amount'].groupby(df['Issue Date'].dt.weekday)
        plot_num(x_axis = range(7), xlab = 'Months', num = gp.count(), numlab = 'Number of Citations per Weekday', title = str(year) + '  ' + 'Number of Citations vs Weekday', isweek = True)
    else:
        gp = df.loc[df['Issue Date'].dt.month == month]['Fine amount'].groupby(df['Issue Date'].dt.weekday)
        plot_num(x_axis = range(7), xlab = 'Months', num = gp.count(), numlab = 'Number of Citations per Weekday', title = str(year) + ' ' + calendar.month_name[month]+ ' Number of Citations vs Month', isweek = True)

def dayofyear(year, month = [1,12]):
    '''
    Plot a line chart. Number of citations vs Date in a specific year 
    Input:
    year: year in [2015, 2016, 2017, 2018]
    '''
    
    assert year in [2015, 2016, 2017, 2018]
    assert isinstance(month, list)
    assert isinstance(month[0], int) and month[0] > 0
    assert isinstance(month[1], int) and month[1] < 13
    
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    df = df[df['Issue Date'].dt.month <= month[1]]
    df = df[df['Issue Date'].dt.month >= month[0]]
    gp = df['Fine amount'].groupby(df['Issue Date'])
    fig = plt.figure()
    x_axis = gp.count().index
    ax_num = fig.add_subplot(111)
    ax_num.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
    #ax_num.plot(x_axis, gp.count(), 'b-', label='num', linewidth = 0.5)
    ax_num.set_xlabel('Date', fontsize = 20)
    ax_num.set_ylabel('Number of Citations per Day', fontsize = 20)
    ax_num.set_title(str(year) + '  ' + 'Number of Citations vs Date', fontsize = 24)
    ax_num.set_ylim([min(gp.count())*0.5, max(gp.count())*1.15])

    #fill
    avg = gp.count().mean()
    plt.fill_between(x_axis, gp.count(), avg, where= gp.count() >= avg, facecolor = 'green', interpolate = True, alpha = 0.7)
    plt.fill_between(x_axis, gp.count(), avg, where= gp.count() <= avg, facecolor = 'red', interpolate = True, alpha = 0.7)

    #annotate
    plt.annotate('Max ' + str(gp.count().idxmax().to_pydatetime().date()) + '  ' + str(gp.count().max()), xy = (gp.count().idxmax(), gp.count().max()), xytext = (gp.count().idxmax() + pd.Timedelta(weeks = 2), gp.count().max()*1.05), arrowprops=dict(facecolor='steelblue', shrink=0.02), fontsize=15, color='black')
    plt.annotate('Min ' + str(gp.count().idxmin().to_pydatetime().date()) + '  ' + str(gp.count().min()), xy = (gp.count().idxmin(), gp.count().min()), xytext = (gp.count().idxmin() - pd.Timedelta(weeks = 6), gp.count().min()*1.00), arrowprops=dict(facecolor='steelblue', shrink=0.02), fontsize=15, color='black')
       
    plt.xticks(pd.date_range(x_axis[0], x_axis[-1], freq = 'M'), rotation = 0)
    plt.show()

def bar_month():
    '''
    Bar chart: x = month y = Number of Citations per Month each year
    y starts from 100000
    '''

    df15 = pd.read_csv('2015parking-citations.csv', parse_dates = ['Issue Date'])
    gp15 = df15['Fine amount'].groupby(df15['Issue Date'].dt.month)
    df16 = pd.read_csv('2016parking-citations.csv', parse_dates = ['Issue Date'])
    gp16 = df16['Fine amount'].groupby(df16['Issue Date'].dt.month)
    df17 = pd.read_csv('2017parking-citations.csv', parse_dates = ['Issue Date'])
    gp17 = df17['Fine amount'].groupby(df17['Issue Date'].dt.month)
    df18 = pd.read_csv('2018parking-citations.csv', parse_dates = ['Issue Date'])
    gp18 = df18['Fine amount'].groupby(df18['Issue Date'].dt.month)


    x_axis = range(2,26,2)
    bar1 = plt.bar(x = [i - 0.15 for i in x_axis], height = gp15.count(), width = 0.3, color = 'red', label = '2015')
    bar2 = plt.bar(x = [i + 0.15 for i in x_axis], height = gp16.count(), width = 0.3, color = 'green', label = '2016')
    bar3 = plt.bar(x = [i + 0.45 for i in x_axis], height = gp17.count(), width = 0.3, color = 'pink', label = '2017')
    bar4 = plt.bar(x = [i + 0.75 for i in x_axis], height = gp18.count(), width = 0.3, color = 'purple', label = '2018')

    plt.ylabel('Number of Citations per Month', fontsize = 20)
    plt.xticks([i + 0.3 for i in x_axis], range(1,13))
    plt.xlabel('Month', fontsize = 20)
    plt.title('Number of Citations vs Month in Each Year', fontsize = 24)
    plt.ylim([120000, 220000])
    plt.legend()

    plt.show()

def timeofday(year):
    '''
    Line Chart: Citations over Period of Day(half an hour)
    '''
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    gp = df['Fine amount'].groupby(df['Issue time'])
    lbin = list(range(30, 2430,100)) + list(range(0, 2500, 100))
    lbin.sort()
    cut1 = pd.cut(df['Issue time'], lbin, right = False, include_lowest = True)
    num = cut1.value_counts(sort = False)
  
    fig = plt.figure()
    ax_num = fig.add_subplot(111)
    ln1 = ax_num.plot(range(48), num, 'r--o', label='num')
    ax_num.set_xlabel('Time Period of Day', fontsize = 20)
    ax_num.set_ylabel('Number of Citations', fontsize = 20)
    ax_num.set_title(str(year) + ' ' + 'Number of Citations vs Time Period of Day', fontsize = 24)
    ax_num.set_ylim([min(num)*0.95, max(num)*1.05])

    
    ax_num.annotate('8:00', xy=(16,num[800]), xytext=(12, num[800] - 6000), arrowprops=dict(arrowstyle='->', connectionstyle='arc3'), fontsize=15, color='black')
    ax_num.annotate('12:00', xy=(24,num[1200]), xytext=(26, num[1200] - 6000), arrowprops=dict(arrowstyle='->', connectionstyle='arc3'), fontsize=15, color='black')

    plt.xticks(range(0, 48, 6), [num.keys()[x] for x in range(0, 48, 6)], rotation = 0, fontsize = 14)
    plt.show()
    
def bar_date(year):
    '''
    Bar chart: Number of Citations via date
    '''
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    gp = df['Fine amount'].groupby(df['Issue Date'])

    x_axis = gp.count().index
    fig = plt.figure()
    ax_num = fig.add_subplot(111)
    ax_num.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
    
    ax_num.bar(x = gp.count().index, height = gp.count(), width = 1, color = 'red', label = str(year))
    ax_num.set_ylabel('Number of Citations per Month')
    ax_num.set_xlabel('Month')
    ax_num.set_title('Number of Citations vs Month in Each Year')
    plt.xticks(pd.date_range(x_axis[0], x_axis[-1], freq = 'M'), rotation = 45)
    plt.show()

def bar_date_top(year, top = 10, reverse = False):
    '''
    Bar chart: Plot top(or bottom) Number of Citations Date

    Input:
    year: which year of data to analyse
    top: number of data to be ploted
    reverse: choose top or bottom(top is False)

    '''
    
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    gp = df['Fine amount'].groupby(df['Issue Date'])
    num = gp.count().sort_values(ascending = reverse)[:top]
    x_axis = range(top)
    
    fig = plt.figure()
    
    ax_num = fig.add_subplot(111)
    ax_num.bar(x = x_axis, height = num, width = 0.8, color = 'red', label = str(year))
    ax_num.set_ylabel('Number of Citations per Day', fontsize = 20)
    if reverse == False:
        ax_num.set_title(str(year) + ' Most Amounts of Citations Date', fontsize = 24)
    else:
        ax_num.set_title(str(year) + ' Least Amounts of Citations Date', fontsize = 24)

    for a,b in zip(x_axis, num):
        ax_num.text(a, b+1, num.index[a].to_pydatetime().strftime("%a") + ', ' + str(b), ha="center", va="bottom", fontsize = 15)
    plt.ylim([0,num.max()*1.3])
    plt.xticks(x_axis,[str(x.to_pydatetime().date()) for x in num.index],rotation = 45, fontsize = 14)
    plt.savefig('')
    plt.show()

def calheatmap(year):
    '''
    Plot a Calendar heat map. Number of citations vs Date in a specific year 
    Input:
    year: year in [2015, 2016, 2017, 2018]
    '''
    
    assert year in [2015, 2016, 2017, 2018]
    
    df = pd.read_csv(str(year)+'parking-citations.csv', parse_dates = ['Issue Date'])
    gp = df['Fine amount'].groupby(df['Issue Date'])
    calmap.calendarplot(gp.count(), fig_kws = {'figsize':(16,10)}, yearlabels = False, subplot_kws = {'title':'Number of Citations in Year ' + str(year)})
    plt.show()
    
if __name__ == "__main__":
    #num_year()
    #dayofyear(2015, [1,4])
    #dayofyear(2016, [1,12])
    #dayofyear(2017, [1,12])
    #dayofyear(2018, [1,4])
    #num_month(2015)
    #num_month(2016)
    #num_month(2017)
    #num_month(2018)
    #num_month('all')
    #bar_month()
    #num_weekday('all', 2015)
    #num_weekday('all', 2016)
    #bar_date_top(year = 2015, top = 10, reverse = False)
    #bar_date_top(year = 2015, top = 10, reverse = True)
    #timeofday(2015)
    #timeofday(2016)
    #timeofday(2017)
    timeofday(2018)
    #calheatmap(2018)
