import sqlite3

# Connect to the SQLite database (it will create 'highscores.db' if it doesn't exist)
conn = sqlite3.connect('highscores.db')
cursor = conn.cursor()

# Create a table for high scores if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS high_scores (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print('Database setup complete.')
