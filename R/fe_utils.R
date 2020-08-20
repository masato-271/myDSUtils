# 特定カラムのレコード重複をチェック
check_duplication <- function(d, colname='id'){
  tmp_d <- d %>% 
    group_by(!!sym(colname)) %>% 
    summarise(n=n())
  
  if(max(tmp_d$n) > 1){
    print('duplicated')
    print(tmp_d %>% filter(n > 1) %>% arrange(!!sym(cn)))
    return(TRUE)
  }else{
    print('not duplicated')
    return(FALSE)
  }
}

find_na_contained_column <- function(d){
  tmp_d <- is.na(d) %>% 
    apply(2, sum) %>% 
    data.frame %>% 
    rownames_to_column()
  
  colnames(tmp_d) <- c('colname', 'n')
  tmp_d$tmp_n <-  nrow(d)
  tmp_d %<>% 
    mutate(ratio = n/tmp_n) %>% 
    arrange(desc(ratio)) %>% 
    select(-tmp_n) %>% 
    filter(n > 0)
  
  if(nrow(tmp_d) > 0){
    print('missing column detected')
    return(tmp_d)
  }else{
    print('no missing column detected')
    return(NULL)
  }
}
