# %%
import os
import sys

import hydra
from omegaconf import DictConfig

from utils.presto_utils import PrestConnection

HYDRA_CONFIG_PATH = "config.yaml"

# hydraにコンフィグ設定任せて実行する例
# information_schemaからテーブル名一覧を拾って、データのサンプルを一気にCSV形式でダンプする

@ hydra.main(config_path=HYDRA_CONFIG_PATH)
def main(cfg):
  con = PrestConnection(**cfg.presto)
  con.connect()
  d = con.get_data(f"select * from information_schema.tables")
  d = d.query(f"table_schema == '{cfg.presto.schema}'")
  print(d)
  
  # TODO
  # なぜかリモートで実行するとこのステップで意図しないディレクトリがwdになるので明示的にchdirしている
  os.chdir("/var/analytics/takahashi/jupyter")
  for i, x in d.iterrows():
    tablename = x["table_name"]
    if tablename not in ["mstcompanyprefecture"]:
      tmp_d = con.get_data(f'''select * from {tablename} limit 100''')
      tmp_d.to_csv(f"./dumped_data/{cfg.presto.schema}__{tablename}.csv", index=False)

      tmp_d = con.get_data(f'''select count(1) as n_records from {tablename}''')
      tmp_d.to_csv(f"./dumped_data/{cfg.presto.schema}__{tablename}__nrow.csv", index=False)


if __name__ == "__main__":
  main()
