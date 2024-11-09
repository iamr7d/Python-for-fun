import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Set up colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
snake_color = (0, 200, 0)  # Customize snake color
bubble_color = (0, 255, 255)  # Color of the bonus bubble

# Set up the display
width = 600
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game with Obstacles and Bonuses')

# Set up the clock
clock = pygame.time.Clock()

snake_block = 10
initial_speed = 15

# Set up the font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load music
pygame.mixer.music.load(r"C:\Users\rahulrajpvr7d\Music\8-bit-retro-game-music-233964.mp3")  # Replace with your music file path
pygame.mixer.music.play(-1)  # Loop the music

def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        color = (0, 255 - (i * 10) % 255, 0)  # Gradient effect for the snake
        pygame.draw.rect(display, color, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])

def score_display(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    display.blit(value, [0, 0])

def bubble_timer_display(time_left):
    timer_msg = score_font.render("Bubble Time: " + str(int(time_left)), True, yellow)
    display.blit(timer_msg, [width - 200, 0])

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0

    # Food position
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Create obstacles
    obstacles = [(round(random.randrange(0, width - snake_block) / 10.0) * 10.0,
                   round(random.randrange(0, height - snake_block) / 10.0) * 10.0) for _ in range(5)]

    # Bubble setup
    bubble = None
    bubble_time = 0

    while not game_over:

        while game_close:
            display.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            score_display(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Check boundaries
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        display.fill(blue)  # Background color
        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])

        # Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(display, red, [obs[0], obs[1], snake_block, snake_block])
        
        # Draw bubble
        if bubble:
            bubble_x, bubble_y = bubble
            pygame.draw.circle(display, bubble_color, (bubble_x, bubble_y), 20)  # Bubble radius 20

            # Check bubble timer
            bubble_time -= 1 / clock.get_fps()
            if bubble_time <= 0:
                bubble = None

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:  # Check collision with itself
                game_close = True
        
        our_snake(snake_block, snake_list)
        score_display(score)
        
        # Check if the snake has eaten the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 10  # Increase score
            
            # Create a bubble every 5 food items eaten
            if score % 50 == 0:
                bubble_x = round(random.randrange(20, width - 20) / 10.0) * 10.0
                bubble_y = round(random.randrange(20, height - 20) / 10.0) * 10.0
                bubble = (bubble_x, bubble_y)
                bubble_time = 5  # Bubble lasts for 5 seconds
        
        # Check if the snake has eaten the bubble
        if bubble and snake_head[0] == bubble[0] and snake_head[1] == bubble[1]:
            score += 50  # Increase score for collecting bubble
            bubble = None  # Remove bubble after collection
        
        # Display bubble timer
        if bubble:
            bubble_timer_display(bubble_time)
        
        pygame.display.update()
        clock.tick(initial_speed)

    pygame.quit()
    quit()

# Start the game
if __name__ == "__main__":
    gameLoop()
