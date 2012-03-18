import pygame
import random
import sys

from game import constants, maze
from game.media import media
from game.scene import Scene

# List of menu options (text, action_method, condition) where condition is None or a callable.
# If it is a callable that returns False, the option is not shown.
CONTINUE = 0
NEW_GAME = 1
QUIT = 2
OPTIONS = [
    ('Continue', 'opt_continue', lambda scene: scene.game_running),
    ('New Course', 'opt_start', None),
    ('Quit', 'opt_quit', None),
]

NUM_PIPES = 50
PIPE_COLORS = (constants.WHITE, (255, 0, 0), (0, 255, 0), (0, 0, 255))
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

class Pipe(object):
    def __init__(self, color):
        self.color = color
        rpoint = (random.randint(0, constants.SCREEN_WIDTH), 
                  random.randint(0, constants.SCREEN_HEIGHT))
        self.pointlist = [rpoint]
        self.current = rpoint
        self.dir = random.choice(DIRS)
        self.speed = random.randint(2, 6)
        self.width = 5 # random.randint(3, 10)

    def update(self):
        # 10% chance of changing direction
        if random.random() <= 0.1:
            self.dir = DIRS[(DIRS.index(self.dir) + random.choice((-1, 1))) % len(DIRS)]
            self.pointlist.append(self.current)
        self.current = (self.current[0] + self.speed * self.dir[0],
                        self.current[1] + self.speed * self.dir[1])

    def draw(self, screen):
        pygame.draw.lines(screen, self.color, False, self.pointlist + [self.current],
                          self.width)

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

class MenuScene(Scene):
    def load(self):
        self.font = pygame.font.Font(constants.MENU_FONT, constants.MENU_FONT_SIZE)
        self.active_font = pygame.font.Font(constants.MENU_FONT, constants.MENU_FONT_SIZE_ACTIVE)
        self.overlay = pygame.Surface(constants.SCREEN)

    def setup(self, first_time=False):
        # Selected menu choice - if "Continue" is there, have that selected
        self._current_option = NEW_GAME if first_time else CONTINUE
        self.game_running = self.manager.get_state('main', 'running')
        self.pipes = [Pipe(random_color()) for _ in range(NUM_PIPES)]
        self.overlay.set_alpha(225)

    def render_options(self, screen):
        x, y = 30, 20
        menuwidth = 200
        menusurf = pygame.Surface((menuwidth, 200))
        menusurf.set_colorkey(constants.TRANSPARENT)
        menusurf.fill(constants.TRANSPARENT)
        for index, (text, action, show) in enumerate(OPTIONS):
            if show is not None and not show(self):
                continue
            active = index == self._current_option
            font = self.active_font if active else self.font
            surf = font.render(text, True, constants.MENU_FONT_COLOR, constants.WHITE)
            menusurf.blit(surf, (x, y))
            if active:
                menusurf.blit(media['img.arrow'], (x - 25, y + 12))
            y += surf.get_height() + 10
        w = constants.SCREEN_WIDTH/2 - menuwidth/2
        t = constants.SCREEN_HEIGHT/2 - y/2
        menuback = pygame.Rect(w, t, menuwidth, y+20)
        self.overlay.set_alpha(max(64, self.overlay.get_alpha() - 2))
        screen.blit(self.overlay, (0, 0))
        pygame.draw.rect(screen, constants.WHITE, menuback)
        screen.blit(menusurf, (w, t))

    def render(self, screen):
        screen.fill(constants.BLACK)
        for pipe in self.pipes:
            pipe.update()
            pipe.draw(screen)
        self.render_options(screen)

    def opt_continue(self):
        self.manager.switch_scene('main')
        return True

    def opt_start(self):
        self.manager.switch_scene('main')
        return True

    def opt_quit(self):
        sys.exit()

    def do_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                if self.game_running:
                    self.manager.switch_scene('main')
                    return
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                media['snd.button'].play()
                move = -1 if event.key == pygame.K_UP else 1
                self._current_option = (self._current_option + move) % len(OPTIONS)
                if self._current_option == CONTINUE and not self.game_running:
                    self._current_option = NEW_GAME if event.key == pygame.K_DOWN else (len(OPTIONS) - 1)
            elif event.key == pygame.K_RETURN:
                if self._current_option != NEW_GAME:
                    media['snd.button_press'].play()
                action = OPTIONS[self._current_option][1]
                return getattr(self, action)()
        return False
