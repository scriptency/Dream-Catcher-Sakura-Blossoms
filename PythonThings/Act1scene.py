import pygame
import sys

# Initialize Pygame
pygame.init()

#Audio
Talksound = pygame.mixer.Sound('Audiofile/DialogueSound.mp3') 

#Variables
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 585
DIALOGUE_WIDTH = SCREEN_WIDTH - 40
DIALOGUE_HEIGHT = 120
DIALOGUE_COLOR = (200, 200, 200)
TYPING_SPEED = 0.05
PLAYER_SPEED = 2.5
ANIMATION_SPEED = 0.005
ANIMATION_SPEED2 = 0.1
FADE_SPEED = 5
transitioning = False
NAME_COLOR = (50, 50, 150) 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

idle_frames = [pygame.transform.scale(pygame.image.load('PythonImage/'f'idle_{i}.png'), (80, 100)) for i in range(1, 3)]
walk_frames = [pygame.transform.scale(pygame.image.load('PythonImage/'f'walk_{i}.png'), (80, 100)) for i in range(1, 3)]
npc_image = pygame.transform.scale(pygame.image.load('PythonImage/idle_1.png'), (80, 100))
npc_profile_image = pygame.transform.scale(pygame.image.load('PythonImage/idle_1.png'), (100, 100))
interaction_icon = pygame.transform.scale(pygame.image.load('PythonImage/EIcon.jpg'), (30, 30))

font = pygame.font.Font(None, 36)
name_font = pygame.font.Font(None, 42) 

full_dialogue_text = "TESTING LANGG"
dialogue_text = ""
typing = False
dialogue_index = 0
dialogue_cooldown = 300
last_dialogue_time = 0
INTERACTION_DISTANCE = 50

class Player:
    def __init__(self):
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.7))
        self.position = pygame.Vector2(self.rect.center)
        self.animation_index = 0
        self.is_walking = False
        self.facing_right = True  

    def update(self, keys):
        self.is_walking = False
        if keys[pygame.K_a]:  
            self.position.x -= PLAYER_SPEED
            self.is_walking = True
            self.facing_right = False  
        if keys[pygame.K_d]:  
            self.position.x += PLAYER_SPEED
            self.is_walking = True
            self.facing_right = True  
        
        self.rect.center = self.position

        
        if self.is_walking:
            self.animation_index += ANIMATION_SPEED2
            if self.animation_index >= len(self.walk_frames):
                self.animation_index = 0
            self.image = self.walk_frames[int(self.animation_index)]
        else:
            
            self.animation_index += ANIMATION_SPEED
            if self.animation_index >= len(self.idle_frames):
                self.animation_index = 0
            self.image = self.idle_frames[int(self.animation_index)]

        
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class NPC:
    def __init__(self):
        self.image = npc_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 1.7))
        self.name = "Peklat"

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def look_at(self, player):
        if player.rect.centerx < self.rect.centerx:
            self.image = pygame.transform.flip(npc_image, True, False)
        else:
            self.image = npc_image

def draw_dialogue_box(name, text, ImageProfile, Colorr):
    pygame.draw.rect(screen, DIALOGUE_COLOR, (20, 20, DIALOGUE_WIDTH, DIALOGUE_HEIGHT), border_radius=10)
    
    name_surface = name_font.render(name, True, NAME_COLOR)
    screen.blit(name_surface, (30, 30))
    
    wrapped_text = wrap_text(text, font, DIALOGUE_WIDTH - 40)
    for i, line in enumerate(wrapped_text):
        text_surface = font.render(line, True, Colorr)
        screen.blit(text_surface, (30, 60 + i * 30))
    screen.blit(ImageProfile, (DIALOGUE_WIDTH - 120, 10))

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

#Main
def mainn():
    global dialogue_text, typing, dialogue_index, last_dialogue_time, PLAYER_SPEED
    player = Player()
    npc = NPC()
    clock = pygame.time.Clock()
    slide_position = SCREEN_HEIGHT
    Dialoguee = 1
    start_time = pygame.time.get_ticks()
    transitioning = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Timer by 5 Seconds
            #current_time = pygame.time.get_ticks()
            #elapsed_time = (current_time - start_time) / 1000
            #Timer = max(8 - int(elapsed_time), 0)
            #if Timer <= 0:
        screen.fill((255, 255, 255))
        player.draw(screen)
        npc.draw(screen)
        transitioning = True


        
        keys = pygame.key.get_pressed()
        player.update(keys)


        if transitioning: #Blackscreen
            pygame.draw.rect(screen, (0, 0, 0), (0, slide_position - SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

        slide_position -= 5

        
        if player.rect.colliderect(npc.rect.inflate(INTERACTION_DISTANCE, INTERACTION_DISTANCE)):
            screen.blit(interaction_icon, (player.rect.centerx + 20, player.rect.centery - 20))

            current_time = pygame.time.get_ticks()
            if keys[pygame.K_e] and current_time - last_dialogue_time > dialogue_cooldown:
                if typing:
                    typing = False
                    PLAYER_SPEED = 2.5
                    Talksound.stop()
                else:
                    PLAYER_SPEED = 0
                    typing = True
                    dialogue_index = 0
                    dialogue_text = ""
                    npc.look_at(player)
                last_dialogue_time = current_time
        else:
            if typing:
                typing = False

        if typing and dialogue_index < len(full_dialogue_text):
            dialogue_text += full_dialogue_text[dialogue_index]
            dialogue_index += 1
            pygame.time.delay(int(TYPING_SPEED * 1000))

        if typing:
            draw_dialogue_box(npc.name, dialogue_text, pygame.transform.scale(pygame.image.load('PythonImage/idle_1.png'), (100, 100)), (0, 0, 0))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    mainn()