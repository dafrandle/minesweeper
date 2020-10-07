import tkinter as tk


class gridFrame():
    def __init__(self, rowPosition, colPosition, masterFrame):
        self.rowPosition = rowPosition
        self.colPosition = colPosition
        self.frame = tk.Frame(masterFrame, width=30, height=30, highlightbackground="gray", highlightthickness=1, bg="dark grey")
        self.frame.grid(row=self.rowPosition, column=self.colPosition, padx=0, pady=0)

    def hideButton(self, button):
        button.grid_forget()

    def bomb(self):
        button = tk.Button(self.frame, text="", width=2, height=1, command=lambda:self.hideButton(button))
        button.grid(padx=1, pady=1)

    def adjacentToBomb(self, numberOfBombs):
        button = tk.Button(self.frame, text=numberOfBombs, width=2, height=1, command=lambda:self.hideButton(button))
        button.grid(padx=0, pady=0)

    def empty(self):
        button = tk.Button(self.frame, text="-", width=2, height=1, command=lambda:self.hideButton(button))
        button.grid(padx=0, pady=0)

def startGame(rowX, columnY):
    gameWindow = tk.Tk()
    cellFrame = tk.Frame(gameWindow)
    cellFrame.pack()
    gameWindow.title("minesweeper")
    gameWindow.resizable(0, 0)

    buttonList = []
    for row in range(rowX):
        for column in range(columnY):
            frameToCreate = gridFrame(row, column, cellFrame)
            buttonList.append(frameToCreate)

    for x in buttonList:
        x.bomb()

root = tk.Tk()
newGameButton = tk.Button(text="New game",command=lambda:startGame(15,15))
newGameButton.pack()




root.mainloop()
