class NodeError(Exception):
    pass

class Node: 
    maxA = 4
    maxB = 3

    def __init__(self, A, B, parent):
        self.A = A
        self.B = B
        self.parent = parent


    def emptyA(self):
        if self.A > 0:
            return Node(0,self.B, self)
        else:
            raise NodeError()

    def emptyB(self):
        if self.B > 0:
            return Node(self.A, 0, self)
        else:
            raise NodeError()
    
    def fillA(self):
        if self.A < Node.maxA:
            return Node(Node.maxA, self.B, self)
        else:
            raise NodeError()

    def fillB(self):
        if self.B < Node.maxB:
            return Node(self.A, Node.maxB, self)
        else:
            raise NodeError

    def pourAB(self):
        if self.A + self.B >= Node.maxB and self.B < Node.maxB:
            return Node(self.A - (Node.maxB - self.B), Node.maxB, self)
        elif self.A + self.B < Node.maxB and self.A > 0:
            return Node(0, self.A + self.B, self)
        else:
            raise NodeError()

    def pourBA(self):
        if self.A + self.B >= Node.maxA and self.A < Node.maxA:
            return Node(Node.maxA, self.B - (Node.maxA - self.A), self)
        elif self.A + self.B < Node.maxA and self.B > 0:
            return Node(self.A + self.B, 0, self)
        else:
            raise NodeError()

    def __eq__(self, other):
        return self.A == other.A and self.B == other.B 

    def __hash__(self):
        return hash((self.A, self.B))

    def __str__(self):
        return "A:{}|B:{}".format(self.A, self.B)