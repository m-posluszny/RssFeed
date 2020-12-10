import mysql.connector


class DatabaseHandler:

    def __init__(self):
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="briefly",
        database="mydatabase",
            )
        self.tables = {
            "user_credentials":["username","password"],
            "user_data":["username","url","url_group"]
        }
        self.cursor = self.mydb.cursor()

    # zapisanie bazy
    def save_base(self):
        self.cursor.commit()
        self.cursor.close()
        
    # usuwanie kolumny z tabeli

    def delete_row(self,table, values):
        sqlQuery ="DELETE FROM {table} WHERE  = {} AND  ;"
        self.cursor.execute(sqlQuery)
        self.cursor.commit()
        self.cursor.close()
        
    # dodawanie kolumny do tabeli
    def add_row(self,table, values):
        columns_str=", ".join(self.tables[table])
        value_str=", ".join(values)
        sqlQuery = "INSERT INTO {table} ({colums_str}) VALUES({value_str}) "
        self.cursor.execute(sqlQuery)
        self.cursor.commit()
        self.cursor.close()
        
    #sortowane danych
    def sort():
        ... 
