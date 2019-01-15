from sqlalchemy import create_engine, Table, MetaData, Column, Integer, ForeignKey, String
from sqlalchemy.sql import select


class WordBase:
    def __init__(self, connection_name: str):
        self.__engine = create_engine(connection_name, echo = True)
        self.__metadata = MetaData()
        self.__tables = dict()
        self.__connector = None
        pass

    def create_table(self, table_name, columns):
        """ Create tables for database
         :param table_name name of the table to create
         :param columns list of column objects
         """

        table = Table(table_name, self.__metadata)
        for col in columns:
            table.append_column(col)
        self.__tables[table_name] = table
        self.__metadata.create_all(self.__engine)
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
