from sqlalchemy import create_engine, Table, MetaData, Column, Integer, ForeignKey, String
from sqlalchemy.engine.base import Connection


class DatabaseWrapper:
    def __init__(self, connection_name: str):
        self.__engine = create_engine(connection_name, echo = False)
        self.__connector = Connection(self.__engine)
        self.__metadata = MetaData()
        self.__tables = dict()
        pass

    def __delete__(self, instance):
        self.__connector.close()
        del self.__connector
        del self.__engine
        del self.__metadata
        pass

    def create_table(self, table_name, columns, drop = True):
        """ Create tables for database
         :param table_name name of the table to create
         :param columns list of column objects
         :param drop Drop existing values
         """
        self.__tables[table_name] = Table(table_name, self.__metadata, *columns)
        if drop:
            self.__metadata.drop_all(self.__engine)
        self.__metadata.create_all(self.__engine)
        return table_name
        pass

    pass

    def insert_values(self, table_name, values: dict):
        self.__connector = self.__engine.connect()
        ins = self.__tables[table_name].insert().values(values)
        result = self.__connector.execute(ins)
        pass

    def select_table(self, table_name):
        result = self.__connector.execute(self.__tables[table_name].select())
        pass

    pass
