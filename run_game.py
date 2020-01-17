import pygame
import time
import random
import numpy as np
import scipy.special
from collections import defaultdict
import pandas as pd
from maze import Maze

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
#https://www.edureka.co/blog/snake-game-with-pygame/
pygame.init()
 
white = (255, 255, 255)
yellow = (155,135,12)
black = (0, 0, 0)
red = (255,0,0)#(213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

maze_w = 40
maze_h = 20
snake_block = 10

dis_width = maze_w * snake_block #600
dis_height = maze_h * snake_block #400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
snake_speed = 240
 
font_style = pygame.font.SysFont("bahnschrift", 15)
score_font = pygame.font.SysFont("comicsansms", 15)


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
    
    step_count=0
    def path_distance(source_no, target_no):
        return (target_no - source_no) % (maze_h*maze_w)
    def next_step(head, tail, food):
        head2 = head[0], maze.h - 1 - head[1]
        tail2 = tail[0], maze.h - 1 - tail[1]
        food2 = food[0], maze.h - 1 - food[1]
        head_num = maze.nodes[maze.coor2idx(head2[0], head2[1])].number
        tail_num = maze.nodes[maze.coor2idx(tail2[0], tail2[1])].number
        food_num = maze.nodes[maze.coor2idx(food2[0], food2[1])].number
        dist_food = path_distance(head_num, food_num)
        dist_tail = path_distance(
            head_num, tail_num) if head_num != tail_num else (maze_h*maze_w)-1
        cutting_amount = dist_tail - 4
        empty_sq = (maze_h*maze_w) - len(snake_List) - 1
        if empty_sq < (maze_h*maze_w)/2:
            cutting_amount = 0 
        elif dist_food < dist_tail:
            cutting_amount -= 1
            cutting_amount -= 10 if ((dist_tail - dist_food)*4) > empty_sq else 0
        cutting_desired = dist_food
        cutting_amount = cutting_desired if cutting_desired < cutting_amount else cutting_amount
        cutting_amount = 0 if cutting_amount < 0 else cutting_amount

        best_dis = -1
        best_dir = None
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = head2[0]+i, head2[1]+j
            if new_x < 0 or new_x >= maze_w or new_y < 0 or new_y >= maze_h or [new_x, new_y] in snake_List:
                continue
            path_num = maze.nodes[maze.coor2idx(new_x, new_y)].number
            # temp_head_num = head_num
            # if head_num > tail_num:
            #     temp_head_num = head_num + (maze_h*maze_w)
            #     path_num += (maze_h*maze_w)
            # if (path_num >= tail_num) and (path_num <= temp_head_num):
            #     continue
            path_dist = path_distance(head_num, path_num)
            # if path_dist >= dist_tail:
            #     continue
            if (path_dist <= cutting_amount) and (path_dist > best_dis): 
                best_dis = path_dist
                best_dir = (-i, -j)
        # print('###################################################################')
        # print(dist_food)
        # print(dist_tail)
        # print(cutting_amount)
        # print(best_dis)
        # print('###################################################################')
        if best_dis >= 0:
            step = best_dir
            # print('shortcuttttttttttttttttttttttttttttttttttttttttttttttttttt')
        else:
            current_index = maze.path.index(head2)
            next_coor = maze.path[(current_index+1)%len(maze.path)]
            step = tuple(np.array(head2)-np.array(next_coor))
        



        # input('>')
        if step == (1,0):
            print("left")
            return LEFT
        elif step == (-1, 0):
            print("right")
            return RIGHT
        elif step == (0, 1):
            print("down")
            return DOWN
        else:
            print("up")
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
            score=Length_of_snake - 1

            if score == (maze_w * maze_h) -1 :
                message("You Won! Press C-Play Again or Q-Quit", blue)
 
            else:
                message("You Lost! Press\n C-Play Again or \nQ-Quit", red)

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
        if len(snake_List) == 0:
            step = next_step((x1//snake_block, y1//snake_block),
                             (x1//snake_block, y1//snake_block),
                             (foodx//snake_block, foody//snake_block))
        else:
            step = next_step((x1//snake_block, y1//snake_block),
                             tuple(np.array(snake_List[0])//snake_block), 
                             (foodx//snake_block, foody//snake_block))
        step_count+=1
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
        pygame.draw.rect(dis, red, [foodx, foody, snake_block-1, snake_block-1])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        print('_________________')
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        if Length_of_snake == (maze_w * maze_h):
            game_close=True 
            continue

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            while [foodx ,foody] in snake_List:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()
