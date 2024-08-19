import sqlite3

DATABASE = 'data.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Création de la table news
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                url TEXT UNIQUE,
                published_at TEXT,
                source_name TEXT,
                author TEXT
            )
        ''')

        # Création de la table kpi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER
            )
        ''')

        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
