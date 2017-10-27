import sqlite3
import datetime

#TODO: try error
conn = sqlite3.connect("/home/pi/Alarmsysteem/alarm_database")
c = conn.cursor()

tijd = datetime.datetime.now().strftime("%H:%M:%S")
print(tijd)

c.execute(
        'UPDATE alarmering SET time = ? WHERE alarm_nr = 1', (tijd,))

conn.commit()
conn.close()