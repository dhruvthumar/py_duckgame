import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Duck Shooter Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
duck_image = pygame.image.load('duck.png')
crosshair_image = pygame.image.load('crosshair.png')

# Resize images
duck_image = pygame.transform.scale(duck_image, (100, 100))
crosshair_image = pygame.transform.scale(crosshair_image, (50, 50))

# Game variables
duck_speed = 3
ducks = [{'x': random.randint(0, SCREEN_WIDTH - 100), 'y': random.randint(0, SCREEN_HEIGHT - 100), 'speed': duck_speed}]
score = 0
streak = 0
font = pygame.font.SysFont(None, 55)

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Function to display streak
def display_streak(streak):
    streak_text = font.render(f"Streak: {streak}", True, BLACK)
    screen.blit(streak_text, (10, 60))

# Function to add a new duck
def add_duck():
    duck = {'x': random.randint(0, SCREEN_WIDTH - 100), 'y': random.randint(0, SCREEN_HEIGHT - 100), 'speed': duck_speed}
    ducks.append(duck)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Get mouse position and update crosshair
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(crosshair_image, (mouse_x - 25, mouse_y - 25))

    # Move and draw ducks
    for duck in ducks:
        duck['x'] += duck['speed']
        if duck['x'] > SCREEN_WIDTH or duck['x'] < 0:
            duck['speed'] = -duck['speed']
            duck['y'] = random.randint(0, SCREEN_HEIGHT - 100)

        # Draw duck
        screen.blit(duck_image, (duck['x'], duck['y']))

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for duck in ducks:
                if duck['x'] < mouse_x < duck['x'] + 100 and duck['y'] < mouse_y < duck['y'] + 100:
                    score += 1
                    streak += 1
                    duck['x'] = random.randint(0, SCREEN_WIDTH - 100)
                    duck['y'] = random.randint(0, SCREEN_HEIGHT - 100)

                    # Check for streak of 3
                    if streak % 3 == 0:
                        add_duck()

    # Display score and streak
    display_score(score)
    display_streak(streak)

    # Update the display
    pygame.display.update()

    # FPS
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()