import mysql.connector

def insert_mood_log(user_input, mood, reason, suggestion):
    try:
        conn = mysql.connector.connect(
            host="localhost",         # Change if using external DB
            user="root",              # Your MySQL username
            password="pRADEEP2001@", # Replace with your MySQL password
            database="mental_health_bot"
        )
        cursor = conn.cursor()

        sql = """
        INSERT INTO mood_logs (user_input, mood, reason, suggestion)
        VALUES (%s, %s, %s, %s)
        """
        values = (user_input, mood, reason, suggestion)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("Mood log inserted into database.")
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
