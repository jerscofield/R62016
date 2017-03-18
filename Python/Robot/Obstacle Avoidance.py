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