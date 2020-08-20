import prestodb
import pandas as pd
from prestodb.exceptions import Error


class DBConnection:
  def connect(self):
    pass


class PrestConnection(DBConnection):
  def __init__(self, host: str, port: int, user: str, catalog: str, schema: str) -> None:
    self.host = host
    self.port = port
    self.user = user
    self.catalog = catalog
    self.schema = schema

  def connect(self):
    try:
      self.conn = prestodb.dbapi.connect(
          host=self.host,
          port=self.port,
          user=self.user,
          catalog=self.catalog,
          schema=self.schema
      )
    except Error as e:
      # TODO
      pass

  def get_data(self, query_str: str, mode="verbose"):
    cur = self.conn.cursor()
    if mode == "verbose":
      print(query_str)
    cur.execute(query_str)
    d = cur.fetchall()
    d = pd.DataFrame(d)
    colnames = [x[0] for x in cur.description]
    if d.shape[0] == 0:
      d = pd.DataFrame(columns=colnames)
    else:
      d.columns = colnames

    cur.close()
    return d

  def delete_presto_obj(self, target_name: str, what="view"):
    try:
      query_str = f"drop {what} if exists {target_name}"

      cur = self.con.cursor()
      cur.execute(query_str)
      _ = cur.fetchall()

      cur.close()
    except Error as e:
      pass
