#SUDO CODE FOR A* ALGORITM

startNode =
endNode =

openList =
closedList =
openList.append(startNode)
while len(openList) > 0:
    openList = sorted(openList, by lowest f value)
    currentNode = openList[0]
    openList.pop(0)
    closedList.append(currentNode)

    if currentNode = endNode:
        Func DrawPath(currentNode, endNode)

    adjacents = findAdjacent()

    for adjacents:
        if adjacent in closedList:
            continue

        adG = currentG + distance between ad and current
        adH = distance from child to end a**2 + b**2
        adF = adG + adH

        if adjacent in openList:
            if adG > openListG:
                continue
            else:
                replace openList
                continue

        add adjacent to openList/replaceOld

    def SetupAStar(self, startNode, endNode):
        #0 is type (0 for normal, 1 for wall, 2 for target)
        #1 is for node index
        #2 is for previous node (x, y)
        #3 if for G value (distance to previous node)
        #4 is x
        #5 is y
        #6 is for F value (G + H)(H is distance to target)
        #self.mainCanvas.itemconfigure(self.grid[startX][startY], fill="blue")
        self.gridType[startX][startY][2] = -1
        self.gridType[startX][startY][3] = 0
        self.complete = False
        self.LoopAStar(self.gridType, startNode, endNode)

    def LoopAStar(self, allNodes, startNode, endNode):
        print(activeNodes)
        openList = []
        closedList = []
        openList.append(startNode)
        while self.complete == False:
            if len(activeNodes) == 0:
                self.complete = "None Found"
                print("Path not found")
                break
            openList = sorted(openList, key=lambda x: x[6], reverse=False)
            currentNode = openList[0]
            openList.pop(0)
            closedList.append(currentNode)
            #self.mainCanvas.itemconfigure(self.grid[targetNode[5]][targetNode[4]], fill="orange")
            #self.mainCanvas.update_idletasks()
            if currentNode[1] = endNode[1]:
                self.complete = True
                self.finalNode = currentNode

            adjacentNodes = self.getAdjacent(allNodes, currentNode, endNode)

            for adjacentIndex, adjacentValue in enumerate(adjacentNodes):
                if any(adjacentValue[1] in sublist[1] for sublist in closedList):
                    continue

                adG = currentNode[3] + 1
                adHX = adjacentValue[4] - endNode[4]
                adHX = adHX ** 2
                adHY = adjacentValue[5] - endNode[5]
                adHY = adHY ** 2
                adH = adHX + adHY
                adF = adG + adH
                adjacentValue[2] = (currentNode[4], currentNode[4])
                adjacentValue[3] = adG
                adjacentValue[6] = adF
                for index, value in openList:
                    if value[1] = adjacentValue[1]:
                        if adG > value[3]:
                            continue
                        else:
                            openList[index] = adjacentValue
                            continue

                openList.append(adjacentValue)
        if self.complete == True:
            print("Drawing")
            self.drawPath(allNodes, self.finalNode, startNode)
            self.mainCanvas.update_idletasks()

    def getAdjacent(self, allNodes, currentNode, endNode):
        adjacent = [[-1, -1], [0, -1], [1, -1],
                    [-1, 0],          [1, 0],
                    [-1, 1], [0, 1], [1, 1]]

        for i in adjacent:
            try:
                thisAdjacent = allNodes[currentNode[5] + i[1]][currentNode[4] + i[0]]
                if ((currentNode[4] + i[0]) >= 0) and ((currentNode[5] + i[1]) >= 0):
                    if thisAdjacent[0] != 1:
                        listOfAdjacents.append(thisAdjacent)
            except IndexError:
                pass

        return listOfAdjacents
