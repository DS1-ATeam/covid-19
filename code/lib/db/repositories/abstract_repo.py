import sqlalchemy as db
import pandas as pd

from lib.db.connection_factory import ConnectionFactory


class AbstractRepository():
    def __init__(self, table_name, connection_string):
        self.engine = ConnectionFactory.get_engine(connection_string)
        self.con = ConnectionFactory.get_connection(connection_string)
        self.table_name = table_name
        self.table = db.Table(table_name, ConnectionFactory.get_meta_data(connection_string), autoload=True, autoload_with=self.engine)

    def data_frame_for_query(self, query):
        results = self.con.execute(query).fetchall()
        df = pd.DataFrame(results)
        if (len(results) > 0):
            df.columns = results[0].keys()
        return df

    def find_all(self):
        query = db.select([self.table])
        return self.data_frame_for_query(query)
