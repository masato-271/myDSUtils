# %%
import os
from pathlib import Path
import mlflow
from mlflow import log_metric, log_param, log_params, log_artifacts, log_artifact

def mlflow_dump_src(target_dir='./', target_ext=['.py', '.r', '.lock', '.toml'], dump_dir=False, artifact_path=None):
    p_root = Path(target_dir)
    if dump_dir:
        print(f'log_artifact\t\t\t{target_dir}')
        log_artifact(target_dir, artifact_path=artifact_path)
    else:
        for p in p_root.iterdir():
            if p.suffix.lower() in target_ext:
                print(f'log_artifact\t\t\t{p}')
                log_artifact(p, artifact_path=artifact_path)

    return 0

def mlflow_dump_feature_importance(d_importance, n_top = -1):
    if n_top > 0:
        d_top = d_importance.head(n_top).reset_index(drop=True)
        fn = f'top_{n_top}__feature_importance.csv'
    else:
        d_top = d_importance.reset_index(drop=True)
        fn = 'all__feature_importance.csv'

    d_top.to_csv(fn, index=False)
    log_artifact(fn)
    os.remove(fn)

