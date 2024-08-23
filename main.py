import tkinter as tk
import random

# Game configuration
LIVES = 5
SCORE_PER_EGG = 250
WINDOW_WIDTH = 700  # Increased the window size width
WINDOW_HEIGHT = 700  # Increased the window size height

# Original sizes of the egg and basket
EGG_WIDTH_ORIGINAL = 100
EGG_HEIGHT_ORIGINAL = 150
BASKET_WIDTH_ORIGINAL = 200
BASKET_HEIGHT_ORIGINAL = 100

# New sizes (10% smaller)
EGG_WIDTH = int(EGG_WIDTH_ORIGINAL * 0.9)
EGG_HEIGHT = int(EGG_HEIGHT_ORIGINAL * 0.9)
BASKET_WIDTH = int(BASKET_WIDTH_ORIGINAL * 0.9)
BASKET_HEIGHT = int(BASKET_HEIGHT_ORIGINAL * 0.9)

# Initialize the main window
root = tk.Tk()
root.title("Catch the Egg Game")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg="lightblue")

# Initialize variables
lives = LIVES
score = 0

# Create a canvas for the game
canvas = tk.Canvas(root, width=WINDOW_WIDTH - 200, height=WINDOW_HEIGHT - 100, bg="lightgreen")
canvas.pack(side=tk.LEFT)

# Create a frame for the score and lives display
info_frame = tk.Frame(root, width=200, height=WINDOW_HEIGHT, bg="lightblue")
info_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Create a score label
score_label = tk.Label(info_frame, text=f"Score: {score}", font=("Arial", 16), bg="lightblue")
score_label.pack(pady=10)

# Create a lives label
lives_label = tk.Label(info_frame, text=f"Lives: {lives}", font=("Arial", 16), bg="lightblue")
lives_label.pack(pady=10)

# Load the egg and basket images
egg_image = tk.PhotoImage(file="egg.png").subsample(10, 10)  # Make the egg image 10% of the original size
basket_image = tk.PhotoImage(file="basket.png").subsample(10, 10)  # Make the basket image 10% of the original size

# Create the basket object
basket = canvas.create_image(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT - 200, image=basket_image)

# List to keep track of all eggs
eggs = []

def create_egg():
    """Create a new egg at a random position."""
    x = random.randint(50, WINDOW_WIDTH - 250)
    y = 50
    egg = canvas.create_image(x, y, image=egg_image)
    eggs.append(egg)

def drop_eggs():
    global score, lives

    for egg in eggs:
        # Move the egg down
        canvas.move(egg, 0, 10)

        # Get the egg's position
        egg_x, egg_y = canvas.coords(egg)

        # Get the basket's position
        basket_x, basket_y = canvas.coords(basket)

        # Check if the egg is off the screen
        if egg_y > (WINDOW_HEIGHT - 150):
            lives -= 1
            lives_label.config(text=f"Lives: {lives}")
            canvas.delete(egg)  # Remove the egg from the canvas
            eggs.remove(egg)  # Remove the egg from the list
            create_egg()  # Create a new egg

            if lives <= 0:
                game_over()

        # Check if the egg is caught
        elif (basket_x - BASKET_WIDTH / 2 < egg_x < basket_x + BASKET_WIDTH / 2) and (
                basket_y - BASKET_HEIGHT / 2 < egg_y < basket_y + BASKET_HEIGHT / 2):
            score += SCORE_PER_EGG
            score_label.config(text=f"Score: {score}")
            canvas.delete(egg)  # Remove the egg from the canvas
            eggs.remove(egg)  # Remove the egg from the list
            create_egg()  # Create a new egg

            # Add more eggs if the score reaches 1500
            if score >= 1500 and len(eggs) == 0:
                for _ in range(3):  # Add 3 eggs when score is 1500
                    create_egg()

    # Increase falling speed based on the score
    speed = max(100 - score // 50, 10)  # Minimum speed of 10 ms
    root.after(speed, drop_eggs)  # Repeat the drop_eggs function

def game_over():
    canvas.create_text(WINDOW_WIDTH / 2 - 100, (WINDOW_HEIGHT - 150) / 2, text="Game Over!", font=("Arial", 24),
                       fill="red")
    root.after(2000, root.quit)  # Close the game after 2 seconds

# Move the basket with mouse
def move_basket(event):
    basket_x = event.x
    if 100 < basket_x < WINDOW_WIDTH - 100:
        canvas.coords(basket, basket_x, WINDOW_HEIGHT - 200)

root.bind("<Motion>", move_basket)

# Start the game loop
for _ in range(1):  # Initial egg
    create_egg()

drop_eggs()

# Run the main loop
root.mainloop()
