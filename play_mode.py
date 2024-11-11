from pico2d import *
import game_framework

import game_world
from grass import Grass
from bird import Bird

# bird = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            bird.handle_event(event)

def init():
    global grass
    global bird

    grass = Grass()
    game_world.add_object(grass, 0)

    bird = Bird()
    game_world.add_object(bird, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

