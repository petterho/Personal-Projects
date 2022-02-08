import turtle as t


def create_sequence(iterations):
    sequence = ['x']
    new_sequence = []

    x = ('y', '+', 'x', '+', 'y')
    y = ('x', '-', 'y', '-', 'x')

    for i in range(iterations):
        for command in sequence:
            if command == 'x':
                new_sequence.extend(x)
            elif command == 'y':
                new_sequence.extend(y)
            elif command == '+':
                new_sequence.append('+')
            elif command == '-':
                new_sequence.append('-')
            else:
                raise TypeError(f"Your command {command} is not valid. The "
                                f"valid types are 'x', 'y', '+', '-'.")
        sequence = new_sequence
        new_sequence = []
        print(sequence)

    for command in sequence:
        if command == '+':
            new_sequence.append('right')
        if command == '-':
            new_sequence.append('left')

    return new_sequence


def turtle_sequence(sequence):
    turtle = t.Turtle()
    turtle.hideturtle()
    turtle.speed(0)
    t.Screen().screensize(3000, 3000)
    angle = 60
    distance = 2

    turtle.forward(distance)
    for command in sequence:
        if command == 'right':
            turtle.right(angle)
        if command == 'left':
            turtle.left(angle)
        turtle.forward(distance)
    t.done()


if __name__ == '__main__':
    sequence_ = create_sequence(9)
    print(sequence_)
    turtle_sequence(sequence_)



