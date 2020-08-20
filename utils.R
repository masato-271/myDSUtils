get_timestamp_str <- function(){
  ts_now <- format(Sys.time(), '%Y%m%d-%H%M%S')
  return(ts_now)
}

write_csvs4py <- function(d, dataname, target_dir){
  d_dtypes <- d %>% 
    sapply(class) %>% 
    t %>% 
    data.frame(stringsAsFactors = F)
  
  fn <- glue('{target_dir}/{dataname}_data_type.csv')
  cat('dtype file exported: ', fn)
  write_csv(d_dtypes, fn)
  
  fn <- glue('{target_dir}/{dataname}.csv')
  cat('file exported: ', fn)
  write_csv(d, fn)
}

make_dir_if_not_exist <- function(dir){
  if(dir.exists(dirname(dir))){
    NULL
  }else{
    dirname(dir) %>% dir.create()
  }
}

adjust_df_colsize <- function(d, target_ncol){ 
  diff_ncol <- target_ncol - ncol(d)
  if(diff_ncol > 0){
    for(i in 1:diff_ncol){
      d <- cbind(d, NA)
    }
  }
  return(d)
}
