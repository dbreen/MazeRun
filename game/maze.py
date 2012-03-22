import math
import pygame
import random

from game import constants
from game.utils import random_color


class Player(object):
    def __init__(self, pos, dir):
        self.x, self.y = pos[0], pos[1]
        self.dir = dir
        self.speed = constants.PLAYER_SPEED
        self.path = [pos]
        self.dir_keys = dict(zip(('left', 'up', 'right', 'down'), Maze.DIRS))

    def update(self):
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed

    def change_dir(self, dir):
        self.path.append((self.x, self.y))
        self.dir = self.dir_keys[dir]

    @property
    def points(self):
        return self.path + [(self.x, self.y)]

    @property
    def current(self):
        return self.x, self.y

class Maze(object):
    DERP, EASY, MEDIUM, HARD, IMPOSSIBRU = range(5)
    WIDTHS = {
        DERP: 128, EASY: 48, MEDIUM: 32, HARD: 24, IMPOSSIBRU: 16,
    }
    # Left, Top, Right, Down
    DIRS = ((-1, 0), (0, -1), (1, 0), (0, 1))

    def __init__(self, width, height, difficulty):
        self.DEBUG = False
        # initialize sizes and the grid representing our walls (or lack thereof)
        self.width = width
        self.height = height
        self.wallwidth = self.WIDTHS[difficulty]
        self.screen_offsets = ((constants.SCREEN_WIDTH - width) / 2,
                               (constants.SCREEN_HEIGHT - height) / 2)
        self.gridsize = (int(math.ceil(width / self.wallwidth)),
                         int(math.ceil(height / self.wallwidth)))
        # grid represents walls - True is a wall, left, top, right, down
        self.grid = [[[True, True, True, True] for y in range(self.gridsize[1])] for x in range(self.gridsize[0])]

        # configure some defaults for this specific maze
        self.wall_color = random_color()
        corners = ((0, 0), (0, self.gridsize[1] - 1), (self.gridsize[0] - 1, 0), (self.gridsize[0] - 1, self.gridsize[1] - 1))
        self.start = random.choice(corners)
        while True:
            self.end = random.choice(corners)
            if self.end != self.start:
                break
        # we will set this when generating the solution
        self.start_dir = None

        self.make_solution()

        self.player = Player(self.grid_to_screen(self.start), self.start_dir)

    def make_solution(self):
        x, y = self.start
        stack = []
        visited = 1
        total = self.gridsize[0] * self.gridsize[1]
        while visited < total:
            neighbors = self.find_neighbors(x, y)
            unvisited = [dir for dir in neighbors if all(self.grid[x+dir[0]][y+dir[1]])]
            if unvisited:
                dir = random.choice(unvisited)
                if not self.start_dir:
                    # this is the direction from the start point that leads to a solution
                    self.start_dir = dir
                    print "starting dir = %s" % str(dir)
                    print unvisited
                # break down the wall bordering this neighbor
                self.grid[x][y][self.DIRS.index(dir)] = False
                x, y = x+dir[0], y+dir[1]
                # break down the wall of this neighbor towards our position
                self.grid[x][y][(self.DIRS.index(dir) + 2) % 4] = False
                stack.append((x, y))
                visited += 1
            else:
                x, y = stack.pop()

    def find_neighbors(self, x, y):
        """Find all x, y pairs in the up/down right/left directions that are still
        within the bounds of the grid. Return the directions towards each neighbor"""
        neighbors = []
        for dir in self.DIRS:
            nx, ny = x + dir[0], y + dir[1]
            if self.gridsize[0] > nx >= 0 <= ny < self.gridsize[1]:
                neighbors.append(dir)
        return neighbors

    def render(self, surface):
        line = pygame.draw.line
        size = self.wallwidth
        for x, row in enumerate(self.grid):
            for y, walls in enumerate(row):
                dx, dy = x * size + self.screen_offsets[0], y * size + self.screen_offsets[1]
                if self.DEBUG:
                    # draw grids
                    pygame.draw.rect(surface, (127, 127, 127), pygame.Rect(dx+8, dy+8, size-16, size-16), 1)
                left, top, right, bottom = walls
                if left:
                    line(surface, self.wall_color, (dx, dy), (dx, dy+size), constants.WALL_THICKNESS)
                if top:
                    line(surface, self.wall_color, (dx, dy), (dx+size, dy), constants.WALL_THICKNESS)
                if right:
                    line(surface, self.wall_color, (dx+size, dy), (dx+size, dy+size), constants.WALL_THICKNESS)
                if bottom:
                    line(surface, self.wall_color, (dx, dy+size), (dx+size, dy+size), constants.WALL_THICKNESS)
        self.draw_marker(surface, self.start, constants.START_COLOR, constants.POINT_MARKER_WIDTH)
        self.draw_marker(surface, self.end, constants.END_COLOR, constants.POINT_MARKER_WIDTH)
        self.draw_player(surface)

    def draw_marker(self, surface, point, color, radius):
        return pygame.draw.circle(surface, color, self.grid_to_screen(point), radius)

    def draw_player(self, surface):
        pygame.draw.lines(surface, constants.PLAYER_LINE_COLOR, False,
                            self.player.points, constants.PLAYER_LINE_THICKNESS)

    def grid_to_screen(self, pos):
        """Convert grid coordinates to screen coordinates"""
        ww = self.wallwidth
        return ((pos[0] + 1) * ww - ww / 2 + constants.WALL_THICKNESS / 2 + self.screen_offsets[0],
                (pos[1] + 1) * ww - ww / 2 + constants.WALL_THICKNESS / 2 + self.screen_offsets[1])
