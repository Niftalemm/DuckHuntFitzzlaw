import pygame
import sys
import math
import json
import random
from trialGenerator import createTrials

# trial_array.py content (for testing)
# trials = [
#     ['L', 's', 'm'],
#     ['R', 'm', 'l'],
#     ['L', 'l', 's'],
#     ['R', 's', 's'],
#     ['L', 'm', 'm'],
#     ['R', 'l', 'l'],
#     ['L', 's', 'l'],
#     ['R', 'm', 's'],
#     ['L', 'l', 'm'],
#     ['R', 's', 'm']
# ]

trials = createTrials()  # Generate trials using the trial generator

# Mapping definitions – adjust these pixel values to suit your game design
DISTANCE_MAP = {'S': 150, 'M': 250, 'L': 350}  # distance from center in pixels
SIZE_MAP = {'S': 20, 'M': 40, 'L': 60}          # target radius in pixels

# Screen dimensions and colors
WIDTH, HEIGHT = 1920, 1080
CENTER = (WIDTH // 2, HEIGHT // 2)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GRAY  = (200, 200, 200)

def draw_button(screen, text, rect, font):
    """Draws a rectangular button with centered text on the given screen."""
    pygame.draw.rect(screen, GRAY, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect

def run_trial(screen, trial, font):
    """
    Runs a single trial.
    
    trial: a list in the format [side, distance_code, size_code]
    Determines target position, starts the timer, and counts misses.
    
    Returns:
    - reaction_time (in ms)
    - misses (number of incorrect clicks before a hit)
    """
    side = trial[0]
    distance_code = trial[1]
    size_code = trial[2]
    distance = DISTANCE_MAP.get(distance_code, 100)
    radius = SIZE_MAP.get(size_code, 20)
    
    # Calculate the target's position based on side (left or right).
    if side.upper() == 'L':
        target_x = CENTER[0] - distance
    else:
        target_x = CENTER[0] + distance
    target_y = CENTER[1]
    target_pos = (target_x, target_y)
    
    # Display the target on the screen.
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, target_pos, radius)
    pygame.display.flip()
    
    misses = 0
    trial_start = pygame.time.get_ticks()  # start timer when target appears
    reaction_time = None

    while reaction_time is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                # Calculate the distance from the click to the target center.
                dx = click_pos[0] - target_x
                dy = click_pos[1] - target_y
                click_distance = math.sqrt(dx**2 + dy**2)
                if click_distance <= radius:
                    # If within the target, record the reaction time.
                    reaction_time = pygame.time.get_ticks() - trial_start
                else:
                    # If the click is a miss, increment the miss counter.
                    misses += 1
        pygame.time.delay(10)
        
    return reaction_time, misses

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fitts's Law Game")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Display the initial start screen with a "Start" button.
    start_button = pygame.Rect(0, 0, 150, 50)
    start_button.center = CENTER
    screen.fill(WHITE)
    draw_button(screen, "Start", start_button, font)
    pygame.display.flip()

    waiting_to_start = True
    while waiting_to_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting_to_start = False
        clock.tick(60)

    # Process each trial and update the trial data with reaction time and misses.
    for trial in trials:
        reaction_time, misses = run_trial(screen, trial, font)
        # Append reaction time and misses to the current trial element.
        trial.append(reaction_time)
        trial.append(misses)
        
        # Display the "Next" button in the center after each trial.
        next_button = pygame.Rect(0, 0, 150, 50)
        next_button.center = CENTER
        screen.fill(WHITE)
        draw_button(screen, "Next", next_button, font)
        pygame.display.flip()
        
        waiting_for_next = True
        while waiting_for_next:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if next_button.collidepoint(event.pos):
                        waiting_for_next = False
            clock.tick(60)
            
    # At the end, print out the updated trials list to the console.
    print("Updated trials (side, distance, size, reaction_time, misses):")
    for trial in trials:
        print(trial)

    # Display an exit screen with an "Exit" button.
    exit_button = pygame.Rect(0, 0, 150, 50)
    exit_button.center = (CENTER[0], CENTER[1] + 50)  # position below the game over text

    while True:
        screen.fill(WHITE)
        # Display game over message.
        end_text = font.render("Game Over", True, BLACK)
        end_rect = end_text.get_rect(center=(CENTER[0], CENTER[1] - 50))
        screen.blit(end_text, end_rect)
        
        # Draw the exit button.
        draw_button(screen, "Exit", exit_button, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save the results to a JSON file when quitting.
                with open('trial_results.json', 'w') as f:
                    json.dump(trials, f)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    # Save the results to a JSON file and exit.
                    with open('trial_results.json', 'w') as f:
                        json.dump(trials, f)
                    pygame.quit()
                    sys.exit()
        clock.tick(60)

if __name__ == "__main__":
    main()
