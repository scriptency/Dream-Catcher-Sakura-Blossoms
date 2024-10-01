import pygame
import time 
import json #Checks DATASAVE
import os #Checks DATASAVE
import random
from Act1scene import mainn

pygame.init()

Talksound = pygame.mixer.Sound('Audiofile/DialogueSound.mp3') 
Glitchsound = pygame.mixer.Sound('Audiofile/Glitch.mp3') 

Cutscene2 = pygame.image.load("PythonImage/cutscene2.jpeg")
Cutscene1 = pygame.image.load("PythonImage/cutscene1.jpeg")
glitch1 = pygame.image.load("PythonImage/glitchimage1.png")
glitch2 = pygame.image.load("PythonImage/glitchimage2.png")
glitch3 = pygame.image.load("PythonImage/glitchimage3.png")

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
    Glitchsound.set_volume(1)
else:
    Glitchsound.set_volume(0)
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
                    fade_Counter += 2
                    
                    pygame.draw.rect(screen, BLACK, (0, 0, fade_Counter, 595 / 2))
                    pygame.draw.rect(screen, BLACK, (1080 - fade_Counter, 585 / 2, 1080, 595 / 2))

            
            #Timer 4 seconds
            pygame.display.update() 
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000
            self.time_left = max(4 - int(elapsed_time), 0)
            if self.time_left <= 0:
                break


def shake_image(image, duration=2000, shake_amount=5):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start_time < duration:
        screen.fill((0, 0, 0))  

        shake_x = shake_amount * (2 * random.random() - 1)
        shake_y = shake_amount * (2 * random.random() - 1)

        screen.blit(image, (540 + shake_x - image.get_width() // 2, 
                             292.5 + shake_y - image.get_height() // 2))

        pygame.display.flip()  
        clock.tick(60)  

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
    showing_first_image = True

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
            if showing_first_image:
                screen.blit(Cutscene1, (0,0))
                pygame.display.flip()
                time.sleep(1.5)
                shake_image(Cutscene1, duration=2000) 
                showing_first_image = False  
                Glitchsound.play()
            if not showing_first_image:
                screen.blit(glitch1, (0,0))
                pygame.display.flip()
                time.sleep(0.1)
                screen.blit(glitch2, (0,0))
                pygame.display.flip()
                time.sleep(0.1)
                screen.blit(glitch3, (0,0))
                pygame.display.flip()
                time.sleep(0.1)
                screen.blit(glitch1, (0,0))
                pygame.display.flip()
                time.sleep(0.1)
                screen.blit(glitch2, (0,0))
                pygame.display.flip()
                time.sleep(0.1)
                screen.blit(glitch3, (0,0))
                pygame.display.flip()
                time.sleep(0.1)
                screen.fill((0, 0, 0))  
                screen.blit(Cutscene2, (540 - Cutscene2.get_width() // 2, 
                                    292.5 - Cutscene2.get_height() // 2))
                pygame.display.flip() 
                pygame.time.delay(2000) 
                Transition()
            running = False
            break

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    dialoguee()
    mainn()