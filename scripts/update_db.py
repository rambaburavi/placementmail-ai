import sqlite3

conn = sqlite3.connect("placementmail.db")

cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE emails ADD COLUMN ai_provider TEXT"
    )
    print("✅ ai_provider added")
except Exception as e:
    print(e)

try:
    cursor.execute(
        "ALTER TABLE emails ADD COLUMN analysis_status TEXT"
    )
    print("✅ analysis_status added")
except Exception as e:
    print(e)

conn.commit()
conn.close()

print("✅ Database Updated")