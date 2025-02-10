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
    
    def size(self):
        table = self.readTable()
        print(table)
        return len(table)

    def insert(self, name, score):
        insert = f"""
        INSERT INTO
        game ( name, score)
        VALUES
        ( '{name}', '{score}');
        """
        self.__execute_query(insert)
    
    def readTable(self):
        table = "SELECT * from game"
        return self.__execute_read_query( table )
    
    def readFirst(self):
        table = self.readTable()
        if len(table) == 0:
            return []
        return table[0]
    
    def read(self, id):
        table = self.readTable()
        if id <= len(table):
            return table[id-1]
        return []

    def update(self, id, name, score):
        prev = self.read(id)
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
        return prev
    
    def delete(self, id):
        delete_query = f"""
        DELETE FROM game WHERE id = {id};
        """
        self.__execute_query(delete_query)
    def pop_last(self):
        query = "DELETE FROM game WHERE id = (SELECT MAX(id) FROM game);"
        self.__execute_query(query)
        print("Last record deleted successfully!")

    def sort_and_store(self):
        # Create a new table with the same schema
        create_temp_table_query = """
        CREATE TABLE temp_game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score FLOAT
        );
        """
        self.__execute_query(create_temp_table_query)

        # Copy sorted data into the new table
        insert_sorted_query = """
        INSERT INTO temp_game (name, score)
        SELECT name, score FROM game ORDER BY score ASC;
        """
        self.__execute_query(insert_sorted_query)

        # Delete the original table
        drop_query = "DROP TABLE game;"
        self.__execute_query(drop_query)

        # Rename temp_game to game
        rename_query = "ALTER TABLE temp_game RENAME TO game;"
        self.__execute_query(rename_query)

        print("Database sorted successfully!")


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

