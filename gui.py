import tkinter as tk
import world as wd

class WorldView(tk.Canvas):
	'''WorldView class

         An object of this class is a display canvas for the simulation.

         It does not include the buttons and widgets and the function attached to it (those are declared in the main section of gui.py).

        Attributes:

        - width (int): width of the canvas in pixel

        - height (int): height of the canvas in pixel

        - window (tk.frame): frame in which the canvas is created

        - color (str): color of the background (black by default)

        - list_ovals (tk.oval[]): list of all the ovals representing the agents

        - pause (bool): boolean stating if the simulation is running or not

        - spaceline (int): space beetween the lines of the grid in pixel


        Lists of method:

        - __init__

        - draw_grid

        - draw_ovals

        - update_ovals

        - switch


        '''
	def __init__(self, window, w=400, h=400, color="black"):
		'''Creation of the canvas

			Parameters:

			- w (int) : width of

			- h (int) : height of

			- bg (str) : colour of the background (black by default)

			- window (tk.frame) : frame in which the canvas is created

			Returns:

			An canvas with the appropriate size and background is created in the "window" frame.

			The "list_ovals" attribute is left empty and can be initialise with the "draw_ovals" function.

            The "spacelines" attribute is initialised at an arbitrary value, as it will be initialised in the "draw_grid" function anyway.

            The "pause" attribute is initialised at "True" (the simulation is paused during initialisation).



		'''
		tk.Canvas.__init__(self, window, width = w, height = h, bg = color) 
		self.window = window
		self.width = w
		self.height = h
		self.color = color
		self.spacelines = 10
		self.list_ovals =[]
		self.pause = True


		
	def draw_grid(self, nblines, nbcolumns):


		'''Initialisation of the grid

                    Parameters:

                    - nblines (int) : number of line to draw

                    - nbcolumns (int) : number of column to draw

                    Returns:

                    Draw the lines and the columns equally spaced on the canvas to represent the grid


        '''


		self.spacelines = self.width/nbcolumns
		for line in range(nblines):
			self.create_line(0,self.spacelines*line,self.width, self.spacelines*line,fill = "grey")
		for column in range(nbcolumns):
			self.create_line(self.spacelines*column,0,self.spacelines*column,self.height,fill = "grey")
		

	def draw_ovals(self, agents):


		'''Initialisation of the ovals

                Parameters:

                - agents (agent[]) : list of agents in the simulation

                Returns:

                Create the ovals representing the agent in the corresponding position and add the to the "list_ovals" attributes.

                The colour of the oval will indicate the state of the agent:

                green for susceptible, blue for recovered, red for infectious.

		'''
		for ag in agents:
			if ag.state == "SUSCEPTIBLE":
				oval = self.create_oval(ag.x*self.spacelines+1,ag.y*self.spacelines+1, (ag.x+1)*self.spacelines -1, (ag.y+1)*self.spacelines-1, fill = "green")
				self.list_ovals.append(oval)

				
			elif ag.state == "INFECTIOUS":
				oval = self.create_oval(ag.x*self.spacelines+1,ag.y*self.spacelines+1, (ag.x+1)*self.spacelines-1, (ag.y+1)*self.spacelines-1, fill = "red")
				self.list_ovals.append(oval)


			elif ag.state == "RECOVERED":
				oval = self.create_oval(ag.x*self.spacelines+1,ag.y*self.spacelines+1, (ag.x+1)*self.spacelines-1, (ag.y+1)*self.spacelines-1, fill = "blue")
				self.list_ovals.append(oval)


			else:
				oval = self.create_oval(ag.x*self.spacelines+1,ag.y*self.spacelines+1, (ag.x+1)*self.spacelines-1, (ag.y+1)*self.spacelines-1, fill = "grey")
				self.list_ovals.append(oval)


	def update_ovals(self,agents):


		'''Updates the ovals

                    Parameters:

                    - agents (agent[]) : new list of agent

                    Returns:

                    Updates the ovals in the "list_ovals" attributes with their new coordinates and colours.

                    The colour of the oval will indicate the state of the agent:

                    green for susceptible, blue for recovered, red for infectious, grey for dead.


        '''

		for ag in range(len(agents)):
			self.coords(self.list_ovals[ag],(agents[ag].x)*self.spacelines+1, (agents[ag].y)*self.spacelines+1,(agents[ag].x+1)*self.spacelines-1, (agents[ag].y+1)*self.spacelines-1)
			if agents[ag].state == "SUSCEPTIBLE":
				self.itemconfig(self.list_ovals[ag],fill = "green")

			elif agents[ag].state == "INFECTIOUS":
				self.itemconfig(self.list_ovals[ag],fill = "red")
	
			elif agents[ag].state == "RECOVERED":
				self.itemconfig(self.list_ovals[ag],fill = "blue")

			else:
				self.itemconfig(self.list_ovals[ag],fill = "grey")



	def switch(self):
		'''this function is used to switch the state of the "pause" attribute'''
		if self.pause ==False:
			self.pause = True
		else:
			self.pause = False
		


#####CODE#####
if __name__ == "__main__":
	

	
	def run_my_world():
		'''make the simulation go forward one time step, by using the "run" function of the world and the "update_ovals" function of the WorldView object'''

		myworld.run()
		mysquare.update_ovals(myworld.pop)

	def update_counters(mystats):
		'''Actualise l'affichage des stats'''
		global nbsusceptible
		nbsusceptible.configure(text=str(mystats[0])+" susceptible agents", fg = "green")
		global nbinfectious
		nbinfectious.configure(text=str(mystats[1])+" infectious agents", fg = "red")
		global nbrecovered
		nbrecovered.configure(text=str(mystats[2])+" recovered agents", fg = "blue")
		global nbdead
		nbdead.configure(text=str(mystats[3])+" dead agents", fg = "grey")
		

	def run_or_pause():
		'''This is the main looped function, it does nothing if the simulation is paused, and makes the simulation go forward one time step if it isn't'''
		global myworld
		global sc_speed
		global mysquare
		if mysquare.pause ==False:
			myworld.run()
			mysquare.update_ovals(myworld.pop)
			newstats = myworld.stats()
			update_counters(newstats)
			global t
			t+=1
			global time
			time.configure(text = 't = ' + str(t))
			space = (1/sc_speed.get())*1000
			mafenetre.after(int(space),run_or_pause)
			
	def switch_play():
		'''Function bound to the "Play/Pause" button, switch the state of the "pause" attribute of the "WorldView" object and call the "run_or_pause" function if needed'''
		mysquare.switch()
		if mysquare.pause ==False:
			run_or_pause()


	def dr_grid ():
		'''Draws the line contained in the "grid" attribute of the "WorldView" object'''
		global sc_size
		mysquare.draw_grid(sc_size.get(), sc_size.get() )

	def dr_agents():
		'''Draws the ovals contained in the "list_ovals" attributes of the "WorldView" object'''
		global sc_size,sc_agents,sc_frac_inf,sc_pisc_pr,sc_pd,myworld, mysquare
		myworld = wd.World(sc_size.get(),sc_size.get())
		myworld.create_agents(nb = sc_agents.get(), prop_infectious = sc_frac_inf.get(), p_i = sc_pi.get(), p_r = sc_pr.get(), p_d = sc_pd.get())
		mysquare.draw_ovals(myworld.pop)
		newstats = myworld.stats()
		update_counters(newstats)

	def reset():
		'''Reset the simulation by deleting all element of the canvas, deleting all agents in the "world" object and setting time back to 0'''
		global myworld, mysquare
		mysquare.delete("all")
		myworld.pop = []
		newstats = myworld.stats()
		update_counters(newstats)
		global time
		global t
		t = 0
		time.configure(text = 't = ' + str(t))
		mysquare.pause = True
		
		

	mafenetre = tk.Tk()

	#Creation frames
	frame1 = tk.Frame(mafenetre)
	frame1.pack(side = 'top')
	frame2 = tk.Frame(mafenetre)
	frame2.pack(side = 'top')
	frame3 = tk.Frame(mafenetre)
	frame3.pack(side = 'top')
	frame4 = tk.Frame(mafenetre)
	frame4.pack(side = 'top')
	frame41 = tk.Frame(frame4)
	frame41.pack(side = "left")
	frame42 = tk.Frame(frame4)
	frame42.pack(side = "right")
	frame421 = tk.Frame(frame42)
	frame421.pack(side = "left")
	frame5 = tk.Frame(mafenetre)
	frame5.pack(side = 'top')
	frame51 = tk.Frame(frame5)
	frame51.pack(side = "left")
	frame52 = tk.Frame(frame5)
	frame52.pack(side = "bottom")
	frame53 = tk.Frame(frame5)
	frame53.pack(side = "bottom")
	frame54 = tk.Frame(frame5)
	frame54.pack(side = "bottom")
	
	mysquare = WorldView(frame51, 400,400)
	mysquare.pack(side = "left")
	
	

	#Création widgets Labels (compteurs)
	#Initialise counters

	nbsusceptible = tk.Label(frame54, text = '')
	nbsusceptible.pack(side = "top")

	nbinfectious = tk.Label(frame54, text = '')
	nbinfectious.pack(side = "top")

	nbrecovered = tk.Label(frame54, text = '')
	nbrecovered.pack(side = "top")

	nbdead = tk.Label(frame54, text = '')
	nbdead.pack(side = "top")





	time = tk.Label(frame54, text = 't = 0')
	time.pack(side = "top")
	t = 0


	#Création widgets boutons

	boutonpause = tk.Button(frame52,text = "Play/Pause", command = switch_play)
	boutonpause.pack(side = "left")

	bt_grid = tk.Button(frame41,text = "Create grid", command = dr_grid)
	bt_grid.pack(side = "left")

	bt_agents = tk.Button(frame421,text = "Create agents", command = dr_agents)
	bt_agents.pack(side = "left")

	bt_obstacles = tk.Button(frame41,text = "Set Obstacles")
	bt_obstacles.pack(side = "right")

	bt_file = tk.Button(frame421,text = "Select Output file")
	bt_file.pack(side = "right")

	bt_reset = tk.Button(frame42,text = "Reset", command = reset)
	bt_reset.pack(side = "right")

	#Création widgets scale

	sc_size = tk.Scale(frame1, orient = "horizontal", from_=1, to=100, label = "Grid size")
	sc_size.pack(side = "left")

	sc_agents = tk.Scale(frame1, orient = "horizontal", from_=1, to=1000, label = "Number of agents")
	sc_agents.pack(side = "right")

	sc_pr = tk.Scale(frame2, orient = "horizontal", from_=0, to=1, label = "Probability of recovery per unit of time", resolution = 0.001)
	sc_pr.pack(side = "right")

	sc_pi = tk.Scale(frame2, orient = "horizontal", from_=0, to=1, label = "Probability of infection uppon contact", resolution = 0.001)
	sc_pi.pack(side = "left")

	sc_pd = tk.Scale(frame3, orient = "horizontal", from_=0, to=1, label = "Probability of death per unit of time", resolution = 0.001)
	sc_pd.pack(side = "left")

	sc_frac_inf = tk.Scale(frame3, orient = "horizontal", from_=0, to=1, label = "Initial fraction of Infected agents", resolution = 0.001)
	sc_frac_inf.pack(side = "right")

	sc_speed = tk.Scale(frame53, orient = "horizontal", from_=1, to = 1000, label = "Speed")
	sc_speed.pack(side = "left")

	

	#Pack de tous les widgets
		
	
	"""
	sc_size.pack(side = 'top')
	sc_agents.pack(side = 'top')
	sc_frac_inf.pack(side = 'top')
	sc_pi.pack(side = 'top')
	sc_pr.pack(side = 'top')
	sc_pd.pack(side = 'top')
	sc_speed.pack(side = 'top')
	
	bt_grid.pack(side = 'top')
	bt_agents.pack(side = 'top')
	mysquare.pack(side = 'right')
	
	nbsusceptible.pack()
	nbinfectious.pack()
	nbrecovered.pack()
	nbdead.pack()
	time.pack()
	boutonpause.pack()
	"""


	#Affichage
	mafenetre.mainloop()

	
