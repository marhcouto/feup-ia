from queue import Queue, LifoQueue
from bucket import Node, NodeError

def breadthFirst(): 
    q = Queue()
    s = set()
    first = Node(0,0,None)
    q.put(first)
    s.add(first)

    funcs = ["emptyA", "emptyB", "fillA", "fillB", "pourAB", "pourBA"]

    while True:

        if q.empty():
            print("Empty queue")
            break

        curNode = q.get()

        if curNode.A == 2:
            print("Success")
            break


        for func in funcs:

            try:
                tempNode = getattr(curNode,func)()
                if tempNode not in s:
                    q.put(tempNode)
                    s.add(tempNode)
                    continue
            except NodeError:
                pass

    while curNode is not None:
        print(curNode)
        curNode = curNode.parent


def depthFirst():
    q = LifoQueue()
    s = set()
    first = Node(0,0,None)
    q.put(first)
    s.add(first)

    funcs = ["emptyA", "emptyB", "fillA", "fillB", "pourAB", "pourBA"]

    while True:

        if q.empty():
            print("Empty queue")
            break

        curNode = q.get()

        if curNode.A == 2:
            print("Success")
            break

        for func in funcs:
            try:
                tempNode = getattr(curNode,func)()
                if tempNode not in s:
                    q.put(tempNode)
                    s.add(tempNode)
            except NodeError:
                pass
       
    while curNode is not None:
        print(curNode)
        curNode = curNode.parent


def iterDepthFirst():

    for i in range(1, 1000):
        s = set()
        s.add(Node(0,0,None))
        result = iterDepthFirstAux(Node(0,0,None), i, 0, s)
        if result is not None:
            break
    
    while result is not None:
        print(result)
        result = result.parent


def iterDepthFirstAux(node, maxDepth, currentDepth, s):

    funcs = ["emptyA", "emptyB", "fillA", "fillB", "pourAB", "pourBA"]
    
    if currentDepth >= maxDepth:
        return None

    if node.A == 2:
        print("Success")
        return node

    for func in funcs:
        try:
            tempNode = getattr(node,func)()
            if tempNode not in s:
                s.add(tempNode)
                result = iterDepthFirstAux(tempNode, maxDepth, currentDepth + 1, s)
                if result is not None:
                    return result
        except NodeError:
            pass
    return None
    


if __name__ == "__main__":


    print("\nBreadth First")
    breadthFirst()

    print("\nDepth First")
    depthFirst()

    print("\nIterative Depth First")
    iterDepthFirst()