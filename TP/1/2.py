from queue import Queue
from river_margin import RiverMargin, BoatError



def dfsAux(node, maxDepth, currentDepth, s):
    if currentDepth >= maxDepth:
        return None

    funcs = ["cannibalsBA", "cannibalsAB", "missionariesBA", "missionariesAB",
    "cannibalBA", "cannibalAB", "missionaryBA", "missionaryAB", "mixedBA", "mixedAB"]

    if node == RiverMargin(3,3,0,0,'A',None) or node == RiverMargin(3,3,0,0,'B',None):
        print("Success")
        return node

    for func in funcs:
        try:
            tempNode = getattr(node,func)()
            if tempNode not in s:
                s.add(tempNode)
                result = dfsAux(tempNode, maxDepth, currentDepth + 1, s)
                if result is not None:
                    return result
        except BoatError:
            pass
    return None



def iterDeepeningDfs():
    for i in range(8, 15):
        s = set()
        s.add(RiverMargin(0,0,3,3,'A',None))
        result = dfsAux(RiverMargin(0,0,3,3,'A',None), i, 0, s)
        if result is not None:
            break

    while result is not None:
        print(result)
        result = result.parent
    



def dfs():

    s = set()
    s.add(RiverMargin(0,0,3,3,'A',None))
    result = dfsAux(RiverMargin(0,0,3,3,'A',None), 10000, 0, s)
    while result is not None:
        print(result)
        result = result.parent


def bfs():

    q = Queue()
    s = set()
    first = RiverMargin(0,0,3,3,'A',None)
    q.put(first)
    s.add(first)

    funcs = ["cannibalsBA", "cannibalsAB", "missionariesBA", "missionariesAB",
    "cannibalBA", "cannibalAB", "missionaryBA", "missionaryAB", "mixedBA", "mixedAB"]


    while True:

        if q.empty():
            print("Empty queue")
            break

        curNode = q.get()

        if curNode.CB == 3 and curNode.MB == 3:
            print("Success")
            break

        for func in funcs:
            try:
                tempNode = getattr(curNode,func)()
                if tempNode not in s:
                    q.put(tempNode)
                    s.add(tempNode)
            except BoatError:
                pass

    while curNode is not None:
        print(curNode)
        curNode = curNode.parent


if __name__ == "__main__":

    print("\nBreadth First")
    bfs()
    print("\nDepth First")
    dfs()
    print("\nIterative Depth First")
    iterDeepeningDfs()
