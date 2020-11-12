import tkinter as tk
import tkinter.messagebox
import random
gameOpen = None

class cellFrame():  # --------------------------------------- this is each cell that holds a button ------------------------------------------
    def __init__(self, rowPosition, colPosition, masterFrame, window,edgeDict,rowX,bombCount):
        self.window = window
        self.rowPosition = rowPosition
        self.colPosition = colPosition
        self.edgeDict = edgeDict
        self.rowX = rowX
        self.bombCount = bombCount
        self.frame = tk.Frame(masterFrame, width=26, height=26, highlightbackground="gray", highlightthickness=1, bg="dark grey")
        self.frame.grid(row=self.rowPosition, column=self.colPosition, padx=0, pady=0)
        self.frame.grid_propagate(0)
        self.button = tk.Button(self.frame, text="", width=2, height=1)
        self.button.grid(padx=0, pady=0)

    isBomb = False
    adjacentBombs = 0
    revealed = False
    lost = False
    # these below are empty because the information they represent can't be passed when the object is created because it isn't in memory yet
    # these values must be set accurately or the program will act strangely, if not crashing outright
    thisCellIndex = None
    buttonList = []

    # set the button type
    def bomb(self):
        self.button.configure(command=lambda: end(self.window, self.buttonList,False))
        self.isBomb = True

    def empty(self):
        self.button.configure(command=lambda: self.showArea())

    def show(self):
        self.button.grid_forget()
        self.revealed = True
        if self.isBomb:
            label = tk.Label(self.frame, text="*", bg="red", highlightbackground="grey", highlightthickness=1)
            self.frame.configure(bg="red")
            label.grid(padx=0, pady=0)
        elif self.adjacentBombs > 0:
            label = tk.Label(self.frame, text=self.adjacentBombs,bg="dark grey", highlightbackground="grey", highlightthickness=1)
            label.grid(padx=0, pady=0)

    def showArea(self):
        if self.adjacentBombs > 0:  # if the cell is adjacent to bomb it only reveals itself
            self.show()
        else:
            showlist = [self.thisCellIndex]  # get cells immediately adjacent to THIS cell + itself and puts it in a list
            for cell in adjacentCellList(self.thisCellIndex, self.edgeDict, self.rowX):
                if not self.buttonList[cell].getBombStatus() and self.buttonList[cell].getAdjacentBombs() == 0:
                    showlist.append(cell)

            for cell in showlist: # get adjacent cells that are not bombs nor adjacent to them and adds them to the list
                addList = []
                for addCell in adjacentCellList(self.buttonList[cell].getIndex(), self.edgeDict, self.rowX):
                    if not self.buttonList[addCell].getBombStatus() and self.buttonList[addCell].getAdjacentBombs() == 0:
                        addList.append(addCell)
                for i in addList:
                    if i not in showlist:  # because this is done while in a loop, the appended numbers will also be checked
                        showlist.append(i)

            addAdjCell = []
            for cell in showlist: # get adjacent cells that are not bombs BUT ARE adjacent to them and adds them to a new list
                for addCell in adjacentCellList(self.buttonList[cell].getIndex(), self.edgeDict, self.rowX):
                    if not self.buttonList[addCell].getBombStatus():
                        if addCell not in showlist:
                            addAdjCell.append(addCell) # a new lits is used to prevent the program from checking added cells
            showlist = showlist + addAdjCell

            for cell in showlist: # for each cell run it's show function
                self.buttonList[cell].show()

        revealedCount = 0  # if all non-bomb are shown, win the game
        for cell in self.buttonList:
            if cell.getRevealed():
                revealedCount = revealedCount + 1
        if revealedCount == len(self.buttonList) - self.bombCount:
            end(self.window, self.buttonList, True)


    # set

    def setAdjacentBombs(self,number):
        self.adjacentBombs = number

    def setThisCellIndex(self,number):
        self.thisCellIndex = number

    def setButtonList(self,list):
        self.buttonList = list

    def setCellCount(self,number):
        self.cellCount = number

    # get

    def getBombStatus(self):
        return self.isBomb

    def getButton(self):
        return self.button

    def getIndex(self):
        return self.thisCellIndex

    def getAdjacentBombs(self):
        return  self.adjacentBombs

    def getCellFrame(self):
        return self.frame

    def getRevealed(self):
        return self.revealed

# --------------------------------------------------------- Game Window -------------------------------------------------------------------

def createGameWindow(rowX, columnY,numberOfBombs):
    gameWindow = tk.Toplevel()
    time.set(0)
    global gameOpen
    gameOpen = True

    infoFrame = tk.Frame(gameWindow,width=columnY*25,height=28)
    infoFrame.pack(side="top")
    infoFrame.pack_propagate(0)

    timeLable = tk.Label(infoFrame, textvariable=timeDisplay)
    timeLable.pack(side="left")
    infoFrame.pack_propagate(0)

    bombCount = tk.Label(infoFrame, text="Bombs left: {}".format(numberOfBombs), justify="center")
    bombCount.pack(side="right")

    gridFrame = tk.Frame(gameWindow,pady=int(rowX*.5))
    gridFrame.pack(side="bottom")
    gameWindow.title("minesweeper")

    # ----------- find edge cells
    edgeDict = {
        "leftColumn" : [],
        "rightColumn" : [],
        "topRow" : [],
        "bottomRow" : []
    }
    for i in range(rowX):
        edgeDict["leftColumn"].append(i*rowX) # left column
        edgeDict["rightColumn"].append(i*rowX+rowX-1) # right column
        edgeDict["topRow"].append(i) # top row
        edgeDict["bottomRow"].append((rowX*columnY-1)-i) # bottom row

    # ------------- create list of cells
    buttonList = []
    for row in range(rowX):
        for column in range(columnY):
            frameToCreate = cellFrame(row, column, gridFrame, gameWindow,edgeDict,rowX,numberOfBombs)
            buttonList.append(frameToCreate)

    # ----- give cells their index's, the list, and the count of list
    for cell in buttonList:
        cell.setThisCellIndex(buttonList.index(cell))
        cell.setButtonList(buttonList)
        cell.setCellCount(len(buttonList))

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
        adjBombs = 0
        if cell.isBomb:
            continue
        else:
            checkList = adjacentCellList(cellIndex,edgeDict,rowX)
        for x in checkList:
            if buttonList[x].isBomb:
                adjBombs = 1 + adjBombs
        if adjBombs > 0:
            adjacentCells.append(cellIndex)
            buttonList[cellIndex].setAdjacentBombs(adjBombs)
            buttonList[cellIndex].empty()

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
    gameWindow.geometry(centerWindow(columnY * 28, (rowX * 28)+28))
    gameWindow.protocol("WM_DELETE_WINDOW", lambda: closeGameWindow(gameWindow))
    timer()


# ------------------------------------------------------- Game End Window ----------------------------------------------------
def end(window, buttonList,won):
    endText = ""

    if won:
        endText = "Win"
    else:
        endText = "Lost"
        for cell in buttonList:
            cell.show()

    global gameOpen
    gameOpen = False
    loseWindow = tk.Toplevel()
    loseWindow.title("You Lost")
    loseWindow.geometry(centerWindow(200, 300))
    loseWindow.resizable(0, 0)
    loseWindow.overrideredirect(True)

    textFrame = tk.Frame(loseWindow)
    textFrame.pack(side="top")

    buttonFrame = tk.Frame(loseWindow)
    buttonFrame.pack(side="bottom")

    gameStats = tk.Label(textFrame, text="You {} \ninfo will go here".format(endText), justify="center")
    gameStats.pack()

    buttonMainMenu = tk.Button(buttonFrame,text="Main Menu",command=lambda:returnToMainMenu(window,loseWindow))
    buttonMainMenu.pack(side="left")
    buttonQuit = tk.Button(buttonFrame,text="Quit",command=lambda:quitGame(window,loseWindow))
    buttonQuit.pack(side="right")


# -------------------------------------------------------- Close window functions ------------------------------------------

def closeGameWindow(window):
    if tk.messagebox.askokcancel("Quit Game?", "Do you want to quit this game?"):
        window.destroy()
        global gameOpen
        gameOpen = False
        root.deiconify()

def quitGame(*args):
    if tk.messagebox.askokcancel("Quit Minesweeper?", "Are you sure you want to quit?"):
        root.destroy()
        try:
            for w in args:
                w.destroy()
        except:
            print("failed to close window")

def returnToMainMenu(gameWindow,scoreWindow):
    gameWindow.destroy()
    scoreWindow.destroy()
    global gameOpen
    gameOpen = False
    root.deiconify()


# ------------------------------------------------------ Other Functions -------------------------------------------

def centerWindow(width, length):
    screenWidth = root.winfo_screenwidth()
    screenLength = root.winfo_screenheight()

    screenX = int((screenWidth / 2) - (width / 2))
    screenY = int((screenLength / 2) - (length / 2))

    return "%dx%d+%d+%d" % (width, length, screenX, screenY)

def timer():
    time.set(time.get()+1)
    min = int(time.get()/60)
    sec = int(time.get()%60)
    timeDisplay.set("{:02d}:{:02d}".format(min,sec))
    if gameOpen:
        root.after(1000, timer)  # call this function again in 1,000 milliseconds

def adjacentCellList(cellIndex,edgeDict,rowX):
    checkList = []
    sideDict = {
        "top": True,
        "bottom": True,
        "left": True,
        "right": True
    }
    if cellIndex not in edgeDict["leftColumn"]:  # check left of cell
        checkList.append(cellIndex - 1)
        sideDict["left"] = False
    if cellIndex not in edgeDict["rightColumn"]:  # check right of cell
        checkList.append(cellIndex + 1)
        sideDict["right"] = False
    if cellIndex not in edgeDict["topRow"]:  # check above cell
        checkList.append(cellIndex - rowX)
        sideDict["top"] = False
    if cellIndex not in edgeDict["bottomRow"]:  # check below cell
        checkList.append(cellIndex + rowX)
        sideDict["bottom"] = False
    if not sideDict["top"] and not sideDict["left"]:  # top left cell
        checkList.append(cellIndex - rowX - 1)
    if not sideDict["top"] and not sideDict["right"]:  # top right cell
        checkList.append(cellIndex - rowX + 1)
    if not sideDict["bottom"] and not sideDict["left"]:  # bottom left cell
        checkList.append(cellIndex + rowX - 1)
    if not sideDict["bottom"] and not sideDict["right"]:  # bottom left cell
        checkList.append(cellIndex + rowX + 1)
    return checkList


# --------------------------------------------------------- Root window ------------------------------------------------
root = tk.Tk()
newGameButton = tk.Button(text="New game", command=lambda: createGameWindow(15, 15 , 10))
newGameButton.pack()

# screen size - center widows

root.title("minesweeper")
root.geometry(centerWindow(400, 200))
root.resizable(0, 0)
root.protocol("WM_DELETE_WINDOW", lambda: quitGame())
time = tk.IntVar()
timeDisplay = tk.StringVar()
timeDisplay.set("00:00")
root.mainloop()
