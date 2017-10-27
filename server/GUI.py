
from tkinter import *                        #imports everything from TKinter
import sqlite3
import datetime
import time
from sshConnect import sendCommand
import threading

kabelNietDoorgesneden = True


class Window(Frame):                         #creates window

    # geeft aan de database door dat de kolom alarm op true moet komen te staan
    def alarm_Activate(self):
        conn = sqlite3.connect("alarm_database")
        c = conn.cursor()

        print('Het alarm gaat nu af!')

        c.execute(
        'UPDATE alarmering SET alarm = 1 WHERE alarm_nr = 1')

        conn.commit()
        conn.close()

        #geeft aan de client door dat de lampjes op rood moet staan
        sendCommand("client.pi", "python3 /home/pi/Alarmsysteem/clientRed.py")

    # geeft aan de database door dat de kolom alarm op false moet komen te staan
    def alarm_Deactivate(self):
        conn = sqlite3.connect("alarm_database")
        c = conn.cursor()

        print('Het alarm gaat niet af.')

        c.execute(
        'UPDATE alarmering SET alarm = 0 WHERE alarm_nr = 1')

        conn.commit()
        conn.close()
        # geeft aan de client door dat de lampjes op groen moet staan
        sendCommand("client.pi", "python3 /home/pi/Alarmsysteem/clientGreen.py")


    # haalt de tijd en de alarmstatus op en bepaalt of het alarm getriggerd moet worden of niet
    def checkDatabase(self):
        conn = sqlite3.connect("alarm_database")
        c = conn.cursor()
        tijd = datetime.datetime.now().strftime("%H:%M:%S")

        print("De tijd van nu is: " + tijd)

        time_update = ""
        for row in c.execute('SELECT alarm, time FROM alarmering WHERE alarm_nr= 1'):
            alarm = row[0]
            time_update = row[1]
        conn.close()

        #zet de huidige tijd in seconden om
        tijd_list = tijd.split(":")
        tijd_sec = int(tijd_list[0]) * 60 * 60 + int(tijd_list[1]) * 60 + int(tijd_list[2])
        # zet de geupdate tijd in seconden om
        time_update_list = time_update.split(":")
        time_update_sec = int(time_update_list[0]) * 60 * 60 + int(time_update_list[1]) * 60 + int(time_update_list[2])
        #berekent het tijdsverschil
        tijdsverschil = time_update_sec - tijd_sec

        print(tijdsverschil)

        if tijdsverschil <= 30 and self.kabelNietDoorgesneden == False:
            self.kabelNietDoorgesneden = True

        #als het tijdsverschil groter dan 30 is, geef een alarm af, zo niet kijk naar de alarmstatus om door te geven
        if(tijdsverschil >=30 and self.kabelNietDoorgesneden == True):
            #TODO: signaal naar database/GUI!
            print("tijdsverschil bereikt!")
            self.kabelNietDoorgesneden = False
            self.alarm_Activate()
            return True
        else:
            return alarm




    def loopingDatabase(self):
        try:
            while True:
                #krijg de status van het alarm door
                alarm = self.checkDatabase()
                # als het alarm niet af gaat, zet de achtergrond op rood en verander de tekst
                # anders, zet de achtergrond op groen en verander de tekst
                if alarm == False:
                    self.kleurlabel['background'] = "green2"
                    self.label['text'] = 'Alarm gaat niet af.'
                else:
                    self.kleurlabel['background'] = "red"
                    self.label['text'] = 'Alarm gaat af!.'
                # update om de 1.5 seconden
                time.sleep(1.5)
                # voer de updates door naar het scherm
                root.update()
        except KeyboardInterrupt:
            print('interrupted!')


    def readDatabaseAgain(self):
        self.refreshButton['state'] = DISABLED
        # maakt nieuwe thread om de updates van de database op te halen
        threadUpdateTime = threading.Thread(target=self.loopingDatabase)
        threadUpdateTime.start()




    def __init__(self, master = None):                      #main window
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def init_window(self):
        self.kabelNietDoorgesneden = True
        self.master.title('Alarmsysteem')

        self.pack(fill=BOTH, expand = 1)

        # initialiseer alle buttons
        self.refreshButton = Button(self, background='white', text='Haal automatische updates op.', command=self.readDatabaseAgain)

        self.refreshButton.pack(side="top", fill='both', expand=True, padx=20, pady=10)


        alarmOn = Button(self, background='white', text='Alarm On', command=self.alarm_Activate)

        alarmOn.pack(side="top", fill='both', expand=True, padx=20, pady=10,)

        alarmOff = Button(self, background='white', text = 'Alarm Off', command=self.alarm_Deactivate)

        alarmOff.pack(side="top", fill='both', expand=True, padx=20, pady=10)

        # kijk welke status het alarm heeft en voer de layout daar op aan
        alarm = self.checkDatabase()

        if alarm == False:
            self.kleurlabel = Label(background='green2')
            self.kleurlabel.pack(fill=X)
            self.label = Label(text='Alarm gaat niet af.', pady = 20, background='white')
            self.label.pack()
        else:
            self.kleurlabel = Label(background='red')
            self.kleurlabel.pack(fill=X)
            self.label = Label(text='Alarm gaat af!', pady = 20, background='white')
            self.label.pack()



root = Tk()

root.configure(background='white')
root.geometry('400x300')
app = Window(root)

root.mainloop()