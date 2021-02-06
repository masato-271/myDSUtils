import pandas as pd 
import lightgbm as lgb

def lgb_get_feature_importance_df(bst):
  d_imp = pd.DataFrame([bst.feature_name(), bst.feature_importance()]).transpose()
  d_imp.columns = ['feature_name', 'importance']
  d_imp.sort_values(['importance'], inplace=True, ascending=False)
  d_imp.reset_index(drop=True, inplace=True)
  return d_imp


