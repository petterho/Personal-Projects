import pygame
import math
import numpy as np
import random
from collections import deque


class Ball:
    def __init__(self, radius=1, mass=1, pos=(1, 1), vel=(0, 0),
                 color=(150, 0, 0)
                 ):
        self.radius = radius
        self.mass = mass

        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.next_pos = self.pos + self.vel
        self.next_vel = self.vel

        self.color = color

        len_queue = 100
        self.tail = deque([self.pos] * len_queue, maxlen=len_queue)

    def update_next_position(self):
        self.next_pos = self.pos + self.vel

    def update_position(self):
        self.pos = self.next_pos

        # Queue stuff
        self.tail.append(self.pos)

    def update_next_velocity(self, factor):
        self.next_vel = factor**2 * self.next_vel

    def update_velocity(self):
        self.vel = self.next_vel

    def gravity(self, gravity_value):
        self.next_vel = self.next_vel + gravity_value


class StationaryBall(Ball):
    def update_position(self):
        pass

    def update_velocity(self):
        pass


def collision(ball1, ball2):
    """
    Modifies the balls

    Parameters
    ----------
    ball1
    ball2

    Returns
    -------
    Nothing, but updates the balls
    """
    dist_centers = np.linalg.norm(ball1.next_pos - ball2.next_pos)
    if dist_centers < ball1.radius + ball2.radius:

        # print(f'Før:   POS: {ball1.pos}\tVEL: {ball1.vel}\n'
        #       f'Tenkt: POS: {ball1.next_pos}\tVEL: {ball1.next_vel}')

        a = collision_point(ball1, ball2)
        pos_collision1 = ball1.pos + a * ball1.vel
        pos_collision2 = ball2.pos + a * ball2.vel

        v1 = ball1.vel
        m1 = ball1.mass
        x1 = pos_collision1
        v2 = ball2.vel
        m2 = ball2.mass
        x2 = pos_collision2

        u1 = v1 - 2 * m2 / (m1 + m2) * np.dot((v1 - v2), (x1 - x2)) / \
             np.linalg.norm(x1 - x2) ** 2 * (x1 - x2)
        u2 = v2 - 2 * m1 / (m2 + m1) * np.dot((v2 - v1), (x2 - x1)) / \
             np.linalg.norm(x2 - x1) ** 2 * (x2 - x1)

        ball1.next_pos = pos_collision1 + (1-a) * u1
        ball2.next_pos = pos_collision2 + (1-a) * u2
        ball1.next_vel = u1
        ball2.next_vel = u2

        # print(f'Etter: POS: {ball1.next_pos}\tVEL: {ball1.next_vel}')

def solve_quadratic_equation(a, b, c):
    sqrt_term = b**2 - 4*a*c
    if sqrt_term < 0:
        return None, None
    elif sqrt_term == 0:
        sol = -b / (2 * a)
        return sol, sol
    sqrt_term = math.sqrt(sqrt_term)
    sol1 = (-b + sqrt_term) / (2 * a)
    sol2 = (-b - sqrt_term) / (2 * a)
    return sol1, sol2


def collision_point(ball1, ball2):
    """

    Parameters
    ----------
    ball1
    ball2

    Returns
    -------


    pos = pos1 - pos2
    vel = vel1 - vel2

    a = vx**2 + vy**2
    b = 2 * (px*vx + py*vy)
    c = px**2 + py**2 - (r1 + r1)2

    solve for x in ax**2 + bx + c = 0

    returns the second solution, the -sqrt term, if that is not None
    """
    pos = ball1.pos - ball2.pos
    vel = ball1.vel - ball2.vel
    px, py = pos
    vx, vy = vel
    a = vx**2 + vy**2
    b = 2 * (px * vx + py * vy)
    c = px**2 + py**2 - (ball1.radius + ball2.radius)**2
    sol1, sol2 = solve_quadratic_equation(a, b, c)

    if sol2 is not None:
        return sol2         # Is sometimes None and causes problems
    else:
        return 0


def gravity(ball1, ball2, gravitational_constant):
    vector_ball1 = ball1.next_pos - ball2.next_pos
    r = np.linalg.norm(vector_ball1)
    f = gravitational_constant * ball1.mass * ball2.mass / r ** 2

    # Reason for minus is that the same vector is used
    a1 = - f / ball1.mass * vector_ball1 / r
    a2 = f / ball2.mass * vector_ball1 / r

    ball1.next_vel = ball1.next_vel + a1
    ball2.next_vel = ball2.next_vel + a2


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


class Game:
    def __init__(self, options=None):
        self.options_dict = {
            # Variables
            'dim_field_x': 400,
            'dim_field_y': 400,
            'frames': 60,
            # Colors
            'color_border': (255, 255, 255),
            'color_playing_field': (0, 0, 0),
            # Balls
            'gravity': np.array((0, 1)),
            'gravitational_constant': 1,
            'friction': 0.99,
            'can_collide_value': 0,  # Used in debugging. Not used now
            'balls': [Ball(50, 1, (100, 350), (1, 1)),
                      Ball(50, 1, (300, 200), (0, 0))
                      ]
        }

        if options is not None:
            self.set_options(options)

        self.can_collide_value = self.options_dict['can_collide_value']
        self.gravity = self.options_dict['gravity']
        self.gravitational_constant = self.options_dict[
            'gravitational_constant']
        self.friction = self.options_dict['friction']
        self.balls = self.options_dict['balls']

        self.game_over = False
        self.frames = self.options_dict['frames']

        self.dim_field_x = self.options_dict['dim_field_x']
        self.dim_field_y = self.options_dict['dim_field_y']

        pygame.init()
        self.display = pygame.display.set_mode(
            (self.dim_field_x,
             self.dim_field_y
             ))
        pygame.display.set_caption("Petter's simulation")
        self.clock = pygame.time.Clock()

    def set_options(self, options):
        """

        Parameters
        ----------
        options

        Returns
        -------

        Should be checked, and is checked

        """
        for key, value in options.items():
            if key in self.options_dict:
                self.options_dict[key] = value

    def pressed_key(self, keystroke):
        if keystroke.key == pygame.K_UP:
            pass
        if keystroke.key == pygame.K_RIGHT:
            pass
        if keystroke.key == pygame.K_DOWN:
            pass
        if keystroke.key == pygame.K_LEFT:
            pass
        if keystroke.key == pygame.K_r:
            self.__init__()

    def check_ball_with_balls(self):
        for i, ball1 in enumerate(self.balls):
            for j, ball2 in enumerate(self.balls[i + 1:]):
                collision(ball1, ball2)

    def check_ball_with_walls(self):
        for ball in self.balls:

            if ball.next_pos[0] + ball.radius > self.dim_field_x:
                # print(f'Høyre vegg treft.\n'
                #      f'Før:   POS: {ball.pos}\t VEL: {ball.vel}\n'
                #      f'Tenkt: POS: {ball.next_pos}\t VEL: {ball.next_vel}')

                a = (self.dim_field_x - ball.pos[0] - ball.radius) / \
                    ball.vel[0]
                pos_wall = ball.pos + a * ball.vel
                ball.next_vel = np.array((-ball.vel[0], ball.vel[1]))
                ball.next_pos = pos_wall + (1-a) * ball.next_vel

                # print(f'Etter: POS: {ball.next_pos}\t VEL: {ball.next_vel}')
            if ball.next_pos[0] - ball.radius <= 0:
                a = (ball.radius - ball.pos[0]) / ball.vel[0]
                pos_wall = ball.pos + a * ball.vel
                ball.next_vel = np.array((-ball.vel[0], ball.vel[1]))
                ball.next_pos = pos_wall + (1 - a) * ball.next_vel
            if ball.next_pos[1] + ball.radius >= self.dim_field_y:
                a = (self.dim_field_y - ball.pos[1] - ball.radius) / \
                    ball.vel[1]
                pos_wall = ball.pos + a * ball.vel
                ball.next_vel = np.array((ball.vel[0], -ball.vel[1]))
                ball.next_pos = pos_wall + (1 - a) * ball.next_vel
            if ball.next_pos[1] - ball.radius <= 0:
                a = (ball.radius - ball.pos[1]) / ball.vel[1]
                pos_wall = ball.pos + a * ball.vel
                ball.next_vel = np.array((ball.vel[0], -ball.vel[1]))
                ball.next_pos = pos_wall + (1 - a) * ball.next_vel

    def check_ball_collisions(self):
        self.check_ball_with_balls()
        self.check_ball_with_walls()

    def update_gravity_between_balls(self):
        for i, ball1 in enumerate(self.balls):
            for j, ball2 in enumerate(self.balls[i + 1:]):
                gravity(ball1, ball2, self.gravitational_constant)

    def update_gravity(self):
        for ball in self.balls:
            ball.gravity(self.gravity)

    def update_position(self):
        for ball in self.balls:
            ball.update_position()

    def update_velocity(self):
        for ball in self.balls:
            ball.update_velocity()

    def update_next_position(self):
        for ball in self.balls:
            ball.update_next_position()

    def update_next_velocity(self):
        for ball in self.balls:
            ball.update_next_velocity(self.friction)

    def update_balls(self):
        self.update_next_velocity()  # A kind of friction
        self.update_next_position()
        self.check_ball_collisions()
        #self.update_gravity()
        self.update_gravity_between_balls()
        self.update_position()
        self.update_velocity()

    def draw_balls(self):
        for ball in self.balls:
            pygame.draw.circle(self.display,
                               ball.color,
                               ball.pos,
                               ball.radius
                               )

    def draw_border_reset_field(self):
        pygame.draw.rect(self.display,
                         self.options_dict['color_playing_field'],
                         (0, 0, self.dim_field_x, self.dim_field_y)
                         )

    def draw_tail(self):
        for ball in self.balls:
            pygame.draw.lines(self.display,
                              ball.color,
                              False,
                              ball.tail
                              )

    def draw_game(self):
        self.draw_border_reset_field()
        self.draw_tail()
        self.draw_balls()
        pygame.display.update()

    def update_game(self):
        self.update_balls()

    def play(self):
        """
        Returns
        -------

        """
        self.draw_game()
        while not self.game_over:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    self.pressed_key(event)
                if event.type == pygame.NOEVENT:
                    pass
                else:
                    pass

            self.update_game()
            self.draw_game()
            self.clock.tick(self.frames)

        pygame.quit()
        quit()


def ball_try():
    dict_ = {
        # Variables
        'dim_field_x': 1000,
        'dim_field_y': 600,
        'frames': 60,
        # Colors
        'color_border': (255, 255, 255),
        'color_playing_field': (0, 0, 0),
        # Balls
        'gravity': np.array((0, 1)),
        'gravitational_constant': 1,
        'friction': 0.99,
        'balls': [Ball(50, 1, (100, 350), (1, 1)),
                  Ball(50, 1, (300, 200), (0, 0))
                  ]
    }
    rand_gen = random.Random()
    ball_list = []
    for i in range(30):
        sw = rand_gen.uniform(15, 40)
        px = rand_gen.uniform(0 + sw, dict_['dim_field_x'] - sw)
        py = rand_gen.uniform(0 + sw, dict_['dim_field_y'] - sw)
        vx = rand_gen.uniform(-5, 5)
        vy = rand_gen.uniform(-5, 5)
        color = [int(rand_gen.uniform(0, 255)) for _ in range(3)]
        # print(type(color), len(color))

        ball_list.append(Ball(radius=sw, mass=sw, pos=(px, py), vel=(vx, vy),
                              color=color))

    dict_['balls'] = ball_list

    game = Game(dict_)
    game.play()


def brownian_motion():
    dict_ = {
        # Variables
        'dim_field_x': 400,
        'dim_field_y': 400,
        'frames': 60,
        # Colors
        'color_border': (255, 255, 255),
        'color_playing_field': (0, 0, 0),
        # Balls
        'gravity': np.array((0, 0)),
        'friction': 0.99,
        'balls': [Ball(50, 1, (100, 350), (1, 1)),
                  Ball(50, 1, (300, 200), (0, 0))
                  ]
    }
    rand_gen = random.Random()
    ball_list = []

    max_size = 10

    for i in range(200):
        sw = rand_gen.uniform(max_size/2, max_size)
        px = (i * 2 * max_size + max_size)  % dict_['dim_field_x']
        py = int((i * 2 * max_size + max_size) / dict_['dim_field_x']) * 2 *\
             max_size + max_size
        vx = rand_gen.uniform(-5, 5)
        vy = rand_gen.uniform(-5, 5)
        color = [int(rand_gen.uniform(0, 255)) for _ in range(3)]
        print(type(color), len(color))

        ball_list.append(Ball(radius=sw, mass=sw, pos=(px, py), vel=(vx, vy),
                              color=color))

    ball_list.append(Ball(50, 50, (300, 300), (0, 0), (200, 0, 0)))

    dict_['balls'] = ball_list

    game = Game(dict_)
    game.play()


def gravity_try():

    dict_ = {
        # Variables
        'dim_field_x': 1000,
        'dim_field_y': 800,
        'frames': 60,
        # Colors
        'color_border': (255, 255, 255),
        'color_playing_field': (0, 0, 0),
        # Balls
        'gravity': np.array((0, 0.1)),
        'gravitational_constant': 0.5,
        'friction': 0.99,
        'balls': [Ball(50, 50, (100, 350), (0, 0)),
                  Ball(50, 50, (300, 200), (0, 0)),
                  Ball(25, 10, (400, 400), (0, 0))
                  ]
    }
    rand_gen = random.Random()
    r1 = 30
    r2 = 5
    r3 = 2
    x = dict_['dim_field_x']
    y = dict_['dim_field_y']

    balls = [StationaryBall(r1, r1**3, (x/2, y/2), (0, 0), (255, 255, 255)),
             Ball(r2, r2**3, (100, 100), (rand_gen.uniform(0, 10), 0),
                  (200, 0, 0)),
             Ball(r3, r3**3, (x-100, y-100), (rand_gen.uniform(-10, 0), 0),
                  (0, 200, 0))]
    max_size = 12
    for i in range(10):
        size = rand_gen.gauss(6, 2)
        px = (i * 2 * max_size + max_size) % dict_['dim_field_x']
        py = int((i * 2 * max_size + max_size) / dict_['dim_field_x']) * 2 * \
             max_size + max_size
        vx = rand_gen.uniform(-5, 5)
        vy = rand_gen.uniform(-5, 5)
        color = [int(rand_gen.uniform(0, 255)) for _ in range(3)]
        ball = Ball(radius=size, mass=size**3, pos=(px, py), vel=(vx, vy),
                    color=color)
        balls.append(ball)

    dict_['balls'] = balls

    game = Game(dict_)
    game.play()


def try_solver():
    b1 = Ball(1, 1, (0, 0), (1, 0))
    b2 = Ball(1, 1, (2, 0.5), (-1, 0))
    a = collision_point(b1, b2)
    print(a)


if __name__ == '__main__':
    gravity_try()

