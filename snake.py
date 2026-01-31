import pygame
import sys
import random

pygame.init()

# Grid settings
ROWS = 8
COLS = 8
LED_SIZE = 50
MARGIN = 5

# Colors
OFF_COLOR = (60, 60, 60)
ON_COLOR = (255, 255, 255)
BG_COLOR = (20, 20, 20)
APPLE_COLOR = (200, 0, 0)

# Screen
WIDTH = COLS * (LED_SIZE + MARGIN) + MARGIN
HEIGHT = ROWS * (LED_SIZE + MARGIN) + MARGIN
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8x8 Snake")

clock = pygame.time.Clock()

# Faces
SMILEY = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]

SAD = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]

# Game states
START = "start"
PLAYING = "playing"
GAME_OVER = "game_over"
state = START

MOVE_EVENT = pygame.USEREVENT
pygame.time.set_timer(MOVE_EVENT, 300)

def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * (LED_SIZE + MARGIN)
            y = MARGIN + r * (LED_SIZE + MARGIN)
            pygame.draw.rect(
                screen, OFF_COLOR,
                (x, y, LED_SIZE, LED_SIZE),
                border_radius=6
            )

def draw_pattern(pattern):
    draw_grid()
    for r in range(ROWS):
        for c in range(COLS):
            if pattern[r][c]:
                x = MARGIN + c * (LED_SIZE + MARGIN)
                y = MARGIN + r * (LED_SIZE + MARGIN)
                pygame.draw.rect(
                    screen, ON_COLOR,
                    (x, y, LED_SIZE, LED_SIZE),
                    border_radius=6
                )

def spawn_apple():
    empty = [(r, c) for r in range(ROWS) for c in range(COLS) if (r, c) not in snake]
    return random.choice(empty)

def reset_game():
    global snake, direction, state, apple, grow, direction_locked
    snake = [(4, 4), (4, 3), (4, 2)]
    direction = (0, 1)
    grow = 0
    apple = spawn_apple()
    state = PLAYING
    direction_locked = False  # New move allows direction change

running = True
direction_locked = False  # Only one direction change per move
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if state in (START, GAME_OVER):
                    reset_game()

            if state == PLAYING and not direction_locked:
                if event.key == pygame.K_LEFT and direction != (0, 1):
                    direction = (0, -1)
                    direction_locked = True
                elif event.key == pygame.K_RIGHT and direction != (0, -1):
                    direction = (0, 1)
                    direction_locked = True
                elif event.key == pygame.K_UP and direction != (1, 0):
                    direction = (-1, 0)
                    direction_locked = True
                elif event.key == pygame.K_DOWN and direction != (-1, 0):
                    direction = (1, 0)
                    direction_locked = True

        if event.type == MOVE_EVENT and state == PLAYING:
            head_r, head_c = snake[0]
            dr, dc = direction
            new_head = (head_r + dr, head_c + dc)

            # Edge collision
            if not (0 <= new_head[0] < ROWS and 0 <= new_head[1] < COLS):
                state = GAME_OVER
                continue

            # Self-collision
            if new_head in snake:
                state = GAME_OVER
                continue

            snake.insert(0, new_head)

            # Apple eaten
            if new_head == apple:
                grow += 1
                apple = spawn_apple()

            if grow > 0:
                grow -= 1
            else:
                snake.pop()

            direction_locked = False  # Unlock for next move

    screen.fill(BG_COLOR)

    if state == START:
        draw_pattern(SMILEY)

    elif state == GAME_OVER:
        draw_pattern(SAD)

    elif state == PLAYING:
        draw_grid()

        # Draw apple
        ar, ac = apple
        x = MARGIN + ac * (LED_SIZE + MARGIN)
        y = MARGIN + ar * (LED_SIZE + MARGIN)
        pygame.draw.rect(
            screen, APPLE_COLOR,
            (x, y, LED_SIZE, LED_SIZE),
            border_radius=6
        )

        # Draw snake
        for r, c in snake:
            x = MARGIN + c * (LED_SIZE + MARGIN)
            y = MARGIN + r * (LED_SIZE + MARGIN)
            pygame.draw.rect(
                screen, ON_COLOR,
                (x, y, LED_SIZE, LED_SIZE),
                border_radius=6
            )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
