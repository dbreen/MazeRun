import pygame

from game import maze, utils
from game.constants import *
from game.media import media
from game.scene import Scene


class MainScene(Scene):
    def load(self):
        # state variables
        self.set_state('running', True)

    def setup(self, first_time):
        self.new_game()

    def new_game(self):
        pass

    def render(self, screen):
        screen.fill(BLACK)

    def do_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_scene('menu')
