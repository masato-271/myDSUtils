import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
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
    _cn = list(_d.query('n_unique == 1').colname.values)
    if(len(_cn)>0):
        print('following column(s) drop')
        print(_cn)
        d.drop(_cn, axis='columns', inplace=True)
    else:
        _cn = None
    return(d, _cn)

def get_now_str():
    str_now = datetime.datetime.now().strftime('%Y%m%d-%H%M')
    print(f'now: {str_now}')
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
    d_train['data_type'] = 'train'
    d_test['data_type'] = 'test'
    # d_test[target_colname] = -1
    d = d_train.append(d_test).reset_index(drop=True).copy()
    return(d)

@print_func_name
def resplit_data(d):
    d_train = d[d['data_type']=='train'].drop('data_type', axis='columns').copy()
    d_test = d[d['data_type']=='test'].drop('data_type', axis='columns').copy()
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

    if type(agg_targets) == str:
        agg_targets = [agg_targets]
        
    tmp_d1 = d[d['data_type']=='train'].copy()
    for af in agg_functions:
        for at in agg_targets:
            tmp_colname = f"agg_{at}_{af}_groupby_{''.join(grouping_key)}"
            print(tmp_colname)
            tmp_d = tmp_d1.groupby(grouping_key)[[at]].agg(af)
            tmp_d.columns = [tmp_colname]
            d = d.merge(tmp_d, how='left', on=grouping_key)
    
    return(d)

@print_func_name
def get_top_diff_df(y, pred, n_sample=100, mode='head'):
    d = pd.DataFrame((y - pred).values, columns=['err'])
    d['abs_err'] = d['err'].abs()
    d['y'] = y.values
    d['pred'] = pred
    d.reset_index(inplace=True)
    if mode=='head':
        sampled_d = d.sort_values(['abs_err']).head(n_sample)
    else:
        sampled_d = d.sort_values(['abs_err']).tail(n_sample)

    return(sampled_d)

@print_func_name
def compare_pred_gt_plot(y, pred, fn='', log=''):
    plt.clf()
    f, ax = plt.subplots(figsize=(7,7))
    if log=='x':
        ax.set(xscale='log')
    elif log=='y':
        ax.set(yscale='log')
    elif log=='xy':
        ax.set(xscale='log', yscale='log')

    sns.histplot(y, binwidth=2, ax=ax, color='red')
    sns.histplot(pred, binwidth=2, ax=ax, color='blue')
    if fn != '':
        plt.savefig(f'./plot/{fn}.png')

@print_func_name
def make_flg_variable(d, target_col, find_str):
  d[f'{target_col}__flag_{find_str}'] = d[target_col].str.match(f'.*{find_str}.*').astype(int)
  return(d)

@print_func_name
def get_ix_order_df(d, n=1, value_mode='', order_mode='largest', exclude_colnames=['<base>']):
  # 各行毎にn番目に大きい要素の列番号を取得
  # 最大値が複数ある場合はすべてのカラム位置を返す
  if value_mode=='abs':
    tmp_d = d.abs()
  else:
    tmp_d = d

  if order_mode=='largest':
    df_ix = tmp_d.drop(exclude_colnames, errors='ignore', axis=1).apply(lambda x: np.where(x == x.nlargest(n).values[0])[0], axis=1)
  elif order_mode=='smallest':
    df_ix = tmp_d.drop(exclude_colnames, errors='ignore', axis=1).apply(lambda x: np.where(x == x.nsmallest(n).values[0])[0], axis=1)
  df_ix = df_ix.to_frame()
  df_ix.columns = ['ix']
  return(df_ix)

@print_func_name
def get_each_row_value_order(d):
    d_ix = d.apply(lambda x: np.argsort(x), axis=1)
    return(d_ix)

@print_func_name
def get_n_largest_valued_colname(d, n=1, value_mode=''):
  d_ix = get_ix_order_df(d, n=n, value_mode=value_mode)
  d_colnames = d_ix.apply(lambda x: list(d.columns[x]), axis=1)
  return(d_colnames)

@print_func_name
def get_n_best_shap_mat(d, n=3, value_mode=''):
  d_ix = get_n_largest_valued_colname(d, n=n, value_mode=value_mode)
  ret = pd.concat([d, d_ix], axis=1).apply(lambda x: x[x['ix']], axis=1)
  return(ret)

@print_func_name
def cleanse_colname(colnames):
    ret = ["".join (c if c.isalnum() else "_" for c in str(x)) for x in colnames]
    return(ret)

