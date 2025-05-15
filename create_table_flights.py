import psycopg2
import os

DATABASE_URL = os.getenv('DATABASE_URL')

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create table
cur.execute('''
CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,
    flight_number TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL
);
''')

conn.commit()
cur.close()
conn.close()

print("Table created successfully.")
