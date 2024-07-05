import sqlite3

def create_table():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            note TEXT NOT NULL
        )
    ''')
    
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_table()
