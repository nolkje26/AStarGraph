import pygame, math
from MinPriorityQueue import *

WIDTH = 800 
WINDOW = pygame.display.set_mode((WIDTH, WIDTH)) # Sets up display w/ dimensions 800 * 800
pygame.display.set_caption("A* Path Finding Algorithm") # Sets caption for display

# Grid colors
ORANGE_YELLOW_CRAYOLA = (233, 196, 106)
SANDY_BROWN = (244, 162, 97)
WHITE = (255, 255, 255)
PERSIAN_GREEN = (42, 157, 143)
CHARCOAL = (38, 70, 83)
BURNT_SIENNA = (231, 111, 81)
GREY = (128, 128, 128)
CG_BLUE = (0, 129, 167)

class Vertex:
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
    
    def is_visited(self):
        return self.color == ORANGE_YELLOW_CRAYOLA
    
    def is_enqueued(self):
        return self.color == SANDY_BROWN
    
    def is_barrier(self):
        return self.color == CHARCOAL

    def is_start(self):
        return self.color == BURNT_SIENNA

    def is_end(self):
        return self.color == CG_BLUE
    
    def reset(self):
        self.color = WHITE

    def make_visited(self):
        self.color = ORANGE_YELLOW_CRAYOLA
    
    def make_enqueued(self):
        self.color = SANDY_BROWN

    def make_barrier(self):
        self.color = CHARCOAL

    def make_start(self):
        self.color = BURNT_SIENNA

    def make_end(self):
        self.color = CG_BLUE

    def make_path(self):
        self.color = PERSIAN_GREEN

    # Draws actual vertex on screen
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    # Check if you can add neighbor vertices to neighbors list - append to neighbors if vertex is w/in bounds and is not a barrier
    def update_neighbors(self, grid):
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

# Heuristic function - Manhattan (L) distance
def h(v1, v2): # v1 and v2 will be coordinates (x1, y1) and (x2, y2)
    x1, y1 = v1
    x2, y2 = v2
    return abs(x1 - x2) + abs(y1 - y2)

def relax(dist_to, edge_to, fringe, end, curr_vertex, neighbor):
    temp_dist_to_neighbor = dist_to[curr_vertex] + 1
    if temp_dist_to_neighbor < dist_to[neighbor]:
        dist_to[neighbor] = temp_dist_to_neighbor
        if neighbor in fringe.values:
            heuristic[neighbor] = dist_to[neighbor] + h(neighbor.get_pos(), end.get_pos())
        else:
            fringe.enqueue(neighbor, dist_to[neighbor] + h(neighbor.get_pos(), end.get_pos()))
        neighbor.make_enqueued()
        edge_to[neighbor] = curr_vertex

def a_star_algorithm(draw, grid, start, end):
    fringe = MinPriorityQueue()
    dist_to = {vertex: float("inf") for row in grid for vertex in row}
    edge_to = {}
    heuristic = {vertex: float("inf") for row in grid for vertex in row} 

    fringe.enqueue(start, 0) # add source with 0 priority
    dist_to[start] = 0
    edge_to[start] = None
    heuristic[start] = h(start.get_pos(), end.get_pos())

    while not fringe.is_empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if fringe.get_smallest().val == end:
            curr_vertex = fringe.dequeue().val
            while curr_vertex != start:
                curr_vertex.make_path()
                draw()
                curr_vertex = edge_to[curr_vertex]
            end.make_end()
            return True

        curr_vertex = fringe.dequeue().val # gets smallest vertex

        for neighbor in curr_vertex.neighbors:
            if not neighbor.is_visited():
                relax(dist_to, edge_to, fringe, end, curr_vertex, neighbor)

        draw()

        if curr_vertex != start:
            curr_vertex.make_visited()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for row in range(rows):
        grid.append([])
        for col in range(rows):
            vertex = Vertex(row, col, gap, rows)
            grid[row].append(vertex)
    return grid

def draw_grid(window, rows, width):
    gap = width // rows
    for row in range(rows):
        pygame.draw.line(window, GREY, (0, row * gap), (width, row * gap))
        for col in range(rows):
            pygame.draw.line(window, GREY, (col * gap, 0), (col * gap, width))

def draw(window, grid, rows, width):
    window.fill(WHITE) # fills entire screen with one color
    for row in grid:
        for vertex in row:
            vertex.draw(window)
    draw_grid(window, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    
    return row, col

def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None # start position
    end = None # end position

    run = True # Running the main loop

    while run: 
        draw(window, grid, ROWS, width)

        for event in pygame.event.get(): # loop through all the events 
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                vertex = grid[row][col]
                if not start and vertex != end:
                    start = vertex
                    start.make_start()
                elif not end and vertex != start:
                    end = vertex
                    end.make_end()
                elif vertex != start and vertex != end:
                    vertex.make_barrier()
            elif pygame.mouse.get_pressed()[2]: # right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                vertex = grid[row][col]
                vertex.reset()
                if vertex == start:
                    start = None
                elif vertex == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for vertex in row:
                            vertex.update_neighbors(grid)
                
                    a_star_algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
            
    pygame.quit()

main(WINDOW, WIDTH)