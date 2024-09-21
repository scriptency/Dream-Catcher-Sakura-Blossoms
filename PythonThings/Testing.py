import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Hover Button Example')

# Load images
button_image = pygame.image.load('PythonImage/Button_play.png')
hover_image = pygame.image.load('PythonImage/Button_exit.png')

# Get button rectangle
button_rect = button_image.get_rect(center=(400, 300))
hover_rect = hover_image.get_rect(center=(500, 300))  # Position of the pop-out image

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouse_pos)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw button
    screen.blit(button_image, button_rect)

    # If hovered, draw the hover image
    if is_hovered:
        screen.blit(hover_image, hover_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()