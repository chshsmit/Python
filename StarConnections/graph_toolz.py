
import os
import sys
import math
import queue

WHITE = 'WHITE'
BLACK = 'BLACK'
GRAY = 'GRAY'

class Graph(object):

    # Initializing empty graph
    def __init__(self):
        self.adj_list = dict()    # Initial adjacency list is empty dictionary
        self.vertices = set()    # Vertices are stored in a set
        self.degrees = dict()    # Degrees stored as dictionary

    # Checks if (node1, node2) is edge of graph. Output is 1 (yes) or 0 (no).
    def isEdge(self,node1,node2):
        if node1 in self.vertices:        # Check if node1 is vertex
            if node2 in self.adj_list[node1]:    # Then check if node2 is neighbor of node1
                return 1            # Edge is present!

        if node2 in self.vertices:        # Check if node2 is vertex
            if node1 in self.adj_list[node2]:    # Then check if node1 is neighbor of node2
                return 1            # Edge is present!

        return 0                # Edge not present!

    # Add undirected, simple edge (node1, node2)
#------------------------------------------------------------------------------------------------------------------------ 
    def addEdge(self,node1,node2):

        # print('Called')
        if node1 == node2:            # Self loop, so do nothing
            # print('self loop')
            return
        if node1 in self.vertices:        # Check if node1 is vertex
            nbrs = self.adj_list[node1]        # nbrs is neighbor list of node1
            if node2 not in nbrs:         # Check if node2 already neighbor of node1
                nbrs.add(node2)            # Add node2 to this list
                self.degrees[node1] = self.degrees[node1]+1    # Increment degree of node1

        else:                    # So node1 is not vertex
            self.vertices.add(node1)        # Add node1 to vertices
            self.adj_list[node1] = {node2}    # Initialize node1's list to have node2
            self.degrees[node1] = 1         # Set degree of node1 to be 1

        if node2 in self.vertices:        # Check if node2 is vertex
            nbrs = self.adj_list[node2]        # nbrs is neighbor list of node2
            if node1 not in nbrs:         # Check if node1 already neighbor of node2
                nbrs.add(node1)            # Add node1 to this list
                self.degrees[node2] = self.degrees[node2]+1    # Increment degree of node2

        else:                    # So node2 is not vertex
            self.vertices.add(node2)        # Add node2 to vertices
            self.adj_list[node2] = {node1}    # Initialize node2's list to have node1
            self.degrees[node2] = 1         # Set degree of node2 to be 1

    # Give the size of the graph. Outputs [vertices edges wedges]
#------------------------------------------------------------------------------------------------------------------------ 

    def size(self):
        n = len(self.vertices)            # Number of vertices

        m = 0                    # Initialize edges/wedges = 0
        wedge = 0
        for node in self.vertices:        # Loop over nodes
            deg = self.degrees[node]      # Get degree of node
            m = m + deg             # Add degree to current edge count
            wedge = wedge+deg*(deg-1)/2        # Add wedges centered at node to wedge count
        return [n, m, wedge]            # Return size info
#------------------------------------------------------------------------------------------------------------------------ 
    # Print the graph
    def output(self,fname,dirname):
        os.chdir(dirname)
        f_output = open(fname,'w')

        for node1 in list(self.adj_list.keys()):
            f_output.write(str(node1)+': ')
            for node2 in (self.adj_list)[node1]:
                f_output.write(str(node2)+' ')
            f_output.write('\n')
        f_output.write('------------------\n')
        f_output.close()

#------------------------------------------------------------------------------------------------------------------------
#Returns the shortest path in a graph from src to dest    
    def path(self, src, dest):
        shortest_path = []         #Initializes array for the path
        color = dict()             #Initializes empty dictionaries for the color, distance, and predecessor of each node
        distance = dict()
        predecessor = dict()
        

        for vertex in self.vertices.difference(src):    #Visit each vertex in the graph except for the source
            color[vertex] = WHITE           #Change every vertex color to white
            distance[vertex] = math.inf     #Set the distance of each vertex to infinity
            predecessor[vertex] = None      #Set each predecessor to undefined

        color[src] = GRAY           #The src has been visited but is in queue
        distance[src] = 0           #The distance from src to src is 0
        predecessor[src] = None     #The src has no predecessor

        myQueue = queue.Queue()     #Initialize an empty queue

        myQueue.put(src)            #Put source in the queue

        while myQueue.empty() == False:     #Runs while the queue is not empty
            node = myQueue.get()        #Node is initial value in queue

            if node == dest:            #We found our destination!!
                break

            for neighbor in self.adj_list[node]:    #Visit every node in the node's adjacency list
                if color[neighbor] == WHITE:        #Checks if the neighbor hasn't been visited
                    color[neighbor] = GRAY          #Neighbor has been visited and is in the queue
                    distance[neighbor] = distance[node] + 1     #The distance from the neighbor to the node increases by 1
                    predecessor[neighbor] = node            #Set the predecessor of neighbor
                    myQueue.put(neighbor)                   #Put neighbor in the queue

            color[node] = BLACK         #The node has been visited and removed from the queue

        while predecessor[node] != None:    #Adds each vertex to the path (implemented as a stack)
            shortest_path.append(node)      #Add node to the path
            node = predecessor[node]        #Node is now its own predecessor

        shortest_path.append(node)      #Add node to path

        shortest_path = list(reversed(shortest_path))   #Reverse the stack
        return shortest_path

#------------------------------------------------------------------------------------------------------------------------ 
#Returns an array where every element corresponds to the number of nodes at a distance i (the index) away from the src

    def levels(self, src):
        level_sizes = []        #Initializes array for the level sizes
        color = dict()          #Initializes empty dictionaries for the color, distance, and predecessor of each node
        distance = dict()
        predecessor = dict()
        
        for i in range(0,7):        #Initializes each value to be 0
            level_sizes.append(0)


        level_sizes[0] = 1          #Only the source node has distance 0

        for vertex in self.vertices.difference(src):        #Visit every vertex in the graph except the source
            color[vertex] = WHITE           #Change every vertex color to white
            distance[vertex] = math.inf     #Set the distance of each vertex to infinity
            predecessor[vertex] = None      #Set each predecessor to undefined

        color[src] = GRAY           #The src has been visited but is in queue
        distance[src] = 0           #The distance from src to src is 0
        predecessor[src] = None     #The src has no predecessor

        myQueue = queue.Queue()     #Initialize an empty queue

        myQueue.put(src)        #Put source in the queue

        while myQueue.empty() == False:         #Runs while the queue is not empty
            node = myQueue.get()                #node is initial value in queue

            for neighbor in self.adj_list[node]:    #Visit every node in the node's adjacency list
                if color[neighbor] == WHITE:        #Checks if the neighbor hasn't been visited
                    color[neighbor] = GRAY          #Neighbor has been visited and is in the queue

                    distance[neighbor] = distance[node] + 1    #We now know the distance to this neighbor!

                    index = distance[neighbor]   #Index is the distance to neighbor

                    if index < 6:               #Increases corresponding level index
                        level_sizes[index] += 1
                    else:
                        # print(neighbor)           #We used these prints to figure out Q5
                        # print(distance[neighbor])
                        level_sizes[6] += 1

                    predecessor[neighbor] = node    #Set the predecessor of neighbor 
                    myQueue.put(neighbor)           #Put neighbor in the queue

            color[node] = BLACK         #The node has been visited and removed from the queue

        #print(level_sizes)
        return level_sizes
