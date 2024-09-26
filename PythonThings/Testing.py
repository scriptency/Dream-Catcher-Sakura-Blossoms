import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
TEXT_SPEED = 5
FONT_SIZE = 50

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Moving Text Example')

# Set up fonts
font = pygame.font.Font(None, FONT_SIZE)

def draw_moving_text(text, start_x, y, speed):
    text_surface = font.render(text, True, (255, 255, 255))  # White text
    text_rect = text_surface.get_rect(topleft=(start_x, y))

    new_x = start_x + speed

    screen.blit(text_surface, text_rect)
    
    return new_x

# Main loop
x_pos = 0
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the screen with black
    screen.fill((0, 0, 0))  # Black background

    # Call the moving text function
    x_pos = draw_moving_text("Hello, Pygame!", x_pos, HEIGHT // 2 - FONT_SIZE // 2, TEXT_SPEED)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)