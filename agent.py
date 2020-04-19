'''

SIRGame

Copyright © 2020 Nathan GAUTHIER

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''






import random

class Agent(object):
	'''Agent class

	 An object of this class is an individual of the simulation.

	Attributes:

	- x(int) and y(int) its coordinates in the grid.

	- state(string) an attribute that equals "SUSCEPTIBLE" if he didn't contract the virus yet, "INFECTIOUS" if he is infected, "RECOVERED" if it recovered from it, and "DEAD" if it died.

	- id(int) its unique ID, starting from 0 and incrementing each time an agent is created

	- p_infection(float) its probability of infecting another susceptible agent when entering in contact with it

	- p_recovery(float) its probability of recovering if it is infected at each time step

	- p_death(float) its probability of dying if it is infected at each time step

	Lists of method:

	- __init__

	- __str__

	- move

	- recover_or_die

	Note : in the main section of the agent.py file is commented an example of agents creation and export in a .txt file.

	This was used as test during the coding phase and was left as tool if the project was to be continued.
	'''


	# Class attributes
	rng = random.Random()
	next_id = 0

	def __init__(self, x = 0, y = 0, state = "SUSCEPTIBLE", p_infection = 1.0, p_recovery = 0.01, p_death = 0.001):
		'''Creation of an agent

			Parameters:

			-x(int) and y(int) its coordinates in the grid.

			-state(string) an attribute that equals "SUSCEPTIBLE" if he didn't contract the virus yet, "INFECTIOUS" if he is infected,
			"RECOVERED" if it recovered from it, and "DEAD" if it died.

			-p_infection(float) its probability of infecting another susceptible agent when entering in contact with it

			-p_recovery(float) its probability of recovering if it is infected at each time step

			-p_death(float) its probability of dying if it is infected at each time step

			Returns:

			An agent with the appropriate parameters is created, its ID is the ID of the last created agent (0 if none) +1

		'''
		self.x = x
		self.y = y
		self.state = state
		self.p_infection = p_infection
		self.p_recovery = p_recovery
		self.p_death = p_death
		self.id = Agent.next_id
		Agent.next_id += 1



	def move(self, theworld):
		'''This function is used at each time step to make the agent move.

			Parameters:

		    theworld (class "world.py") world in which the agent evolve

		    Returns:

		    If the agent is not dead, changes its coordinates to make it move 1 position in a randomly chosen cardinal direction.

		    If this position is occupied by an obstacle the agent doesn't move.

		'''
		w = theworld.w
		h = theworld.h
		#print("Agent", self.id, "moving, state=", self.state)
		if (self.state != "DEAD"):
			alea = Agent.rng.randrange(0,4)
			if alea == 0:
				# move south
				newx = self.x
				newy = self.y + 1
				if (newy >= h):
					newy -= h
			elif alea == 1:
				# move east
				newx = self.x + 1
				newy = self.y
				if (newx >= w):
					newx -= w 
			elif alea == 2:
				# move north
				newx = self.x
				newy = self.y - 1
				if newy < 0:
					newy += h
			else: # (alea == 3)
				# move west
				newx = self.x - 1
				newy = self.y
				if newx < 0:
					newx += w

			if (newx, newy) not in theworld.obstacles:
				self.x = newx
				self.y = newy

			


	def recover_or_die(self):
		'''Check if the agent recovers, then if that's not the case if it dies'''
		if self.state == "INFECTIOUS":
			if (Agent.rng.random() < self.p_recovery):
				self.state = "RECOVERED" 
			else:
				if (Agent.rng.random() < self.p_death):
					self.state = "DEAD"

	def __str__(self):
		'''returns a string containing the ID, the state and the coordinates of the agent'''
		return "Agent #{0:>3} at x={1:>3} and y={2:>3}, state={3}".format(self.id, self.x, self.y, self.state)



if __name__ == "__main__":
	'''
	alex = Agent(50, 25, "INFECTIOUS")
	with open("test.txt", "w") as output_file:
		for i in range(2000):
			# alex.move(100, 50)
			alex.resist_or_die()
			output_file.write("{0} {1} {2} {3}\n".format(i, alex.x, alex.y, alex.state))
	'''



			

