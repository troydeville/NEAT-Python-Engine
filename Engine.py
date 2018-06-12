import re
import math
import operator
from Link import Link
from Node import Node


class Engine():
    
    def __init__(self, confURL):
        file = open(confURL, 'r').read()
        nodeLines = re.findall(r'NODE_.*', file)
        linkLines = re.findall(r'Innovation_.*', file)

        linksToAdd = []
        nodesToAdd = []

        for link in linkLines:
            innovation = int(re.findall(r'Innovation_(.*?), ', link)[0])
            fromID = int(re.findall(r'from=(.*?) :', link)[0])
            toID = int(re.findall(r'to=(.*?) ],', link)[0])
            weight = float(re.findall(r'Weight: (.*?) --', link)[0])
            linksToAdd += [Link(innovation, toID, fromID, weight)]

        for node in nodeLines:
            nodeID = int(re.findall(r'NODE_(.*?), ', node)[0])
            nodeType = re.findall(r'Type: (.*?), ', node)[0]
            responseType = re.findall(r'Activation: (.*?), ', node)[0]
            response = float(re.findall(r'Response: (.*?), ', node)[0])
            position = float(re.findall(r'y: (.*?), z:', node)[0])
            nodesToAdd += [Node(nodeID, nodeType, responseType, response, position)]

        inputAmount = 0
        for node in nodesToAdd:
            if node.nodeType == "input":
                inputAmount += 1

        self.inputCount = inputAmount

        nodesToAdd.sort(key=operator.attrgetter('position'))

        
        
        self.nodes = nodesToAdd
        
        self.links = linksToAdd
        

    def run(self, inputs):

        output = []

        cNode = 0

        # run input nodes
        for x in range(0, self.inputCount):
            self.nodes[cNode].output = inputs[cNode]
            self.nodes[cNode].output = self.doActivation(self.nodes[cNode].responseType, self.nodes[cNode].output, self.nodes[cNode].response)
            cNode += 1

        # run bias node
        self.nodes[cNode].output = 1.0
        self.nodes[cNode].output = self.doActivation(self.nodes[cNode].responseType, self.nodes[cNode].output, self.nodes[cNode].response)
        cNode += 1

        # run hidden and output nodes
        while cNode < len(self.nodes):
            summation = 0.0

            cNodeId = self.nodes[cNode].nodeID
            incomingNodeIds = []
            incomingLinks = []

            for link in self.links:
                if link.toID == cNodeId:
                    incomingNodeIds += [link.fromID]

            for inNodeIds in range(0, len(incomingNodeIds)):
                for link in self.links:
                    if link.fromID == incomingNodeIds[inNodeIds] and link.toID == cNodeId:
                        incomingLinks += [link]
                        break
                    #endif
                # end for
            # end for
            #print("***START***")
            for link in incomingLinks:
                #print(link.innovation)
                #print(link.weight)
                weight = link.weight
                nodeOutput = 0.0
                for iNode in range(0, len(self.nodes)):
                    if self.nodes[iNode].nodeID == link.fromID:
                        nodeOutput = self.nodes[iNode].output
                        break
                # end for
                #print(nodeOutput)
                summation += weight * nodeOutput
                #print("\n")
            # end for
            #print("***END***")
            #print(summation)
            self.nodes[cNode].output = self.doActivation(self.nodes[cNode].responseType, summation, self.nodes[cNode].response)

            # Append to output
            if self.nodes[cNode].nodeType == "output":
                output += [self.nodes[cNode].output]

            cNode += 1
        # end while

        for node in range(0, len(self.nodes)):
            self.nodes[node].output = 0.0
            
        #print("\n")
        return output

    def doActivation(self, aType, x, response):

        if aType == "add":
            return x * response
        elif aType == "sigmoid":
            return 1 / (1 + math.exp(-4.9 * x * response))
        elif aType == "tanh":
            return math.tanh(x * response)
        elif aType == "relu":
            if x <= 0.0:
                return 0.0
            else:
                return x * response
        elif aType == "sine":
            return math.sin(x * response)
        elif aType == "abs":
            return math.fabs(x * response)
        elif aType == "square":
            return x * x * response
        elif aType == "cube":
            return x * x * x * response
        elif aType == "gauss":
            return (1 / math.sqrt(2*math.pi)) * math.exp((-1/2)*(x-response)*(x-response))
        elif aType == "clamped":
            if x < (-1 * response):
                return -1 * response
            elif x > (1 * response):
                return 1 * response
            else:
                return x * response
        elif aType == "hat":
            if x < (-1 * response):
                return 0.0
            elif x > (1 * response):
                return 0.0
            else:
                return x * response
        elif aType == "sinh":
            return math.sinh(x * (1/response))
        elif aType == "sech":
            return 1 / math.cosh(x * response)







        
