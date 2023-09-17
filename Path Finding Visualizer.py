import pygame
from tkinter import messagebox ,Tk											# to create message boxes
import sys

window_width = 600
window_height = 600

window = pygame.display.set_mode((window_width, window_height))				# to create the window

rows = 30
columns = 30

box_width = window_width // columns
box_height = window_height // rows

grid = []																	# empty lists to store each node
queue = []
path = []

class Box:
	def __init__(self, i, j):
		self.x = i   														# x and y coordinates
		self.y = j

		self.start = False													# flags
		self.block = False
		self.target = False

		self.queued = False													# algorithm control flags
		self.visited = False	
		self.neighbour = []													# empty list to store neighbour nodes	

		self.prior = None  													# prior node					

	def draw(self, window, color):											# to draw the boxes
		pygame.draw.rect(window, color, (self.x * box_width, self.y * box_height, box_width - 1, box_height - 1))

	def neighbour_nodes(self):												# appending neighbouring nodes to list 

		# virtical nodes
		if self.x > 0:
			self.neighbour.append(grid[self.x - 1][self.y])

		if self.x < rows - 1:
			self.neighbour.append(grid[self.x + 1][self.y])

		# horizontal nodes
		if self.y > 0:
			self.neighbour.append(grid[self.x][self.y - 1])

		if self.y < columns - 1:
			self.neighbour.append(grid[self.x][self.y + 1])


for i in range(rows):														# to create the grid
	temp = []
	for j in range(columns):
		temp.append(Box(i, j))
	grid.append(temp)

for i in range(rows):														# setting neighbour list
	for j in range(columns):
		grid[i][j].neighbour_nodes()


def main():	
	start_search = False													# main loop flags														
	set_target_node = False
	set_start_node = False														

	searching = True														# algoritm flags
	target_box = None

	pygame.display.set_caption("Dijkstra Path Finding Visualizer")

	Tk().wm_withdraw()
	messagebox.showinfo("Path Finding Visualizer", "\t\tInstructions:\n\n1.Click LEFT mouse button to set the START node.\n\n2.Click and drag mouse SCROLL button to create BLOCKING nodes.\n\n3.Click RIGHT mouse button to set the TARGET node.\n\n4.Press ENTER button to visualize the shortest path between the two nodes.")

	while True:																# main loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:									# to exit the window
				pygame.quit()
				sys.exit()

			elif event.type == pygame.MOUSEMOTION:							# mouse events
				x = pygame.mouse.get_pos()[0]
				y = pygame.mouse.get_pos()[1]

				if event.buttons[0]:										# mouse LEFT click (start)
					if not set_start_node:
						i = x // box_width
						j = y // box_height
						start_box = grid[i][j]
						start_box.start = True
						set_start_node = True

						queue.append(start_box)								# appending the start node into the queue
						start_box.visited = True

				if event.buttons[1]:										# mouse CENTER click (block)
					if set_start_node or set_target_node:
						try:
							i = x // box_width
							j = y // box_height
							blocked_box = grid[i][j]
							blocked_box.block = True
						except IndexError as e:
							Tk().wm_withdraw()
							messagebox.showinfo("Path Finding Visualizer", "Please draw within the grid lines")

				if event.buttons[2]:										# mouse RIGHT click (target) and target_set = False
					if not set_target_node:
						i = x // box_width
						j = y // box_height
						target_box = grid[i][j]
						target_box.target = True
						set_target_node = True

			elif event.type == pygame.KEYDOWN and set_target_node:			# press ENTER to start searching path
				if event.key == pygame.K_RETURN:
					start_search = True

		if start_search:													# algorithm logic
			if len(queue) > 0 and searching:						
				current_box = queue.pop(0)
				current_box.visited = True

				if current_box == target_box:
					searching = False
					while current_box.prior != start_box:					# path logic
						path.append(current_box.prior)
						current_box = current_box.prior

				else:
					for neighbour in current_box.neighbour:
						if not neighbour.queued and not neighbour.block:
							neighbour.queued = True
							neighbour.prior = current_box
							queue.append(neighbour)

			else:															# if there is no solution
				if searching:
					Tk().wm_withdraw()
					messagebox.showinfo("Path Finding Visualizer", "Sorry, there is no solution")
					searching = False
					break


		window.fill((0, 0, 0))												# to fill the window with a color

		for i in range(rows):												# calling draw function on each box in grid
			for j in range(columns):
				Box = grid[i][j]
				Box.draw(window, (128, 128, 128))

				if Box.queued:												# queued nodes
					Box.draw(window, (0, 255, 0))

				if Box.visited:												# visited nodes
					Box.draw(window, (255, 255, 255))

				if Box in path:												# path nodes
					Box.draw(window, (255, 255, 0))

				if Box.start:												# draw START node
					Box.draw(window, (0, 255, 0))

				if Box.block:												# draw BLOCK node
					Box.draw(window, (0, 0, 0))

				if Box.target:												# draw TARGET node
					Box.draw(window, (255, 0, 0))


		pygame.display.update()												# to update the window


main()