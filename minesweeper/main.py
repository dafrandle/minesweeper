import tkinter as tk

# root = tk.Tk()
# root.resizable(0, 0)
# root.geometry('800x800')
#
# frameGridBase = tk.Frame(root,height = 20,width = 20, highlightbackground = "black", highlightthickness = 1)
# frameGridBase.grid()
#
#
#
# root.mainloop()




class gridButtons():
    def __init__(self,rowPosition, colPosition,masterFrame):
        self.rowPosition = rowPosition
        self.colPosition = colPosition

        self.button = tk.Button(masterFrame,width=2,height=1)
        self.button.grid(row = self.rowPosition,column = self.colPosition,padx=0, pady=0)

root = tk.Tk()
buttonFrame = tk.Frame(root)
buttonFrame.pack()
root.title("minesweeper")

buttonList = []
for r in range(10):
    for c in range(10):
        buttonToCreate = gridButtons(r,c,buttonFrame)
        buttonList.append(buttonToCreate)
root.mainloop()