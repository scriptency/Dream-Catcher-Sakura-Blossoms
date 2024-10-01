import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NPC Dialogue Example")

# Define the player and NPC classes
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 50, 50)  # Player's rectangle

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

class NPC:
    def __init__(self):
        self.rect = pygame.Rect(400, 300, 50, 50)  # NPC's rectangle
        self.dialogues = [
            "Hello, traveler!",
            "How can I help you?",
            "Safe travels!",
        ]
        self.current_dialogue_index = 0
        self.dialogue_active = False

    def check_interaction(self, player):
        if self.rect.colliderect(player.rect):
            self.dialogue_active = True

    def next_dialogue(self):
        if self.dialogue_active:
            if self.current_dialogue_index < len(self.dialogues) - 1:
                self.current_dialogue_index += 1
            else:
                self.dialogue_active = False

# Instantiate player and NPC
player = Player()
npc = NPC()

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if npc.dialogue_active:
                    npc.next_dialogue()
                npc.check_interaction(player)

    # Move the player
    player.move()

    # Check if the player is near the NPC
    npc.check_interaction(player)

    # Fill the screen
    screen.fill(WHITE)

    # Draw player and NPC
    pygame.draw.rect(screen, BLACK, player.rect)
    pygame.draw.rect(screen, (255, 0, 0), npc.rect)

    # Display the current dialogue if active
    if npc.dialogue_active:
        font = pygame.font.Font(None, 36)
        text = font.render(npc.dialogues[npc.current_dialogue_index], True, BLACK)
        screen.blit(text, (50, 50))

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)