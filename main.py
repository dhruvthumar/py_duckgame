import pygame
import random
import sys
import time

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

# Load images
duck_image = pygame.image.load('duck.png')
crosshair_image = pygame.image.load('crosshair.png')
golden_duck_image = pygame.image.load('golden_duck.png')  # Placeholder for golden duck
powerup_image = pygame.image.load('powerup.png')  # Placeholder for power-up

# Resize images
duck_image = pygame.transform.scale(duck_image, (100, 100))
crosshair_image = pygame.transform.scale(crosshair_image, (50, 50))
golden_duck_image = pygame.transform.scale(golden_duck_image, (100, 100))
powerup_image = pygame.transform.scale(powerup_image, (50, 50))

# Load sounds
shoot_sound = pygame.mixer.Sound('shoot.mp3')
hit_sound = pygame.mixer.Sound('hit.mp3')
powerup_sound = pygame.mixer.Sound('powerup.mp3')

# Background music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-6)  # Loop background music

# Game variables
duck_speed = 3
ducks = [{'x': random.randint(0, SCREEN_WIDTH - 100), 'y': random.randint(0, SCREEN_HEIGHT - 100), 'speed': duck_speed, 'image': duck_image, 'points': 1}]
score = 0
streak = 0
lives = 3
powerup_active = False
powerup_duration = 5
powerup_time = 0
powerup_x, powerup_y = -100, -100  # Initialize off-screen to avoid immediate power-up placement

# Timer
time_limit = 60  # seconds
start_time = time.time()

# Font settings
font = pygame.font.SysFont(None, 40)

# High score tracking
try:
    with open('high_score.txt', 'r') as file:
        high_score = int(file.read())
except:
    high_score = 0

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Function to display streak
def display_streak(streak):
    streak_text = font.render(f"Streak: {streak}", True, BLACK)
    screen.blit(streak_text, (10, 50))

# Function to display lives
def display_lives(lives):
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(lives_text, (10, 90))

# Function to display timer
def display_timer(remaining_time):
    timer_text = font.render(f"Time: {remaining_time}", True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))

# Function to display high score
def display_high_score(high_score):
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (SCREEN_WIDTH - 300, 50))

# Function to add a new duck
def add_duck():
    duck_type = random.choice([{'image': duck_image, 'speed': 3, 'points': 1},
                               {'image': golden_duck_image, 'speed': 5, 'points': 5}])
    ducks.append({'x': random.randint(0, SCREEN_WIDTH - 100), 'y': random.randint(0, SCREEN_HEIGHT - 100), 'speed': duck_type['speed'], 'image': duck_type['image'], 'points': duck_type['points']})

# Game loop
running = True
while running:
    screen.fill(WHITE)  # Clear the screen each frame
    
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
        screen.blit(duck['image'], (duck['x'], duck['y']))

    # Spawn power-up occasionally
    if random.randint(1, 500) == 1 and not powerup_active:  # Random chance to spawn a power-up
        powerup_x = random.randint(0, SCREEN_WIDTH - 50)
        powerup_y = random.randint(0, SCREEN_HEIGHT - 50)
        screen.blit(powerup_image, (powerup_x, powerup_y))

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.Sound.play(shoot_sound)  # Play shooting sound
            hit = False
            for duck in ducks:
                if duck['x'] < mouse_x < duck['x'] + 100 and duck['y'] < mouse_y < duck['y'] + 100:
                    hit = True
                    pygame.mixer.Sound.play(hit_sound)  # Play hit sound
                    score += duck['points']
                    streak += 1
                    duck['x'] = random.randint(0, SCREEN_WIDTH - 100)
                    duck['y'] = random.randint(0, SCREEN_HEIGHT - 100)

                    # Check for streak of 3
                    if streak % 3 == 0:
                        add_duck()
            if not hit:
                lives -= 1

            # Check if player hits a power-up
            if powerup_x < mouse_x < powerup_x + 50 and powerup_y < mouse_y < powerup_y + 50:
                pygame.mixer.Sound.play(powerup_sound)  # Play power-up sound
                powerup_active = True
                powerup_time = time.time()

    # Apply power-up effect (slow motion)
    if powerup_active:
        if time.time() - powerup_time <= powerup_duration:
            game_speed = 0.5  # Slow down the game
        else:
            powerup_active = False
            game_speed = 1  # Reset speed

    # Timer logic
    remaining_time = int(time_limit - (time.time() - start_time))
    if remaining_time <= 0:
        running = False  # End game if time runs out

    # End game if no lives left
    if lives <= 0:
        running = False

    # Display score, streak, lives, timer, and high score
    display_score(score)
    display_streak(streak)
    display_lives(lives)
    display_timer(remaining_time)
    display_high_score(high_score)

    # Update the display
    pygame.display.update()

    # FPS control (game speed)
    pygame.time.Clock().tick(60)

# Game Over: Update high score if needed
if score > high_score:
    high_score = score
    with open('high_score.txt', 'w') as file:
        file.write(str(high_score))

# Show final score and high score
screen.fill(WHITE)
game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
pygame.display.update()

# Pause before exiting
pygame.time.wait(3000)

# Quit Pygame
pygame.quit()
sys.exit()
