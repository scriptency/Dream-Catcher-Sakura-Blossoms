import pygame
import sys
import time
import json #Checks DATASAVE
import os #Checks DATASAVE

pygame.init()


#Audio
Talksound = pygame.mixer.Sound('Audiofile/DialogueSound.mp3') 
Doorsound = pygame.mixer.Sound('Audiofile/Doorsound.mp3') 

#Variables
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 585
DIALOGUE_WIDTH = SCREEN_WIDTH - 40
DIALOGUE_HEIGHT = 120
DIALOGUE_COLOR = (200, 200, 200)
TYPING_SPEED = 0.02
PLAYER_SPEED = 2.5
ANIMATION_SPEED = 0.009
ANIMATION_SPEED2 = 0.1
FADE_SPEED = 5
transitioning = False
NAME_COLOR = (50, 50, 150) 
LoopedTime = True

box_width, box_height = 1080, 150
box_x = (SCREEN_WIDTH - box_width) // 1 
box_y = (SCREEN_HEIGHT - box_height) // 1  

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

idle_frames = [pygame.transform.scale(pygame.image.load('PythonImage/'f'idle_{i}.png'), (100, 120)) for i in range(1, 3)]
walk_frames = [pygame.transform.scale(pygame.image.load('PythonImage/'f'walk_{i}.png'), (100, 120)) for i in range(1, 3)]
npc_image = pygame.transform.scale(pygame.image.load('PythonImage/Girlnpc1.png'), (100, 120))
npc_profile_image = pygame.transform.scale(pygame.image.load('PythonImage/idle_1.png'), (100, 100))
interaction_icon = pygame.transform.scale(pygame.image.load('PythonImage/EIcon.png'), (30, 30))
BackgroundRoom = pygame.transform.scale(pygame.image.load('PythonImage/RoomBackground.jpg'), (1080, 585))
Hallway = pygame.transform.scale(pygame.image.load('PythonImage/hallwaybg.jpeg'), (1080, 585))

Doors1 = pygame.transform.scale(pygame.image.load('PythonImage/DoorHitbox.png'), (100, 120))

#LocketAdd
Locket = pygame.image.load("PythonImage/Lockett.png")
scaled_image = pygame.transform.scale(Locket, (60, 60))
image_pos = (400, 400)

font = pygame.font.Font(None, 36)
name_font = pygame.font.Font(None, 42) 

game_data = {
    'level': 1,
    'Sound': 1,
    'Musics': 1,
}
save_file = 'savefile.json'

def save_game():
    with open(save_file, 'w') as f:
        json.dump(game_data, f)
    print("Game saved!")

# Function to load game data
def load_game():
    global game_data
    if os.path.exists(save_file):
        with open(save_file, 'r') as f:
            game_data = json.load(f)
        print("Game loaded!")
    else:
        print("No save file found. Starting a new game.")

load_game()

player_pos = (50, 50)
full_dialogue_text = "TESTING LANGG"
dialogue_text = ""
typing = False
dialogue_index = 0
dialogue_cooldown = 300
last_dialogue_time = 0
INTERACTION_DISTANCE = 0.5
scene = 1
pos_player = "none"

if game_data['Sound'] == 0:
    Talksound.set_volume(1)
    Doorsound.set_volume(1)
else:
    Doorsound.set_volume(0)
    Talksound.set_volume(0)

def draw_moving_text(text, start_x, y, speed):
    text_surface = pygame.font.Font(None, 50).render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(topleft=(start_x, y))

    new_x = start_x + speed

    screen.blit(text_surface, text_rect)
    return new_x, new_x > SCREEN_WIDTH

class Player():
    global player_pos, scene

    def __init__(self):
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.3))
        self.position = pygame.Vector2(self.rect.center)
        self.animation_index = 0
        self.is_walking = False
        self.facing_right = True  

    def update(self, keys):
        self.is_walking = False
        global scene, pos_player
        
        if keys[pygame.K_LEFT]:  
            self.position.x -= PLAYER_SPEED
            self.is_walking = True
            self.facing_right = False  
        if keys[pygame.K_RIGHT]:  
            #print(self.position.x)

            self.position.x += PLAYER_SPEED
            self.is_walking = True
            self.facing_right = True  

        self.rect.center = self.position

        if pos_player == "start":
            self.position = pygame.Vector2(60, 448)
            pos_player = "none"


        if self.position.x < 30: #Pabalik START
            if scene == 1: #Fix pos
                self.position = pygame.Vector2(30, 448)
                self.rect.center = self.position

            if scene == 2: #Door enter
                self.position = pygame.Vector2(1050,448)
                self.rect.center = self.position
                Doorsound.play()
                scene = 1
                

            if scene == 3:
                scene -= 1
                self.position = pygame.Vector2(1050,448)
                self.rect.center = self.position
            
        elif self.position.x > 1050: #Papunta END
            if scene == 1: #Fix pos
                self.position = pygame.Vector2(1050,448)
                self.rect.center = self.position
            if scene == 3: #Fix pos
                self.position = pygame.Vector2(1050,448)
                self.rect.center = self.position

            if scene == 2:
                scene += 1
                self.position = pygame.Vector2(30, 448)
                self.rect.center = self.position
        


        else:
            pass

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

    def teleport(self, new_position):
        self.position = pygame.Vector2(new_position)
        self.rect.center = self.position

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class NPC:
    def __init__(self):
        self.image = npc_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 1.4))
        self.name = "???"

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def look_at(self, player):
        if player.rect.centerx < self.rect.centerx:
            self.image = pygame.transform.flip(npc_image, True, False)
        else:
            self.image = npc_image

class RoomDoor:
    def __init__(self):
        self.image = Doors1
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 1.5))
        

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def change_position(self, x, y):
        self.rect.center = (x, y)

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
    global scene
    global dialogue_text, typing, dialogue_index, last_dialogue_time, PLAYER_SPEED, player_pos, Interactt, pos_player
    print(player_pos)
    player = Player()
    npc = NPC()
    doorhitbox = RoomDoor()
    clock = pygame.time.Clock()
    slide_position = SCREEN_HEIGHT
    transitioning = False
    locketposition = scaled_image.get_rect(topleft=image_pos)
    some_condition = True
    LoopedTime = True
    # Constants
    TEXT_SPEED = 6
    FONT_SIZE = 35
    text_done = False
    x_pos = -1000
    Interactt = ""
    PLAYER_SPEED = 2.6
    pos_player = "start"

    while True:
        #pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #This find lockett pick up
                if locketposition == None:
                   pass
                else:
                    if locketposition.collidepoint(event.pos):
                        locketposition = None 
                        print("Testing")

        if scene == 1: #Room
            if LoopedTime:
                screen.fill((0, 0, 0))
                pygame.display.update() 
                LoopedTime = False
                time.sleep(2)
            doorhitbox.change_position(1032, 442)
            screen.blit(BackgroundRoom, (0,0))
            #pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
            npc.draw(screen)
            doorhitbox.draw(screen)
            #text = pygame.font.Font(None, 74).render("Background 1 Test", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(400, 300)))
            #Add Locket

            if locketposition:
                screen.blit(scaled_image, locketposition.topleft,)
            player.draw(screen)


            if player.rect.colliderect(npc.rect.inflate(INTERACTION_DISTANCE, INTERACTION_DISTANCE)):
                Interactt = "NPC1"
                interaction_position = (player.rect.centerx - 15, player.rect.centery - 80)
                screen.blit(interaction_icon, interaction_position)

                current_time = pygame.time.get_ticks()

                if keys[pygame.K_e] and current_time - last_dialogue_time > dialogue_cooldown:
                    if Interactt == "NPC1":
                        if typing:
                            typing = False
                            PLAYER_SPEED = 2.5
                            Talksound.stop()
                            print("Test1")
                        else:
                            PLAYER_SPEED = 0
                            typing = True
                            dialogue_index = 0
                            dialogue_text = ""
                            npc.look_at(player)
                        last_dialogue_time = current_time

            elif player.rect.colliderect(doorhitbox.rect.inflate(INTERACTION_DISTANCE, INTERACTION_DISTANCE)):
                Interactt = "Door1"
                interaction_position = (player.rect.centerx - 15, player.rect.centery - 80)
                screen.blit(interaction_icon, interaction_position)

                current_time = pygame.time.get_ticks()

                if keys[pygame.K_e] and current_time - last_dialogue_time > dialogue_cooldown:
                    print("Test2")
                    scene = 2
                    pos_player = "start"
                    Doorsound.play()
            else:
                Interactt = None
                if typing:
                    typing = False

        elif scene == 2:

            #if some_condition:
                #player.teleport((400, 410))
                #some_condition = False
            screen.blit(Hallway, (0,0))
   
            #screen.fill((255, 255, 255))
            text = pygame.font.Font(None, 74).render("Background 2 Test", True, (255, 255, 255)); screen.blit(text, text.get_rect(center=(400, 300)))
            #pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
            player.draw(screen)


        #Timer by 5 Seconds
            #current_time = pygame.time.get_ticks()
            #elapsed_time = (current_time - start_time) / 1000
            #Timer = max(8 - int(elapsed_time), 0)
            #if Timer <= 0:

        elif scene == 3:

            #if some_condition:
                #player.teleport((400, 410))
                #some_condition = False
            screen.blit(Hallway, (0,0))
   
            #screen.fill((255, 255, 255))
            text = pygame.font.Font(None, 74).render("Background 3 Test", True, (255, 255, 255)); screen.blit(text, text.get_rect(center=(400, 300)))
            #pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
            player.draw(screen)


        #Timer by 5 Seconds
            #current_time = pygame.time.get_ticks()
            #elapsed_time = (current_time - start_time) / 1000
            #Timer = max(8 - int(elapsed_time), 0)
            #if Timer <= 0:
        
        keys = pygame.key.get_pressed()
        player.update(keys)


        if typing and dialogue_index < len(full_dialogue_text):
            dialogue_text += full_dialogue_text[dialogue_index]
            dialogue_index += 1
            pygame.time.delay(int(TYPING_SPEED * 1000))

        

        if typing:
            draw_dialogue_box(npc.name, dialogue_text, pygame.transform.scale(pygame.image.load('PythonImage/Girlnpc1.png'), (100, 100)), (0, 0, 0))

        if not text_done:  
            x_pos, text_done = draw_moving_text("(ARK1)ACT 1 - Orphanage", x_pos, SCREEN_HEIGHT // 3 - FONT_SIZE // 1.5, TEXT_SPEED)


        if transitioning: #Blackscreen
            pygame.draw.rect(screen, (0, 0, 0), (0, slide_position - SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

        slide_position -= 5

        transitioning = True
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    mainn()

    