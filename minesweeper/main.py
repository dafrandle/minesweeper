import tkinter as tk
import tkinter.messagebox
import random
import re

gameOpen = None


class cellFrame():  # --------------------------------------- this is each cell that holds a button ------------------------------------------
    def __init__(self, rowPosition, colPosition, masterFrame, window, edgeDict, rowX, columnY, bombCount):
        self.__window = window
        self.__rowPosition = rowPosition
        self.__colPosition = colPosition
        self.__edgeDict = edgeDict
        self.__rowX = rowX
        self.__columnY = columnY
        self.__bombCount = bombCount
        self.__frame = tk.Frame(masterFrame, width=26, height=26, highlightbackground="gray", highlightthickness=1,
                                bg="dark grey")
        self.__frame.grid(row=self.__rowPosition, column=self.__colPosition, padx=0, pady=0)
        self.__frame.grid_propagate(0)
        self.__button = tk.Button(self.__frame, text="", width=2, height=1, bg="light grey")
        self.__button.grid(padx=0, pady=0)

    __isBomb = False
    __adjacentBombs = 0
    __revealed = False
    __lost = False
    __flagged = False
    # these below are empty because the information they represent can't be passed when the object is created because it isn't in memory yet
    # these values must be set accurately or the program will act strangely, if not crashing outright
    __thisCellIndex = None
    __buttonList = []

    # set the button type
    def bomb(self):
        self.__button.configure(command=lambda: self.leftClickHandler(True))
        self.__isBomb = True

    def empty(self):
        self.__button.configure(command=lambda: self.leftClickHandler(False))

    def show(self):
        self.__button.grid_forget()
        self.__revealed = True
        if self.__isBomb:
            label = tk.Label(self.__frame, text="*", bg="red", highlightbackground="grey", highlightthickness=1)
            self.__frame.configure(bg="red")
            label.grid(padx=0, pady=0)
        elif self.__adjacentBombs > 0:
            label = tk.Label(self.__frame, text=self.__adjacentBombs, bg="dark grey", highlightbackground="grey",highlightthickness=1)
            label.grid(padx=0, pady=0)

    def showArea(self):
        if self.__adjacentBombs > 0:  # if the cell is adjacent to bomb it only reveals itself
            self.show()
        else:
            showlist = [
                self.__thisCellIndex]  # get cells immediately adjacent to THIS cell + itself and puts it in a list
            for cell in adjacentCellList(self.__thisCellIndex, self.__edgeDict, self.__columnY):
                if not self.__buttonList[cell].getBombStatus() and self.__buttonList[cell].getAdjacentBombs() == 0 and not self.__buttonList[cell].getFlagged():
                    showlist.append(cell)

            for cell in showlist:  # get adjacent cells that are not bombs (or flagged) nor adjacent to them and adds them to the list
                addList = []
                for addCell in adjacentCellList(self.__buttonList[cell].getIndex(), self.__edgeDict, self.__columnY):
                    if not self.__buttonList[addCell].getBombStatus() and self.__buttonList[addCell].getAdjacentBombs() == 0 and not self.__buttonList[addCell].getFlagged():
                        addList.append(addCell)
                for i in addList:
                    if i not in showlist:  # because this is done while in a loop, the appended numbers will also be checked
                        showlist.append(i)

            addAdjCell = []
            for cell in showlist:  # get adjacent cells that are not bombs (or flagged) BUT ARE adjacent to them and adds them to a new list
                for addCell in adjacentCellList(self.__buttonList[cell].getIndex(), self.__edgeDict, self.__columnY):
                    if not self.__buttonList[addCell].getBombStatus() and not self.__buttonList[addCell].getFlagged():
                        if addCell not in showlist:
                            addAdjCell.append(
                                addCell)  # a new lits is used to prevent the program from checking added cells
            showlist = showlist + addAdjCell

            for cell in showlist:  # for each cell run it's show function
                self.__buttonList[cell].show()

        revealedCount = 0  # if all non-bomb are shown, win the game
        for cell in self.__buttonList:
            if cell.getRevealed():
                revealedCount = revealedCount + 1
        flagTuple = checkFlags(self.__buttonList)
        if revealedCount == len(self.__buttonList) - self.__bombCount:
            end(self.__window, self.__buttonList, True, self.__rowX, self.__columnY, self.__bombCount, flagTuple[0], flagTuple[1])

    def flagCell(self):
        if self.__flagged:
            self.__flagged = False
            self.__button.configure(bg="light grey")
        else:
            self.__flagged = True
            self.__button.configure(bg="green")
        flaggedCount = 0
        for cell in self.__buttonList:
            if cell.getFlagged():
                flaggedCount = flaggedCount + 1
        bombsLeft.set("Bombs left: {}".format(self.__bombCount - flaggedCount))

    def leftClickHandler(self, isBomb):
        if not self.__flagged:
            if isBomb:
                flagTuple = checkFlags(self.__buttonList)
                end(self.__window, self.__buttonList, False, self.__rowX, self.__columnY, self.__bombCount, flagTuple[0], flagTuple[1])
            else:
                self.showArea()

    # set

    def setAdjacentBombs(self, number):
        self.__adjacentBombs = number

    def setThisCellIndex(self, number):
        self.__thisCellIndex = number

    def setButtonList(self, list):
        self.__buttonList = list

    def setCellCount(self, number):
        self.__cellCount = number

    # get

    def getBombStatus(self):
        return self.__isBomb

    def getButton(self):
        return self.__button

    def getIndex(self):
        return self.__thisCellIndex

    def getAdjacentBombs(self):
        return self.__adjacentBombs

    def getCellFrame(self):
        return self.__frame

    def getRevealed(self):
        return self.__revealed

    def getFlagged(self):
        return self.__flagged


# --------------------------------------------------------- Game Window -------------------------------------------------------------------

def createGameWindow(rowX, columnY, numberOfBombs):
    gameWindow = tk.Toplevel()
    time.set(0)
    global gameOpen
    gameOpen = True

    infoFrame = tk.Frame(gameWindow, width=columnY * 25, height=28)
    infoFrame.pack(side="top")
    infoFrame.pack_propagate(0)

    timeLable = tk.Label(infoFrame, textvariable=timeDisplay)
    timeLable.pack(side="left")
    infoFrame.pack_propagate(0)

    bombsLeft.set("Bombs left: {}".format(numberOfBombs))

    bombCount = tk.Label(infoFrame, textvariable=bombsLeft, justify="center")
    bombCount.pack(side="right")

    gridFrame = tk.Frame(gameWindow, pady=int(rowX * .5))
    gridFrame.pack(side="bottom")
    gameWindow.title("minesweeper")

    # ----------- find edge cells
    edgeDict = {
        "leftColumn": [],
        "rightColumn": [],
        "topRow": [],
        "bottomRow": []
    }
    for i in range(rowX):  # columns
        edgeDict["leftColumn"].append(i * columnY)  # left column
        edgeDict["rightColumn"].append(i * columnY + columnY - 1)  # right column
    for i in range(columnY):  # rows
        edgeDict["topRow"].append(i)  # top row
        edgeDict["bottomRow"].append((rowX * columnY - 1) - i)  # bottom row

    # ------------- create list of cells
    buttonList = []
    for row in range(rowX):
        for column in range(columnY):
            frameToCreate = cellFrame(row, column, gridFrame, gameWindow, edgeDict, rowX, columnY, numberOfBombs)
            buttonList.append(frameToCreate)

    # ----- give cells their index's, the list, and the count of list
    for cell in buttonList:
        cell.setThisCellIndex(buttonList.index(cell))
        cell.setButtonList(buttonList)
        cell.setCellCount(len(buttonList))
        # cell.button.configure(text=buttonList.index(cell))

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
        if cell.getBombStatus():
            continue
        else:
            checkList = adjacentCellList(cellIndex, edgeDict, columnY)
        for x in checkList:
            if buttonList[x].getBombStatus():
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
    gameWindow.geometry(centerWindow(columnY * 28, (rowX * 28) + 28))
    gameWindow.protocol("WM_DELETE_WINDOW", lambda: closeGameWindow(gameWindow))
    timer()
    gameWindow.bind("<Button-2>", lambda e: tryFlag(currentWidget.get(), buttonList))
    gameWindow.bind("<Button-3>", lambda e: tryFlag(currentWidget.get(), buttonList))


# ------------------------------------------------------- Game End Window ----------------------------------------------------
def end(window, buttonList, won, x, y, bombCount, correctFlags, incorrectFlags):
    endText = ""
    difficulty = "NaN"

    if won:
        endText = "Win"
    else:
        endText = "Lost"
        for cell in buttonList:
            cell.show()

    global gameOpen
    gameOpen = False
    loseWindow = tk.Toplevel()
    loseWindow.title("You " + endText)
    loseWindow.geometry(centerWindow(200, 300))
    loseWindow.resizable(0, 0)
    loseWindow.protocol("WM_DELETE_WINDOW", lambda: quitGame(window, loseWindow))

    textFrame = tk.Frame(loseWindow)
    textFrame.pack(side="top")

    buttonFrame = tk.Frame(loseWindow)
    buttonFrame.pack(side="bottom")

    if x == 9 and y == 9 and bombCount == 10:
        difficulty = "Difficulty: Easy"
    elif x == 16 and y == 16 and bombCount == 40:
        difficulty = "Difficulty: Medium"
    elif ((x == 30 and y == 16) or ( x== 16 and y == 30))and bombCount == 99:
        difficulty = "Difficulty: Hard"
    else:
        difficulty = "Grid Size: "+str(x)+"x"+str(y)+"\nBombs: "+str(bombCount)

    gameStats = tk.Label(textFrame, text="You {}\n\n\n\nElapsed Time: {}\n{}\nCorrect Flags: {}\nIncorrect Flags: {}".format(endText,timeDisplay.get(),difficulty,correctFlags,incorrectFlags), justify="center")
    gameStats.pack()

    buttonPlayAgain = tk.Button(buttonFrame, text="Play Again",
                                command=lambda: playAgain(window, loseWindow, x, y, bombCount))
    buttonPlayAgain.pack(side="left")
    buttonMainMenu = tk.Button(buttonFrame, text="Main Menu", command=lambda: returnToMainMenu(window, loseWindow))
    buttonMainMenu.pack(side="left")
    buttonQuit = tk.Button(buttonFrame, text="Quit", command=lambda: quitGame(window, loseWindow))
    buttonQuit.pack(side="right")


# ------------------------------------------------------- Custom Game window --------------------------------------------

def customGame():
    root.withdraw()
    customEntryWindow = tk.Toplevel()
    customEntryWindow.title("minesweeper")
    customEntryWindow.geometry(centerWindow(250, 200))
    customEntryWindow.resizable(0, 0)
    customEntryWindow.protocol("WM_DELETE_WINDOW", lambda: cancelCustom(customEntryWindow))

    lineOne = tk.Frame(customEntryWindow, width="250")
    lineOne.pack(side="top", pady="15", padx="20")

    lineTwo = tk.Frame(customEntryWindow, width="250")
    lineTwo.pack(side="top", pady="15", padx="20")

    lineThree = tk.Frame(customEntryWindow, width="250")
    lineThree.pack(side="top", pady="15", padx="20")

    lineFour = tk.Frame(customEntryWindow, width="250")
    lineFour.pack(side="top", pady="15", padx="20")

    widthLable = tk.Label(lineOne, text="Width: ")  # x
    widthLable.pack(side="left")
    widthEntry = tk.Entry(lineOne)
    widthEntry.pack(side="left")

    heightLable = tk.Label(lineTwo, text="Height: ")  # y
    heightLable.pack(side="left")
    heightEntry = tk.Entry(lineTwo)
    heightEntry.pack(side="left")

    bombsLable = tk.Label(lineThree, text="Bombs: ")  # bombs
    bombsLable.pack(side="left")
    bombsEntry = tk.Entry(lineThree)
    bombsEntry.pack(side="left")

    submitButton = tk.Button(lineFour, text="Submit", command=lambda: startCustomGame(widthEntry.get(),heightEntry.get(),bombsEntry.get(),customEntryWindow))
    submitButton.pack(side="left")
    cancelButton = tk.Button(lineFour, text="Cancel", command=lambda: cancelCustom(customEntryWindow))
    cancelButton.pack(side="left")
    customEntryWindow.bind("<Return>", lambda e: startCustomGame(widthEntry.get(),heightEntry.get(),bombsEntry.get(),customEntryWindow))


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
            print("failed to close a window")


def returnToMainMenu(gameWindow, scoreWindow):
    gameWindow.destroy()
    scoreWindow.destroy()
    global gameOpen
    gameOpen = False
    root.deiconify()


def playAgain(gameWindow, scoreWindow, x, y, bombs):
    gameWindow.destroy()
    scoreWindow.destroy()
    global gameOpen
    gameOpen = False
    createGameWindow(x, y, bombs)


def cancelCustom(customWidnow):
    root.deiconify()
    customWidnow.destroy()


# ------------------------------------------------------ Other Functions -------------------------------------------

def centerWindow(width, length):
    screenWidth = root.winfo_screenwidth()
    screenLength = root.winfo_screenheight()

    screenX = int((screenWidth / 2) - (width / 2))
    screenY = int((screenLength / 2) - (length / 2))

    return "%dx%d+%d+%d" % (width, length, screenX, screenY)


def timer():
    time.set(time.get() + 1)
    min = int(time.get() / 60)
    sec = int(time.get() % 60)
    timeDisplay.set("{:02d}:{:02d}".format(min, sec))
    if gameOpen:
        root.after(1000, timer)  # call this function again in 1,000 milliseconds


def adjacentCellList(cellIndex, edgeDict, columnY):
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
        checkList.append(cellIndex - columnY)
        sideDict["top"] = False
    if cellIndex not in edgeDict["bottomRow"]:  # check below cell
        checkList.append(cellIndex + columnY)
        sideDict["bottom"] = False
    if not sideDict["top"] and not sideDict["left"]:  # top left cell
        checkList.append(cellIndex - columnY - 1)
    if not sideDict["top"] and not sideDict["right"]:  # top right cell
        checkList.append(cellIndex - columnY + 1)
    if not sideDict["bottom"] and not sideDict["left"]:  # bottom left cell
        checkList.append(cellIndex + columnY - 1)
    if not sideDict["bottom"] and not sideDict["right"]:  # bottom left cell
        checkList.append(cellIndex + columnY + 1)
    return checkList


def getWidgetUnderMouse(root):
    x, y = root.winfo_pointerxy()
    widget = root.winfo_containing(x, y)
    currentWidget.set(widget)
    # print(currentWidget.get())
    root.after(10, getWidgetUnderMouse, root)


def tryFlag(rawString, buttonList):  # .!toplevel###.!frame2.!frame###.!button
    print(rawString)
    phase1 = re.split(".*\.!frame2\.!frame", rawString)
    if len(phase1) == 2:
        phase2 = re.split("\.", phase1[1])
        if len(phase2) == 2:
            if phase2[0] == "":
                buttonList[0].flagCell()
            else:
                buttonList[int(phase2[0]) - 1].flagCell()


def startCustomGame(xRaw, yRaw, bombsRaw,customEntryWindow):
    x = None
    y = None
    q1 = False
    q2 = False
    bombs = None
    goodInput = False
    try:
        x = int(xRaw)
        y = int(yRaw)
        bombs = int(bombsRaw)
        goodInput = True
    except:
        tkinter.messagebox.showwarning("Invalid Input", "Please use only numbers in the boxes.")
    if goodInput:
        if not x*y <= bombs:
            if y > 20 or x > 50:
                if tkinter.messagebox.askyesno("Game Window may be too large", "The numbers your entered may make a window larger than your screen, would you still like to continue?"):
                    q1 = True
            else:
                q1 = True
            if q1:
                if x*y >= 1000:
                    if tkinter.messagebox.askyesno("Low Performance", "This game will run slowly due to the number of cells, would you still like to continue?"):
                        q2 = True
                else:
                    q2 = True
        else:
            tkinter.messagebox.showerror("To Many Bombs", "If this field generated all cells would be bombs.\n\nTry making the field larger or decreasing the number of bombs.")
        if q1 and q2:
            createGameWindow(x,y,bombs)
            customEntryWindow.destroy()

def checkFlags(buttonList):
    correctFlags = 0
    incorrectFlags = 0
    for cell in buttonList:
        if cell.getBombStatus() and cell.getFlagged():
            correctFlags = correctFlags + 1
        elif not cell.getBombStatus() and cell.getFlagged():
            incorrectFlags = incorrectFlags + 1
    flagTuple = (correctFlags,incorrectFlags)
    return flagTuple

# --------------------------------------------------------- Root window ------------------------------------------------
root = tk.Tk()

titleFrame = tk.Frame(root, width="200")
titleFrame.pack(side="top")

buttonFrame = tk.Frame(root, width="320")
buttonFrame.pack(side="bottom", pady="30", padx="30")

easyGameButton = tk.Button(buttonFrame, text="Easy game", command=lambda: createGameWindow(9, 9, 10))  # (x,y,bombs)
easyGameButton.pack(side="left")
mediumGameButton = tk.Button(buttonFrame, text="Medium game", command=lambda: createGameWindow(16, 16, 40))
mediumGameButton.pack(side="left")
hardGameButton = tk.Button(buttonFrame, text="Hard game", command=lambda: createGameWindow(16, 30, 99))
hardGameButton.pack(side="left")
customGameButton = tk.Button(buttonFrame, text="Custom game", command=lambda: customGame())
customGameButton.pack(side="left")

titleLable = tk.Label(titleFrame, text="M I N E S W E E P E R\n Project by:\nDustin Frandle\n&\nQuinn Hubanks")
titleLable.pack()

# screen size - center widows

root.title("minesweeper")
root.geometry(centerWindow(400, 200))
root.resizable(0, 0)
root.protocol("WM_DELETE_WINDOW", lambda: quitGame())
time = tk.IntVar()
bombsLeft = tk.StringVar()
timeDisplay = tk.StringVar()
currentWidget = tk.StringVar()
currentWidget.set(None)
timeDisplay.set("00:00")
getWidgetUnderMouse(root)
root.mainloop()
