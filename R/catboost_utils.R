library(catboost)
library(tidyverse)
library(magrittr)
library(reshape2)

get_exclude_colname_str <- function(model){
  s <- catboost.get_feature_importance_df(model) %>% 
    filter(imp == 0) %>% 
    extract2('rowname') %>% 
    paste0(collapse = '",\n"') %>% 
    paste0('"', ., '"')
  
  return(s)
}

get_top_factornames <- function(fstr, n_terms=3, mode='magnitude'){
  prefix = 'reason_'
  
  if(is.matrix(fstr)){
    fstr %<>% as.data.frame()
  }
  
  fstr %<>% select(-`X.base.`)
  
  # check n_term size and reset 
  n_terms <- min(n_terms, ncol(fstr))
  
  if(mode == 'magnitude'){
    f <- function(x){
      abs(x) %>% 
        sort(decreasing = TRUE) %>% 
        head(n_terms) %>% 
        attr('names') %>% 
        return
    }
    
    top_terms <- fstr %>% 
      apply(1, f) %>% 
      t
    
    tmp_colnames <- paste0(prefix, 1:n_terms)
    colnames(top_terms) <- tmp_colnames
    
  }else if(mode == 'gain'){
    fstr %<>% mutate(idx = row_number())
    top_terms <- fstr %>% 
      melt(id.vars='idx') %>% 
      arrange(idx, desc(value)) %>% 
      filter(value > 0) %>% 
      group_by(idx) %>% 
      dplyr::top_n(n_terms, value)
    
    top_terms %<>% mutate(value = row_number())
    top_terms <- spread(top_terms, key=value, value=variable) %>% 
      ungroup() %>% 
      arrange(idx) %>% 
      select(-idx)
    
  }
  
  tmp_colnames <- paste0(prefix, 1:n_terms)
  colnames(top_terms) <- tmp_colnames
  
  top_terms %>% 
    data.frame(stringsAsFactors = F) %>% 
    return
  
}

catboost.get_feature_importance_df <- function(model){
  imp <- catboost.get_feature_importance(model)
  imp %<>% data.frame(imp=.) %>% rownames_to_column()
  tmp_levels <- imp %>% arrange(imp) %>% select(rowname) %>% unlist
  imp$rowname %<>% factor(levels = tmp_levels)
  
  return(imp)
}

plot_importance <- function(model, n_top=30){
  imp <- catboost.get_feature_importance_df(model)
  
  imp2 <- imp %>% 
    arrange(imp, rowname) %>%
    mutate(rn=row_number()) %>% 
    top_n(n_top, rn)
  g <- ggplot(imp2, aes(x=rowname, y=imp)) + geom_bar(stat='identity') + coord_flip()
  g <- g + theme_gray(base_family = 'HiraKakuPro-W3')
  
  return(g)
}

catboost.dummp_parameters <- function(params, model, ts_now, dir=''){
  tmp_params <- catboost.get_model_params(model)
  tmp_params$flat_params
  tmp_params$best_iteration <- model$tree_count
  
  fn <- glue('{dir}/{ts_now}_catboost_params.json')
  jsonlite::write_json(tmp_params, fn, simmplifyVector=T, pretty=T)
  print(glue('parameter saved: {fn}'))
}

