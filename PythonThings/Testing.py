import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hover Effect Example")

# Load your image (make sure to have a valid image file)
image = pygame.image.load('PythonImage/idle_1.png')  # Replace with your image file
image_rect = image.get_rect()

# Button properties
button_color = (100, 200, 100)
button_rect = pygame.Rect(300, 250, 200, 100)  # x, y, width, height

# Main loop
hovering = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Check if mouse is hovering over the button
    hovering = button_rect.collidepoint(mouse_pos)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect)

    # Draw the image if hovering
    if hovering:
        image_rect.topleft = (300, 100)  # Set position where you want the image to appear
        screen.blit(image, image_rect)

    # Update the display
    pygame.display.flip()