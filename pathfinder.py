# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 21:51:20 2021

@author: eminm
"""

import tkinter as tk
import numpy as np

'''
left click once: start node
left click twice: end node
right click once: create barrier
right click twice: start search
'''

# Node class for astar algorithm
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# class for the blocks in the grid
class Spot(Node):
    def __init__(self, row, col, width, total_rows):
        super().__init__(parent=None, position=None)   #inherit parent class' methods/attributes
        self.row = row
        self.col = col
        self.x = col*width
        self.y = row*width
        self.color = "white"
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows


    def get_pos(self):
        return self.row, self.col

    #check blocks
    def is_closed(self):
        return self.color == "red"

    def is_open(self):
        return self.color == "green"

    def is_barrier(self):
        return self.color == "black"

    def is_start(self):
        return self.color == "orange"

    def is_end(self):
        return self.color == "blue"

    def is_walkable(self):
        self.color == "white"

    #change blocks
    def make_closed(self):
        self.color = "red"

    def make_open(self):
        self.color = "green"

    def make_barrier(self):
        self.color = "black"

    def make_start(self):
        self.color = "orange"

    def make_end(self):
        self.color = "blue"

    def make_path(self):
        self.color = "magenta"

    #draw blocks
    def draw(self,win):
        win.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.width, fill=self.color)



# astar algorithm
def astar_algorithm(maze, win, width, total_rows):

    #find start and end
    for i in range(len(maze)-1):
        for j in range(len(maze)-1):
            if maze[i][j].is_start():
                start_node = maze[i][j]
                start_node.position = (i,j)
            elif maze[i][j].is_end():
                end_node = maze[i][j]
                end_node.position = (i,j)


    #open and closed list
    open_list = []
    closed_list = []

    #add starting node to open list
    open_list.append(start_node)

    #loop until end is found
    while len(open_list) > 0:

        #get current node
        current_node = open_list[0]
        current_index = 0
        for index,node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index


        #remove current node from open and add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        #draw current node red
        current_node.make_closed()
        current_node.draw(win)
        win.update()

        #check if end was found
        if current_node == end_node:
            current = current_node
            while current is not None:
                current.make_path()
                current.draw(win)
                win.update()
                current = current.parent
                if current is None:
                    return

        #create children nodes
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), \
                             (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            #get node_position
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            #check if inside grid
            if node_position[0] > (len(maze)-1) or node_position[0] < 0 or \
                node_position[1] > (len(maze)-1) or node_position[1] < 0:
                    continue

            #check if walkable terrain
            if maze[node_position[0]][node_position[1]].is_barrier():
                continue

            #check if neighbour already in closed list
            if Node(current_node,node_position) in closed_list:
                continue

            #create new node
            new_node = Spot(node_position[0], node_position[1], width, total_rows)
            new_node.parent = current_node
            new_node.position = node_position
            children.append(new_node)

        #loop through children nodes
        for child in children:

            #check if child is in closed list
            if child in closed_list:
                continue

            #create f,g,h values
            child.g = current_node.g + 1
            child.h = np.abs(child.position[0]-end_node.position[0]) + np.abs(child.position[1]-end_node.position[1])
            child.f = child.g + child.h

            #check if child already in open list
            for node in open_list:
                if child == node and child.g > node.g:
                    break

            #addchild to open list
            open_list.append(child)

            #draw children green
            child.make_open()
            child.draw(win)
            win.update()


def make_grid(rows,width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)

    return grid

def draw_grid(win,rows,width):
    gap = width//rows
    for i in range(rows):
        win.create_line(0,i*gap,width,i*gap,fill="black")
        for j in range(rows):
            win.create_line(j*gap,0,j*gap,width,fill="black")

def draw(win, grid, rows, width):

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)


def get_clicked_pos(x, y, rows, width):
    gap = width//rows

    col = x//gap
    row = y//gap

    return row,col

def main(win, width):
    rows = 50
    grid = make_grid(rows, width)
    draw(win, grid, rows, width)

    #function for start spot
    def set_start(event):
        #get mouse coordinates
        x, y = event.x, event.y

        #get grid position
        row, col = get_clicked_pos(x, y, rows, width)

        grid[row][col].make_start()
        grid[row][col].draw(win)


    #function for end spot
    def set_end(event):
        #get mouse coordinates
        x, y = event.x, event.y

        #get grid position
        row, col = get_clicked_pos(x, y, rows, width)

        grid[row][col].make_end()
        grid[row][col].draw(win)

    #function for barriers
    def set_barrier(event):
        #get mouse coordinates
        x, y = event.x, event.y

        #get grid position
        row, col = get_clicked_pos(x, y, rows, width)

        grid[row][col].make_barrier()
        grid[row][col].draw(win)

    #astar path solver
    def solve(event):
        astar_algorithm(grid, win, width//rows, rows)

    win.bind("<Button-1>", set_start)
    win.bind("<Double-1>", set_end)
    win.bind("<B3-Motion>", set_barrier)
    win.bind("<Button-3>", set_barrier)
    win.bind("<Double-3>", solve)


    win.pack()
    tk.mainloop()



if __name__ == "__main__":
    #tkinter canvas
    WIDTH = 800
    master = tk.Tk()
    WIN = tk.Canvas(master, width=WIDTH, height=WIDTH)

    main(WIN, WIDTH)
