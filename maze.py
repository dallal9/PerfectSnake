import numpy as np
import pandas as pd

class Node:
    def __init__(self, x, y, p, c):
        self.x = x
        self.y = y
        self.coor = (x, y)
        self.parent = p # p is a tuple in the form (x,y)
        self.child = c # c is a tuple in the form (x,y)
        self.number = -1
class Maze:
    def __init__(self, width, height):
        self.nodes = [] # list of nodes
        self.w = width
        self.h = height
        self.start = Node(0,0,-1, (1,0))
        self.end = Node(0, height-1, (1, height-1), -1)
    def generate_hamiltonian_path(self):
        reverse = -1
        for j in range(self.h):
            reverse *= -1
            for i in range(self.w)[::reverse]:
                if (i,j) == self.start.coor:
                    self.nodes.append(self.start)
                    continue
                if (i,j) == self.end.coor:
                    self.nodes.append(self.end)
                    continue
                if i > 0 and i < self.w-1:
                    self.nodes.append(Node(i, j, (i-reverse, j), (i+reverse, j)))
                else:
                    if j%2==0:
                        self.nodes.append(Node(i, j, (i, j-1), (i+1, j)) if i == 0 else Node(i, j, (i-1, j), (i, j+1)))
                    else:
                        self.nodes.append(Node(i, j, (i+1, j), (i, j+1)) if i == 0 else Node(i, j, (i, j-1), (i-1, j)))
    def coor2idx(self,x,y):
        return int(x + y*(self.w) if y%2==0 else self.w - 1 - x + y*(self.w))
    def __get_neighbors(self, node):
        x, y = node.coor
        neighbors = []
        steps = [(1,0), (-1,0), (0,1), (0,-1)]
        for i,j in steps:
            new_x, new_y = x+i, y+j
            if new_x < 0 or new_x >= self.w or new_y < 0 or new_y >= self.h:
                continue
            if ((new_x,new_y) == node.child) or ((new_x,new_y) == node.parent):
                continue
            neighbors.append((new_x, new_y))
        assert len(neighbors) > 0, "something wrong with neighborhood generation"
        return neighbors
    def are_neighbors(self, node1, node2):
        return 1 if (abs(node1.x - node2.x) + abs(node1.y - node2.y)) < 2 else 0
    def __fix_circuit(self, start, end):
        # start and end are both tuples in the form (x, y)
        current = start
        current_parent = self.nodes[self.coor2idx(current[0], current[1])].parent
        while current != end:
            old = current
            current = current_parent
            current_parent = self.nodes[self.coor2idx(current[0], current[1])].parent
            self.nodes[self.coor2idx(current[0], current[1])].parent = old
            self.nodes[self.coor2idx(old[0], old[1])].child = current
        self.nodes[self.coor2idx(start[0], start[1])].parent = -1


        
    def generate_cycle(self):
        while not(self.are_neighbors(self.start, self.end)):
            start_neighbors = self.__get_neighbors(self.start)
            next_idx = np.random.choice(range(len(start_neighbors)))
            end = start_neighbors[next_idx]
            self.start.parent = end
            start = self.nodes[self.coor2idx(end[0], end[1])].parent
            self.start = self.nodes[self.coor2idx(start[0], start[1])]
            self.__fix_circuit(start, end)
        self.start.parent = self.end.coor
        self.end.child = self.start.coor
        self.path = self.get_path()
    def get_path(self):
        path = []
        current = self.start.coor
        i = 0
        while (current != self.start.coor) or (i==0):
            path.append(current)
            self.nodes[self.coor2idx(current[0], current[1])].number = i
            i += 1
            current = self.nodes[self.coor2idx(current[0], current[1])].child
            if current == -1:
                break
        return path
    def draw_path(self):
        plt.figure(figsize=(16,16))
        path = self.get_path()
        x, y = [], []
        for i, j in path:
            x.append(i)
            y.append(j)
        plt.plot(x, y, '--x')
#         for i in range(len(x)):
#             plt.annotate(i, (x[i], y[i]))
 
