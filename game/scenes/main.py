import pygame

from game import maze, utils
from game.constants import *
from game.maze import Maze
from game.media import media
from game.scene import Scene
from game.utils import center


class MainScene(Scene):
    def load(self):
        # state variables
        self.set_state('running', True)
        self.font = pygame.font.Font(MENU_FONT, 64)
        self.dead_print = self.font.render("You're Dead, Bro", True, WHITE)

    def setup(self, first_time, new_game=True, game_mode=Maze.EASY):
        if new_game:
            self.new_game(game_mode)

    def new_game(self, difficulty):
        self.maze = Maze(MAZE_WIDTH, MAZE_HEIGHT, difficulty)
        self.set_state('dead', False)

    def render(self, screen):
        if not self.get_state('dead'):
            self.maze.player.update()

        if screen.get_at(self.maze.player.current) == self.maze.wall_color:
            self.set_state('dead', True)

        screen.fill(BLACK)
        self.maze.render(screen)

        if self.get_state('dead'):
            screen.blit(self.dead_print, center(self.dead_print))

    def do_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_scene('menu')
            elif event.key == pygame.K_LEFT:
                self.maze.player.change_dir('left')
            elif event.key == pygame.K_RIGHT:
                self.maze.player.change_dir('right')
            elif event.key == pygame.K_UP:
                self.maze.player.change_dir('up')
            elif event.key == pygame.K_DOWN:
                self.maze.player.change_dir('down')
