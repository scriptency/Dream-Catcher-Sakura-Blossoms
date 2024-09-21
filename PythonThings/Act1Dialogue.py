import pygame
import time
from Act1scene import mainn

pygame.init()

WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))


Talksound = pygame.mixer.Sound('Audiofile/DialogueSound.mp3') 


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
    """Generator for simulating typing effect."""
    for char in message:
        yield char
        time.sleep(speed)

def dialoguee1():
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
    dialoguee1()
    mainn()