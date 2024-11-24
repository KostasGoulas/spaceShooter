import sqlite3
from sqlite3 import Error

class GamesDataBase :
    def __init__(self) :
        self.connection = self.__create_connection("space_shooter.sqlite")

        # The game will need a table with the hight score. Ill keep an name also and im gona keep the first 3 (higher-scors):
        # So ill delete the next to make the database 'litter'
        initial_table = """
        CREATE TABLE IF NOT EXISTS game (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score FLOAT
        );
        """
        # Initialize the table
        self.__execute_query(initial_table)
    
    def insert(self, name, score):
        insert = f"""
        INSERT INTO
        game ( name, score)
        VALUES
        ( '{name}', '{score}');
        """
        self.execute_query(insert)
    
    def readTable(self):
        table = "SELECT * from game"
        return self.__execute_read_query( table )
    
    def update(self, id, name, score):
        tmp_table = self.readTable()
        if len(tmp_table) < id :
            return len(tmp_table)
        update = f"""
        UPDATE
        game
        SET
        name = "{name}",
        score = {score}
        WHERE
        id = {id}
        """
        self.__execute_query(update)
        return id
    
    # private :
    def __create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successfull")
        except Error as e:
            print(f"The error '{e}' occured")
        return connection

    def __execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query execute successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def __execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
