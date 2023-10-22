import os
import sys
import pygame
import random

pygame.init()
pygame.font.init()
CLOCK = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

HEADER_SIZE = (500, 50)
WINDOW_SIZE = (500, 550)

FONT = pygame.font.SysFont('arial', 32)

PATH = r'C:\Users\William Geyer\source\repos\snake_game'


class Orientation:
    VERTICAL = 0
    HORIZONTAL = 1


class Moving:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Square:
    def __init__(self, x=None, y=None, food=False):
        self.x = x
        self.y = y
        if not food:
            self.img = pygame.image.load(os.path.join(PATH, 'imgs', 'square.png')).convert()
        else:
            self.img = pygame.image.load(os.path.join(PATH, 'imgs', 'food.png')).convert()
        self.length = self.img.get_size()[0]


class Snake:
    def __init__(self):
        self.body = []
        self.head_path = []
        self.head_x = 250
        self.head_y = 250
        self.head_path.append((self.head_x, self.head_y))
        self.head = Square()
        self.score = 0

    def update_position(self, new_x, new_y):
        # if snake head inbounds, update position
        if new_x >= 0 and new_x <= WINDOW_SIZE[0] - self.head.length:
            self.head_x = new_x
        if new_y >= HEADER_SIZE[1] and new_y <= WINDOW_SIZE[1] - self.head.length:
            self.head_y = new_y

        # if snake head goes outabounds, end game
        if new_x < 0 or new_x > WINDOW_SIZE[0] - self.head.length or new_y < HEADER_SIZE[1] or new_y > WINDOW_SIZE[
            1] - self.head.length:
            end_game(self.score)


class Food:
    def __init__(self):
        self.square = Square(food=True)
        self.x = random.randrange(0, WINDOW_SIZE[0], self.square.length)
        self.y = random.randrange(HEADER_SIZE[1], WINDOW_SIZE[1], self.square.length)


class GridLine:
    def __init__(self, orientation):

        # Create dict of each grid square. If value of key is 1, the grid square contains a piece of the snake.
        self.grid = {}
        for x in range(0, WINDOW_SIZE[0], 10):
            for y in range(HEADER_SIZE[1], WINDOW_SIZE[1], 10):
                self.grid[str((x, y))] = 0

        if orientation == Orientation.VERTICAL:
            self.img = pygame.image.load(os.path.join(PATH, 'imgs', 'vertical_grid_line.png'))
        else:
            self.img = pygame.image.load(os.path.join(PATH, 'imgs', 'horizontal_grid_line.png'))


def setup_game_window():
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Snake')
    window.fill(WHITE)

    return window


def end_game(score):
    print(f"Final Score: {score}")
    pygame.quit()
    sys.exit()


def play_snake():
    window = setup_game_window()
    score_txt = FONT.render('Score: ', True, BLACK)

    snake = Snake()
    food = Food()

    running = True
    moving_direction = None
    prev_moving_direction = None
    while running:
        CLOCK.tick(10)  # Frame rate

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Determine moving direction based off pressed key (arrow keys or WASD)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    moving_direction = Moving.LEFT
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    moving_direction = Moving.RIGHT
                if event.key == pygame.K_UP or event.key == ord('w'):
                    moving_direction = Moving.UP
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    moving_direction = Moving.DOWN

            # Quit when 'q' is pressed
            if event.type == pygame.KEYUP:
                if event.key == ord('q'):
                    end_game(snake.score)

        # Update position of snake head
        new_x = snake.head_x
        new_y = snake.head_y
        if moving_direction == Moving.LEFT:
            if prev_moving_direction != Moving.RIGHT:
                prev_moving_direction = moving_direction
                new_x -= snake.head.length
                snake.update_position(new_x, snake.head_y)
            else:
                new_x += snake.head.length
                snake.update_position(new_x, snake.head_y)
        elif moving_direction == Moving.RIGHT:
            if prev_moving_direction != Moving.LEFT:
                prev_moving_direction = moving_direction
                new_x += snake.head.length
                snake.update_position(new_x, snake.head_y)
            else:
                new_x -= snake.head.length
                snake.update_position(new_x, snake.head_y)
        elif moving_direction == Moving.UP:
            if prev_moving_direction != Moving.DOWN:
                prev_moving_direction = moving_direction
                new_y -= snake.head.length
                snake.update_position(snake.head_x, new_y)
            else:
                new_y += snake.head.length
                snake.update_position(snake.head_x, new_y)
        elif moving_direction == Moving.DOWN:
            if prev_moving_direction != Moving.UP:
                prev_moving_direction = moving_direction
                new_y += snake.head.length
                snake.update_position(snake.head_x, new_y)
            else:
                new_y -= snake.head.length
                snake.update_position(snake.head_x, new_y)

        # Append new positions to head path
        if snake.head_path[-1] != (snake.head_x, snake.head_y):
            snake.head_path.append((snake.head_x, snake.head_y))

        window.fill(WHITE)
        window.blit(snake.head.img, (snake.head_x, snake.head_y))
        window.blit(food.square.img, (food.x, food.y))

        for x in range(0, WINDOW_SIZE[0] + 1, snake.head.length):
            window.blit(GridLine(Orientation.VERTICAL).img, (x, HEADER_SIZE[1]))

        for y in range(HEADER_SIZE[1], WINDOW_SIZE[1] + 1, snake.head.length):
            window.blit(GridLine(Orientation.HORIZONTAL).img, (0, y))

        # If we don't score continue, else grow the snake and increment the score
        if (snake.head_x, snake.head_y) != (food.x, food.y):
            window.blit(food.square.img, (food.x, food.y))
        else:
            food = Food()
            snake.body.append(Square())
            window.blit(food.square.img, (food.x, food.y))
            snake.score += 1

        # Load score
        window.blit(score_txt, (0, 0))
        score_var = FONT.render(str(snake.score), True, BLACK)
        window.blit(score_var, (100, 0))

        # Load body
        for idx, body in enumerate(snake.body):
            # print(f"{idx}. {snake.head_path[-(idx+1)]}")
            window.blit(body.img, snake.head_path[-(idx + 2)])
            body.x, body.y = snake.head_path[-(idx + 2)]

        # If head touched body, end game
        for idx, body in enumerate(snake.body):
            if (snake.head_x, snake.head_y) == (body.x, body.y):
                end_game(snake.score)

        pygame.display.update()


if __name__ == '__main__':
    play_snake()
