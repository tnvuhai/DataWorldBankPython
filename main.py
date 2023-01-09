from tkinter import *
import tkinter as tk
from tkinter import messagebox,ttk
from pandastable import Table
import wbgapi as wb
import pandas as pd
from tkinter import filedialog

IDSelectedStr = ""

def InitialLoad():
    return pd.DataFrame(wb.series.list())

def SearchNameIndicators(df):
    try:
        SearchStr = str(SearchEntry.get())
        newDf = df[df.value.str.contains(SearchStr,regex=True)]
        pt.model.df = newDf
        pt.redraw()
    except Exception as e:
        messagebox.showerror("Error", "Error found:" + str(e))

def TrackIDSelected(e):
    typed = str(IDSelected.get(1.0,END))
    typed = typed.replace("\n", "")
    global IDSelectedStr
    IDSelectedStr = typed


def CADAction():
    global IDSelectedStr
    def exportFile():
        SaveFileString = """Your excel file's location is"""
        try:
            File = filedialog.askdirectory()
            UserSetFile = str(NameExportText.get(1.0,END))
            UserSetFile = UserSetFile.replace("\n", "")
            FileName = f"{UserSetFile}.xlsx"
            pt.doExport(filename=f"{File}/{FileName}")
            ExportDf = pt.model.df
            ExportDf.to_excel(File + "/" + FileName, engine='xlsxwriter')
            messagebox.showinfo("Notification", f"Export file successfully!\n"
                                                f"{SaveFileString}: {File}/{FileName}")
            print(File + "/" + FileName)
        except Exception as e:
            messagebox.showerror("Error", "Error found:" + str(e))

    def configureApp():
        for i in range(0, 3):
            rootCAD.columnconfigure(i, weight=2, minsize=50)
        for i in range(0, 4):
            rootCAD.rowconfigure(i, weight=2, minsize=50)
        # Column 0
        TopLabel.grid(row=0, column=0,columnspan = 4, sticky='')
        f.grid(row=1, column=0, columnspan=2, rowspan=6)

        # Column 2
        NameExportLabel.grid(row=1, column=2)
        NameExportText.grid(row=2, column=2)
        ImportButton.grid(row=3, column=2)

    rootCAD = tk.Toplevel()
    rootCAD.title("CAD ACTION")
    rootCAD.geometry('960x650')
    TopLabel = tk.Label(rootCAD,text = "CONFIG AND DOWNLOAD SELECTED DATA", font = ("bold",16))
    try:
        SelectedDf = pd.DataFrame()
        CountriesInput = CountriesCombobox.get()
        Start = int(YearStartText.get(1.0,END))
        End = int(YearEndText.get(1.0,END))
        print(IDSelectedStr)
        print(CountriesInput)
        print(f"\n{Start}-{End}")
        if (CountriesInput == "All countries"):
            SelectedDf = wb.data.DataFrame(IDSelectedStr,time=range(Start,End), labels=True, columns='series').reset_index()
        elif(CountriesInput == "ASEAN countries"):
            SelectedDf = wb.data.DataFrame(IDSelectedStr,'EAS',time=range(Start,End), labels=True, columns='series').reset_index()
        else:
            SelectedDf = wb.data.DataFrame(IDSelectedStr,['USA','MEX','CAN'],time=range(Start,End), labels=True, columns='series').reset_index()

    except Exception as e:
        messagebox.showerror("Error", "Error found:" + str(e))
    #SelectedDf = wb.data.DataFrame(IDSelectedStr,time=range(2000,2015),labels = True,columns='series').reset_index()
    f = Frame(rootCAD)
    pt = Table(f, dataframe=SelectedDf, showtoolbar=True, showstatusbar=True)
    pt.show()
    NameExportLabel = Label(rootCAD,text="Name of excel file:",font = ("bold", 15))
    NameExportText = Text(rootCAD,font = ("bold", 13),height = 2, width = 20)
    ImportButton = tk.Button(rootCAD, text = "Save excel file",font = ("bold",12),command=exportFile)
    configureApp()
    mainloop()




def configureApp():
    try:
        for i in range(0, 3):
            window.columnconfigure(i, weight=2, minsize=50)
        for i in range(0, 7):
            window.rowconfigure(i, weight=1, minsize=60)

        # Layout column 0
        GeneralLabel.grid(row = 0, column = 0, columnspan = 4,sticky = "")
        SearchEntry.grid(row=1, column=0,columnspan=2,sticky="W",padx=45)
        f.grid(row = 2, column = 0,columnspan = 2,rowspan = 5)

        # Layout column 1
        SearchDataButton.grid(row=1, column=1)

        # Layout column 2
        IDSelectedLabel.grid(row = 1, column =2)
        IDSelected.grid(row = 2, column =2)

        YearStartEndLabel.grid(row=3, column=2)
        YearStartText.grid(row=4, column=2, sticky="W",padx=45)
        strikethroughLabel.grid(row=4, column=2, sticky="")
        YearEndText.grid(row=4, column=2, sticky="E",padx=45)
        CountriesComboboxLabel.grid(row=5, column=2, sticky="W")
        CountriesCombobox.grid(row=5, column=2,sticky="E",padx=50)

        ConfigAndDownload.grid(row=6, column=2)

    except Exception as e:
        messagebox.showerror("Error", "Error found:" + str(e))


window = tk.Tk()
window.title("APP WBGAPI")
window.geometry('960x650')

GeneralLabel = tk.Label(text="APP FOR SEARCHING AND DOWNLOADING DATA FROM DATA.WORLDBANK.ORG", font=("bold", 15), padx=40, pady=50)
f = Frame(window)
EnglishLabel = tk.Label(text="Searching data", font=("bold", 16))
SearchEntry = Entry(window, font=("TimeNewRoman",14),width=30)
df = InitialLoad()
SearchDataButton = tk.Button(window, text="Search",font=("bold", 14),command=lambda: SearchNameIndicators(df))
pt = Table(f, dataframe=df, showstatusbar=True)
pt.show()
IDSelectedLabel = tk.Label(text="ID Select:", font=("bold", 14))
IDSelected = Text(window,font = ("bold", 13),height = 2, width = 20)
YearStartEndLabel = Label(window,text = "Year Start and End", font = ("bold",14))
YearStartText = Text(window,font = ("bold", 13),height = 2, width = 10)
strikethroughLabel = Label(window,text = "-", font = ("bold",14))
YearEndText = Text(window,font = ("bold", 13),height = 2, width = 10)

CountriesComboboxLabel = Label(text="Countries select", font = ("bold",14))
CountriesCombobox = ttk.Combobox(window, state='readonly')
CountriesCombobox["values"] = ["All countries","ASEAN countries","NAFTA countries"]
CountriesCombobox.current(1)
ConfigAndDownload = tk.Button(window, text="Config and download selected data",font=("bold", 15),command=lambda: CADAction())


IDSelected.bind("<KeyRelease>",TrackIDSelected)
configureApp()
#launch the app
window.mainloop()