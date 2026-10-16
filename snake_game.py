
import tkinter as tk
import random

CELL = 20
COLS = 30
ROWS = 25
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

BG = "#101820"
SNAKE_COLOR = "#39E75F"
FOOD_COLOR = "#FF4757"
TEXT_COLOR = "#FFFFFF"

root = tk.Tk()
root.title("Python Snake Game")
root.resizable(False, False)
root.configure(bg=BG)

score = 0
direction = "Right"
next_direction = "Right"
running = True
game_over = False

snake = [(8, 10), (7, 10), (6, 10)]
food = (15, 10)

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=12, pady=10)

title = tk.Label(
    header, text="🐍 SNAKE GAME",
    font=("Arial", 18, "bold"),
    fg=SNAKE_COLOR, bg=BG
)
title.pack(side="left")

score_label = tk.Label(
    header, text="Score: 0",
    font=("Arial", 13, "bold"),
    fg=TEXT_COLOR, bg=BG
)
score_label.pack(side="right")

canvas = tk.Canvas(
    root, width=WIDTH, height=HEIGHT,
    bg=BG, highlightthickness=0
)
canvas.pack(padx=10)

footer = tk.Label(
    root,
    text="Arrow keys: Move   |   P: Pause   |   R: Restart",
    font=("Arial", 10),
    fg=TEXT_COLOR, bg=BG
)
footer.pack(pady=10)

def place_food():
    global food
    empty = [
        (x, y)
        for x in range(COLS)
        for y in range(ROWS)
        if (x, y) not in snake
    ]
    if empty:
        food = random.choice(empty)
    else:
        finish_game("YOU WIN!")

def draw():
    canvas.delete("all")

    fx, fy = food
    canvas.create_oval(
        fx * CELL + 3, fy * CELL + 3,
        (fx + 1) * CELL - 3, (fy + 1) * CELL - 3,
        fill=FOOD_COLOR, outline=""
    )

    for i, (x, y) in enumerate(snake):
        color = "#8BFF9E" if i == 0 else SNAKE_COLOR
        canvas.create_rectangle(
            x * CELL + 1, y * CELL + 1,
            (x + 1) * CELL - 1, (y + 1) * CELL - 1,
            fill=color, outline=""
        )

    if game_over:
        canvas.create_rectangle(
            45, HEIGHT // 2 - 65,
            WIDTH - 45, HEIGHT // 2 + 65,
            fill="#202C38", outline=SNAKE_COLOR, width=2
        )
        canvas.create_text(
            WIDTH // 2, HEIGHT // 2 - 28,
            text=message,
            fill=FOOD_COLOR,
            font=("Arial", 23, "bold")
        )
        canvas.create_text(
            WIDTH // 2, HEIGHT // 2 + 15,
            text=f"Final score: {score}",
            fill=TEXT_COLOR,
            font=("Arial", 14)
        )
        canvas.create_text(
            WIDTH // 2, HEIGHT // 2 + 42,
            text="Press R to play again",
            fill=SNAKE_COLOR,
            font=("Arial", 11)
        )

def finish_game(reason="GAME OVER"):
    global running, game_over, message
    running = False
    game_over = True
    message = reason
    draw()

def change_direction(new_direction):
    global next_direction
    opposites = {
        "Up": "Down",
        "Down": "Up",
        "Left": "Right",
        "Right": "Left"
    }
    if new_direction != opposites.get(direction):
        next_direction = new_direction

def on_key(event):
    global running, direction, next_direction

    key = event.keysym

    if key in ("Up", "Down", "Left", "Right"):
        change_direction(key)

    elif key.lower() == "r":
        restart()

    elif key.lower() == "p" and not game_over:
        running = not running
        if running:
            direction = next_direction
            tick()
        else:
            canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                text="PAUSED",
                fill=TEXT_COLOR,
                font=("Arial", 24, "bold")
            )

def tick():
    global snake, direction, score, running

    if not running or game_over:
        return

    direction = next_direction
    x, y = snake[0]

    if direction == "Up":
        y -= 1
    elif direction == "Down":
        y += 1
    elif direction == "Left":
        x -= 1
    else:
        x += 1

    new_head = (x, y)
    eating = new_head == food
    body_to_check = snake if eating else snake[:-1]

    if (
        x < 0 or x >= COLS
        or y < 0 or y >= ROWS
        or new_head in body_to_check
    ):
        finish_game()
        return

    snake.insert(0, new_head)

    if eating:
        score += 1
        score_label.config(text=f"Score: {score}")
        place_food()
        if game_over:
            draw()
            return
    else:
        snake.pop()

    draw()

    delay = max(65, 130 - score * 2)
    root.after(delay, tick)

def restart():
    global snake, food, score, direction
    global next_direction, running, game_over

    snake = [(8, 10), (7, 10), (6, 10)]
    direction = "Right"
    next_direction = "Right"
    score = 0
    running = True
    game_over = False
    score_label.config(text="Score: 0")
    place_food()
    draw()
    tick()

root.bind("<KeyPress>", on_key)

draw()
tick()
root.mainloop()
