'''
Created on Mar 21, 2019

@author: reteg
'''
import heapq
import pydoc

class DirectedGraph(object):
    '''
    Graph class
    Create the graph and all does all operation on graph (add/remove edge/vertex, cost of edge etc)
    '''
    def __init__(self, fileName):
        self.__vertices = 0
        self.__verticesList = []
        self.__edges = 0
        self.__graphIn = {}
        self.__graphOut = {}
        self.__costs = {}
        self.__edgeIDs = {}
        self.__edgesList = []
        self.readGraph(fileName)

    def __str__(self):
        string=''
        for i in self.__graphOut.keys():
            string+=str(i)+"\n"
            string+=str(self.__graphIn[i])+"\n"
            
            string+=str(self.__graphOut[i])+"\n"
            
        return string
            
    def readGraph(self, fileName):
        '''
        Function that read and create an graph
        '''
        
        id = 0
        with open(fileName, "r") as graph:
            line = graph.readline().split()
            self.__vertices = int(line[0])
            self.__verticesList = [el for el in range(self.__vertices)]
            for i in range(0, self.__vertices):
                self.graphOut[i] = []
                self.graphIn[i] = []

            self.__edges = int(line[1])
            
           
            try:
                line = graph.readline().split()
                while line != []:
                    edge = Edge(int(line[0]), int(line[1]), int(line[2]), id)
                    id += 1
                    self.addEdge(edge.x, edge.y, edge.cost, edge.ID)
                    line = graph.readline().split()

            except EOFError as eof:
                graph.close()
            except Exception as ex:
                print(ex)


    def addEdge(self, vertexStart, vertexEnd, cost, id):
        '''
        Function that add an edge to graph
        '''
        if self.vertexExists(vertexStart) and self.vertexExists(vertexEnd):
            if not self.isEdge(vertexStart, vertexEnd):
                if id not in self.__edgeIDs.keys():
                    self.__edgesList.append(Edge(vertexStart, vertexEnd, cost, id))
                    self.__edgesList.append(Edge(vertexEnd, vertexStart, cost, id))
                    self.__graphOut[vertexStart].append(vertexEnd)
                    self.__graphIn[vertexEnd].append(vertexStart)
                    self.__costs[vertexStart, vertexEnd] = cost
                    self.__edgeIDs[id] = [vertexStart, vertexEnd]
                else:
                    raise Exception("ID {0} already exists!".format(id))
            else:
                raise Exception("Edge {0} -> {1} already exists!".format(vertexStart, vertexEnd))
        else:
            raise Exception("One or both vertices does not exists!")

    def removeEdge(self, vertexStart, vertexEnd):
        '''
        Function that remove an edge to graph
        '''
        if self.isEdge(vertexStart, vertexEnd):
            self.__graphOut[vertexStart].remove(vertexEnd)
            self.__graphIn[vertexEnd].remove(vertexStart)
            
            self.__costs.pop(vertexStart, vertexEnd)

            for id, edge in self.__edgeIDs.copy().items():
                if edge == [vertexStart, vertexEnd]:
                    self.__edgeIDs.pop(id)
                   

        else:
            raise Exception("Edge {0} -> {1} does not exists!".format(vertexStart, vertexEnd))

    def getCostOf(self, edgeID):
        '''
        Function that check if edge exist and return costs
        '''
        if self.edgeIDExists(edgeID):
            return self.__costs[tuple(self.__edgeIDs[edgeID])]
        else:
            raise Exception("Edge with id {0} does not exists!".format(edgeID))

    def getCostOfEdge(self, vStart, vEnd):
        '''
        return the cost of an edge
        '''
        c1 = None
        c2 = None
        c1 = self.__costs.get(tuple([vStart, vEnd]))
        c2 = self.__costs.get(tuple([vEnd, vStart]))

        if c1 != None:
            return c1

        if c2 != None:
            return c2

        return None

    def modifyCostOf(self, edgeID, newCost):
        '''
        modify the cost of an edge
        '''
        if self.edgeIDExists(edgeID):
            self.__costs[tuple(self.__edgeIDs[edgeID])] = newCost
        else:
            raise Exception("Edge with id {0} does not exists!".format(edgeID))

    def getEndpointsOf(self, edgeID):
        
        if self.edgeIDExists(edgeID):
            return self.__edgeIDs[edgeID]
        else:
            raise Exception("Edge with id {0} does not exists!".format(edgeID))


    def edgeIDExists(self, edgeID):
        '''
        return True if edge exist; else return False 
        '''
        return edgeID in self.__edgeIDs.keys()

    def isEdge(self, vertexStart, vertexEnd):
        '''
        
        '''
        return vertexEnd in self.__graphOut[vertexStart]

    def inDegreeOf(self, vertex):
        '''
        return in degree of a vertex
        '''
        return len(self.__graphIn[vertex])

    def outDegreeOf(self, vertex):
        '''
        return out degree of a vertex
        '''
        return len(self.__graphOut[vertex])

    def vertexExists(self, vertex):
        '''
        check if vertex exists
        '''
        return vertex in self.verticesList

    def outboundEdgesOf(self, vertex):
        '''
        return out bounds list of a vertex
        '''
        return self.__graphOut[vertex]

    def inboundEdgesOf(self, vertex):
        '''
        return in bounds list of a vertex
        '''
        return self.__graphIn[vertex]

    def isolatedNodes(self):
        '''
        creates a list with isloated nodes
        '''
        isolated = []
        for el in range(self.vertices):
            if self.graphIn[el] == [] and self.graphOut[el] == []:
                isolated.append(el)
        return isolated

    def addVertex(self, vertex):
        '''
        add a vertex
        '''
        self.graphIn[vertex] = []
        self.graphOut[vertex] = []
        self.vertices = 1
        self.verticesList.append(vertex)

    def removeVertex(self, vertex):
        '''
        remove a vertex
        '''
        self.verticesList.remove(vertex)
        self.graphOut.pop(vertex)
        self.graphIn.pop(vertex)
        self.vertices = -1


    @property
    def verticesList(self):
        return self.__verticesList

    @property
    def vertices(self):
        return self.__vertices

    @vertices.setter
    def vertices(self, increment):
        self.__vertices += increment

    @property
    def edges(self):
        return len(self.__costs)

    @property
    def graphIn(self):
        return self.__graphIn

    @property
    def graphOut(self):
        return self.__graphOut

    @property
    def costs(self):
        return self.__costs

    @property
    def edgeIDs(self):
        return self.__edgeIDs

class Edge(object):
    '''
    class that refer to an edge: from which vertex, cost and id 
    '''
    def __init__(self, x, y, cost, ID):
        self.__x = x
        self.__y = y
        self.__cost = cost
        self.__ID = ID

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def cost(self):
        return self.__cost

    @property
    def ID(self):
        return self.__ID

#help(DirectedGraph)
