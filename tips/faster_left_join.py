# https://www.kaggle.com/tkm2261/fast-pandas-left-join-357x-faster-than-pd-merge

# %%timeit
for df_test in list_df:
    df_test.merge(df_user, how='left', on='user_id')
# 1.67 s ± 74.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# Mentioned by @alijs1 in https://www.kaggle.com/c/riiid-test-answer-prediction/discussion/197023.
# It should takes around 139 ms. This is 13 times faster!
# %%timeit
for df_test in list_df:
    df_test.merge(df_user, how='left', left_on='user_id', right_index=True)
# 128 ms ± 3.85 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


# Fast left join
# It should takes around 4.89 ms sec, **357 TIMES FASTER!!!!!!**
# %%timeit
for df_test in list_df:
    pd.concat([df_test.reset_index(drop=True), df_user.reindex(df_test['user_id'].values).reset_index(drop=True)], axis=1)

# 5.03 ms ± 221 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

