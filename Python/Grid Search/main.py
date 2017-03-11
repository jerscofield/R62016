from __future__ import print_function
from __future__ import division

import grid

##import rotationMotorTest

import time
#from BrickPi import *  # import BrickPi.py file to use BrickPi operations
#from MultiMotorDriving import *  # So can do precision motor rotations


def recursion(*grid):
	
	#look in front
	#if no object is in front
	forward(grid)

	#turn right
	if grid.orientation == 'e'
		grid.orientation = 's'
	if grid.orientation == 'n'
		grid.orientation = 'e'
	if grid.orientation == 'w'
		grid.orientation = 'n'
	if grid.orientation == 's'
		grid.orientation = 'w'
	#look in front
	#if no object is in front
	forward(grid)

	#turn left
	if grid.orientation == 'e'
		grid.orientation = 'n'
	if grid.orientation == 'n'
		grid.orientation = 'w'
	if grid.orientation == 'w'
		grid.orientation = 's'
	if grid.orientation == 's'
		grid.orientation = 'e'
	#look in front
	#if no object is in front
	forward(grid)

def forward(tunnel_state, *grid):
	#motors move forward
	#get orientation

	#increment grid
	if grid.orientation == 'e'
		course_nodes.current_node = course_nodes.current_node + 1
	if grid.orientation == 'n'
		course_nodes.current_node = course_nodes.current_node + 7
	if grid.orientation == 'w'
		course_nodes.current_node = course_nodes.current_node - 1
	if grid.orientation == 's'
		course_nodes.current_node = course_nodes.current_node - 7

	if course_nodes[course_nodes.current_node].is_tunnel == 0:
		return
	if course_nodes[course_nodes.current_node].is_perimeter = 1:
		return
	#go back
	#return 1
	#if course_nodes == perimeter
	#go back 1 node
	#recurse

def set_orientation(*grid):




def main():
    number_of_nodes = 49

    course_nodes = grid.Grid(number_of_nodes)
    course_nodes.is_searching = 1

    course_nodes.current_node = 3
    course_nodes.orientation = 'n'
	
    course_nodes[1].is_tunnel = 0
    course_nodes[2].is_tunnel = 0
    course_nodes[3].is_tunnel = 1
    course_nodes[4].is_tunnel = 0
    course_nodes[5].is_tunnel = 0
    course_nodes[6].is_tunnel = 0
    course_nodes[7].is_tunnel = 0
    course_nodes[8].is_tunnel = 0
    course_nodes[9].is_tunnel = 0
    course_nodes[10].is_tunnel = 1
    course_nodes[11].is_tunnel = 0
    course_nodes[12].is_tunnel = 0
    course_nodes[13].is_tunnel = 0
    course_nodes[14].is_tunnel = 0
    course_nodes[15].is_tunnel = 0
    course_nodes[16].is_tunnel = 0
    course_nodes[17].is_tunnel = 1
    course_nodes[18].is_tunnel = 0
    course_nodes[19].is_tunnel = 0
    course_nodes[20].is_tunnel = 0
    course_nodes[21].is_tunnel = 0
    course_nodes[22].is_tunnel = 0
    course_nodes[23].is_tunnel = 1
    course_nodes[24].is_tunnel = 1
    course_nodes[25].is_tunnel = 0
    course_nodes[26].is_tunnel = 0
    course_nodes[27].is_tunnel = 0
    course_nodes[28].is_tunnel = 0
    course_nodes[29].is_tunnel = 0
    course_nodes[30].is_tunnel = 0
    course_nodes[31].is_tunnel = 0
    course_nodes[32].is_tunnel = 1
    course_nodes[33].is_tunnel = 1
    course_nodes[34].is_tunnel = 0
    course_nodes[35].is_tunnel = 0
    course_nodes[36].is_tunnel = 0
    course_nodes[37].is_tunnel = 0
    course_nodes[38].is_tunnel = 0
    course_nodes[39].is_tunnel = 0
    course_nodes[40].is_tunnel = 1
    course_nodes[41].is_tunnel = 0
    course_nodes[42].is_tunnel = 0
    course_nodes[43].is_tunnel = 0
    course_nodes[44].is_tunnel = 0
    course_nodes[45].is_tunnel = 0
    course_nodes[46].is_tunnel = 0
    course_nodes[47].is_tunnel = 1
    course_nodes[48].is_tunnel = 0
    course_nodes[49].is_tunnel = 0

    

    time.sleep(10)  # sleep for 10 ms    


    


    while 1:
        time.sleep(.01)


if __name__ == "__main__":
    main()
