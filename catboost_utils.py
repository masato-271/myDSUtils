import os
import numpy as np
import pandas as pd
from pathlib import Path
import shutil
import matplotlib.pyplot as plt
import seaborn as sns

def get_feature_importance_df(model):
    d_imp = pd.DataFrame({'feature_name': model.feature_names_, 'importance':model.get_feature_importance()})
    d_imp.sort_values(['importance'], ascending=False, inplace=True)
    return d_imp

def rmsle(pred, gt):
    _pred = np.log(pred + 1)
    _gt = np.log(gt + 1)
    return np.sqrt(np.square(_pred - _gt).mean())

def clear_catboost_info_dir(target_dir='./catboost_info'):
    # clear catboost_info directory
    for p in Path(target_dir).iterdir():
        if p.is_file():
            os.remove(p)
    try:
        shutil.rmtree(os.path.join(target_dir, 'learn'))
    except:
        pass

    try:
        shutil.rmtree(os.path.join(target_dir, 'test'))
    except:
        pass

    try:
        shutil.rmtree(os.path.join(target_dir, 'tmp'))
    except:
        pass


def get_shapValue_df(model, pool):
    cn = list(pool.get_feature_names()) + ['<base>']
    _d = pd.DataFrame(model.get_feature_importance(pool, type='ShapValues'), columns=cn)

    return _d

def get_object_col_idx(d):
    bix = d.columns.isin(d.columns[d.dtypes == object])
    return list(np.where(bix))[0]

def plot_catboost_learning_curve(loss_function='RMSE', log_dir='./catboost_info/'):
    if isinstance(log_dir, str):
        log_dir = Path(log_dir)

    d_learn = pd.read_table(log_dir / 'learn_error.tsv')

    plt.clf()
    f, ax = plt.subplots()
    sns.lineplot(x='iter', y=loss_function, data=d_learn, label='Learn')

    # テスト分があれば、その分もプロット
    f = log_dir / 'test_error.tsv'
    if os.path.exists(f):
        d_test = pd.read_table(f)
        sns.lineplot(x='iter', y=loss_function, data=d_test, label='Test')
    ax.legend()
    plt.show()
