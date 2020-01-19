from tkinter import *
from math import ceil
import time
import math

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
        """NEEDS TO BE CHANGED SO YOU CAN EDIT SIZE WITH BUTTON"""
        self.createMenu()
        self.mainCanvas.focus_set()

    def createGrid(self):
        x = self.gridSizeX.get()
        y = self.gridSizeX.get()
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
        self.createGridBtn = Button(self.buttonCanvas, text="Start", command=self.createGrid)
        self.createGridBtn.place(x = 20, y = 100)
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
        self.state = 0
        self.LoopDjykstras(currentNodes, startNode)
        """
        while (self.state == 0):
            print(self.state)
            currentNodes = sorted(currentNodes, key=lambda x: (x[3]), reverse=False)
            for i, iValue in enumerate(currentNodes):
                self.mainCanvas.itemconfigure(self.grid[currentNodes[i][5]][currentNodes[i][4]], fill="orange")
                self.mainCanvas.pack()
                if self.state == 1:
                    break
                if iValue[6] == 0:
                    currentNode = currentNodes[i]
                    currentNodes[i][6] = 1
                    print(currentNodes)
                    currentNodes = self.findAdjacent(currentNode, self.gridType, currentNodes, startNode)
        """

    def LoopDjykstras(self, currentNodes, startNode):
        #Move Test nodes into different list so it takes less time to sort
        while self.state == 0:
            time.sleep(0.1)
            currentNodes = sorted(currentNodes, key=lambda x: (x[3], x[4], x[5]), reverse=False)
            print("START LOOP")
            nextNode = -1
            for i, iValue in enumerate(currentNodes):
                if iValue[6] == 0:
                    nextNode = i
                    break
            if nextNode == -1:
                self.state = 1
            currentNode = currentNodes[nextNode]
            currentNodes[i][6] = 1
            self.mainCanvas.itemconfigure(self.grid[currentNodes[nextNode][5]][currentNodes[nextNode][4]], fill="orange")
            self.mainCanvas.update_idletasks()
            currentNodes = self.findAdjacent(currentNode, self.gridType, currentNodes, startNode)
        else:
            print("Done")


    def findAdjacent(self, Node, Nodes, currentNodes, startNode):
        adjacent = [[-1, -1], [0, -1], [1, -1],
                    [-1, 0],          [1, 0],
                    [-1, 1], [0, 1], [1, 1]]
        state = 0
        adjacentActive = []
        NodeX = Node[4]
        NodeY = Node[5]
        distance = Node[3]
        for i in range(0, 8):
            #if self.gridType[NodeX + adjacent[i][1]][NodeY + adjacent[i][0]][0] == 0:
            try:
                if ((NodeX + adjacent[i][0]) >= 0) and ((NodeY + adjacent[i][1]) >= 0):
                    print("Passed out of bounds check")
                    print(Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]])
                    #print(Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]])
                    if (Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][0]) == 0:
                        print("Passed proper type check")
                        print(Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]])
                        """MAKE ENABLING CORNERS OPTIONAL"""
                        if i == 0 or i == 2 or i == 5 or i == 7:
                            if Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][3] > (distance + math.sqrt(2)):
                                Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][3] = (distance + math.sqrt(2))
                                Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][2] = (Node[1])
                        else:
                            if Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][3] > (distance + 1):
                                Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][3] = (distance + 1)
                                Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][2] = (Node[1])
                        adjacentActive.append(Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]])
                    if Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][0] == 2:
                        self.state = 1
                        Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][2] = (Node[1])
                        self.drawPath(currentNodes, Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]], startNode)
                        print(Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]])
                        print("Completed")
            except IndexError:
                pass
        print("All adjacentActive Nodes")
        print(adjacentActive)
        for i, iValue in enumerate(adjacentActive):
            contains = False
            for j, jValue in enumerate(currentNodes):
                if iValue[1] == jValue[1]:
                    print("Value changed")
                    print(iValue)
                    print(jValue)
                    contains = True
                    if iValue[3] < jValue[3]:
                        currentNodes[j] = adjacentActive[i]
            if contains == False:
                print("Passed Appened")
                print(adjacentActive[i])
                currentNodes.append(adjacentActive[i])
                self.mainCanvas.itemconfigure(self.grid[iValue[5]][iValue[4]], fill="yellow")
        currentNodes = sorted(currentNodes, key=lambda x: (x[3]), reverse=False)
        return(currentNodes)

    def drawPath(self, currentNodes, finalNode, startNode):
        lastNode = finalNode
        completed = False
        while completed != True:
            if lastNode[2] == -1:
                break
            for i, iValue in enumerate(currentNodes):
                if iValue[1] == lastNode[2]:
                    currentNode = iValue
                    self.mainCanvas.create_line(currentNode[4] *self.boxSizeX +(self.boxSizeX/2), currentNode[5]*self.boxSizeY +(self.boxSizeY/2), lastNode[4]*self.boxSizeX + (self.boxSizeX/2), lastNode[5]*self.boxSizeY + (self.boxSizeY/2))
                    lastNode = currentNode
                    break;






root = Tk()
app = App(root)
root.title('Pathfinding')
root.mainloop()
