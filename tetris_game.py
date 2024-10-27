import pygame
import random

# Initialize the game
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Game variables
grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
current_shape = random.choice(SHAPES)
current_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2
current_y = 0
game_over = False
score = 0

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock
clock = pygame.time.Clock()

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_shape(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, WHITE, ((offset_x + x) * BLOCK_SIZE, (offset_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def check_collision(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if y + offset_y >= len(grid) or x + offset_x >= len(grid[0]) or x + offset_x < 0 or grid[y + offset_y][x + offset_x]:
                    return True
    return False

def merge_shape(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + offset_y][x + offset_x] = 1

def clear_lines():
    global grid, score
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = len(grid) - len(new_grid)
    score += lines_cleared
    grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(lines_cleared)] + new_grid

def display_result():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(current_shape, current_x - 1, current_y):
                    current_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(current_shape, current_x + 1, current_y):
                    current_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(current_shape, current_x, current_y + 1):
                    current_y += 1
            elif event.key == pygame.K_UP:
                rotated_shape = list(zip(*current_shape[::-1]))
                if not check_collision(rotated_shape, current_x, current_y):
                    current_shape = rotated_shape

    if not check_collision(current_shape, current_x, current_y + 1):
        current_y += 1
    else:
        merge_shape(current_shape, current_x, current_y)
        clear_lines()
        current_shape = random.choice(SHAPES)
        current_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2
        current_y = 0
        if check_collision(current_shape, current_x, current_y):
            game_over = True

    screen.fill(BLACK)
    draw_grid()
    draw_shape(current_shape, current_x, current_y)
    pygame.display.flip()
    clock.tick(10)

display_result()
pygame.quit()
