'''

SIRGame

Copyright © 2020 Nathan GAUTHIER

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


'''




import random
import agent

class World(object):
	'''World class

		 An object of this class is a world in which the simulation takes place.

		Attributes:

		- w(int) and h(int): the width and height of the world

		- pop(agent[]): the list of agent (class in agent.py) forming the population simulated

		- obstacles((int,int)[]): a list of (x,y) tuple, coordinates occupied by the obstacles

		Lists of method:

		- __init__

		- __str__

		- put_obstacles

		- create_agents

		- nb

		- move

		- infect

		- contact

		- recover_or_die

		- run

		- stats

		- erase

		Note : in the main section of the world.py file is commented an example of worlds creation and export in a .txt file.

		This was used as test during the coding phase and was left as tool if the project was to be continued.
		'''
	def __init__(self, w = 100, h = 100):
		'''Creation of a world

				Parameters:

				-w(int) : width

				-h(int) : height

				Returns:

				An world with the appropriate dimension is created, its "obstacles" and "pop" attributes are left empty and can be initialised with
				the "put_obstacles" and "create_agents" functions.

			'''
		self.w = w
		self.h = h
		self.pop = []
		self.obstacles = []
		self.rng = random.Random()
		


	def put_obstacles(self, config = "WALL_WITH_HOLE"):
		'''This function is used to create the obstacles

			Parameters:

			config(str): configuration of the obstacle (the only one implemented for now is "WALL_WITH_HOLE", a vertical wall with a 1 sized gap
			in the middle, placed in the middle of the horizontal axe).

			Returns:

			Add all position obstructed by the obstacle to the obstacles attribute.


		'''
		self.obstacles = []

		if (config == "WALL_WITH_HOLE"):
			halfwidth = int(round(self.w/2))
			halfheight = int(round(self.h/2))
			for i in range(0, halfheight):
				self.obstacles.append((halfwidth, i))
			for i in range(halfheight + 1, self.h):
				self.obstacles.append((halfwidth, i))
		else:
			print("Warning: Unknown obstacle configuration.")


	def create_agents(self, nb = 1000, prop_infectious = 0.2, p_i = 0, p_r = 0, p_d = 0):
		'''This function is used to create the population of agents.

			    Parameters:

			    -nb(int):number of created agent

			    -prop_infectious(float): proportion of infected agent in the created population

			    -p_i(float): probability of infection of infected agents

			    -p_r(float):probability of recovery of infected agents

			    -p_d(float):probability of death of infected agents


			    Returns:

			    Create the agents using the "__init__" function of the "agent.py" class, and add them to the "pop" attribute of this object.


		'''
		self.pop = []
		nb_infectious = round(prop_infectious*nb)
		for i in range(nb):
			ok = False
			while not ok:
				x = self.rng.randrange(0, self.w)
				y = self.rng.randrange(0, self.h)
				ok = ((x, y) not in self.obstacles)
			if (i < nb_infectious):
				state = "INFECTIOUS"
			else:
				state = "SUSCEPTIBLE"
			newagent = agent.Agent(x, y, state, p_i, p_r, p_d)
			self.pop.append(newagent)


	def nb(self):
		'''returns the number of agent in the population'''
		return len(self.pop)

	def move(self):
		'''applies the function "move()" to all agents in the population (see agent.py documentation)'''
		for ag in self.pop:
			ag.move(self)

	def infect(self, list_of_agents):
		'''This function is used after the agents moved.

		    Parameters:

		    list_of_agents (agent[]): list of agents present in the same position.

		    Returns:

		    If one of the agent is infected, check if the other agents of the list who are susceptible become infected too,
		    and then changes its state to "INFECTIOUS" if it is the case.


		'''
		list_of_initially_infectious = [ag for ag in list_of_agents if ag.state == "INFECTIOUS"]	
		if len(list_of_initially_infectious) >= 1:
			list_of_susceptibles = [ag for ag in list_of_agents if ag.state == "SUSCEPTIBLE"]
			for ag in list_of_susceptibles:
				if (self.rng.random() < ag.p_infection):
					ag.state = "INFECTIOUS"


	def contact(self):
		'''returns a dimension 2 tab of the dimension of the grid, containing a list of agents present for each position.'''
		result = [[[] for j in range(self.w)] for i in range(self.h)]
		for ag in self.pop:
			result[ag.y][ag.x].append(ag)
		return result

	def recover_or_die(self):
		'''applies the function "recover_or_die()" to all agents in the population (see agent.py documentation)'''
		for ag in self.pop:
			ag.recover_or_die()

	def run(self):
		'''Makes the world move one time step forward, by applying successively the functions move(), infect() on the superposing agents, and recover_or_die()'''

		self.move()
		contacts = self.contact()
		for i in range(self.h):
			for j in range(self.w):
				if len(contacts[i][j]) > 2:
					self.infect(contacts[i][j])
		self.recover_or_die()

	def __str__(self):
		'''returns a string containing the "__str__" description of all obstacles and agents in this object'''
		res = "Obstacles:\n"
		for o in self.obstacles:
			res += str(o) + "\n"
		res += ("Agents:\n")
		for ag in self.pop:
			res += str(ag) + "\n"
		return res

	def stats(self):
		'''returns the tuple (number of susceptible agents, infected, recovered, dead) present in the population'''
		nb_susceptibles = 0
		nb_infectious = 0
		nb_recovered = 0
		nb_dead = 0
		for ag in self.pop:
			if ag.state == "SUSCEPTIBLE":
				nb_susceptibles += 1
			elif ag.state == "INFECTIOUS":
				nb_infectious += 1
			elif ag.state == "RECOVERED":
				nb_recovered += 1
			elif ag.state == "DEAD":
				nb_dead +=1
			else:
				print("Warning: Unknown agent state.")
		return (nb_susceptibles, nb_infectious, nb_recovered, nb_dead)

	def erase(self):
		'''Delete all agent and obstacle from memory, pop and obstacles become empty list.'''
		del self.obstacles[:]
		self.obstacles = []
		del self.pop[:]
		self.pop = []


if __name__ == "__main__":



	'''
	p_i = 1.0
	p_r = 0.01
	p_d = 0.001
	init_prop = 0.01
	w = 100
	h = 100
	nb_agents = 1000



	myworld = World(w, h)
	myworld.put_obstacles("WALL_WITH_HOLE")
	myworld.create_agents(nb_agents, init_prop, p_i, p_r, p_d)

	print(myworld)

	filename = "sir_{0}_{1}_{2}_{3}.txt".format(p_i, p_r, p_d, init_prop)
	with open(filename, "w") as output_file:
		t = 0
		mytuple = myworld.stats()
		output_file.write("# time nb_susceptibles nb_infectious nb_recovered nb_dead\n")
		while (t < 10000 and mytuple[1] > 0):
			mytuple = myworld.stats()
			output_file.write("{0} {1} {2} {3} {4}\n".format(t, mytuple[0], mytuple[1], mytuple[2], mytuple[3]))
			myworld.run()
			t += 1

	'''