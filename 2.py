import pygame
import random

pygame.init()

width = 800
height = 800

screen = pygame.display.set_mode((width, height))

# Variables and their initialization
score = 0
level = 1
fruit_eaten = False
speed = 200  # Initial speed
snake_length = 4  
speed_increase_threshold = 30

# Function to generate random food position
def generate_food(squares):
    while True:
        fr_x = random.randrange(1, width // 10) * 10
        fr_y = random.randrange(1, height // 10) * 10
        if [fr_x, fr_y] not in squares:  # Ensure food does not spawn on the snake
            return [fr_x, fr_y]

fruit_coor = generate_food([])  # Generate initial food position
head_square = [100, 100]

squares = [
    [60, 100],
    [70, 100],
    [80, 100],
    [90, 100]
]

direction = "right"
next_dir = "right"

done = False

def game_over(font, size, color):
    global done
    g_o_font = pygame.font.SysFont(font, size)
    g_o_surface = g_o_font.render("Game Over, your score: " + str(score), True, color)
    g_o_rect = g_o_surface.get_rect(center=(width // 2, height // 2))

    screen.blit(g_o_surface, g_o_rect)
    pygame.display.update()

    pygame.time.delay(4000)
    pygame.quit()

# Start of gameplay loop
while not done:
    # Gameplay event conditions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                next_dir = "down"
            if event.key == pygame.K_UP:
                next_dir = "up"
            if event.key == pygame.K_LEFT:
                next_dir = "left"
            if event.key == pygame.K_RIGHT:
                next_dir = "right"

    # Check for collisions with the snake itself
    for square in squares[:-1]:
        if head_square[0] == square[0] and head_square[1] == square[1]:
            game_over("times new roman", 45, (128, 128, 128))

    # Check for border collisions
    if head_square[0] >= width or head_square[1] >= height or head_square[0] < 0 or head_square[1] < 0:
        game_over("times new roman", 45, (128, 128, 128))

    # Scene logic
    if next_dir == "right" and direction != "left":
        direction = "right"
    if next_dir == "up" and direction != "down":
        direction = "up"
    if next_dir == "left" and direction != "right":
        direction = "left"
    if next_dir == "down" and direction != "up":
        direction = "down"

    if direction == "right":
        head_square[0] += 10
    if direction == "left":
        head_square[0] -= 10
    if direction == "up":
        head_square[1] -= 10
    if direction == "down":
        head_square[1] += 10

    # Add new segment only if fruit is eaten
    if head_square[0] == fruit_coor[0] and head_square[1] == fruit_coor[1]:
        fruit_eaten = True
        score += 10
        # Increase the length of the snake
        snake_length += 1

    # Update the snake's body
    if fruit_eaten:
        fruit_coor = generate_food(squares)  # Generate new food position
        fruit_eaten = False
    else:
        # Remove the last segment if fruit is not eaten
        squares.pop(0)

    # Add the new head position
    squares.append([head_square[0], head_square[1]])

    # Check if the snake's length exceeds the fixed length
    if len(squares) > snake_length:
        squares = squares[-snake_length:]  

    #Speed up logic
    if score // speed_increase_threshold > level - 1:  # Increase speed every 30 points
        level += 1
        speed = max(50, speed - 20)  # Increase speed, but not below 50ms

    # Drawing section
    screen.fill((0, 0, 0))

    score_font = pygame.font.SysFont("times new roman", 20)
    score_surface = score_font.render("Score: " + str(score) + " Level: " + str(level), True, (128, 128, 128))
    score_rect = score_surface.get_rect()

    screen.blit(score_surface, score_rect)

    if not fruit_eaten:
        pygame.draw.circle(screen, (0, 255, 0), (fruit_coor[0] + 5, fruit_coor[1] + 5), 5)

    for el in squares:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))

    pygame.display.flip()
    pygame.time.delay(speed)  # Use the speed variable for delay

pygame.quit()