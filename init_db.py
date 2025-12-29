import sqlite3
import os

os.makedirs('data', exist_ok=True)

DB_PATH = 'data/jobs.db'

def setup():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # drop the existing db if exists
    cursor.execute('DROP TABLE IF EXISTS jobs')

    # create the jobs table
    cursor.execute('''
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT UNIQUE,
            company TEXT,
            role TEXT,
            link TEXT,
            source TEXT,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully at data/jobs.db")

if __name__ == "__main__":
    setup()