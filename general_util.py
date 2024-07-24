import datetime
import math
import os
import shutil
from pathlib import Path
import datetime
import dateutil

from logging import getLogger

import numpy as np
import pandas as pd
import psutil
from sklearn import datasets

logger = getLogger(__name__)

def __check_str_col(d, cn):
    x = d[cn]
    print(f'most frequently appeard value::\n{x.mode()}\n')
    print('value counts...')
    print(x.value_counts())

def __check_numeric_col(d, cn):
    x_min = d[cn].min()
    x_max = d[cn].max()
    print(f'value range::{x_min},{x_max}')
    x_mean = d[[cn]].mean().values[0]
    print(f'mean::{x_mean}')
    x_median = d[[cn]].median().values[0]
    print(f'median::{x_median}')

    q01 = d[[cn]].quantile(0.01)[0]
    q10 = d[[cn]].quantile(0.10)[0]
    q25 = d[[cn]].quantile(0.25)[0]
    q50 = d[[cn]].quantile(0.50)[0]
    q75 = d[[cn]].quantile(0.75)[0]
    q90 = d[[cn]].quantile(0.90)[0]
    q99 = d[[cn]].quantile(0.99)[0]
    print('quantiles::1%, 10%, 25%, 50%, 75%, 90%, 99%')
    print((q01, q10, q25, q50, q75, q90, q99))

# pandas-profileっぽい感じので、ほしい情報を自分でいろいろつくれるように自作
def check_col_stats(d, cn):
    print(f'target column name...{cn}')
    print('______________________________________________')
    x = np.squeeze(d[[cn]].values)
    x_notnan = np.squeeze(d.loc[~d[cn].isna(), cn].values)
    n_unique = len(d[cn].unique())
    print(f'unique values::{n_unique}')

    n_missing = d[[cn]].isna().values.squeeze().sum()
    print(f'missing value count::{n_missing}')

    if isinstance(x_notnan[0], (str)):
        __check_str_col(d, cn)
    elif isinstance(x_notnan[0], (bool, int, float, np.float, np.double, np.integer)):
        __check_numeric_col(d, cn)

    print('\n')

def zen2han_num(x):
    x = x.replace("０", "0")
    x = x.replace("１", "1")
    x = x.replace("２", "2")
    x = x.replace("３", "3")
    x = x.replace("４", "4")
    x = x.replace("５", "5")
    x = x.replace("６", "6")
    x = x.replace("７", "7")
    x = x.replace("８", "8")
    x = x.replace("９", "9")
    return x

def add_target_enc(d, target_colname, grouping_colnames, agg_function, prefix=''):
    if type(grouping_colnames) is not list:
        grouping_colnames = [grouping_colnames]
    if prefix != '':
        prefix = prefix + '_'

    new_colname = f"{prefix}{agg_function.__name__}__{''.join(grouping_colnames)}__{target_colname}"
    tmp_d = d.groupby(grouping_colnames)[target_colname].agg(__c1__=agg_function)
    tmp_d = tmp_d.rename({'__c1__': new_colname}, axis='columns')
    d = d.merge(tmp_d, on=grouping_colnames, how='left')
    return d

def print_func_name(func):
    def f(*args, **k):
        t0 = datetime.datetime.now()
        p = psutil.Process(os.getpid())
        m0 = p.memory_info()[0] / 2. ** 30

        logger.info(func.__name__ + '\t\t\tstart')
        result = func(*args, **k)

        m1 = p.memory_info()[0] / 2. ** 30
        mem_usage_delta = m1 - m0
        sign = '+' if mem_usage_delta >= 0 else '-'
        mem_usage_delta = math.fabs(mem_usage_delta)

        logger.info(f'{func.__name__}\t\t\tend\tproc time:{str(datetime.datetime.now() - t0)}\t[{m1:.1f}GB({sign}{mem_usage_delta:.1f}GB)]')
        return result
    return f

def archive_old_files(target_dir: Path, target_ext: str, n_max_files=3):
    if isinstance(target_dir, str):
        target_dir = Path(target_dir)
    archive_dir = target_dir / 'old'

    if not archive_dir.exists():
        archive_dir.mkdir()

    files = [x for x in target_dir.iterdir() if x.suffix == target_ext]
    files.sort()
    archive_files = files[0:(len(files) - n_max_files)]
    if len(archive_files) > n_max_files:
        for x in archive_files:
            shutil.move(x, archive_dir / x.name)

def get_latest_filename(search_root_dir, target_suffix):
  if isinstance(search_root_dir, str):
    search_root_dir = Path(search_root_dir)
  ret = []
  for p in search_root_dir.iterdir():
    if p.suffix == target_suffix:
      ret.append(p)
  ret.sort()

  return (ret[-1])


def calc_date_str(date_str, unit='months', qty=1, date_format='%Y-%m-%d'):
    """文字列として持っている日付か

    Args:
        date_str (str or datetime): 計算対象とする日付
        unit (str, optional): ずらす期間の単位. Defaults to 'months'.
        qty (int, optional): ずらす量 ＋ーどちらでもOK. Defaults to 1.
        date_format (str, optional): 処理対象が文字列の場合、パージするフォーマット . Defaults to '%Y-%m-%d'.

    Raises:
        ValueError: 想定していない単位を指定された場合にはエラーを出す
    """

    if unit not in ['days', 'weeks', 'months', 'years']:
        raise ValueError('not implimented unit')

    tmp_s = date_str
    if isinstance(date_str, str):
        tmp_s = datetime.datetime.strptime(date_str, date_format)

    if unit == 'days':
        tmp_delta = dateutil.relativedelta.relativedelta(days=qty)
    elif unit == 'weeks':
        tmp_delta = dateutil.relativedelta.relativedelta(weeks=qty)
    elif unit == 'months':
        tmp_delta = dateutil.relativedelta.relativedelta(months=qty)
    elif unit == 'years':
        tmp_delta = dateutil.relativedelta.relativedelta(years=qty)

    ret = (tmp_s + tmp_delta).strftime(date_format)

    return (ret)


def round_datestr2quarter(date_str, date_format='%Y-%m-%d', direction='forward', month='head'):
    """date_strで与えた日付をクオーター単位で丸める
    directionがforwardはdate_strを起点に未来方向へ、backwardの場合は過去方向へ丸める
    monthはreturnの月の取り扱いを指定するパラメータで、クオーターの頭の月の場合head、最後の月はtailを指定する

    Args:
        date_str (str or datetime): 処理対象とする日付
        date_format (str, optional): パージする日付のフォーマット. Defaults to '%Y-%m-%d'.
        direction (str, optional): 丸める方向. forward Defaults to 'forward'.
        month (str, optional): [description]. Defaults to 'head'.
    """

    if direction not in ['forward', 'backward']:
        raise ValueError('direction should be forward or backward')

    if month not in ['head', 'tail']:
        raise ValueError('month should be head or tail')

    tmp_s = date_str
    if isinstance(date_str, str):
        tmp_s = datetime.datetime.strptime(date_str, date_format)

    tmp_delta = dateutil.relativedelta.relativedelta(months=1)

    if month == 'head':
        frac = 1
    elif month == 'tail':
        frac = 0

    tmp_date = tmp_s
    for i in range(4):
        if tmp_date.month % 3 == frac:
            break
        if direction == 'forward':
            tmp_date += tmp_delta
        elif direction == 'backward':
            tmp_date -= tmp_delta
    ret = tmp_date.strftime(date_format)[:-2] + '01'
    return (ret)
