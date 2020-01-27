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
