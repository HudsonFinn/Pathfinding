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
        self.mainCanvas.bind('<Button-1>', self.click)
        self.mainCanvas.bind('<Button-3>', self.rightClick)
        self.mainCanvas.bind('<space>', self.start)
        self.createGrid(10, 10)
        self.mainCanvas.focus_set()

    def createGrid(self, x, y):
        self.grid = []
        self.gridType = []
        self.boxSizeX = (self.canvasWidth/x)
        self.boxSizeY = (self.canvasHeight/y)
        for i in range(y):
            self.grid.append([])
            self.gridType.append([])
            for j in range(x):
                self.grid[i].append(self.mainCanvas.create_rectangle(0, 0, 50, 50, fill="white"))
                self.gridType[i].append([0, (10*i)+ j, 0, 1000000, j, i, 0])
                print(i, j)
                self.mainCanvas.coords(self.grid[i][j], j*self.boxSizeX, i*self.boxSizeY, j*self.boxSizeX + self.boxSizeX, i*self.boxSizeY + self.boxSizeY)
        print(self.gridType)

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
        print(self.gridType)

    def start(self, event):
        print("Hi")
        self.UseDjykstras(9, 9)

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
        print(self.gridType)

    def UseDjykstras(self, startX, startY):
        #0 is type (0 for normal, 1 for wall, 2 for target)
        #1 is for node index
        #2 is for previous node
        #3 is for distance
        #4 is x
        #5 is y
        #6 is unvisited
        print(self.gridType)
        self.gridType[startX][startY][2] = -1
        self.gridType[startX][startY][3] = 0
        found = False
        startNode = self.gridType[startY][startX]
        currentNode = self.gridType[startY][startX]
        currentNodes = [currentNode]
        self.state = 0

        while (self.state == 0):
            print(self.state)
            currentNodes = sorted(currentNodes, key=lambda x: (x[3]), reverse=False)
            for i, iValue in enumerate(currentNodes):
                self.mainCanvas.itemconfigure(self.grid[currentNodes[i][5]][currentNodes[i][4]], fill="orange")#
                self.mainCanvas.pack()
                if self.state == 1:
                    break
                if iValue[6] == 0:
                    currentNode = currentNodes[i]
                    currentNodes[i][6] = 1
                    print(currentNodes)
                    currentNodes = self.findAdjacent(currentNode, self.gridType, currentNodes, startNode)


    def findAdjacent(self, Node, Nodes, currentNodes, startNode):
        adjacent = [[-1, -1], [0, -1], [1, -1],
                    [-1, 0],          [1, 0],
                    [-1, 1], [0, 1], [1, 1]]
        state = 0
        adjacentActive = []
        print(Node)
        NodeX = Node[4]
        NodeY = Node[5]
        distance = Node[3]
        for i in range(0, 8):
            #if self.gridType[NodeX + adjacent[i][1]][NodeY + adjacent[i][0]][0] == 0:
            try:
                if ((NodeX + adjacent[i][0]) >= 0) and ((NodeY + adjacent[i][1]) >= 0):
                    print(Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]])
                    if Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][0] == 0:
                        if Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][3] > (distance + 1):
                            if i == 0 or i == 2 or i == 5 or i == 7:
                                Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][3] = (distance + math.sqrt(2))
                            else:
                                Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][3] = (distance + 1)
                            Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][2] = (Node[1])
                        adjacentActive.append(Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]])
                print(adjacentActive)
                print("singles")
                if Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][0] == 2:
                    self.state = 1
                    Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]][2] = (Node[1])
                    self.drawPath(currentNodes, Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]], startNode)
                    print(Nodes[NodeY + adjacent[i][1]][NodeX + adjacent[i][0]])
                    print("Completed")
            except IndexError:
                pass
        for i, iValue in enumerate(adjacentActive):
            contains = False
            for j, jValue in enumerate(currentNodes):
                if iValue[1] == jValue[1]:
                    contains = True
                    if iValue[3] < jValue[3]:
                        currentNodes[j] = adjacentActive[i]
            if contains == False:
                currentNodes.append(adjacentActive[i])
        print(currentNodes)
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
                    print(lastNode)
                    self.mainCanvas.create_line(currentNode[4] *self.boxSizeX +(self.boxSizeX/2), currentNode[5]*self.boxSizeY +(self.boxSizeY/2), lastNode[4]*self.boxSizeX + (self.boxSizeX/2), lastNode[5]*self.boxSizeY + (self.boxSizeY/2))
                    lastNode = currentNode
                    break;






root = Tk()
app = App(root)
root.title('Pathfinding')
root.mainloop()
