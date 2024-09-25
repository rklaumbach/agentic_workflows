import os
import random
import time
import sys
import threading

# Constants
WIDTH = 20
HEIGHT = 10
SNAKE_CHAR = 'O'
FOOD_CHAR = '*'
EMPTY_CHAR = ' '

# Initialize game state
snake = [(5, 5)]
direction = (0, 1)
food = (random.randint(0, HEIGHT-1), random.randint(0, WIDTH-1))
score = 0
game_over = False
input_direction = None

def print_board():
    os.system('cls' if os.name == 'nt' else 'clear')
    board = [[EMPTY_CHAR for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for y, x in snake:
        board[y][x] = SNAKE_CHAR
    board[food[0]][food[1]] = FOOD_CHAR
    print('\n'.join(''.join(row) for row in board))
    print(f'Score: {score}')
    print("Use 'w', 'a', 's', 'd' to move")

def move_snake():
    global snake, food, score, game_over
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if (new_head in snake or
        new_head[0] < 0 or new_head[0] >= HEIGHT or
        new_head[1] < 0 or new_head[1] >= WIDTH):
        game_over = True
        return
    snake = [new_head] + snake
    if new_head == food:
        score += 1
        while True:
            food = (random.randint(0, HEIGHT-1), random.randint(0, WIDTH-1))
            if food not in snake:
                break
    else:
        snake.pop()

def change_direction(new_direction):
    global direction
    if (direction[0] + new_direction[0], direction[1] + new_direction[1]) != (0, 0):
        direction = new_direction

def get_input():
    global input_direction, game_over
    while not game_over:
        input_direction = input().strip().lower()

# Start input thread
input_thread = threading.Thread(target=get_input)
input_thread.daemon = True
input_thread.start()

# Game loop
while not game_over:
    print_board()
    time.sleep(0.1)
    
    if input_direction:
        if input_direction == 'w':
            change_direction((-1, 0))
        elif input_direction == 's':
            change_direction((1, 0))
        elif input_direction == 'a':
            change_direction((0, -1))
        elif input_direction == 'd':
            change_direction((0, 1))
        input_direction = None
    
    move_snake()

print("Game Over!")
