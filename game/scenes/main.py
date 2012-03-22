import pygame

from game import maze, utils
from game.constants import *
from game.maze import Maze
from game.media import media
from game.scene import Scene
from game.utils import center


class MainScene(Scene):
    STARTING, PLAYING, DEAD, WIN = range(4)

    def load(self):
        # state variables
        self.set_state('running', True)
        self.font = pygame.font.Font(MENU_FONT, 64)
        #TODO: it's pretty jumpy...
        self.timer_fonts = [
            pygame.font.Font(MENU_FONT, 128 + size*10)
            for size in range(60)
        ]
        self.dead_print = self.font.render("You're Dead, Bro", True, WHITE)
        self.win_print = self.font.render("WINNING!!!", True, WHITE)

    def setup(self, first_time, new_game=True, game_mode=Maze.EASY):
        if self.get_state('status') != self.DEAD:
            self.set_state('status', self.STARTING)
        if new_game:
            self.new_game(game_mode)

    def new_game(self, difficulty):
        self.maze = Maze(MAZE_WIDTH, MAZE_HEIGHT, difficulty)
        self.set_state('status', self.STARTING)
        #TODO: base this off FPS, or actual clock time
        self.starting_ticks = 180 - 1

    def render(self, screen):
        screen.fill(BLACK)

        self.maze.render(screen)

        if self.get_state('status') == self.DEAD:
            screen.blit(self.dead_print, center(self.dead_print))
        elif self.get_state('status') == self.WIN:
            screen.blit(self.win_print, center(self.win_print))

        status = self.get_state('status')
        if status == self.PLAYING:
            self.maze.player.update()
        elif status == self.STARTING:
            self.do_starting(screen)

        cur_pixel = screen.get_at(self.maze.player.current)
        if cur_pixel == self.maze.wall_color:
            self.set_state('status', self.DEAD)
        elif cur_pixel == END_COLOR:
            #TODO: there's a 1 in 17 million chance for this to falsely win because
            # maze color matches winning marker color
            self.set_state('status', self.WIN)

    def do_starting(self, screen):
        seconds = self.starting_ticks / 60 + 1
        font = self.timer_fonts[(self.starting_ticks % 60)]
        countdown = font.render(str(seconds), True, WHITE)
        screen.blit(countdown, center(countdown))
        #TODO: base this on FPS
        self.starting_ticks -= 2
        if self.starting_ticks <= 0:
            self.set_state('status', self.PLAYING)

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
            elif event.key == pygame.K_q:
                self.maze.DEBUG = not self.maze.DEBUG
            elif event.key == pygame.K_w:
                self.maze.player.speed += 1
            elif event.key == pygame.K_d:
                self.maze.player.speed -= 1
