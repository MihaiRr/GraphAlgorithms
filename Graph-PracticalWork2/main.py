'''
Created on Mar 21, 2019

@author: reteg
'''
import traceback

from directed_graph import DirectedGraph
from ui import UI
import pydoc


def main():
    '''
    Main program
    '''
    graph = DirectedGraph("graph1k.txt")
    cmdDict = {0: UI.exitApp,
               1: UI.nrOfVertices,
               2: UI.edgeBetween,
               3: UI.inOutDegree,
               4: UI.outboundEdges,
               5: UI.inboundEdges,
               6: UI.endpointsOfEdge,
               7: UI.retriveCost,
               8: UI.modifyCost,
               9: UI.addVertex,
               10: UI.removeVertex,
               11: UI.addEdge,
               12: UI.removeEdge,
               13: UI.saveGraph,
               14: UI.printMenu}

    UI.printMenu()
    while True:
        try:
            cmd = UI.readCommand()
            cmdDict[cmd](graph)
        except Exception as ex:
            traceback.print_exc()
            print(ex)


main()