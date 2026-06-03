import sys
import os
from graph import Graph, Vertex
from priority_queue import PriorityQueue
class DeliveryService:
    def __init__(self)->None:
        self.city_map=Graph()
        self.MST=None
    def buildMap(self,filename:str)->None: 
        filepath=os.path.join(os.getcwd(),filename) #full path to file
        with open(filepath,'r') as file:
            lines=file.readlines() #reads lines from file
        for line in lines:
            node1,node2,cost=map(int,line.strip().split('|'))
            vertex1=self.city_map.getVertex(node1) #recieves vertex from node1
            vertex2=self.city_map.getVertex(node2) #recieves vertex from node2
            if vertex1 is None:
                vertex1=self.city_map.addVertex(node1) #adds vertex for node1 if doesnt already exist
            if vertex2 is None:
                vertex2=self.city_map.addVertex(node2) #adds vertex for node2 if doesnt already exist
            self.city_map.addEdge(node1,node2,cost) #adds edge between node1 and node2 with given cost
            self.city_map.addEdge(node2,node1,cost) #adds bidirectional edge
    def isWithinServiceRange(self,restaurant:int,user:int,threshold:int)->bool:
        if user not in self.city_map.vertList: #if user node not found, not in service range
            return False
        visit=set() #keeps tracks of visited nodes during traversal
        queue=[restaurant] #starts BFS from restaurant node
        while queue:
            currentnode=queue.pop(0) #dequeues front-most node
            if currentnode==user:
                return True #if user node reached, return True
            visit.add(currentnode) #mark current node as visited
            for neighbor in self.city_map.vertList[currentnode].getConnections(): #enqueues neighboring nodes
                if neighbor.getId() not in visit:
                    queue.append(neighbor.getId())
        return False #if user node still not reached, return False
    def buildMST(self,restaurant:int)->bool:
        self.MST=Graph() #initialize MST as graph
        visit=set() #keeps track of visited nodes
        priority_queue=PriorityQueue() #Priority queue to keep track of visted nodes and their distances
        for v in self.city_map: #initializes distance for all vertices
            v.setDistance(float('inf'))
            v.setPred(None)
        start=self.city_map.getVertex(restaurant) #starting vertex
        start.setDistance(0) #sets starting distance to 0
        priority_queue.buildHeap([(v.getDistance(),v) for v in self.city_map]) #builds heap for priority queue with distances and vertices
        while not priority_queue.isEmpty():
            currentvertex=priority_queue.delMin() #dequeues vertex with smallest distance
            if currentvertex.getId() not in visit:
                visit.add(currentvertex.getId()) #marks current vertex as visited
                if currentvertex.getPred() is not None: #adds vertex and its edge to MST
                    self.MST.addVertex(currentvertex.getId())
                    self.MST.addEdge(currentvertex.getPred().getId(),currentvertex.getId(),currentvertex.getDistance(),)
                for nextvertex in currentvertex.getConnections():
                    newcost=currentvertex.getWeight(nextvertex)
                    if nextvertex in priority_queue and newcost<nextvertex.getDistance():
                        nextvertex.setPred(currentvertex)
                        nextvertex.setDistance(newcost)
                        priority_queue.decreaseKey(nextvertex,newcost)
        return True
    def minimalDeliveryTime(self,restaurant:int,user:int)->int:
        if restaurant not in self.city_map.vertList or user not in self.city_map.vertList:
            return -1
        dist={}
        for v in self.MST:
            dist[v.getId()]=float('inf')
        dist[restaurant]=0
        for a in range(len(self.MST.vertList)-1):
            for v in self.MST:
                for nextvertex in v.getConnections():
                    weight=v.getWeight(nextvertex)
                    if dist[v.getId()]!=float("inf") and dist[v.getId()]+weight<dist[nextvertex.getId()]:
                        dist[nextvertex.getId()]=dist[v.getId()]+weight
        return dist[user]
    def findDeliveryPath(self,restaurant:int,user:int)->str:
        if restaurant not in self.city_map.vertList or user not in self.city_map.vertList:
            return "INVALID"
        dist={}
        pred={}
        for v in self.city_map:
            dist[v.getId()]=float('inf')
            pred[v.getId()]=None
        dist[restaurant]=0
        for b in range(len(self.city_map.vertList)-1):
            for v in self.city_map:
                for nextvertex in v.getConnections():
                    weight=v.getWeight(nextvertex)
                    if dist[v.getId()]!=float('inf') and dist[v.getId()]+weight<dist[nextvertex.getId()]:
                        dist[nextvertex.getId()]=dist[v.getId()]+weight
                        pred[nextvertex.getId()]=v.getId()
        path=[user]
        currentvertex=user
        while pred[currentvertex] is not None:
            path.append(pred[currentvertex])
            currentvertex=pred[currentvertex]
        path.reverse()
        totdist=0
        for i in range(len(path)-1):
            totdist+=self.city_map.getVertex(path[i]).getWeight(self.city_map.getVertex(path[i+1]))
        return "->".join(map(str,path))+f"({totdist})"
    def findDeliveryPathWithDelay(self,restaurant:int,user:int,delay_info:dict[int,int])->str:
        if restaurant not in self.city_map.vertList or user not in self.city_map.vertList:
            return "INVALID"
        dist={}
        pred={}
        for v in self.city_map:
            dist[v.getId()]=float('inf')
            pred[v.getId()]=None
        dist[restaurant]=0
        for c in range(len(self.city_map.vertList)-1):
            for v in self.city_map:
                for nextvertex in v.getConnections():
                    weight=v.getWeight(nextvertex)
                    delay=delay_info.get(nextvertex.getId(),0)
                    if dist[v.getId()]!=float('inf') and dist[v.getId()]+weight+delay<dist[nextvertex.getId()]:
                        dist[nextvertex.getId()]=dist[v.getId()]+weight+delay
                        pred[nextvertex.getId()]=v.getId()
        path=[user]
        currentvertex=user
        while pred[currentvertex] is not None:
            path.append(pred[currentvertex])
            currentvertex=pred[currentvertex]
        path.reverse()
        totdist=0
        for i in range(len(path)-1):
            totdist+=self.city_map.getVertex(path[i]).getWeight(self.city_map.getVertex(path[i+1]))
        return "->".join(map(str,path))+f"({totdist})"
    ## DO NOT MODIFY CODE BELOW!
    @staticmethod
    def nodeEdgeWeight(v):
        return sum([w for w in v.connectedTo.values()])

    @staticmethod
    def totalEdgeWeight(g):
        return sum([DeliveryService.nodeEdgeWeight(v) for v in g]) // 2

    @staticmethod
    def checkMST(g):
        for v in g:
            v.color = 'white'

        for v in g:
            if v.color == 'white' and not DeliveryService.DFS(g, v):
                return 'Your MST contains circles'
        return 'MST'

    @staticmethod
    def DFS(g, v):
        v.color = 'gray'
        for nextVertex in v.getConnections():
            if nextVertex.color == 'white':
                if not DeliveryService.DFS(g, nextVertex):
                    return False
            elif nextVertex.color == 'black':
                return False
        v.color = 'black'

        return True

# NO MORE TESTING CODE BELOW!
# TO TEST YOUR CODE, MODIFY test_delivery_service.py

learnrate=0.2
num_iteration=1000


