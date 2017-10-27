import sqlite3
import datetime

conn = sqlite3.connect("/home/pi/Alarmsysteem/alarm_database")
c = conn.cursor()

tijd = datetime.datetime.now().strftime("%H:%M:%S")
print(tijd)

c.execute(
        'UPDATE alarmering SET alarm = 1, time = ? WHERE alarm_nr = 1', (tijd,))

conn.commit()
conn.close()
