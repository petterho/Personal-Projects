"""
Inspiration from:
https://www.edureka.co/blog/snake-game-with-pygame/
"""

import pygame
from copy import copy
from random import choice


class Queue:
    def __init__(self, elements_for_queue=None):
        self.queue = []
        if elements_for_queue is not None:
            for element in elements_for_queue:
                self.enqueue(element)

        self._counter = 0

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.pop(0)

    def front(self):
        return self.queue[-1]

    def rear(self):
        return self.queue[0]

    def __len__(self):
        return len(self.queue)

    def __iter__(self):
        self._counter = len(self)
        return self

    def __next__(self):
        self._counter -= 1
        if self._counter >= 0:
            return self.queue[self._counter]
        else:
            raise StopIteration

    def __str__(self):
        return self.queue.__str__()


class SnakeBodyPart:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

    def __repr__(self):
        return f'x: {self.x}, y: {self.y}'

    def __copy__(self):
        return SnakeBodyPart(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Snake:
    def __init__(self, direction=None, head=None, body=None, move=None):
        standard_snake = {'direction': 1,
                          'head': SnakeBodyPart(1, 1),
                          'body': Queue([SnakeBodyPart(1, 5),
                                         SnakeBodyPart(1, 4),
                                         SnakeBodyPart(1, 3),
                                         SnakeBodyPart(1, 2)]),
                          'move': 0.25}
        if direction is None and head is None and body is None:
            self.__init__(**standard_snake)
        else:
            self.direction = direction
            self.head = head
            self.body = body
            self.chop_tail_bool = True
            self.chop_tail_counter = 1/move
            self.move = move

    def __str__(self):
        return f'Direction: {self.direction} \n' \
               f'Head: {self.head} \n' \
               f'Body: {self.body} \n'

    def __len__(self):
        return len(self.body + 1)

    def __iter__(self):
        self._head_given = False
        self._body_iter = self.body.__iter__()
        return self

    def __next__(self):
        if self._head_given:
            return next(self._body_iter)
        else:
            self._head_given = True
            return self.head

    def chop_tail(self):
        self.body.dequeue()

    def add_head(self, new_head):
        self.body.enqueue(self.head)
        self.head = new_head

    def eat(self):
        self.chop_tail_bool = False
        self.chop_tail_counter = 0

    def change_direction(self, direction):
        if direction == 0 and self.direction != 2:
            self.direction = direction
        elif direction == 1 and self.direction != 3:
            self.direction = direction
        elif direction == 2 and self.direction != 0:
            self.direction = direction
        elif direction == 3 and self.direction != 1:
            self.direction = direction

    def move(self):
        new_head = copy(self.head)
        if self.direction == 0:
            new_head.y += -1
        if self.direction == 1:
            new_head.x += 1
        if self.direction == 2:
            new_head.y += 1
        if self.direction == 3:
            new_head.x += -1
        self.add_head(new_head)
        if self.chop_tail_bool:
            self.chop_tail()
        else:
            self.chop_tail_bool = True

    def move_partly(self):
        new_head = copy(self.head)
        if self.direction == 0:
            new_head.y += -self.move
        if self.direction == 1:
            new_head.x += self.move
        if self.direction == 2:
            new_head.y += self.move
        if self.direction == 3:
            new_head.x += -self.move
        self.add_head(new_head)
        if self.chop_tail_counter < 1/self.move:
            self.chop_tail_counter += 1
        else:
            self.chop_tail()


class Game:
    def __init__(self, options=None):
        self.options_dict = {
            # Variables
            'dimensions': 20,
            'dim_square': 20,
            'start_speed': 1,
            'speed_increase': 0.1,
            # Colors
            'color_snake_body': (0, 200, 0),
            'color_snake_head': (0, 0, 255),
            'color_food': (255, 0, 0),
            'color_border': (255, 255, 255),
            'color_playing_field': (0, 0, 0),

            'snake': {'direction': 1,
                      'head': SnakeBodyPart(1, 1),
                      'body': Queue([SnakeBodyPart(1, 5),
                                     SnakeBodyPart(1, 4),
                                     SnakeBodyPart(1, 3),
                                     SnakeBodyPart(1, 2)]),
                      'move': 0.25}
        }

        if options is not None:
            self.set_options(options)

        self.frames_per_move = int(1 / self.options_dict['snake']['move'])
        self.snake = Snake(**self.options_dict['snake'])
        self.food = SnakeBodyPart(2, 2)
        self.food_set = None
        self.place_food()

        self.game_over = False
        self.speed = self.options_dict['start_speed']

        pygame.init()
        self.display = pygame.display.set_mode(
            (self.options_dict['dimensions'] * self.options_dict['dim_square'],
             self.options_dict['dimensions'] * self.options_dict['dim_square']
             ))
        pygame.display.set_caption("Petter's game")
        self.clock = pygame.time.Clock()

    def place_food(self):
        self.make_food_grid()
        if self.food_set == set():
            self.game_over = True
        else:
            x, y = choice(list(self.food_set))
            self.food = SnakeBodyPart(x, y)

    def make_food_grid(self):
        self.food_set = set()
        for x in range(1, self.options_dict['dimensions'] - 1):
            for y in range(1, self.options_dict['dimensions'] - 1):
                self.food_set.add((x, y))

        tiles_to_remove = set()
        for body_part in self.snake:
            tuple_ = (body_part.x, body_part.y)
            tiles_to_remove.add(tuple_)
        self.food_set = self.food_set.difference(tiles_to_remove)

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
            self.snake.change_direction(0)
        if keystroke.key == pygame.K_RIGHT:
            self.snake.change_direction(1)
        if keystroke.key == pygame.K_DOWN:
            self.snake.change_direction(2)
        if keystroke.key == pygame.K_LEFT:
            self.snake.change_direction(3)

    def draw_snake(self):
        for body_part in self.snake.body:
            pygame.draw.rect(self.display,
                             self.options_dict['color_snake_body'],
                             (body_part.x * self.options_dict['dim_square']
                              + 1,
                              body_part.y * self.options_dict['dim_square']
                              + 1,
                              self.options_dict['dim_square'] - 2,
                              self.options_dict['dim_square'] - 2))

        pygame.draw.rect(self.display,
                         self.options_dict['color_snake_head'],
                         (self.snake.head.x * self.options_dict['dim_square'],
                          self.snake.head.y * self.options_dict['dim_square'],
                          self.options_dict['dim_square'],
                          self.options_dict['dim_square']))

    def draw_border_reset_field(self):
        pygame.draw.rect(self.display,
                         self.options_dict['color_border'],
                         (0,
                          0,
                          self.options_dict['dimensions'] *
                          self.options_dict['dim_square'],
                          self.options_dict['dimensions'] *
                          self.options_dict['dim_square']))

        pygame.draw.rect(self.display,
                         self.options_dict['color_playing_field'],
                         (self.options_dict['dim_square'],
                          self.options_dict['dim_square'],
                          (self.options_dict['dimensions'] - 2) *
                          self.options_dict['dim_square'],
                          (self.options_dict['dimensions'] - 2) *
                          self.options_dict['dim_square']))

    def draw_food(self):
        pygame.draw.circle(self.display,
                           self.options_dict['color_food'],
                           ((self.food.x + 0.5) * self.options_dict[
                               'dim_square'],
                            (self.food.y + 0.5) * self.options_dict[
                             'dim_square']),
                           self.options_dict['dim_square'] / 2)

    def draw_game(self):
        self.draw_border_reset_field()
        self.draw_snake()
        self.draw_food()
        pygame.display.update()

    def check_for_walls(self):
        if self.snake.head.y < 1 or self.snake.head.y > self.options_dict[
                                                         'dimensions'] - 2 \
                or \
           self.snake.head.x < 1 or self.snake.head.x > self.options_dict[
                                                       'dimensions'] - 2:
            self.game_over = True

    def check_for_food(self):
        if self.snake.head.y == self.food.y and \
         self.snake.head.x == self.food.x:
            self.snake.eat()
            self.place_food()
            self.speed += self.options_dict['speed_increase']

    def check_for_body(self):
        if self.snake.head in self.snake.body:
            self.game_over = True

    def check_for_items(self):
        self.check_for_walls()
        self.check_for_food()
        self.check_for_body()

    def play_hard_style(self):

        self.draw_game()

        while not self.game_over:
            first_keypress = True
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if first_keypress:
                        self.pressed_key(event)
                        first_keypress = False

            self.snake.move()
            self.check_for_items()
            self.draw_game()
            self.clock.tick(self.speed)

        pygame.quit()
        quit()

    def play(self):
        """
        Enables queuing key presses
        Returns
        -------

        """
        self.draw_game()
        only_move = self.frames_per_move
        while not self.game_over:
            if only_move < self.frames_per_move - 1:
                self.snake.move_partly()
                only_move += 1
            else:
                looking_for_moves = True
                while looking_for_moves:
                    event = pygame.event.poll()
                    print(event)
                    if event.type == pygame.QUIT:
                        self.game_over = True
                        looking_for_moves = False
                    elif event.type == pygame.KEYDOWN:
                        self.pressed_key(event)
                        looking_for_moves = False
                    elif event.type == pygame.NOEVENT:
                        break
                print(f'Snake head: {self.snake.head}')
                print(f'Food: {self.food}')

                self.check_for_items()
                self.snake.move_partly()
                only_move = 0

            self.draw_game()
            self.clock.tick(self.speed * self.frames_per_move)

        pygame.quit()
        quit()


if __name__ == '__main__':
    options_dict = {
        # Variables
        'dimensions': 8,
        'dim_square': 20,
        'start_speed': 5,
        'speed_increase': 0.0,
        # Colors
        'color_snake_body': (0, 200, 0),
        'color_snake_head': (0, 0, 255),
        'color_food': (255, 0, 0),
        'color_border': (255, 255, 255),
        'color_playing_field': (0, 0, 0),

        'snake': {'direction': 1,
                  'head': SnakeBodyPart(1, 1),
                  'body': Queue([SnakeBodyPart(1, 5),
                                 SnakeBodyPart(1, 4),
                                 SnakeBodyPart(1, 3),
                                 SnakeBodyPart(1, 2)]),
                  'move': 1/16} # Because of rounding error it has to be 1/2^n
    }
    game = Game(options_dict)
    game.play()
