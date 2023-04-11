from operator import truediv
import pygame
import math
from queue import PriorityQueue

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):

		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, path):
	while current in came_from:
		path.append(current)
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, journey, path):

    journey_len= len(journey)-2

    for i in range(journey_len):
        print(i)
        count = 0
        came_from = {}
        open_set = PriorityQueue()
        open_set.put((0,count,journey[i]))
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[journey[i]] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[journey[i]] = h(journey[i].get_pos(), journey[i+1].get_pos())

        open_set_hash = {journey[i]}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == journey[i+1]:
                reconstruct_path(came_from, journey[i+1], draw, path)
                journey[i].make_start()
                journey[i+1].make_end()
                return True
                
                

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), journey[i+1].get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        if neighbor not in path and neighbor not in journey:
                            neighbor.make_open() 
            
            draw()

            if current not in journey  and  current not in path :
                current.make_closed()
        
        return False
    
    


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = [None]
	journey = [None]
	end = []
	i = 1
	toggle = True
	path = []

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
            
			# mouse left click
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]

				# make starting point 
				if not journey[0] and spot not in journey:
					journey[0] = spot
					journey[0].make_start()
                
				# make destionations 
				elif spot != journey[0]:
					journey.append(spot)
					journey[i].make_end()
					i = i+1
            
			# mouse right click
			if  pygame.mouse.get_pressed()[2]: 
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
                
				#eraser function for the mouse right click
				if toggle == True:
					spot.reset()

					if spot == journey[0]:
						journey[0] = None				
				    
					elif spot in journey:
						journey.remove(spot)
						i= i-1

                # make_barrier function for the mouse right click
				elif spot not in journey : 
					spot.make_barrier()
            
			 
			if event.type == pygame.KEYDOWN:
				
				# press SPACE to initiate the pathfinding algorithm
				if event.key == pygame.K_SPACE and journey[0] and journey[1]:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
                    
					algorithm(lambda: draw(win, grid, ROWS, width), grid, journey, path)
                
				# press c to clear the python console
				if event.key == pygame.K_c:
					journey = [None]
					i = 1
					grid = make_grid(ROWS, width)

                # press t to toggle between the make_barrier and eraser function for
				# the mouse right click
				if event.key == pygame.K_t:
					if toggle == True:
						toggle = False

					else:
						toggle = True 

	pygame.quit()

main(WIN, WIDTH)