import pygame
import sys
import json #Checks DATASAVE
import os #Checks DATASAVE
import time

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
ANIMATION_SPEED = 0.009
ANIMATION_SPEED2 = 0.1
FADE_SPEED = 5
transitioning = False
NAME_COLOR = (50, 50, 150) 
DialogueText = ""

box_width, box_height = 9999, 150
box_x = (SCREEN_WIDTH - box_width) // 1 
box_y = (SCREEN_HEIGHT - box_height) // 1  

BLACK = (0,0,0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

idle_frames = [pygame.transform.scale(pygame.image.load('PythonImage/'f'idle_{i}.png'), (80, 100)) for i in range(1, 3)]
walk_frames = [pygame.transform.scale(pygame.image.load('PythonImage/'f'walk_{i}.png'), (80, 100)) for i in range(1, 3)]
npc_image = pygame.transform.scale(pygame.image.load('PythonImage/idle_1.png'), (80, 100))
npc_profile_image = pygame.transform.scale(pygame.image.load('PythonImage/idle_1.png'), (100, 100))
interaction_icon = pygame.transform.scale(pygame.image.load('PythonImage/EIcon.png'), (30, 30))

#LocketAdd
Locket = pygame.image.load("PythonImage/ObjectTest.png")
scaled_image = pygame.transform.scale(Locket, (60, 60))
image_pos = (400, 450)

font = pygame.font.Font(None, 36)
name_font = pygame.font.Font(None, 42) 

full_dialogue_text = [
    "",
    "Congrats you made it!                      ",
    "Teleporting back to menu.                                       ",
    "",
    ""
]

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

dialogue_text = ""
typing = False
dialogue_index = 0
dialogue_cooldown = 300
last_dialogue_time = 0
INTERACTION_DISTANCE = 30
player_pos = (50, 50)
scene = 1
current_text = ""

class Player():
    global player_pos

    def __init__(self):
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.4))
        self.position = pygame.Vector2(self.rect.center)
        self.animation_index = 0
        self.is_walking = False
        self.facing_right = True  

    def update(self, keys):
        self.is_walking = False
        global scene
        
        if keys[pygame.K_LEFT]:  
            self.position.x -= PLAYER_SPEED
            self.is_walking = True
            self.facing_right = False  
        if keys[pygame.K_RIGHT]:  
            self.position.x += PLAYER_SPEED
            self.is_walking = True
            self.facing_right = True  

        self.rect.center = self.position

        if self.position.x < 30: #Pabalik START
            if scene == 1: #Fix
                self.position = pygame.Vector2(30, 418)
                self.rect.center = self.position

            if scene == 2:
                scene -= 1
                
                self.position = pygame.Vector2(1050,418)
                self.rect.center = self.position
            
        elif self.position.x > 1050: #Papunta END
            if scene == 2:
                self.position = pygame.Vector2(1050,418)
                self.rect.center = self.position

            if scene == 1:
                scene += 1
                self.position = pygame.Vector2(30, 418)
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
        self.name = "NPC"

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
    # Split by new lines first
    lines = text.split('\n')
    wrapped_lines = []

    for line in lines:
        words = line.split(' ')
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:  # Avoid adding empty lines
                    wrapped_lines.append(current_line)
                current_line = word

        if current_line:
            wrapped_lines.append(current_line)

    return wrapped_lines

def update_dialogue(name, text, image_profile, color):
    draw_dialogue_box(name, text, image_profile, color)

class Transition:
    def __init__(self):
        TurnTransion = True
        fade_Counter = 0
        self.time_left = 4  #seconds
        self.start_time = pygame.time.get_ticks()
        while True:
            pygame.init()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            

        #Transion
            if TurnTransion == True:
                if fade_Counter < 1080:
                    fade_Counter += 1
                    
                    pygame.draw.rect(screen, BLACK, (0, 0, fade_Counter, 595 / 2))
                    pygame.draw.rect(screen, BLACK, (1080 - fade_Counter, 585 / 2, 1080, 595 / 2))

            
            #Timer 4 seconds
            pygame.display.update() 
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000
            self.time_left = max(4 - int(elapsed_time), 0)
            if self.time_left <= 0:
                break

def main():
    global scene
    global dialogue_text, typing, dialogue_index, last_dialogue_time, PLAYER_SPEED, player_pos, DialogueText, current_text
    print(player_pos)
    player = Player()
    npc = NPC()
    clock = pygame.time.Clock()
    slide_position = SCREEN_HEIGHT
    transitioning = False
    locketposition = scaled_image.get_rect(topleft=image_pos)
    some_condition = True
    BLACK = (0, 0, 0)
    Next = 1
    PickYN = 0 #1 Is yes and 2 is no #3 is active
    looped = True
    looped1 = True
    Ready = True
    Talked = True
    loopedTime = True

    while True:
        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
        if loopedTime:
                loopedTime = False
                time.sleep(1)
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
                        print("sKULL")
                        Next += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                        Next += 1

                elif event.key == pygame.K_y:
                    if PickYN == 3:
                        print("Yes")    
                        PickYN = 1
                        pass
                elif event.key == pygame.K_n:
                    if PickYN == 3:
                        print("No")
                        PickYN = 2
                        pass
                elif event.key == pygame.K_LEFT:
                    if Next == 5:
                        Next = 6
                        pass
                elif event.key == pygame.K_RIGHT:
                    if Next == 5:
                        Next = 6
                        pass
#MainGame------------------------------------------------------------------------------------------------------------------------------------------------------
        if scene == 1:
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
            player.draw(screen)
            if Next >= 5:
                keys = pygame.key.get_pressed()
                player.update(keys)
            if Next == 1:
                #DialogueText = "Hello!\nHow are you?\nThis is a longer message that might wrap."
                DialogueText = "Hello, and welcome to the tutorial!"
                text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
            if Next == 2:
                #DialogueText = "Hello!\nHow are you?\nThis is a longer message that might wrap."
                DialogueText = "Let's get started on learning the basics."
                text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
            if Next >= 3:
                if looped:
                    PickYN = 3
                    Next = 3
                    print(PickYN)
                    looped = False
                DialogueText = "Would you like to skip the tutorial? Press (Y) if yes, Or Press (N) if no"
                update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                if PickYN == 1: #Yes
                    
                    keys = pygame.key.get_pressed()
                    player.update(keys)
                    DialogueText = "Walk right and then straight."
                    text = pygame.font.Font(None, 25).render("", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                    update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                elif PickYN == 2: #No
                    if looped1:
                        Next = 2
                        looped1 = False
                    DialogueText = "Today I will teach you how to move a character."
                    text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                    update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 4:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "In your keyboard."
                        text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 5:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "Press Left Arrow to walk left and press Right arrow to walk right."
                        text = pygame.font.Font(None, 25).render("Press T To Skip:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 6:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "Niceee!"
                        text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 7:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "Use these keys to navigate through the game."
                        text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 8:
                        DialogueText = "Second step, grab the object by clicking them."
                        text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 9:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "Try to grab the [Skull]."
                        text = pygame.font.Font(None, 25).render("Press T To Skip:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                        if locketposition:
                            screen.blit(scaled_image, locketposition.topleft,)
                    if Next == 10:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "Goodjob!"
                        text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 11:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "Clicking on the highlighted objects or areas on the screen."
                        text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 12:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "Interact of these items to progress through the game."
                        text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next == 13:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "also to achieve your goals!"
                        text = pygame.font.Font(None, 25).render("Press T To Continue:", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(120, 150)))
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                    if Next >= 14:
                        screen.fill((255, 255, 255))
                        pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
                        player.draw(screen)
                        DialogueText = "Now, try to walk right and then straight."
                        update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))
                                    
                        

        elif scene == 2:
            player_pos = 30
            screen.fill((255, 255, 255))
            #text = pygame.font.Font(None, 74).render("Background 2 Test", True, (0, 0, 0)); screen.blit(text, text.get_rect(center=(400, 300)))
            pygame.draw.rect(screen, (92, 64, 51), (box_x, box_y, box_width, box_height))
            npc.draw(screen)
            #Add Locket
            keys = pygame.key.get_pressed()
            player.update(keys)
            if Talked:
                DialogueText = "Talk to the npc to end your tutorial!"
                update_dialogue("Guide", DialogueText, pygame.image.load('PythonImage/guide.png'), (0, 0, 0))


            #if locketposition:
                #screen.blit(scaled_image, locketposition.topleft,)

            if player.rect.colliderect(npc.rect.inflate(INTERACTION_DISTANCE, INTERACTION_DISTANCE)):
                screen.blit(interaction_icon, (player.rect.centerx + -15, player.rect.centery - 80))

                current_time = pygame.time.get_ticks()
                if keys[pygame.K_e] and current_time - last_dialogue_time > dialogue_cooldown:
                    if typing:
                        typing = False
                        PLAYER_SPEED = 2.5
                        Talksound.stop()
                    else:
                        Talked = False
                        PLAYER_SPEED = 0
                        typing = True
                        dialogue_index = 0
                        dialogue_text = ""
                        npc.look_at(player)
                    last_dialogue_time = current_time
            else:
                if typing:
                    typing = False

            #if some_condition:
                #player.teleport((400, 410))
                #some_condition = False

            player.draw(screen)
            

        #Timer by 5 Seconds
            #current_time = pygame.time.get_ticks()
            #elapsed_time = (current_time - start_time) / 1000
            #Timer = max(8 - int(elapsed_time), 0)
            #if Timer <= 0:


        if typing and dialogue_index < len(full_dialogue_text):
            if len(current_text) < len(full_dialogue_text[dialogue_index]):
                current_text += full_dialogue_text[dialogue_index][len(current_text)]
                pygame.time.delay(int(TYPING_SPEED * 1000))
            else:
                dialogue_index += 1
                current_text = ""  
                if dialogue_index >= 5:
                    Transition()
                    screen.fill((255, 255, 255))
                    game_data['level'] = 1
                    print(game_data['level'])
                    save_game()
                    break


        if typing:
            draw_dialogue_box(npc.name, current_text, pygame.transform.scale(pygame.image.load('PythonImage/idle_1.png'), (100, 100)), (0, 0, 0))


        if transitioning: #Blackscreen
            pygame.draw.rect(screen, (0, 0, 0), (0, slide_position - SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

        slide_position -= 5

        transitioning = True
        pygame.display.flip()
        clock.tick(60)