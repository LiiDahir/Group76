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

    def search_data(self, ID=None, name=None, student_class=None, telphone=None):
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

        conditions_str = ' AND '.join(conditions) if conditions else '1=1'

        sql = f"SELECT * FROM Student WHERE {conditions_str}"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            print(f"Search results for conditions: {conditions_str}")
            return rows
        except Error as e:
            print(e)
            return []

# Example usage of the module
# if __name__ == "__main__":
#     db = Data()
#     # db.create_table()
#     x=db.count()
#     print(x)
# #     # Insert data
#     db.insert_data("1", "Alice", "10th Grade", "1234567890", "alice.png")
#     db.insert_data("2", "Bob", "9th Grade", "0987654321", "bob.png")

#     # Update data
#     db.update_data("1", name="Alicia")

#     # Search data
#     results = db.search_data(name="Alicia")
#     for row in results:
#         print(row)

#     # Delete data
#     db.delete_data("2")
