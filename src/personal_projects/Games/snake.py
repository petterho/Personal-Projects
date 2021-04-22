"""
Inspiration from:
https://www.edureka.co/blog/snake-game-with-pygame/
"""

import pygame
from copy import copy


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
        return 'This is a queue'


class SnakeBodyPart:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

    def __copy__(self):
        return SnakeBodyPart(self.x, self.y)


class Snake:
    def __init__(self, direction, head, body):
        self.direction = direction
        self.head = head
        self.body = body

    def __len__(self):
        return len(self.body)

    def __str__(self):
        return f'Direction: {self.direction} \n' \
               f'Head: {self.head} \n'

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

    def eat(self, value_food):
        for i in range(value_food):
            self.body.enqueue(copy(self.body.rear()))

    def move(self, direction):
        new_head = copy(self.head)
        if direction == 0 and self.direction != 2:
            self.direction = direction
            new_head.y += -1
        elif direction == 1 and self.direction != 3:
            self.direction = direction
            new_head.x += 1
        elif direction == 2 and self.direction != 0:
            self.direction = direction
            new_head.y += 1
        elif direction == 3 and self.direction != 1:
            self.direction = direction
            new_head.x += -1
        else:
            if self.direction == 0:
                new_head.y += -1
            if self.direction == 1:
                new_head.x += 1
            if self.direction == 2:
                new_head.y += 1
            if self.direction == 3:
                new_head.x += -1
        self.add_head(new_head)


def pressed_key(keystroke, snake):
    if keystroke.key == pygame.K_UP:
        snake.move(0)
    if keystroke.key == pygame.K_RIGHT:
        snake.move(1)
    if keystroke.key == pygame.K_DOWN:
        snake.move(2)
    if keystroke.key == pygame.K_LEFT:
        snake.move(3)


def draw_snake(display, snake):
    pygame.draw.rect(display, color_snake_head, [snake.head.x * dim_square,
                                                 snake.head.y * dim_square,
                                                 dim_square,
                                                 dim_square])
    for body_part in snake.body:
        pygame.draw.rect(display, color_snake_body, [body_part.x * dim_square,
                                                     body_part.y * dim_square,
                                                     dim_square,
                                                     dim_square])


standard_snake = {'direction': 3,
                  'head': SnakeBodyPart(10, 10),
                  'body': Queue([SnakeBodyPart(10, 14),
                                 SnakeBodyPart(10, 13),
                                 SnakeBodyPart(10, 12),
                                 SnakeBodyPart(10, 11)])}

if __name__ == '__main__':
    # Variables
    dimensions = 400
    dim_square = 10

    # Colors
    color_snake_body = (0, 200, 0)
    color_snake_head = (0, 0, 255)
    color_food = (255, 0, 0)
    # Initialization
    # The snake
    snake1 = Snake(**standard_snake)

    # Pygame
    pygame.init()
    dis = pygame.display.set_mode((dimensions, dimensions))
    pygame.display.update()
    pygame.display.set_caption('Petters game')
    clock = pygame.time.Clock()

    game_over = False

    # Main game
    while not game_over:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                pressed_key(event, snake1)

            draw_snake(dis, snake1)
            pygame.display.update()
    pygame.quit()
    quit()
