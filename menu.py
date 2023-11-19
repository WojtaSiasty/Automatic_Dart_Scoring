import tkinter as tk
from tkinter import ttk

class Menu():

    def __init__(self):
        self.turn = 1
        self.gamescore1 = 501
        self.gamescore2 = 501

        self.hit1_value = 0
        self.hit2_value = 0
        self.hit3_value = 0

        self.window = tk.Tk()
        self.window.title("Dart")
        self.window.geometry("400x400")

        label1 = ttk.Label(master = self.window, text = "Gracz 1")
        score1 = ttk.Label(master = self.window, text = self.gamescore1)
        label2 = ttk.Label(master = self.window, text = "Gracz 2")
        score2 = ttk.Label(master = self.window, text = self.gamescore2)
        self.hit1 = ttk.Entry(master = self.window, textvariable = self.hit1_value)
        self.hit2 = ttk.Entry(master = self.window, textvariable = self.hit2_value)
        self.hit3 = ttk.Entry(master = self.window, textvariable = self.hit3_value)
        button = ttk.Button(master = self.window, text = "Następny Gracz", command = self.button_func)


        self.window.columnconfigure((0,1,2), weight=1)
        self.window.rowconfigure((0,1,2,3,4,5,6), weight=1)

        label1.grid(row=0, column=0, sticky="s", pady=10)
        score1.grid(row=1, column=0, sticky="n")
        label2.grid(row=0, column=2, sticky="s", pady=10)
        score2.grid(row=1, column=2, sticky="n")

        self.hit1.grid(row=2, column=1)
        self.hit2.grid(row=3, column=1)
        self.hit3.grid(row=4, column=1)

        button.grid(row=6, column=1, sticky="n")

    def button_func(self):
        print("Button pressed")
        # if turn == 1:
        #     score = 

    # def get_window(self):
    #     return self.window

    def window_exist(self):
        try:
            return self.window.winfo_exists()
        except:
            return False
    
    def destroy(self):
        self.window.destroy()