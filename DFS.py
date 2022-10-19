from array import *
import pygame
from pygame.locals import *
import os
import sys

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
light_yellow = (255, 255, 102)
# Initialize pygame
pygame.init()
#create the screen
screen = pygame.display.set_mode((20*60, 20*30))
# fill a cell with a color and draw a border
def fill_cell (x1, y1, x2, y2, color):
    pygame.draw.rect(screen, color, (x1, y1, x2, y2))
    pygame.draw.rect(screen, black, (x1, y1, x2, y2), 1)
#fill screen background with white
screen.fill(black)
#read maze from file
def read_maze(file_path):
    maze = []
    bonus = {}
    with open(file_path, "r") as f:
        n = int(f.readline()) # number of bonus point
        if n > 0:
            for i in range(n):
                i, j, p = map(int, f.readline().split())
                bonus[(i, j)] = p
        for line in f:
            maze.append(line)
    # check the goal in maze
    for i in range(len(maze[0])):
        if maze[0][i] == " ":
            maze[0] = maze[0][:i] + "G" + maze[0][i+1:] #if " " is found in border, change it to "G"
    for i in range(len(maze[len(maze) - 1])):
        if maze[len(maze) - 1][i] == " ":
            maze[len(maze) - 1] = maze[len(maze) - 1][:i] + "G" + maze[len(maze) - 1][i+1:]
    for i in range(1, len(maze) - 2):
        if maze[i][0] == " ":
            maze[i] = maze[i][:0] + "G" + maze[i][1:]
        elif maze[i][len(maze[i]) - 1] == " ":
            maze[i] = maze[i][:len(maze[i]) - 1] + "G" + maze[i][len(maze[i]):]
    return maze, bonus

#set the maze
def setup_maze(maze):                          
    for y in range(len(maze)):                 
        for x in range(len(maze[y])):          
            if maze[y][x] == "X":              # if the cell is a wall
                fill_cell(x*20, y*20, 20, 20, blue)
                pygame.display.update()
            #if maze[y][x] == " ":                   

            if maze[y][x] == "G":                      # if the cell is the goal
                fill_cell(x*20, y*20, 20, 20, red)
                pygame.display.update()
            if maze[y][x] == "S":               # if the cell is the start
                fill_cell(x*20, y*20, 20, 20, white)
                pygame.display.update()

# find the start point
def f_start(maze):  
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "S":
                start=(y,x)
                return start
    return None

# find the goal point
def f_goal(maze): 
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "G":
                goal=(y,x)
                return goal
    return None

# find the neighbors of the current cell
def find_neighbors(maze, current):  
    neighbors = []
    if current[0] > 0:
        if maze[current[0] - 1][current[1]] != "X": # check if the cell above is not a wall
            neighbors.append((current[0] - 1, current[1]))
    if current[0] < len(maze) - 1:
        if maze[current[0] + 1][current[1]] != "X": # check if the cell below is not a wall
            neighbors.append((current[0] + 1, current[1]))
    if current[1] > 0:
        if maze[current[0]][current[1] - 1] != "X": # check if the cell to the left is not a wall
            neighbors.append((current[0], current[1] - 1))
    if current[1] < len(maze[0]) - 1:
        if maze[current[0]][current[1] + 1] != "X": # check if the cell to the right is not a wall
            neighbors.append((current[0], current[1] + 1))
    return neighbors

#find the path from the start to the goal
def search(maze):
    start = f_start(maze)       # find the start position
    goal=f_goal(maze)           # find the goal position
    frontier=[]                # create a frontier list_ LIFO
    frontier.append(start)      # add the start position to the frontier list
    visited={}                  # create a visited dictionary
    visited[start]=None         # add the start position to the visited dictionary
    flag=0   
    if(start !=None and goal!=None)  :                    # flag to indicate if the goal has been found
        while len(frontier) > 0:                           # loop until the frontier list is empty
            cur=frontier.pop()                            # current cell equals x and  y positions
            if cur==goal:
                fill_cell(cur[1]*20, cur[0]*20, 20, 20, red)    # fill the current cell with red
                flag=1                                      #find the goal_ flag=1
                break
            for next in find_neighbors(maze,cur):           # find the neighbors of the current cell
                if next not in visited:                     # if the neighbor is not in the visited dictionary
                    frontier.append(next )
                    visited[next]=cur
                    fill_cell(next[1]*20, next[0]*20, 20, 20, green)    # fill the neighbor cell with green
                    pygame.display.update()
                    pygame.time.wait(10)   
    return visited,flag                                     # return the visited dictionary and the flag
    
def draw_path(maze, visited,flag): # draw the path from the start to the goal if the goal is found
    if flag==1:
        start=f_start(maze)
        goal=f_goal(maze)
        current = goal
        while current != start:
            current = visited[current]
            fill_cell(current[1]*20, current[0]*20, 20, 20, light_yellow)
            pygame.display.update()
            pygame.time.wait(10)
        fill_cell(current[1]*20, current[0]*20, 20, 20, white)
        pygame.display.update()
        pygame.time.wait(10)
        print("The goal is found")
    else:
        print("no path found")

#write path to output file
def write_output(maze, visited, file_path,flag):
    if flag==1:
        # directory of output file
        f = open("./output/DFS/" + file_path + "_DFS.txt", "w")
        start=f_start(maze)
        goal=f_goal(maze)
        if visited == None:
            f.write("NO")
        else:
            cost = 0
            current = goal
            while current != start:
                current = visited[current]
                cost += 1
            f.write(str(cost))
            f.close()
            # save screen to output file
            pygame.image.save(screen, "./output/DFS/" + file_path + "_DFS.jpg")

def input1():
    maze,bonus=read_maze("./INPUT/input1.txt")
    setup_maze(maze)                       # call setup maze function
    visited,flag=search(maze)                # call search function
    draw_path(maze,visited,flag)           # call draw path function
    write_output(maze,visited,"output1",flag) # call write output function
    pygame.time.wait(1000)
    

def input2():
    screen.fill(black)
    maze,bonus=read_maze("./INPUT/input2.txt")
    setup_maze(maze)                       # call setup maze function
    visited,flag=search(maze)                # call search function
    draw_path(maze,visited,flag)           # call draw path function
    write_output(maze,visited,"output2",flag) # call write output function
    pygame.time.wait(1000)
    

def input3():
    screen.fill(black)
    maze,bonus=read_maze("./INPUT/input3.txt")
    setup_maze(maze)                       # call setup maze function
    visited,flag=search(maze)                # call search function
    draw_path(maze,visited,flag)           # call draw path function
    write_output(maze,visited,"output3",flag) # call write output function
    pygame.time.wait(1000)
    

def input5():
    screen.fill(black)
    maze,bonus=read_maze("./INPUT/input5.txt")
    setup_maze(maze)                       # call setup maze function
    visited,flag=search(maze)                # call search function
    draw_path(maze,visited,flag)           # call draw path function
    write_output(maze,visited,"output5",flag) # call write output function
    pygame.time.wait(1000)
    

def input4():
    screen.fill(black)
    maze,bonus=read_maze("./INPUT/input4.txt")
    setup_maze(maze)                       # call setup maze function
    visited,flag=search(maze)                # call search function
    draw_path(maze,visited,flag)           # call draw path function
    write_output(maze,visited,"output4",flag) # call write output function
    pygame.time.wait(1000)
    
def main():
    input1()
    input2()
    input3()
    input4()
    input5()
    pygame.quit()
    sys.exit()

main()
    