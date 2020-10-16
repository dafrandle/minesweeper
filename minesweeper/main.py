import tkinter as tk
import tkinter.messagebox
import random


class cellFrame():  # --------------------------------------- this is each cell that holds a button ------------------------------------------
    def __init__(self, rowPosition, colPosition, masterFrame, window):
        self.window = window
        self.rowPosition = rowPosition
        self.colPosition = colPosition
        self.frame = tk.Frame(masterFrame, width=30, height=30, highlightbackground="gray", highlightthickness=1, bg="dark grey")
        self.frame.grid(row=self.rowPosition, column=self.colPosition, padx=0, pady=0)

    def hideButton(self, button):
        button.grid_forget()

    def bomb(self):
        button = tk.Button(self.frame, text="*", width=2, height=1, command=lambda: lose(self.window))
        button.grid(padx=1, pady=1)

    def adjacentToBomb(self, numberOfBombs):
        button = tk.Button(self.frame, text=numberOfBombs, width=2, height=1, command=lambda: self.hideButton(button))
        button.grid(padx=0, pady=0)

    def empty(self):
        button = tk.Button(self.frame, text=" ", width=2, height=1, command=lambda: self.hideButton(button))
        button.grid(padx=0, pady=0)


# --------------------------------------------------------- Game Window -------------------------------------------------------------------

def createGameWindow(rowX, columnY):
    gameWindow = tk.Tk()
    gridFrame = tk.Frame(gameWindow,pady=int(rowX*.5))
    gridFrame.pack()
    gameWindow.title("minesweeper")

    buttonList = []
    for row in range(rowX):
        for column in range(columnY):
            frameToCreate = cellFrame(row, column, gridFrame, gameWindow)
            buttonList.append(frameToCreate)

    bombListSize = 10
    bombList = []
    i = 0
    while i < bombListSize:
        randomTitle = random.randint(0, (rowX * columnY) - 1)
        if randomTitle in bombList:  # prevents duplicates
            continue
        else:
            bombList.append(randomTitle)
            i = i + 1

    for t in bombList:
        buttonList[t].bomb()

    for x in buttonList:
        tile = buttonList.index(x)
        if tile in bombList:
            continue
        else:
            x.empty()
    root.withdraw()
    gameWindow.resizable(0, 0)
    gameWindow.geometry(CenterWindow(columnY*30,rowX*30))
    gameWindow.protocol("WM_DELETE_WINDOW", lambda: closeGameWindow(gameWindow))


# ------------------------------------------------------- Lose Window ----------------------------------------------------
def lose(window):
    loseWindow = tk.Tk()
    loseWindow.title("You Lost")
    loseWindow.geometry(CenterWindow(200, 300))
    loseWindow.resizable(0, 0)
    loseWindow.overrideredirect(True)

    textFrame = tk.Frame(loseWindow)
    textFrame.pack(side="top")

    buttonFrame = tk.Frame(loseWindow)
    buttonFrame.pack(side="bottom")

    gameStats = tk.Label(textFrame, text="You Lost \ninfo will go here", justify="center")
    gameStats.pack()

    buttonMainMenu = tk.Button(buttonFrame,text="Main Menu",command=lambda:returnToMainMenu(window,loseWindow))
    buttonMainMenu.pack(side="left")
    buttonQuit = tk.Button(buttonFrame,text="Quit",command=lambda:quitGame(window,loseWindow))
    buttonQuit.pack(side="right")


# -------------------------------------------------------- Close window functions ------------------------------------------

def closeGameWindow(window):
    if tk.messagebox.askokcancel("Quit Game?", "Do you want to quit this game?"):
        window.destroy()
        root.deiconify()

def quitGame(*args):
    if tk.messagebox.askokcancel("Quit Minesweeper?", "Are you sure you want to quit?"):
        root.destroy()
        try:
            for w in args:
                w.destroy()
        except:
            print(w.type)
            print("failed to close window")

def returnToMainMenu(gameWindow,scoreWindow):
    gameWindow.destroy()
    scoreWindow.destroy()
    root.deiconify()


# ------------------------------------------------------ Other Functions -------------------------------------------

def CenterWindow(width, length):
    screenWidth = root.winfo_screenwidth()
    screenLength = root.winfo_screenheight()

    screenX = int((screenWidth / 2) - (width / 2))
    screenY = int((screenLength / 2) - (length / 2))

    return "%dx%d+%d+%d" % (width, length, screenX, screenY)





# --------------------------------------------------------- Root window ------------------------------------------------
root = tk.Tk()
newGameButton = tk.Button(text="New game", command=lambda: createGameWindow(15, 15))
newGameButton.pack()

# screen size - center widows

root.title("minesweeper")
root.geometry(CenterWindow(400, 200))
root.resizable(0, 0)
root.protocol("WM_DELETE_WINDOW", lambda: quitGame())
root.mainloop()
