from tkinter import *
from math import ceil
import time
import math
import timeit

class App:
    def __init__(self, master):
        self.master = master

        Grid = mainGrid(self.master, 0, 0)

class mainGrid:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.container = Frame(self.parent)
        self.container.grid(row=x, column=y)
        self.canvasWidth = 500
        self.canvasHeight = 500
        self.mainCanvas = Canvas(self.container, bg="black", width = self.canvasWidth, height = self.canvasHeight)
        self.mainCanvas.grid(row=0, column=0)
        self.buttonCanvas = Canvas(self.container, bg="white", width = 200, height = self.canvasHeight)
        self.buttonCanvas.grid(row=0, column= 1)
        self.mainCanvas.bind('<Button-1>', self.click)
        self.mainCanvas.bind('<Button-3>', self.rightClick)
        self.mainCanvas.bind('<space>', self.start)
        self.createMenu()
        self.mainCanvas.focus_set()

    def setGridSize(self):
        self.gridHeightX = self.gridSizeX.get()
        self.gridHeightY = self.gridSizeX.get()
        self.createGrid()

    def refreshGrid(self):
        self.createGrid()

    def createGrid(self):
        x = self.gridHeightX
        y = self.gridHeightY
        x = int(x)
        y = int(y)
        self.grid = []
        self.gridType = []
        self.boxSizeX = (self.canvasWidth/x)
        self.boxSizeY = (self.canvasHeight/y)
        for i in range(y):
            self.grid.append([])
            self.gridType.append([])
            for j in range(x):
                self.grid[i].append(self.mainCanvas.create_rectangle(0, 0, 50, 50, fill="white"))
                self.gridType[i].append([0, ((y)*i)+ j, 0, 1000000, j, i, 0])
                self.mainCanvas.coords(self.grid[i][j], j*self.boxSizeX, i*self.boxSizeY, j*self.boxSizeX + self.boxSizeX, i*self.boxSizeY + self.boxSizeY)

    def createMenu(self):
        self.startAlgoBtn = Button(self.buttonCanvas, text="Start", command=self.start)
        self.startAlgoBtn.place(x = 20, y = 200)
        self.startEntryX = Entry(self.buttonCanvas)
        self.startEntryX.config(width=4, font="Serif 10 bold")
        self.startEntryX.insert(0, "10")
        self.startEntryX.place(x=30, y=150)
        self.startEntryY = Entry(self.buttonCanvas)
        self.startEntryY.config(width=4, font="Serif 10 bold")
        self.startEntryY.insert(0, "10")
        self.startEntryY.place(x=30, y=170)
        self.buttonCanvas.create_text(20, 160, fill="black", font="Arial 10 bold", text="X:")
        self.buttonCanvas.create_text(20, 180, fill="black", font="Arial 10 bold", text="Y:")
        self.createGridBtn = Button(self.buttonCanvas, text="Start", command=self.setGridSize)
        self.refreshGridBtn = Button(self.buttonCanvas, text="Reset", command=self.refreshGrid)
        self.createGridBtn.place(x = 20, y = 100)
        self.refreshGridBtn.place(x = 20, y = 125)
        self.gridSizeX = Entry(self.buttonCanvas)
        self.gridSizeX.config(width=4, font="Serif 10 bold")
        self.gridSizeX.insert(0, "10")
        self.gridSizeX.place(x=70, y=50)
        self.gridSizeY = Entry(self.buttonCanvas)
        self.gridSizeY.config(width=4, font="Serif 10 bold")
        self.gridSizeY.insert(0, "10")
        self.gridSizeY.place(x=70, y=70)
        self.buttonCanvas.create_text(40, 60, fill="black", font="Arial 10 bold", text="WIDTH:")
        self.buttonCanvas.create_text(40, 80, fill="black", font="Arial 10 bold", text="HEIGHT:")
        self.cornersEnabledButton = IntVar()
        self.cornersCheckBox = Checkbutton(self.buttonCanvas, text='Diagonals Enabled', variable = self.cornersEnabledButton)
        self.cornersCheckBox.place(x=20, y=225)

    def click(self, event):
        x, y = event.x, event.y
        self.updateGridClick(x, y)

    def rightClick(self, event):
        x, y = event.x, event.y
        self.updateGridRightclick(x, y)

    def updateGridClick(self, x, y):
        gridX = (ceil(x/self.boxSizeX)) - 1
        gridY = (ceil(y/self.boxSizeY)) - 1
        if self.gridType[gridY][gridX][0] == 0:
            self.mainCanvas.itemconfigure(self.grid[gridY][gridX], fill="red")
            self.gridType[gridY][gridX][0] = 1
        elif self.gridType[gridY][gridX][0] == 1:
            self.mainCanvas.itemconfigure(self.grid[gridY][gridX], fill="white")
            self.gridType[gridY][gridX][0] = 0
        print(gridX, gridY)

    def start(self):
        print("Hi")
        x = self.startEntryX.get()
        y = self.startEntryY.get()
        x = int(x)
        y = int(y)
        self.cornersEnabled = self.cornersEnabledButton.get()
        self.SetupDjykstras(x, y)

    def updateGridRightclick(self, x, y):
        gridX = (ceil(x/self.boxSizeX)) - 1
        gridY = (ceil(y/self.boxSizeY)) - 1
        if self.gridType[gridY][gridX][0] == 0:
            self.mainCanvas.itemconfigure(self.grid[gridY][gridX], fill="green")
            self.gridType[gridY][gridX][0] = 2
        elif self.gridType[gridY][gridX][0] == 2:
            self.mainCanvas.itemconfigure(self.grid[gridY][gridX], fill="white")
            self.gridType[gridY][gridX][0] = 0

        print(gridX, gridY)

    def SetupDjykstras(self, startX, startY):
        #0 is type (0 for normal, 1 for wall, 2 for target)
        #1 is for node index
        #2 is for previous node
        #3 is for distance
        #4 is x
        #5 is y
        #6 is unvisited
        self.mainCanvas.itemconfigure(self.grid[startX][startY], fill="blue")
        self.gridType[startX][startY][2] = -1
        self.gridType[startX][startY][3] = 0
        startNode = self.gridType[startY][startX]
        currentNode = self.gridType[startY][startX]
        currentNodes = [currentNode]
        self.complete = False
        self.LoopDijkstra(self.gridType, currentNodes, startNode)


    def LoopDijkstra(self, allNodes, activeNodes, startNode):
        print(activeNodes)
        while self.complete == False:
            if len(activeNodes) == 0:
                self.complete = "None Found"
                print("Path not found")
                break
            activeNodes = sorted(activeNodes, key=lambda x: (x[3], x[4], x[5]), reverse=False)
            targetNode = activeNodes[0]
            allNodes[targetNode[5]][targetNode[4]][6] = 1
            self.mainCanvas.itemconfigure(self.grid[targetNode[5]][targetNode[4]], fill="orange")
            activeNodes.pop(0)
            print("activeNodes")
            print(activeNodes)
            self.mainCanvas.update_idletasks()
            activeNodes, allNodes = self.findAdjacent(targetNode, activeNodes, allNodes)

        if self.complete == True:
            print("Drawing")
            self.drawPath(allNodes, self.finalNode, startNode)
            self.mainCanvas.update_idletasks()


    def findAdjacent(self, targetNode, activeNodes, allNodes):
        print("Target Node:")
        print(targetNode)
        adjacent = [[-1, -1], [0, -1], [1, -1],
                    [-1, 0],          [1, 0],
                    [-1, 1], [0, 1], [1, 1]]
        corners = [0, 2, 5, 7]
        targetNodeX = targetNode[4]
        targetNodeY = targetNode[5]
        targetDistance = targetNode[3]
        unvisitedNodes = []
        for i in range(0, 8):
            try:
                if ((targetNodeX + adjacent[i][0]) >= 0) and ((targetNodeY + adjacent[i][1]) >= 0):
                    print("passed out of bounds")
                    print(allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]])
                    if (allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][0]) != 1:
                        print("passed out of type check")
                        print(allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]])
                        if (allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][6]) == 0:
                            print("passed already contains check")
                            print(allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]])
                            if i in corners:
                                if self.cornersEnabled:
                                    if allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][3] > (targetDistance + math.sqrt(2)):
                                        allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][3] = (targetDistance + math.sqrt(2))
                                        allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][2] = (targetNode[4], targetNode[5])
                                else:
                                    continue
                            else:
                                if allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][3] > (targetDistance + 1):
                                    allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][3] = (targetDistance + 1)
                                    allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][2] = (targetNode[4], targetNode[5])
                            contains = False
                            if (allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][0]) == 2:
                                self.complete = True
                                print("Complete")
                                self.finalNode = allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]]
                                break
                            for j, jValue in enumerate(activeNodes):
                                if jValue[1] == allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]][1]:
                                    contains = True
                            if contains == False:
                                print("appending")
                                print(allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]])
                                activeNodes.append(allNodes[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]])
                                self.mainCanvas.itemconfigure(self.grid[targetNodeY + adjacent[i][1]][targetNodeX + adjacent[i][0]], fill="yellow")
            except IndexError:
                pass
        self.mainCanvas.update_idletasks()
        print("Returned active Nodes:")
        print(activeNodes)
        return activeNodes, allNodes

    def drawPath(self, currentNodes, finalNode, startNode):
        lastNode = finalNode
        completed = False
        while completed != True:
            if lastNode[2] == -1:
                break
            currentNode = currentNodes[lastNode[2][1]][lastNode[2][0]]
            print(lastNode)
            self.mainCanvas.create_line(currentNode[4] *self.boxSizeX +(self.boxSizeX/2), currentNode[5]*self.boxSizeY +(self.boxSizeY/2), lastNode[4]*self.boxSizeX + (self.boxSizeX/2), lastNode[5]*self.boxSizeY + (self.boxSizeY/2))
            lastNode = currentNode






root = Tk()
app = App(root)
root.title('Pathfinding')
root.mainloop()
