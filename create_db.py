import sqlite3

# Function to create the merged database and table
def create_merged_database():
    conn_merged = sqlite3.connect('all_songs.db')
    cursor_merged = conn_merged.cursor()

    # Create table with auto-incrementing song_id
    cursor_merged.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        song_id INTEGER PRIMARY KEY AUTOINCREMENT,
        album TEXT,
        artist TEXT,
        title TEXT,
        release_date DATE,
        lyrics TEXT
    )
    ''')

    conn_merged.commit()
    return conn_merged, cursor_merged

# Function to extract and insert data from source databases
def extract_and_insert(source_db, cursor_merged):
    conn_source = sqlite3.connect(source_db)
    cursor_source = conn_source.cursor()

    # Fetch data from source database
    cursor_source.execute('''
    SELECT album, artist, title, release_date, lyrics FROM songs
    ''')
    
    rows = cursor_source.fetchall()
    
    for row in rows:
        try:
            # Insert into merged database (omit song_id as it's auto-incremented)
            cursor_merged.execute('''
            INSERT INTO songs (album, artist, title, release_date, lyrics)
            VALUES (?, ?, ?, ?, ?)
            ''', (row[0], row[1], row[2], row[3], row[4]))
        except sqlite3.IntegrityError:
            # Skip duplicates based on song_id primary key
            pass

    conn_source.close()

# Main function to control the flow
def main():
    conn_merged, cursor_merged = create_merged_database()
    
    # Source databases
    source_databases = ['songs.db']
    
    for db in source_databases:
        extract_and_insert(db, cursor_merged)
    
    # Close the merged database connection
    conn_merged.commit()
    conn_merged.close()

if __name__ == "__main__":
    main()
