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
        #put all of the variables in a data object


class Grid(object):
    def __init__(self, number_of_nodes):
        self.current_node = 1
        self.is_searching = False
        self.current_side = 's'
        self.number_of_nodes = number_of_nodes
        self.grid = []
        for i in range(number_of_nodes):
            self.grid.append(ObstacleNode(i + 1))

    def __getitem__(self,index):
        return self.grid.node_number[index]

    def __setitem__(self,index,value):
        self.grid.node_number[index] = value

    def __delitem__(self,index):{}

    def get_value(self,which_node):
        return self.grid[which_node].node_number, self.grid[which_node].which_side

    def search_perimeter(self):
        # search the perimeter for as long as we haven't returned to the first corner
        # if we are back at the first corner, exit loop
        self.is_searching = 1
        while self.is_searching == 1:
            # Is there a die cache on this node?
            # If yes, check die cache and update LED
            # get and save information and update node data
            #self.updateNode()
            # go to next node
            self.next_node()

    def update_node(self):{}
       #figure out later

    def next_node(self):
        # turn left if Berto is at a corner
        if self.current_node == 7:
            self.current_side = 'e'
            self.current_node = (self.current_node + 1)
        elif self.current_node == 49:
            self.current_side = 'n'
        elif self.current_node == 43:
            self.current_side = 'w'
        elif self.current_node == 8:
            self.current_side = 'd'
            self.is_searching = 0

        if self.current_side == 's':
            self.current_node = (self.current_node + 1)
        elif self.current_side == 'e':
            self.current_node = (self.current_node + 7)
        elif self.current_side == 'n':
            self.current_node = (self.current_node - 1)
        elif self.current_side == 'w' or self.current_side == 'd':
            self.current_node = (self.current_node - 7)


def main():
    number_of_nodes = 49
    course_nodes = Grid(number_of_nodes)
    course_nodes.search_perimeter()

    for i in range(number_of_nodes):
        print (course_nodes[i].node_number)

if __name__ == "__main__":
    main()