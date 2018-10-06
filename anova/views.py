from django.shortcuts import render

import pandas as pd
pd.set_option('display.max_columns', None)
from scipy import stats


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
    dfr = dfr.pivot(index='week', columns='speed', values='result')
    return dfr.to_html()

# def read_excel(filename):
#     return pd.read_excel(filename).dropna()
#
# def find_uniq_names(data):
#     uniq_names = []
#     for col_name in data:
#         uniq_names.append(col_name[:-2])
#     return list(set(uniq_names))
#
# def find_positions(uniq_names):
#     dict_pos = dict.fromkeys(uniq_names)
#     for uniq_name in uniq_names:
#         tmp=[]
#         for pos, col_name in enumerate(df.columns):
#             if uniq_name+"#" in col_name:
#                 tmp.append(pos)
#             dict_pos[uniq_name]=tmp
#     return dict_pos
#
# def create_result(df):
#     speed = []
#     week = []
#     res = []
#     for i in range(df.shape[0]):
#         a = []
#         for uniq_name in dict_pos.keys():
#             a.append(list(df.iloc[i,dict_pos.get(uniq_name)].values))
#         F,p = anova(*a)
#         week.append(df.iloc[i,0])
#         speed.append(df.iloc[i,1])
#         res.append(F)
#
#     dfr = pd.DataFrame({"speed" : speed, "week" : week, "result" : res}, index = range(len(week)))
#     dfr = dfr.pivot(index='week', columns='speed', values='result')
#     return dfr
