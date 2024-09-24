import pygame
import time 
import json #Checks DATASAVE
import os #Checks DATASAVE
from Act1scene import mainn

pygame.init()

Talksound = pygame.mixer.Sound('Audiofile/DialogueSound.mp3') 

#Checks DATASAVE
save_file = 'savefile.json'

def save_game():
    with open(save_file, 'w') as f:
        json.dump(game_data, f)
    print("Game saved!")

#Function to load game data
def load_game():
    global game_data
    if os.path.exists(save_file):
        with open(save_file, 'r') as f:
            game_data = json.load(f)
        print("Game loaded!")
    else:
        print("No save file found. Starting a new game.")


load_game()

if game_data['Sound'] == 0:
    Talksound.set_volume(1)
else:
    Talksound.set_volume(0)

if game_data['Musics'] == 0:
    pass
else:
    pass

#-------------------------------------------------------------------------------

WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

scale_factor = 1.5
font_size = int(36 * scale_factor)
font = pygame.font.Font(None, font_size)

messages = [
    "Is it all done? or... Did it all repeat itself?",
    "I still remember it like it was just Yesterday...",
    "It all Started in the Orphanage...",
    "",
]

def typewriter_effect(message, speed=0.05):
    for char in message:
        yield char
        time.sleep(speed)

def dialoguee():

    import MainMenuu

    clock = pygame.time.Clock()
    running = True
    current_message = 0
    current_text = ""
    typing = False
    typing_generator = None
    EndDialogue = 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not typing:
                    if current_message < len(messages):
                        Talksound.play(-1)
                        current_text = ""
                        typing = True
                        typing_generator = typewriter_effect(messages[current_message])
                        current_message += 1
                        EndDialogue = EndDialogue + 1
                        print(EndDialogue)

        if typing:
            try:
                current_text += next(typing_generator)
            except StopIteration:
                Talksound.stop()
                typing = False 

        text_surface = font.render(current_text, True, WHITE)
        screen.blit(text_surface, (50, 250))


        if not typing and current_message < len(messages):
            prompt_surface = font.render("Press E to continue", True, WHITE)
            screen.blit(prompt_surface, (50, 500))

        if EndDialogue == 4:
            break

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    dialoguee()
    mainn()