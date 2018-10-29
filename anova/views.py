from django.shortcuts import render

import pandas as pd
pd.set_option('display.max_columns', None)
from scipy import stats
import itertools
import math
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison

def anova(*args):
    F, p = stats.f_oneway(*args)
    return F,p

def read_excel(filename):
    df = pd.read_excel(filename).dropna()
    uniq_names = []
    for col_name in df.columns[2:]:
        uniq_names.append(col_name[:-2])
    uniq_names = list(set(uniq_names))
    dict_pos = dict.fromkeys(uniq_names)
    for uniq_name in uniq_names:
        tmp=[]
        for pos, col_name in enumerate(df.columns):
            if uniq_name+"#" in col_name:
                tmp.append(pos)
            dict_pos[uniq_name]=tmp
    speed,week,res = [],[],[]
    for i in range(df.shape[0]):
        a = []
        for uniq_name in dict_pos.keys():
            a.append(list(df.iloc[i,dict_pos.get(uniq_name)].values))
        F,p = anova(*a)
        week.append(df.iloc[i,0])
        speed.append(df.iloc[i,1])
        res.append(p)
    dfr = pd.DataFrame({"speed" : speed, "week" : week, "result" : res}, index = range(len(week)))
    dfr = dfr.pivot(index='speed', columns='week', values='result')
    dfr = dfr.round(4)
    return dfr, dict_pos, uniq_names, df
    # return dfr.to_html(), dict_pos, uniq_names, df

def create_dict(df, dfr, dict_pos, uniq_names):
    # create an uniq pairs
    pairs = list(itertools.permutations(uniq_names, 2))
    for k,v in enumerate(pairs):
        pairs[k] = list(v)
    tmp_pairs = pairs
    for pair in tmp_pairs:
        if pair[::-1] in pairs:
            del pairs[pairs.index(pair)]
    # create a dict with none values
    dict_positions = dict.fromkeys(dfr.columns.get_values())
    for column in dfr.columns:
        if len(dfr[dfr[column]<=0.05].index.get_values()) > 0:
            dict_positions[column]=dict.fromkeys(dfr[dfr[column]<=0.05].index.get_values())
        else:
            dict_positions.pop(column)
    for week in dict_positions.keys():
        for speed in dict_positions[week].keys():
            dict_positions[week][speed] = dict.fromkeys(uniq_names)
            for uname in dict_positions[week][speed]:
                tmp = df[(df['week'] == week) & (df['speed'] == speed)].get_values().squeeze()
                tmp_list = []
                for i in dict_pos[uname]:
                    tmp_list.append(tmp[i])
                dict_positions[week][speed][uname] = tmp_list
    return dict_positions, pairs

def t_test(df, dfr, dict_pos, uniq_names):
    dict_positions, pairs = create_dict(df, dfr, dict_pos, uniq_names)
    # create a pairs
    for week in dict_positions.keys():
        for speed in dict_positions[week].keys():
            for a,b in pairs:
                dict_positions[week][speed].setdefault(a+'#'+b,[dict_positions[week][speed][a],dict_positions[week][speed][b]])
    # Del not pairs
    for week in dict_positions.keys():
        for speed in dict_positions[week].keys():
            for name in uniq_names:
                dict_positions[week][speed].pop(name)
    #Evaluate t-test
    for week in dict_positions.keys():
        for speed in dict_positions[week].keys():
            for name in dict_positions[week][speed].keys():
                dict_positions[week][speed][name].append(stats.ttest_ind(dict_positions[week][speed][name][0],dict_positions[week][speed][name][1], equal_var = False))
    # remain only values p-value/statistics
    for week in dict_positions.keys():
        for speed in dict_positions[week].keys():
            for name in dict_positions[week][speed].keys():
                dict_positions[week][speed][name] = dict_positions[week][speed][name][2][1]
    newDF = pd.DataFrame() #creates a new dataframe that's empty
    for i in dict_positions.keys():
        newDF = newDF.append(pd.DataFrame.from_dict(dict_positions[i]).T, ignore_index=False)
    return newDF.round(3), len(pairs)

def tukeys(df, dfr, dict_pos, uniq_names):
    dict_positions, _ = create_dict(df, dfr, dict_pos, uniq_names)
    result = []
    for week in dict_positions.keys():
        for speed in dict_positions[week].keys():
            groups,b = [],[]
            for name in dict_positions[week][speed].keys():
                values = dict_positions[week][speed][name]
                names = [name for x in range(len(values))]
                groups.extend(names)
                b.extend(values)
            tmp = pairwise_tukeyhsd(endog=b, groups=groups,alpha=0.5)
            result.append(tmp)
    return result
