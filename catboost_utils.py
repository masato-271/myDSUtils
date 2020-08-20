import os
import numpy as np 
import pandas as pd
from pathlib import Path
import shutil

def get_feature_importance_df(model, feature_name):
    d_importance = pd.DataFrame({'feature_name':feature_name, 'imp':model.get_feature_importance()})
    d_importance.sort_values(['imp'], ascending=False, inplace=True)
    return d_importance

def rmsle(pred, gt):
    _pred = np.log(pred+1)
    _gt = np.log(gt+1)
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
