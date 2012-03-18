import os


BASE_PATH = os.path.dirname(os.path.dirname(__file__))
MEDIA_PATH = os.path.join(BASE_PATH, 'media')
IMAGE_PATH = os.path.join(MEDIA_PATH, 'img')
SOUND_PATH = os.path.join(MEDIA_PATH, 'sound')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (255, 0, 255)

# Menu
MENU_FONT = os.path.join(MEDIA_PATH, "fonts", "inconsolata.otf")
MENU_FONT_SIZE = 20
MENU_FONT_SIZE_ACTIVE = 30
MENU_FONT_COLOR = (0, 0, 0)

# Game
MAZE_SPEED = 10

# Media

IMAGES = {
    'arrow': 'arrow.png',
}
SOUNDS = {
    'button': 'button.wav',
    'button_press': 'button2.wav',
}
MUSIC = {
}
