import psycopg2

TOKEN = 'TOKEN_HERE'
MAIN_ADMIN_ID = 832997789

conn = psycopg2.connect(host="localhost", port=5432, database="", user="", password="")
cur = conn.cursor()
print("Database opened successfully")