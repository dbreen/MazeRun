import math
import random


class Maze(object):
    EASY, MEDIUM, HARD = 0, 1, 2
    WIDTHS = {
        EASY: 32, MEDIUM: 24, HARD: 16,
    }
    # Left, Top, Right, Down
    DIRS = ((-1, 0), (0, -1), (1, 0), (0, 1))

    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.wallwidth = self.WIDTHS[difficulty]
        self.gridsize = (int(math.ceil(width / self.wallwidth)),
                         int(math.ceil(height / self.wallwidth)))
        self.grid = [[[True, True, True, True] for y in range(self.gridsize[1])] for x in range(self.gridsize[0])]
        self.make_solution()

    def make_solution(self):
        total = self.gridsize[0] * self.gridsize[1]
        x, y = 0, 0
        stack = []
        visited = 1
        while visited < total:
            neighbors = self.find_neighbors(x, y)
            unvisited = [dir for dir in neighbors if all(self.grid[x+dir[0]][y+dir[1]])]
            if unvisited:
                dir = random.choice(unvisited)
                self.grid[x][y][self.DIRS.index(dir)] = False
                x, y = x+dir[0], y+dir[1]
                self.grid[x][y][(self.DIRS.index(dir) + 2) % 4] = False
                stack.insert(0, (x, y))
                visited += 1
            else:
                x, y = stack.pop(0)

    def find_neighbors(self, x, y):
        """Find all x, y pairs in the up/down right/left directions that are still
        within the bounds of the grid. Return the directions towards each neighbor"""
        neighbors = []
        for dir in self.DIRS:
            nx, ny = x + dir[0], y + dir[1]
            if self.gridsize[0] > nx >= 0 <= ny < self.gridsize[1]:
                neighbors.append(dir)
        return neighbors

if __name__ == "__main__":
    import pygame, sys
    pygame.init()
    pygame.display.set_caption("Maze Test")
    screen = pygame.display.set_mode((800, 600))
    line = pygame.draw.line
    RED = (255, 0, 0)

    maze = Maze(768, 576, Maze.EASY)
    size = maze.wallwidth
    thickness = 3

    for x, row in enumerate(maze.grid):
        for y, walls in enumerate(row):
            dx, dy = x * size + 10, y * size + 10
            left, top, right, bottom = walls
            if left:
                line(screen, RED, (dx, dy), (dx, dy+size), thickness)
            if top:
                line(screen, RED, (dx, dy), (dx+size, dy), thickness)
            if right:
                line(screen, RED, (dx+size, dy), (dx+size, dy+size), thickness)
            if bottom:
                line(screen, RED, (dx, dy+size), (dx+size, dy+size), thickness)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
