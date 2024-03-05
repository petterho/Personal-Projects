import pygame
import math
import numpy as np
import random

class Ball:
    def __init__(self, size=1, mass=1, pos=(1, 1), vel=(0, 0),
                 color=(150, 0, 0)
                 ):
        self.size = size
        self.mass = mass

        self.pos = np.array(pos)
        self.vel = np.array(vel)

        self.color = color

    def update_position(self):
        self.pos = self.pos + self.vel

    def gravity(self, gravity_value):
        self.vel = self.vel + gravity_value


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
    dist_centers = np.linalg.norm(ball1.pos - ball2.pos)
    if dist_centers < ball1.size + ball2.size:
        v1 = ball1.vel
        m1 = ball1.mass
        x1 = ball1.pos
        v2 = ball2.vel
        m2 = ball2.mass
        x2 = ball2.pos

        u1 = v1 - 2 * m2 / (m1 + m2) * np.dot((v1 - v2), (x1 - x2)) / \
             np.linalg.norm(x1 - x2) ** 2 * (x1 - x2)
        u2 = v2 - 2 * m1 / (m2 + m1) * np.dot((v2 - v1), (x2 - x1)) / \
             np.linalg.norm(x2 - x1) ** 2 * (x2 - x1)

        ball1.pos = ball1.pos - ball1.vel
        ball2.pos = ball2.pos - ball2.vel
        ball1.vel = u1
        ball2.vel = u2


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
    """
    pos = ball1.pos - ball2.pos
    vel = ball1.vel - ball2.vel
    px, py = pos
    vx, vy = vel
    a = vx**2 + vy**2
    b = 2 * (px * vx + py * vy)
    c = px**2 + py**2 -(ball1.size + ball2.size)**2
    sol1, sol2 = solve_quadratic_equation(a, b, c)
    return sol1, sol2


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
            'can_collide_value': 0,  # Used in debugging. Not used now
            'balls': [Ball(50, 1, (100, 350), (1, 1)),
                      Ball(50, 1, (300, 200), (0, 0))
                      ]
        }

        if options is not None:
            self.set_options(options)

        self.can_collide_value = self.options_dict['can_collide_value']
        self.gravity = self.options_dict['gravity']
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
            bx, by = ball.pos
            vx, vy = ball.vel

            if bx + ball.size > self.dim_field_x:
                ball.pos = (bx - vx, by)
                ball.vel = (-vx, vy)
            if bx - ball.size <= 0:
                ball.pos = (bx - vx, by)
                ball.vel = (-vx, vy)
            if by + ball.size >= self.dim_field_y:
                ball.pos = (bx, by - vy)
                ball.vel = (vx, -vy)
            if by - ball.size <= 0:
                ball.pos = (bx, by - vy)
                ball.vel = (vx, -vy)

    def check_ball_collisions(self):
        self.check_ball_with_balls()
        self.check_ball_with_walls()

    def update_gravity(self):
        for ball in self.balls:
            ball.gravity(self.gravity)

    def update_position(self):
        for ball in self.balls:
            ball.update_position()

    def update_balls(self):
        self.check_ball_collisions()
        self.update_gravity()
        self.update_position()

    def draw_balls(self):
        for ball in self.balls:
            pygame.draw.circle(self.display,
                               ball.color,
                               ball.pos,
                               ball.size
                               )

    def draw_border_reset_field(self):
        pygame.draw.rect(self.display,
                         self.options_dict['color_playing_field'],
                         (0, 0, self.dim_field_x, self.dim_field_y)
                         )

    def draw_game(self):
        self.draw_border_reset_field()
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


def ball_test():
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
        'balls': [Ball(50, 1, (100, 350), (1, 1)),
                  Ball(50, 1, (300, 200), (0, 0))
                  ]
    }
    rand_gen = random.Random()
    ball_list = []
    for i in range(15):
        sw = rand_gen.uniform(10, 30)
        px = rand_gen.uniform(0 + sw, dict_['dim_field_x'] - sw)
        py = rand_gen.uniform(0 + sw, dict_['dim_field_y'] - sw)
        vx = rand_gen.uniform(-5, 5)
        vy = rand_gen.uniform(-5, 5)
        color = [int(rand_gen.uniform(0, 255)) for _ in range(3)]
        print(type(color), len(color))

        ball_list.append(Ball(size=sw, mass=sw, pos=(px, py), vel=(vx, vy),
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

        ball_list.append(Ball(size=sw, mass=sw, pos=(px, py), vel=(vx, vy),
                              color=color))

    ball_list.append(Ball(50, 50, (300, 300), (0, 0), (200, 0, 0)))

    dict_['balls'] = ball_list

    game = Game(dict_)
    game.play()


if __name__ == '__main__':
    b1 = Ball(1, 1, (0, 0), (1, 0))
    b2 = Ball(1, 1, (2, 0.5), (-1, 0))
    sol1, sol2 = collision_point(b1, b2)
    print(sol1, sol2)

