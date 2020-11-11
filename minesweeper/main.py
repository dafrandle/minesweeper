import tkinter as tk
import tkinter.messagebox
import random


class cellFrame():  # --------------------------------------- this is each cell that holds a button ------------------------------------------
    isBomb = False
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
        self.isBomb = True

    def adjacentToBomb(self,numberOfBombs):
        button = tk.Button(self.frame, text=numberOfBombs, width=2, height=1, command=lambda: self.hideButton(button))
        button.grid(padx=0, pady=0)

    def empty(self):
        button = tk.Button(self.frame, text="", width=2, height=1, command=lambda: self.hideButton(button))
        button.grid(padx=0, pady=0)

    def getBombStatus(self):
        return self.isBomb

# --------------------------------------------------------- Game Window -------------------------------------------------------------------

def createGameWindow(rowX, columnY,numberOfBombs):
    gameWindow = tk.Tk()
    gridFrame = tk.Frame(gameWindow,pady=int(rowX*.5))
    gridFrame.pack()
    gameWindow.title("minesweeper")

    # ------------- create list of cells
    buttonList = []
    for row in range(rowX):
        for column in range(columnY):
            frameToCreate = cellFrame(row, column, gridFrame, gameWindow)
            buttonList.append(frameToCreate)

    # ----------- find edge cells
    leftColumn = []
    rightColumn = []
    topRow = []
    bottomRow = []
    for i in range(rowX):
        leftColumn.append(i*rowX) # left column
        rightColumn.append(i*rowX+rowX-1) # right column
        topRow.append(i) # top row
        bottomRow.append((rowX*columnY-1)-i) # bottom row


    # ------------- bomb cell list
    bombListSize = numberOfBombs
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

    # -------------- create list adjacent cells
    adjacentCells = []
    for cell in buttonList:
        cellIndex = buttonList.index(cell)
        checkList = []
        top = True
        bottom = True
        left = True
        right = True
        adjBombs = 0
        if cell.isBomb:
            continue
        else:
            if cellIndex not in leftColumn: # check left of cell
                checkList.append(cellIndex - 1)
                left = False
            if cellIndex not in rightColumn: # check right of cell
                checkList.append(cellIndex + 1)
                right = False
            if cellIndex not in topRow: # check above cell
                checkList.append(cellIndex - rowX)
                top = False
            if cellIndex not in bottomRow: # check below cell
                checkList.append(cellIndex + rowX)
                bottom = False
            if not top and not left: # top left cell
                checkList.append(cellIndex - rowX - 1)
            if not top and not right: # top right cell
                checkList.append(cellIndex - rowX + 1)
            if not bottom and not left: # bottom left cell
                checkList.append(cellIndex + rowX - 1)
            if not bottom and not right: # bottom left cell
                checkList.append(cellIndex + rowX + 1)
        for x in checkList:
            if buttonList[x].isBomb:
                adjBombs = 1 + adjBombs
        if adjBombs > 0:
            adjacentCells.append(cellIndex)
            buttonList[cellIndex].adjacentToBomb(adjBombs)

    # -------------- normal cell list
    for x in buttonList:
        tile = buttonList.index(x)
        if tile in bombList:
            continue
        if tile in adjacentCells:
            continue
        else:
            x.empty()

    # --- draw game window
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
newGameButton = tk.Button(text="New game", command=lambda: createGameWindow(15, 15 , 40))
newGameButton.pack()

# screen size - center widows

root.title("minesweeper")
root.geometry(CenterWindow(400, 200))
root.resizable(0, 0)
root.protocol("WM_DELETE_WINDOW", lambda: quitGame())
root.mainloop()
