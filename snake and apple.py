import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Set up colors and font styles
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
bubble_color = (0, 255, 255)

# Set up the display
width = 600
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake & Apple')

# Fonts
font_style = pygame.font.SysFont("MS Gothic", 25)
title_font = pygame.font.SysFont("MS Gothic", 60)
score_font = pygame.font.SysFont("MS Gothic", 25)  # Courier font for score

# Set up the clock
clock = pygame.time.Clock()

# Snake settings
snake_block = 10
initial_speed = 15

# Load music
pygame.mixer.music.load(r"C:\Users\rahulrajpvr7d\Music\8-bit-retro-game-music-233964.mp3")  # Replace with your music file path
pygame.mixer.music.play(-1)

# Functions
def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        color = (0, 255 - (i * 10) % 255, 0)  # Gradient effect
        pygame.draw.rect(display, color, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3 + y_displace])

def main_menu():
    display.fill(blue)
    title_text = title_font.render("Snake Game", True, yellow)
    display.blit(title_text, [width / 3 - 50, height / 4])
    message("Press '1' for New Game", white, 50)
    message("Press '2' for Quit", white, 100)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Start New Game
                    waiting = False
                elif event.key == pygame.K_2:  # Quit
                    pygame.quit()
                    quit()

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

    # Food and obstacles
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
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

        # Snake wraps around the screen
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        x1 += x1_change
        y1 += y1_change
        display.fill(blue)
        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])

        for obs in obstacles:
            pygame.draw.rect(display, red, [obs[0], obs[1], snake_block, snake_block])
        
        if bubble:
            bubble_x, bubble_y = bubble
            pygame.draw.circle(display, bubble_color, (bubble_x, bubble_y), 20)
            bubble_time -= 1 / clock.get_fps()
            if bubble_time <= 0:
                bubble = None

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
        
        our_snake(snake_block, snake_list)
        score_display(score)

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 10

            if score % 50 == 0:
                bubble_x = round(random.randrange(20, width - 20) / 10.0) * 10.0
                bubble_y = round(random.randrange(20, height - 20) / 10.0) * 10.0
                bubble = (bubble_x, bubble_y)
                bubble_time = 5
        
        if bubble and snake_head[0] == bubble[0] and snake_head[1] == bubble[1]:
            score += 50
            bubble = None

        if bubble:
            bubble_timer_display(bubble_time)
        
        pygame.display.update()
        clock.tick(initial_speed)

    pygame.quit()
    quit()

# Start the game with the main menu
if __name__ == "__main__":
    while True:
        main_menu()
        gameLoop()
