import sqlite3
from datetime import datetime

def create_database():
    """Initialize the SQLite database with required tables"""
    
    conn = sqlite3.connect('smart_notes.db')
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Summaries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            input_type TEXT NOT NULL CHECK(input_type IN ('text', 'pdf', 'docx')),
            content TEXT NOT NULL,
            summary TEXT NOT NULL,
            qa_pairs TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_summaries_user_id ON summaries(user_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_summaries_created_at ON summaries(created_at DESC)
    ''')
    
    conn.commit()
    print("✅ Database tables created successfully!")
    
    # Display table structure
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
    print("\n📋 Users Table Structure:")
    print(cursor.fetchone()[0])
    
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='summaries'")
    print("\n📋 Summaries Table Structure:")
    print(cursor.fetchone()[0])
    
    conn.close()

def add_sample_data():
    """Add sample data for testing (optional)"""
    from werkzeug.security import generate_password_hash
    import json
    
    conn = sqlite3.connect('smart_notes.db')
    cursor = conn.cursor()
    
    # Add sample user
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        ''', ('Test User', 'test@example.com', generate_password_hash('password123')))
        
        user_id = cursor.lastrowid
        
        # Add sample summary
        sample_qa = json.dumps([
            {"question": "What is the main topic?", "answer": "This is a sample summary."},
            {"question": "What are the key points?", "answer": "Key points include testing and demonstration."}
        ])
        
        cursor.execute('''
            INSERT INTO summaries (user_id, input_type, content, summary, qa_pairs)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'text', 'Sample content for testing', 
              'This is a sample summary for testing purposes.', sample_qa))
        
        conn.commit()
        print("\n✅ Sample data added successfully!")
        print(f"   Email: test@example.com")
        print(f"   Password: password123")
    except sqlite3.IntegrityError:
        print("\n⚠️  Sample data already exists")
    
    conn.close()

def reset_database():
    """Drop all tables and recreate them"""
    conn = sqlite3.connect('smart_notes.db')
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS summaries")
    cursor.execute("DROP TABLE IF EXISTS users")
    
    conn.commit()
    conn.close()
    
    print("🗑️  Database reset complete")
    create_database()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        create_database()
    
    # Uncomment to add sample data
    # add_sample_data()