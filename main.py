from tkinter import *
import tkinter as tk
from tkinter import messagebox
from pandastable import Table, TableModel

def configureApp():
    try:
        for i in range(0, 3):
            window.columnconfigure(i, weight=2, minsize=50)
        for i in range(0, 4):
            window.rowconfigure(i, weight=1, minsize=60)

        # Layout column 0
        GeneralLabel.grid(row = 0, column = 0, columnspan = 4,sticky = "")
        SearchEntry.grid(row=1, column=0,columnspan=2,sticky="W",padx=45)
        f.grid(row = 2, column = 0,columnspan = 2)

        # Layout column 1
        SearchDataButton.grid(row=1, column=1)



    except Exception as e:
        messagebox.showerror("Lỗi", "Phát hiện lỗi:" + str(e))


window = tk.Tk()
window.title("APP WBGAPI")
window.geometry('960x650')

GeneralLabel = tk.Label(text="APP FOR SEARCHING AND DOWNLOADING DATA FROM DATA.WORLDBANK.ORG", font=("bold", 15), padx=40, pady=50)
f = Frame(window)
EnglishLabel = tk.Label(text="Searching data", font=("bold", 16))
SearchEntry = Entry(window, font=("TimeNewRoman",14),width=30)
SearchDataButton = tk.Button(window, text="Search",font=("bold", 14))
df = TableModel.getSampleData()
pt = Table(f, dataframe=df, showstatusbar=True)
#pt = Table(f, dataframe=df,showtoolbar=True, showstatusbar=True)
pt.show()
configureApp()
#launch the app
window.mainloop()