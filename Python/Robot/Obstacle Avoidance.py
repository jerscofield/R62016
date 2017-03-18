	def obstacleAvoidance(self, rowType, startRow):

		if rowType == 'e':
			# if there is no obstacle to the right
		#	if not rightObstacle:
				direction = 'r'
				self.change_orientation('r')
				#go straight
				#change current node (increment_node)
		#	elif not middleObstacle:
				direction = 's'
				#go straight
				#change current node
		#	elif not leftObstacle:
				direction = 'l'
				self.change_orientation('l')
				#go straight
				#change current node
		elif rowType == 'o':
		#	if not leftObstacle:
				direction = 'l'
				self.change_orientation('l')
				#go straight
				#change current node
		#	elif not middleObstacle:
				direction = 's'
				#go straight
				#change current node
		#	elif not rightObstacle:
				direction = 'r'
				self.change_orientation('r')
				#go straight
				#change current node

		if self[self.current_node].row_number == startRow and (self[self.current_node].tr6aversed == False):
				self.avoidingObstacle = False

		return direction






		# 0 go straight
		# 1 turn left, go straight
		# 2 turn left, go straight, turn left
		# 3 turn right, go straight, turn right
		# 4 stop
		# 5 straight, right
		# 6 straight, left
		# 7 right
		# 8 left


	def obstacleAvoidance(course_nodes, motor):
		startRow = course_nodes[course_nodes.current_node].row_number
		startOrientation = course_nodes.orientation
		course_nodes.avoidingObstacle = True

		if course_nodes[course_nodes.current_node].row_number % 2 == 0:
			motor.move_bot('a')  # turn left
			course_nodes.change_orientation('l')

			while course_nodes.avoidingObstacle == True:
				course_nodes.obstacleAvoidance('e', startRow, evaluateNode())
				turnDirection(direction)
				course_nodes.change_orientation('r')
				motor.move_bot('w')  # go straight
			# change current node


	if course_nodes[course_nodes.current_node].row_number % 2 == 1:
		motor.move_bot('d')  # turn right
		course_nodes.change_orientation('r')

		while course_nodes.avoidingObstacle:
			# will need to put a dictionary or something in here to show what values we get when we use the IR sensors
			course_nodes.obstacleAvoidance('o', startRow, evaluateNode())
			turnDirection(direction)
			course_nodes.change_orientation('l')
			motor.move_bot('w')
			change
			current
			node

			# should maybe create a separate function for this inside the grid class.
			# reorient()