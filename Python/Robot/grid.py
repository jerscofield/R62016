#!/usr/bin/env python


class ObstacleNode:
    def __init__(self, node_number):
        self.die_value = 0
        self.is_perimeter = 0
        self.has_been_here = 0
        self.which_side = '*'
        self.is_searching = 0
        #self.which_quadrant
        self.node_number = node_number
        self.is_tunnel = 0
        self.row_number = 0
        self.col_number = 0
        self.cache_present = 0
        #put all of the variables in a data object


class Grid(object):
    def __init__(self, number_of_nodes):
        self.current_node = 1
        self.is_searching = False
        self.is_grid_search = False
        self.current_side = 's'
        self.number_of_nodes = number_of_nodes
        self.is_corner = 0
        self.orientation = 'e'
        self.grid = []
        for i in range(number_of_nodes):
            self.grid.append(ObstacleNode(i + 1))
            #Determine what direction we are facing
            #if e  +1,  if n +7,  if s -7, if w -1.

    def __getitem__(self,index):
        return self.grid[index]

    def __setitem__(self,index,value):
        self.grid[index] = value

    def get_value(self,which_node):
        return self.grid[which_node].node_number, self.grid[which_node].which_side

    def update_node(self, is_tunnel):
        course_nodes[current_node].is_tunnel = is_tunnel
       #figure out later

    def next_node(self):
        self.is_corner = 1  # will this set corner every time?

        # turn left if Berto is at a corner
        if self.current_node == 7:
            self.current_side = 'e'
            self.current_node = (self.current_node + 1)
        elif self.current_node == 49:
            self.current_side = 'n'
        elif self.current_node == 43:
            self.current_side = 'w'
            self.is_corner = 1
        elif self.current_node == 8:
            self.current_side = 'd'
            self.is_searching = 0
            self.is_corner = 3
        elif self.current_node == 6:    #robot is right before corner
            self.is_corner = 2
        elif self.current_node == 42:
            self.is_corner = 2
        elif self.current_node == 44:
            self.is_corner = 2
        else:
            self.is_corner = 0

        if self.current_side == 's':
            self.current_node = (self.current_node + 1)
        elif self.current_side == 'e':
            self.current_node = (self.current_node + 7)
        elif self.current_side == 'n':
            self.current_node = (self.current_node - 1)
        elif self.current_side == 'w':
            self.current_node = (self.current_node - 7)

        ###notes:  Jeremy
        ##if self.current_node <= 7:       # south edge
        ##    self.is_perimiter = 1
        ##elif self.current_node % 7 == 0  # east edge    
        ##    self.is_perimiter = 1
        ##elif self.current_node >= 43:    # south edge
        ##    self.is_perimiter = 1
        ##elif self.current_node % 7 == 1  # west edge    
        ##    self.is_perimiter = 1
        
        #if robot is at a corner, logs 1. Otherwise, logs 0
        #if self.current_node % == (1|7|43|49): self.is_perimeter=1
        #corner node numbers  1, 7, 43, 49

        return self.is_corner
        # if self.current.node%7== (0 | 1)  #  modulus equals 1 or 0.

    #turn types:
    #0: go straight
    #1: turn left, go straight
    #2: turn left, go straight, turn left
    #3: turn right, go straight, turn right
    #4: stop
    def next_node_grid(self):
                #if we are on the westmost edge of the inner grid
        if self.current_node == 41:
            self.is_searching = 0
            turnType = 4
        elif self.current_node == 8:
            self.current_node = self.current_node + 1
            self.orientation = 'e'
            turnType = 1
        elif self.current_node == 9:
            self.current_node = self.current_node + 1
            turnType = 0
        #if we are on the westmost side of the inner grid
        elif self.current_node % 7 == 1 and self.orientation != 'e':
            self.current_node = self.current_node + 7
            self.orientation = 'e'
            self.in_turn = 0
            turnType = 3
        #if we are on the eastmost side of the inner grid
        elif self.current_node % 7 == 6 and self.orientation !=  'w':
            self.current_node = self.current_node + 7
            self.orientation = 'w'
            self.in_turn = 0
            turnType = 2  
        elif self.orientation == 'e':        
            self.current_node = self.current_node + 1
            self.in_turn = 1
            turnType = 0   
        elif self.orientation == 'w':
            turnType = 0             #go straight
            self.current_node = self.current_node - 1
            self.in_turn = 1
        elif self.current_node == 41:
            self.is_searching = 0
            turnType = 4
            
        return turnType

    #def return_to_start(self):
