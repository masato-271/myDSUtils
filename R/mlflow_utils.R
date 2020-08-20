
mlflow_get_experiment_id <- function(target_experiment_name){
  target_experiment_name <- as.character(target_experiment_name)
  
  tmp_mlflow_experiments <- mlflow_list_experiments()
  
  if(!any(tmp_mlflow_experiments$name %in% target_experiment_name)){
    mlflow_create_experiment(target_experiment_name)
  }
  tmp_mlflow_experiments <- mlflow_list_experiments()
  exp_id <- tmp_mlflow_experiments %>% 
    dplyr::filter(name == target_experiment_name) %>% 
    magrittr::extract2('experiment_id')
  
  return(exp_id)
}


mlflow_log_catboost_params <- function(run_id='', exp_id=NULL, params, model){
  tmp_run_info <- mlflow_list_run_infos(experiment_id = exp_id)
  if(!run_id %in% tmp_run_info$run_id){
    run_id <- NULL
  }
  
  with(mlflow_start_run(run_id = run_id, experiment_id = exp_id), {
    tmp_run_info <- mlflow_get_run()
    for(i in 1:length(params)){
      tmp_param <- params[i]
      mlflow_log_param(attr(tmp_param, 'names'), tmp_param[[1]])
    }
    mlflow_log_param('finished_tree_count', model$tree_count)
    mlflow_log_param('split_ratio', split_ratio)
    mlflow_log_param('fileID', ts_now)
  })
  
  return(tmp_run_info$run_id)
}

mlflow_log_snapshot_sources_as_artifact <- function(run_id){
  # save all source as artifact
  print('a')
  with(mlflow_start_run(run_id = run_id), {
    source_files <- list.files(path = './', pattern = '.R$', include.dirs = F)
    for(f in source_files){
      print(f)
      if(file.size(f) > 0){
        mlflow_log_artifact(f, run_id = run_id, artifact_path = 'src')
      }
    }
  })
}
