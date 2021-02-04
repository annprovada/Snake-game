import pygame
import sys
import random

pygame.init()

SIZE_WINDOW = [500, 500]
SIZE_BLOCK = 20
COUNT_BLOCKS = 20
MARGIN = 1
HEADER_MARGIN = 90
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        HEADER_MARGIN + SIZE_BLOCK * COUNT_BLOCKS + SIZE_BLOCK + MARGIN * COUNT_BLOCKS]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('verdana', 25)

screen_color = (56, 119, 28)
frame_color = (67, 140, 35)
dark_green = (147, 211, 35)
light_green = (155, 219, 47)
snake_color = (61, 125, 251)
red = (255, 50, 1)
white = (255, 255, 255)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def get_random_empty_block():
    x = random.randint(0, COUNT_BLOCKS - 1)
    y = random.randint(0, COUNT_BLOCKS - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake:
        empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
        empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
    return empty_block


def draw_blocks(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])


snake = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
apple = get_random_empty_block()
d_row = 0
d_column = 1
total = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and d_column != 0:
                d_row = -1
                d_column = 0
            elif event.key == pygame.K_DOWN and d_column != 0:
                d_row = 1
                d_column = 0
            elif event.key == pygame.K_LEFT and d_row != 0:
                d_row = 0
                d_column = -1
            elif event.key == pygame.K_RIGHT and d_row != 0:
                d_row = 0
                d_column = 1
    screen.fill(screen_color)
    pygame.draw.rect(screen, frame_color, [0, HEADER_MARGIN - SIZE_BLOCK, size[0], size[1]])

    text_total = courier.render(f'Total: {total}', 0, white)
    screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))

    for row in range(COUNT_BLOCKS):
        for column in range(COUNT_BLOCKS):
            if (row + column) % 2 == 0:
                color = light_green
            else:
                color = dark_green
            draw_blocks(color, row, column)

    head = snake[-1]
    if not head.is_inside():
        print('crash')
        pygame.quit()
        sys.exit()

    draw_blocks(red, apple.x, apple.y)
    for block in snake:
        draw_blocks(snake_color, block.x, block.y)

    if apple == head:
        total += 1
        snake.append(apple)
        apple = get_random_empty_block()

    new_head = SnakeBlock(head.x + d_row, head.y + d_column)
    snake.append(new_head)
    snake.pop(0)

    pygame.display.flip()
    timer.tick(4)
