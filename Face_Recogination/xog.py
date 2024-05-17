# student_module.py

import sqlite3
from sqlite3 import Error

class Data:
    def __init__(self):
        """Initialize the connection to the SQLite database."""
        self.db_file = "just.db"
        self.conn = self.create_connection()

    def create_connection(self):
        """Create a database connection to the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file, check_same_thread=False)  # Allow thread sharing
            print(f"Connected to database: {self.db_file}")
        except Error as e:
            print(e)
        return conn
    
    def count(self):
        count="select count(*) from Student "
        try:
            c = self.conn.cursor()
            cou=c.execute(count)
            count=c.fetchone()[0]
            return count
        except:
            pass

    def create_table(self):
        """Create the Student table if it does not exist."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Student (
            ID text PRIMARY KEY,
            Name text NOT NULL,
            Class text NOT NULL,
            Telphone text NOT NULL,
            Image text NOT NULL
        );
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            print("Table Student created or already exists.")
        except Error as e:
            print(e)

    def insert_data(self, ID, name, student_class, telphone, image):
        """Insert a new row into the Student table."""
        sql = "INSERT INTO Student (ID, Name, Class, Telphone, Image) VALUES (?, ?, ?, ?, ?)"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (ID, name, student_class, telphone, image))
            self.conn.commit()
            print(f"Inserted data: ID={ID}, Name={name}, Class={student_class}, Telphone={telphone}, Image={image}")
        except Error as e:
            print(e)

    def update_data(self, ID, name=None, student_class=None, telphone=None, image=None):
        """Update rows in the Student table."""
        updates = []
        params = []

        if name:
            updates.append("Name = ?")
            params.append(name)
        if student_class:
            updates.append("Class = ?")
            params.append(student_class)
        if telphone:
            updates.append("Telphone = ?")
            params.append(telphone)
        if image:
            updates.append("Image = ?")
            params.append(image)

        if updates:
            updates_str = ', '.join(updates)
            params.append(ID)

            sql = f"UPDATE Student SET {updates_str} WHERE ID = ?"
            try:
                cur = self.conn.cursor()
                cur.execute(sql, tuple(params))
                self.conn.commit()
                print(f"Updated student with ID={ID}")
            except Error as e:
                print(e)
        else:
            print("No updates provided.")

    def delete_data(self, student_id):
        """Delete rows from the Student table."""
        sql = "DELETE FROM Student WHERE ID = ?"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (student_id,))
            self.conn.commit()
            print(f"Deleted student with ID={student_id}")
        except Error as e:
            print(e)

    def search_data(self, ID=None, name=None, student_class=None, telphone=None,Image=None):
        """Search for rows in the Student table."""
        conditions = []
        params = []

        if ID:
            conditions.append("ID = ?")
            params.append(ID)
        if name:
            conditions.append("Name = ?")
            params.append(name)
        if student_class:
            conditions.append("Class = ?")
            params.append(student_class)
        if telphone:
            conditions.append("Telphone = ?")
            params.append(telphone)
        if Image:
            conditions.append("Image = ?")
            params.append(Image)
        conditions_str = ' AND '.join(conditions) if conditions else '1=1'

        sql = f"SELECT * FROM Student WHERE {conditions_str}"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            List = []
            for i in rows:
                for n in i:
                    List.append(n)
            return List
        except Error as e:
            print(e)
            return []
    def get_column(self,col):
        sql = "Select " + col + "from Student"
        try: 
            cur = self.conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            modify_row = [item[0] for item in rows]
            return modify_row
        except Error as e:
            print(e)
            return []


