#!/usr/bin/env python


class ObstacleNode:
    def __init__(self, node_number):
        self.die_value = 0
        self.is_perimeter = False
        self.is_inner_perimeter = False
        self.is_corner = False
        self.is_inner_corner = False
        self.has_been_here = False
        self.which_side = '*'
        # self.which_quadrant
        self.node_number = node_number
        self.is_tunnel = 0
        self.row_number = 0
        self.col_number = 0
        self.cache_present = 0
        # put all of the variables in a data object


class Grid(object):
    def __init__(self, number_of_nodes):
        self.current_node = int(1)
        self.is_searching = False
        self.is_grid_search = False
        self.current_side = 's'
        self.number_of_nodes = number_of_nodes
        self.orientation = 'e'
        self.grid = []
        for j in range(8):
            for i in range(8):
                self.grid.append(ObstacleNode(i))
                # Determine what direction we are facing
                # if e  +1,  if n +7,  if s -7, if w -1.



def __getitem__(self, index):
    return self.grid[index]


def __setitem__(self, index, value):
    self.grid[index] = value


def get_value(self, which_node):
    return self.grid[which_node].node_number, self.grid[which_node].which_side


def initialize(self):
    self.orientation = 'e'
    for i in range(50):
        if i % 7 == 6 or i % 7 == 2:
            self.grid[i].is_inner_perimeter = True
        if i % 7 == 0 or i % 7 == 1 or i > 42 or i < 8:
            self.grid[i].is_perimeter = True
            self.grid[i].cache_present = 1
            self.grid[i].is_inner_perimeter = False
        if i == 1 or i == 7 or i == 43 or i == 49:
            self.grid[i].is_corner = True
            self.grid[i].cache_present = 0
        if i == 9 or i == 13 or i == 41 or i == 37:
            self.grid[i].is_inner_corner = 1
            self.grid[i].is_inner_perimeter = True


def update_node(self, is_tunnel):
    self.course_nodes[self.current_node].is_tunnel = is_tunnel
    # figure out later


# turn types:
# 0: go straight
# 1: go straight, turn left
# 2: go straight, turn left
# 3: stop
# 4: turn 180 degrees
def next_node_perim(self):
    # we are right before the corner
    if self.grid[self.current_node + self.increment_node()].is_corner == True:
        self.current_node = self.current_node + self.increment_node()
        self.orientation = self.change_orientation('l')
        turn_type = 1  # go stright 1, then turn left. Make sure to update orientation
    elif self.current_node == 15:
        turn_type = 1  # go stright 1, then turn left. Make sure to update orientation
        self.is_searching = False
        self.current_node = self.current_node + self.increment_node()
        self.orientation = self.change_orientation('l')
    else:
        turn_type = 0  # go straight 1
        self.current_node = self.current_node + self.increment_node()
    return turn_type


def increment_node(self):
    if self.orientation == 's':
        increment = int(-7)
    elif self.orientation == 'e':
        increment = int(1)
    elif self.orientation == 'n':
        increment = int(7)
    elif self.orientation == 'w':
        increment = int(-1)
    else:
        increment = int(0)
        print ("error here. current orientation is: ", self.orientation)
    return increment


def change_orientation(self, turnDirection):
    if turnDirection == 'r':
        if self.orientation == 'n':
            orientation = 'e'
        if self.orientation == 'e':
            orientation = 's'
        if self.orientation == 's':
            orientation = 'w'
        if self.orientation == 'w':
            orientation = 'n'
    elif turnDirection == 'l':
        if self.orientation == 'n':
            orientation = 'w'
        if self.orientation == 'e':
            orientation = 'n'
        if self.orientation == 's':
            orientation = 'e'
        if self.orientation == 'w':
            orientation = 's'
    # total orientation change
    elif turnDirection == 't':
        if self.orientation == 'n':
            orientation = 's'
        if self.orientation == 'e':
            orientation = 'w'
        if self.orientation == 's':
            orientation = 'n'
        if self.orientation == 'w':
            orientation = 'e'
    return orientation


    ###notes:  Jeremy
    ##if self.current_node <= 7:       # south edge
    ##    self.is_perimiter = 1
    ##elif self.current_node % 7 == 0  # east edge
    ##    self.is_perimiter = 1
    ##elif self.current_node >= 43:    # south edge
    ##    self.is_perimiter = 1
    ##elif self.current_node % 7 == 1  # west edge
    ##    self.is_perimiter = 1

    # if robot is at a corner, logs 1. Otherwise, logs 0
    # if self.current_node % == (1|7|43|49): self.is_perimeter=1
    # corner node numbers  1, 7, 43, 49

    # if self.current.node%7== (0 | 1)  #  modulus equals 1 or 0.


# turn types:
# 0: go straight
# 1: go straight, turn left
# 2: go straight, turn right
# 3: stop
# 4: turn 180 degrees
def next_node_grid(self):
    # if we are at the final node in the search

    if self.current_node == 41:
        self.is_searching = False
        turnType = 3
    # if we are at the first node in the search
    elif self.current_node == 8:
        self.current_node = self.current_node + self.increment_node()
        turnType = 0
    # if we are at or right before the inner perimeter, on east side
    elif (self.grid[self.current_node + 2].is_perimeter == True and self.orientation == 'e') or (
            self.grid[self.current_node + 1].is_perimeter == True and self.orientation == 'n'):
        print ("We got to this point!!!")
        self.current_node = self.current_node + self.increment_node()
        self.orientation = self.change_orientation('l')
        turnType = 1
    # if we are at or right before the inner perimeter, on west side
    elif (self.grid[self.current_node - 2].is_perimeter == True and self.orientation == 'w') or (
            self.grid[self.current_node - 1].is_perimeter == True and self.orientation == 'n'):
        self.current_node = self.current_node + self.increment_node()
        self.orientation = self.change_orientation('r')
        turnType = 2
    # no turns ahead, go straight
    else:
        self.current_node = self.current_node + self.increment_node()
        turnType = 0

    return turnType

    # def return_to_start(self):


while 1:
    course_nodes = Grid(50)
    print (course_nodes[1].die_cache)

