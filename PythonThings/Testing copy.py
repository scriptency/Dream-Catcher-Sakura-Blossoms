import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dialogue Example")

# Fonts
font = pygame.font.Font(None, 36)
name_font = pygame.font.Font(None, 24)

# Colors
DIALOGUE_COLOR = (255, 255, 255)
NAME_COLOR = (0, 0, 0)

# Load an image for the profile (replace 'profile.png' with your image)
image_profile = pygame.image.load('PythonImage/guide.jpg')

def draw_dialogue_box(name, text, image_profile, color):
    pygame.draw.rect(screen, DIALOGUE_COLOR, (20, 20, 400, 150), border_radius=10)
    name_surface = name_font.render(name, True, NAME_COLOR)
    screen.blit(name_surface, (30, 30))
    wrapped_text = wrap_text(text, font, 360)
    for i, line in enumerate(wrapped_text):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (30, 60 + i * 30))
    screen.blit(image_profile, (280, 10))

def wrap_text(text, font, max_width):
    words = text.split(' ')
    wrapped_lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word
    if current_line:
        wrapped_lines.append(current_line)
    return wrapped_lines

def update_dialogue(name, text, image_profile, color):
    draw_dialogue_box(name, text, image_profile, color)

# Main loop
running = True
dialogue_state = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Change dialogue on space press
                dialogue_state += 1

    screen.fill((0, 0, 0))  # Clear the screen

    # Example dialogues
    if dialogue_state == 0:
        update_dialogue("Character 1", "Hello! This is the first dialogue.", image_profile, (0, 0, 0))
    elif dialogue_state == 1:
        update_dialogue("Character 2", "Hi there! Now it’s my turn.", image_profile, (0, 0, 0))
    elif dialogue_state == 2:
        update_dialogue("Character 1", "Great to see you again!", image_profile, (0, 0, 0))
    elif dialogue_state >= 3:
        update_dialogue("End", "Thanks for reading!", image_profile, (0, 0, 0))

    pygame.display.flip()  # Update the display

# Quit Pygame
pygame.quit()
sys.exit()