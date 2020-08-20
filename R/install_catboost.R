library(glue)
target_os <- "windows"
target_version <- "0.22"
target_url <- glue("https://github.com/catboost/catboost/releases/download/v{target_version}/catboost-R-{target_os}-{target_version}.tgz")
devtools::install_url(target_url, INSTALL_opts = c("--no-multiarch"))
