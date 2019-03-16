import numpy as np
import pandas as pd

def split_count(x):
    '''
    Parameters:
        x (Series): is the column of interest
    Returns:
        out (Pandas DataFrame): dataframe with counts of items in x
    '''


    assert isinstance(x,pd.Series)

    dummy_dict = {}
    for i in x:

        try :
            dummy_dict[i] += 1
            # dummy_dict[value] +=1
        except KeyError:
            dummy_dict.update({i:1})
            # dummy_dict.update({value:1})
    out = pd.DataFrame.from_dict(dummy_dict, orient='index').rename(columns={0:'count'}).sort_values(by='count')
    return out


def group_top_and_other(df, num_entries = 6):
    '''
    Parameters:
        df (DataFrame): dataframe with counts (index are what has been counter)
                        ex. output of split_count.
        num_entries (int): how many independent entries do you want
    Returns:
        out (Pandas DaraFrame): same dataframe but the smallest only 8 entries are passed
                                rest are combined to an 'other' entry
    '''
    assert isinstance(df, pd.DataFrame)
    assert (num_entries > 0)
    df_entries = len(list(df.index))
    assert (df_entries >= num_entries)

    size_other = df_entries - num_entries
    other_indexes = list(df.index)[0:size_other]
    other_sum = int(sum(df.loc[other_indexes].values))
    new_df = df.iloc[size_other:]
    df2 = pd.Series({'count':other_sum})
    df2.name = 'Other'
    new_df = new_df.append(df2)
    new_df = new_df.sort_values(by = 'count', axis = 0)

    return new_df


def split_count2(x,instances, values):
    '''
    Parameters:
        x (df): is the df of interest
        instances(str): name of column to use for counts
        values(str): name of column to use as values
    Returns:
        out (Pandas DataFrame): dataframe with sum of values
    '''
    assert isinstance(x,pd.DataFrame)
    df = x[[instances,values]]
    length = df.shape[0]
    dummy_dict = {}
    for row in range(length):
        # print(df.loc[row][0])
        try :
            dummy_dict[df.loc[row][0]] += df.loc[row][1]
        except KeyError:
            dummy_dict.update({df.loc[row][0]:df.loc[row][1]})
    out = pd.DataFrame.from_dict(dummy_dict, orient='index').rename(columns={0:'count'}).sort_values(by='count')
    return out
