import pygame
import time
import random
import numpy as np
import scipy.special
from collections import defaultdict
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt


pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255,0,0)#(213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

maze_w = 10
maze_h = 10
snake_block = 10

dis_width = maze_w * snake_block #600
dis_height = maze_h * snake_block #400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 15)
score_font = pygame.font.SysFont("comicsansms", 15)

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
        return x + y*(self.w) if y%2==0 else self.w - 1 - x + y*(self.w)
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
 
 
def Your_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [dis_height-70, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

UP, LEFT, RIGHT, DOWN = range(4)

 
 
def gameLoop():
    game_over = False
    game_close = False
    maze = Maze(maze_w, maze_h)
    maze.generate_hamiltonian_path()
    maze.generate_cycle()
    print(maze.path)
    
    def next_step(head):
        head2 = head[0], maze.h - 1 - head[1]
        current_index = maze.path.index(head2)
        next_coor = maze.path[(current_index+1)%len(maze.path)]
        step = tuple(np.array(head2)-np.array(next_coor))
        print(next_coor)
        print(head2)
        print(step)
        # input('>')
        if step == (1,0):
            return LEFT
        elif step == (-1, 0):
            return RIGHT
        elif step == (0, 1):
            return DOWN
        else:
            return UP

    x1 = maze.start.x #dis_width / 2
    y1 =( maze_h - 1 - maze.start.y)*snake_block#dis_height / 2
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
        
        while game_close == True:
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         game_over = True
            # print((x1//snake_block, y1//snake_block))
        step = next_step((x1//snake_block, y1//snake_block))
            # if event.type == pygame.KEYDOWN:
                #i = random.randint(1,4)
        if step == LEFT:
        #if i == 1:
            x1_change = -snake_block
            y1_change = 0
        elif step == RIGHT:
        #elif i == 2:
            x1_change = snake_block
            y1_change = 0
        elif step == UP:
        #elif i==3:
            y1_change = -snake_block
            x1_change = 0
        elif step == DOWN:
        #elif i==4:
            y1_change = snake_block
            x1_change = 0
        # try:
        #     print(snake_List[0],snake_List[-1])
        # except:
            # pass
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        print('555555555555555555555555555555555')
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()
