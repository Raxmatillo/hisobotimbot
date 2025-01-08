import datetime
import sqlite3


class Database:
    def __init__(self, path_to_db="database/users.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            region VARCHAR(255) NOT NULL,
            district VARCHAR(255) NOT NULL,
            school_number INTEGER,
            teacher_name VARCHAR(100) NOT NULL,
            position VARCHAR(100) NOT NULL,
            director_name VARCHAR(100) NOT NULL,
            year VARCHAR(100) NOT NULL,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.execute(sql, commit=True)

    def create_table_documents(self):
        sql = """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            title VARCHAR(60) NOT NULL,
            text VARCHAR(300) NOT NULL,
            images TEXT NOT NULL,
            month VARCHAR(50) NOT NULL,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.execute(sql, commit=True)

    def add_document(self, telegram_id: int, title: str, text: str, images: str):
        sql = """
        INSERT INTO documents(telegram_id, title, text, images) VALUES (?, ?, ?, ?)
        """
        self.execute(sql, parameters=(telegram_id, title, text, images), commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(
            self, 
            telegram_id: int, 
            region: str, 
            district: str, 
            school_number: int, 
            teacher_name: str, 
            position: str,
            director_name: str,
            year: str
            ):

        sql = """
        INSERT INTO users(telegram_id, region, district, school_number, teacher_name, position, director_name, year) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(telegram_id, region, district, school_number, teacher_name, position, director_name, year), commit=True)

    def update_user(
            self, 
            region: str, 
            district: str, 
            school_number: int, 
            teacher_name: str, 
            position: str,
            director_name: str,
            year: str,
            telegram_id: int, 
            ):

        sql = """
        UPDATE users SET region=?, district=?, school_number=?, teacher_name=?, position=?, director_name=?, year=? WHERE telegram_id=?
        """
        self.execute(sql, parameters=(region, district, school_number, teacher_name, position, director_name, year, telegram_id), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM users WHERE TRUE", commit=True)

    def get_weekly_users(self):
        query = """
        SELECT COUNT(*) FROM users 
        WHERE joined_date >= date('now', '-7 days');
        """
        return self.execute(query, fetchone=True)
    
    def get_monthly_users(self):
        query = """
        SELECT COUNT(*) FROM users 
        WHERE joined_date >= date('now', '-30 days');
        """
        return self.execute(query, fetchone=True)
    
    # documents
    def add_document(self, telegram_id: int, title: str, text: str, images: str, month: str):
        sql = """
        INSERT INTO documents(telegram_id, title, text, images, month) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(telegram_id, title, text, images, month), commit=True)

    def select_document(self, telegram_id: int):
        sql = "SELECT * FROM documents WHERE telegram_id=?"
        return self.execute(sql, parameters=(telegram_id, ), fetchall=True)

    def delete_documents(self):
        self.execute("DROP TABLE documents", commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
