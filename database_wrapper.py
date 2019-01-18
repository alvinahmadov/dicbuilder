from sqlalchemy import create_engine, Table, MetaData, Column, DefaultClause
from sqlalchemy.engine.base import Connection


class DatabaseWrapper:
    def __init__(self, connection_name: str):
        self._engine = create_engine(connection_name, echo = False)
        self.__connector = self._engine.connect()
        self.__metadata = MetaData()
        self.__tables = dict()

    def __delete__(self, instance):
        self.__connector.close()
        del self.__connector
        del self._engine
        del self.__metadata

    def create_table(self, table_name, columns, drop = True):
        """ Create tables for database
         :param table_name name of the table to create
         :param columns list of column objects
         :param drop Drop existing values
         """
        self.__tables[table_name] = Table(table_name, self.__metadata, *columns)
        if drop:
            self.__metadata.drop_all(self._engine)
        else:
            self.__metadata.create_all(self._engine)
        self.update_table(table_name)
        return table_name

    def update_table(self, table_name):
        print(self.__metadata.get_children())
        Table.select()
        for col in self.__tables[table_name].primary_key:
            print(col.key)
        pass

    def has_table(self, table_name) -> bool:
        return self._engine.has_table(table_name)

    def drop_table(self, table_name):
        self.__metadata.remove(self.__tables[table_name])
        pass

    def insert_values(self, table_name, values: dict):
        ins = self.__tables[table_name].insert().values(values)
        self.__connector.execute(ins)

    def select_table(self, table_name):
        self.__connector.execute(self.__tables[table_name].select())

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
            if index == primarykey_index:
                columns.append(Column(col_name, col_type, primary_key = True))
            else:
                columns.append(Column(col_name, col_type))
            index += 1
        return columns
