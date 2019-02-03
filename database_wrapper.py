from sqlalchemy import create_engine, Table, MetaData, Column
from sqlalchemy.engine import ResultProxy, RowProxy
from utils import concat


class DatabaseWrapper:
    def __init__(self, connection_name: str):
        self._engine = create_engine(connection_name, echo = False)
        self._connection = self._engine.connect()
        self._metadata = MetaData()
        self._db_name = connection_name[connection_name.rfind('/') + 1:]
        self._tables = {}

    def __delete__(self, instance):
        self._connection.close()
        del self._connection
        del self._engine
        del self._metadata

    def create_table(self, table_name, columns):
        """ Create tables for database
         :param table_name name of the table to create
         :param columns list of column objects
         :param drop Drop existing values
         """
        self._tables[table_name] = Table(table_name, self._metadata, *columns)
        self._metadata.drop_all(self._engine)
        self._metadata.create_all(self._engine)
        return table_name

    def update_table(self, table_name):
        pass

    def fetch_row(self, table_name: str, row_number: int, column: int):
        if not self.has_table(table_name):
            return
        result = self._connection.execute(concat("select * from ", table_name))
        rows = result.fetchall()
        if row_number is -1 or row_number >= len(rows):
            row_number = self.row_count(table_name) - 1
        else:
            row_number -= 1
        if column >= self.column_count(table_name):
            raise IndexError("Colum index %d out of range %d " % (column, len(result.keys())))
        if column is -1:
            return rows[row_number][:]
        return rows[row_number][column]

    def row_count(self, table_name) -> int:
        res = self._connection.execute(concat("select * from ", table_name))
        rows = res.fetchall()
        return len(rows)

    def column_count(self, table_name) -> int:
        result = self._connection.execute(concat("select * from ", table_name))
        return len(result.keys())

    def has_table(self, table_name) -> bool:
        return self._engine.has_table(table_name)

    def drop_table(self, table_name) -> None:
        self._metadata.remove(self._tables[table_name])

    def insert_values(self, table_name, values: dict, unique = False):
        ins = self._tables[table_name].insert().values(values)
        self._connection.execute(ins)

    def select_table(self, table_name) -> ResultProxy:
        return self._connection.execute(self._tables[table_name].select())

    def get_dbname(self):
        return self._db_name

    @staticmethod
    def generate_columns(column_infos: dict, primarykey_index):
        """ Generate database columns
        :param column_infos dictionary of column name as key and column type with additional size info
        :type column_infos dict
        :param primarykey_index index of column which is primary key
        :type primarykey_index int
         """
        columns = list()
        index = 0
        for (col_name, col_type) in column_infos.items():
            primary = index == primarykey_index
            columns.append(Column(col_name, col_type, primary_key = primary))
            index += 1
        return columns
