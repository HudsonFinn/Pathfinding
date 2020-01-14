from tkinter import *
from math import ceil

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
        self.createGrid(20, 20)

    def createGrid(self, x, y):
        self.grid = []
        self.gridType = []
        self.boxSizeX = (self.canvasWidth/x)
        self.boxSizeY = (self.canvasHeight/y)
        for i in range(y):
            self.grid.append([])
            for j in range(x):
                self.grid[i].append(self.mainCanvas.create_rectangle(0, 0, 50, 50, fill="white"))
                print(self.grid)
                print(i, j)
                self.mainCanvas.coords(self.grid[i][j], j*self.boxSizeX, i*self.boxSizeY, j*self.boxSizeX + self.boxSizeX, i*self.boxSizeY + self.boxSizeY)
        print(self.grid)

    def click(self, event):
        x, y = event.x, event.y
        self.updateGridClick(x, y)

    def updateGridClick(self, x, y):
        gridX = (ceil(x/self.boxSizeX)) - 1
        gridY = (ceil(y/self.boxSizeY)) - 1
        self.mainCanvas.itemconfigure(self.grid[gridY][gridX], fill="red")
        print(gridX, gridY)



root = Tk()
app = App(root)
root.title('Pathfinding')
root.mainloop()
