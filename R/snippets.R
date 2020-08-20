# mlflow examples
library(mlflow)
library(Metrics)

source('myDSUtils/mlflow_utils.R')

exp_id <- mlflow_get_experiment_id(target_experiment_name = split_ratio)
run_id <- mlflow_log_catboost_params(exp_id = exp_id, params = params, model = model)
# その他色々保存する部分
with(mlflow_start_run(run_id = run_id),{
  tmp_mape <- Metrics::mape(y_valid$keiyaku_pr, y_pred)
  mlflow_log_metric('smape', 100 * tmp_mape)
  
  # save inspection assets 
  mlflow_log_artifact(DIR_INSPECTION_ASSET)
})
mlflow_log_snapshot_sources_as_artifact(run_id = run_id)



#' データフレームをn_colで指定したカラム数になるように微調整
#' 指定したカラム数が元のデータフレームより小さい列数を指定していた場合、元のデータフレームをそのまま返す
#'
#' @param d 加工するデータフレーム
#' @param n_col 調整したいデータフレームのカラム数
#'
#' @examples
#' iris_adjusted <- adjust_df_colsize(iris, 10)
#' iris_adjusted %>% dim

adjust_df_colsize <- function(d, n_col=1){
  if(n_col > ncol(d)){
    diff_ncol <- n_col - ncol(d)
    for(i in 1:diff_ncol){
      d <- cbind(d, NA)
    }
  }
  return(d)
}

