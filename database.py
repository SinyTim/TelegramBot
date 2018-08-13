import sqlite3


class Database:

    def __init__(self, db_name="db.sqlite"):

        self.db_name = db_name
        self.connection = None

        self.table_name = 'todo_items'
        self.column1_name = 'task'
        self.column2_name = 'owner'

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def close_connection(self):
        self.connection.close()

    def execute(self, command, args=None):
        self.connect()
        if args:
            records = self.connection.execute(command, args)
        else:
            records = self.connection.execute(command)
        result = [record for record in records]
        self.connection.commit()
        self.close_connection()
        return result

    def create_table(self):
        column_type = 'text'
        command = "CREATE TABLE IF NOT EXISTS {table_name} " \
                  "({column1_name} {column_type}, {column2_name} {column_type})" \
            .format(table_name=self.table_name, column1_name=self.column1_name,
                    column_type=column_type, column2_name=self.column2_name)
        self.execute(command)

    def add_item(self, item_text, owner):
        command = "INSERT INTO {table_name} " \
                  "({column1_name}, {column2_name}) VALUES (?, ?)" \
            .format(table_name=self.table_name,
                    column1_name=self.column1_name, column2_name=self.column2_name)
        args = (item_text, owner)
        self.execute(command, args)

    def delete_item(self, item_text, owner):
        command = "DELETE FROM {table_name} " \
                  "WHERE {column1_name} = (?) AND {column2_name} = (?)" \
            .format(table_name=self.table_name,
                    column1_name=self.column1_name, column2_name=self.column2_name)
        args = (item_text, owner)
        self.execute(command, args)

    def get_items(self, owner):
        command = "SELECT {column1_name} FROM {table_name} WHERE " \
                  "{column2_name} = (?)" \
            .format(table_name=self.table_name, column1_name=self.column1_name,
                    column2_name=self.column2_name)
        args = (owner, )
        records = self.execute(command, args)
        return [record[0] for record in records]


database = Database()
