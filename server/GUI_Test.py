
from tkinter import *                        #imports everything from TKinter
import sqlite3
import datetime
import time



class Window(Frame):                         #creates window

    def alarm_Activate(self):
        conn = sqlite3.connect("alarm_database")
        c = conn.cursor()

        tijd = datetime.datetime.now().strftime("%H:%M:%S")
        print('Het alarm gaat nu af!')

        c.execute(
        'UPDATE alarmering SET alarm = 1 WHERE alarm_nr = 1')

        conn.commit()
        conn.close()

    def alarm_Deactivate(self):
        conn = sqlite3.connect("alarm_database")
        c = conn.cursor()

        tijd = datetime.datetime.now().strftime("%H:%M:%S")
        print('Het alarm gaat niet af.')

        c.execute(
        'UPDATE alarmering SET alarm = 0 WHERE alarm_nr = 1')

        conn.commit()
        conn.close()


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

        tijd_list = tijd.split(":")
        tijd_sec = int(tijd_list[0]) * 60 * 60 + int(tijd_list[1]) * 60 + int(tijd_list[2])

        time_update_list = time_update.split(":")
        time_update_sec = int(time_update_list[0]) * 60 * 60 + int(time_update_list[1]) * 60 + int(time_update_list[2])

        tijdsverschil = time_update_sec - tijd_sec

        print(tijdsverschil)

        if(tijdsverschil >=30):
            #TODO: signaal naar database/GUI!
            print("tijdsverschil bereikt!")
            return True
        else:
            return alarm

    def readDatabaseAgain(self):
        self.refreshButton['state'] = DISABLED
        try:
            while True:
                alarm = self.checkDatabase()
                if alarm == False:
                    self.kleurlabel['background'] = "green2"
                    self.label['text'] = 'Alarm gaat niet af.'
                else:
                    self.kleurlabel['background'] = "red"
                    self.label['text'] = 'Alarm gaat af!.'
                time.sleep(1.5)
                root.update()
        except KeyboardInterrupt:
            print('interrupted!')


    def __init__(self, master = None):                      #main window
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def init_window(self):

        self.master.title('Alarmsysteem')

        self.pack(fill=BOTH, expand = 1)


        self.refreshButton = Button(self, background='white', text='Haal automatische updates op.', command=self.readDatabaseAgain)

        self.refreshButton.pack(side="top", fill='both', expand=True, padx=20, pady=10)


        alarmOn = Button(self, background='white', text='Alarm On', command=self.alarm_Activate)

        alarmOn.pack(side="top", fill='both', expand=True, padx=20, pady=10,)

        alarmOff = Button(self, background='white', text = 'Alarm Off', command=self.alarm_Deactivate)

        alarmOff.pack(side="top", fill='both', expand=True, padx=20, pady=10)


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


    def exit_window(self):
        exit()



root = Tk()

root.configure(background='white')
root.geometry('400x300')
app = Window(root)

root.mainloop()




