import datetime
import numpy as np
import pandas as pd

def na_count_per_column(d):
    tmp_d = d.apply(lambda x: x.isna().sum(), axis='rows')
    tmp_d = tmp_d.to_frame().reset_index()
    tmp_d.columns = ['colname', 'na_count']
    return tmp_d

def drop_unique_value_column(d):
    _d = d.apply(lambda x: len(x.unique()), axis='rows')
    _d = pd.DataFrame(_d).reset_index()
    _d.columns = ['colname', 'n_unique']
    _cn = list(_d[_d.n_unique == 1]['colname'])
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