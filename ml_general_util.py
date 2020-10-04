import datetime
import numpy as np
import pandas as pd
from myDSUtils.general_util import print_func_name

def na_count_per_column(d):
    tmp_d = d.apply(lambda x: x.isna().sum(), axis='rows')
    tmp_d = tmp_d.to_frame().reset_index()
    tmp_d.columns = ['colname', 'na_count']
    return tmp_d

def get_unique_value_count(d):
    _d = d.apply(lambda x: len(x.unique()), axis='rows').to_frame().reset_index()
    _d.columns = ['colname', 'n_unique']

    return _d

def drop_unique_value_column(d):
    _d = get_unique_value_count(d)
    _cn = list(_d.query('n_unique == 1'))
    if(len(_cn)>0):
        print('following column(s) drop')
        print(_cn)
        d.drop(_cn, axis='columns', inplace=True)

    return d

def get_now_str():
    str_now = datetime.datetime.now().strftime('%Y%m%d-%H%M')
    return str_now

def is_ipython_env():
    # ipython kernelをimportすると正しく判定できないので
    # Warningは無視する必要がある
    if 'get_ipython' not in globals():
        # Python shell
        return False
    env_name = get_ipython().__class__.__name__
    if env_name == 'TerminalInteractiveShell':
        # IPython shell
        return True
    # Jupyter Notebook
    return True

@print_func_name
def bind_data(d_train, d_test):
    d_test['y'] = -1
    d = d_train.append(d_test).reset_index(drop=True)
    return(d)

@print_func_name
def resplit_data(d):
    d_train = d[d['y'] >= 0].copy()
    d_test = d[d['y'] < 0].copy()
    return(d_train, d_test)

from pathlib import Path 
@print_func_name
def dump_processed_data(d_train: pd.DataFrame, d_valid: pd.DataFrame, d_test: pd.DataFrame, dir_intermediate_products=Path('./intermediate_products')):
    d_train.to_pickle(dir_intermediate_products / f'd_train.pkl')
    d_test.to_pickle(dir_intermediate_products / f'd_test.pkl')
    if d_valid.shape[0] > 0:
        d_valid.to_pickle(dir_intermediate_products / f'd_valid.pkl')

@print_func_name
def get_numeric_colnames(d):
    ret = [x for x in d.columns if pd.api.types.is_numeric_dtype(d[x])]
    return(ret)

@print_func_name
def get_categorical_colnames(d):
    ret = [x for x in d.columns if not pd.api.types.is_numeric_dtype(d[x])]
    return(ret)

from typing import List
@print_func_name
def add_agg_stats_cols(
    d, 
    grouping_key:List[str], 
    agg_targets:List[str], 
    agg_functions:List[str]
    ):
    for af in agg_functions:
        for at in agg_targets:
            tmp_colname = f"agg_{at}_{af}_groupby_{''.join(grouping_key)}"
            tmp_d = d.groupby(grouping_key)[[at]].agg(af)
            tmp_d.columns = [tmp_colname]
            d = d.merge(tmp_d, how='left', right_on=grouping_key)
    
    return(d)
