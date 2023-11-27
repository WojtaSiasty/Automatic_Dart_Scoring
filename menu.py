import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD, NORMAL, Font
class Menu():

    def __init__(self):
        self.turn = 1
        self.gamescore1 = 501
        self.gamescore2 = 501

        self.window = tk.Tk()
        self.window.title("Dart")
        self.window.geometry("400x400")
        
        self.label1 = ttk.Label(master = self.window, text = "Gracz 1")
        self.score1 = ttk.Label(master = self.window, text = self.gamescore1)
        self.label2 = ttk.Label(master = self.window, text = "Gracz 2")
        self.score2 = ttk.Label(master = self.window, text = self.gamescore2)
        self.hit1 = ttk.Entry(master = self.window)
        self.hit2 = ttk.Entry(master = self.window)
        self.hit3 = ttk.Entry(master = self.window)
        self.button = ttk.Button(master = self.window, text = "Następny Gracz", command = self.button_func)

        self.label1.config(font=Font(self.window, weight=BOLD))
        self.label2.config(font=Font(self.window, weight=NORMAL))

        self.hit1_updated = False
        self.hit2_updated = False
        self.hit3_updated = False

        self.hit1.insert(0,"0")
        self.hit2.insert(0,"0")
        self.hit3.insert(0,"0")

        self.window.columnconfigure((0,1,2), weight=1)
        self.window.rowconfigure((0,1,2,3,4,5,6), weight=1)

        self.label1.grid(row=0, column=0, sticky="s", pady=10)
        self.score1.grid(row=1, column=0, sticky="n")
        self.label2.grid(row=0, column=2, sticky="s", pady=10)
        self.score2.grid(row=1, column=2, sticky="n")

        self.hit1.grid(row=2, column=1)
        self.hit2.grid(row=3, column=1)
        self.hit3.grid(row=4, column=1)

        self.button.grid(row=6, column=1, sticky="n")

    def button_func(self):
        hit1_value = int(self.hit1.get())
        hit2_value = int(self.hit2.get())
        hit3_value = int(self.hit3.get())
        score = hit1_value + hit2_value + hit3_value

        if self.turn == 1:
            self.label2.config(font=Font(self.window, weight=BOLD))
            self.label1.config(font=Font(self.window, weight=NORMAL))
            if self.gamescore1 == score:
                self.show_winner(1)

            if score < self.gamescore1:
                self.gamescore1 -= score
                self.score1.config(text=self.gamescore1)

            self.turn = 2
        else:
            self.label1.config(font=Font(self.window, weight=BOLD))
            self.label2.config(font=Font(self.window, weight=NORMAL))
            if self.gamescore2 == score:
                self.show_winner(2)

            if score < self.gamescore2:
                self.gamescore2 -= score
                self.score2.config(text=self.gamescore2)

            self.turn = 1

        self.hit1.delete(0, tk.END)
        self.hit2.delete(0, tk.END)
        self.hit3.delete(0, tk.END)

        self.hit1.insert(0,"0")
        self.hit2.insert(0,"0")
        self.hit3.insert(0,"0")

        self.hit1_updated = False
        self.hit2_updated = False
        self.hit3_updated = False

    def show_winner(self, player):
        self.window.destroy()
        messagebox.showinfo("Koniec gry!", f"Gracz nr {player} wygrał!")


    def window_exist(self):
        try:
            return self.window.winfo_exists()
        except:
            return False
    
    def add_button_event(self, func):
        self.button.bind('<ButtonPress>', func, True)

    def update_hit(self, number, value):
        if value == None:
            value = 0
        if number == 1 and not self.hit1_updated:
            self.hit1.delete(0, tk.END)
            self.hit1.insert(0, str(value))
            self.hit1_updated = True
        elif number == 2 and not self.hit2_updated:
            self.hit2.delete(0, tk.END)
            self.hit2.insert(0, str(value))
            self.hit2_updated = True
        elif number == 3 and not self.hit3_updated:
            self.hit3.delete(0, tk.END)
            self.hit3.insert(0, str(value))
            self.hit3_updated = True