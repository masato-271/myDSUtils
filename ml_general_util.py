import datetime
import numpy as np
import pandas as pd

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