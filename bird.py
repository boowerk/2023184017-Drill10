# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
from ball import Ball
import game_world
import game_framework

# bird Run Speed
PIXEL_PER_METER = (10.0 / 0.5)
RUN_SPEED_KMPH = 25.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

class Idle:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.action = 3
            bird.face_dir = 1
        elif right_down(e) or left_up(e):
            bird.action = 2
            bird.face_dir = -1
        elif left_down(e) or right_up(e):
            bird.action = 3
            bird.face_dir = 1

        bird.frame = 0
        bird.wait_time = get_time()

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - bird.wait_time > 2:
            bird.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(bird):
        bird.image.clip_draw(int(bird.frame) * 100, bird.action * 100, 100, 100, bird.x, bird.y)

class Run:
    @staticmethod
    def enter(bird, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = -1, -1, 0

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()


    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        # bird.x += bird.dir * 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(bird):
        bird.image.clip_draw(int(bird.frame) * 100, bird.action * 100, 100, 100, bird.x, bird.y)

class Bird:

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.font = load_font('ENCR10B.TTF', 16)
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 60, self.y + 50, f'(Time: {get_time(): .2f})' , (255, 255, 0))

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.face_dir * 10)
        game_world.add_object(ball)