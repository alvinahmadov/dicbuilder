from sqlalchemy import create_engine, Table, MetaData, Column, DefaultClause


class DatabaseWrapper:
    def __init__(self, connection_name: str):
        self._engine = create_engine(connection_name, echo = False)
        self._connector = self._engine.connect()
        self._metadata = MetaData()
        self._tables = dict()

    def __delete__(self, instance):
        self._connector.close()
        del self._connector
        del self._engine
        del self._metadata

    def create_table(self, table_name, columns, drop = True):
        """ Create tables for database
         :param table_name name of the table to create
         :param columns list of column objects
         :param drop Drop existing values
         """
        self._tables[table_name] = Table(table_name, self._metadata, *columns)
        if drop:
            self._metadata.drop_all(self._engine)
        else:
            self._metadata.create_all(self._engine)
        self.update_table(table_name)
        return table_name

    def update_table(self, table_name):
        print(self._metadata.get_children())
        Table.select()
        for col in self._tables[table_name].primary_key:
            print(col.key)
        pass

    def has_table(self, table_name) -> bool:
        return self._engine.has_table(table_name)

    def drop_table(self, table_name):
        self._metadata.remove(self._tables[table_name])
        pass

    def insert_values(self, table_name, values: dict):
        ins = self._tables[table_name].insert().values(values)
        self._connector.execute(ins)

    def select_table(self, table_name):
        self._connector.execute(self._tables[table_name].select())

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
