import pygame
import json #Checks DATASAVE
import os #Checks DATASAVE
import sys
import time
from sys import exit
from Tutorial import main
from button import Button
from Act1Dialogue import dialoguee
from Act1scene import mainn



import time
pygame.init()
#f

WIDTH, HEIGHT = 1080, 585

#Title and logo hehe
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Dream Catcher: Sakura Blossoms')
pygame.display.set_icon(pygame.image.load('PythonImage/Logo.png'))
        
#Variables
Cooldownn = False
transparent = (0, 0, 0, 0)
BLACK = (0, 0, 0)
fade_Counter = 0
Actt = 1
loopedTime = True

#Checks DATASAVE

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

#Audio
Buttonsound = pygame.mixer.Sound('Audiofile/Button.mp3')
Ark1music = pygame.mixer.Sound('Audiofile/Act1Theme.mp3') 
Swoosh = pygame.mixer.Sound('Audiofile/Swoosh.mp3') 
ActSelection = pygame.mixer.Sound('Audiofile/Act_selection.mp3') 
ArkSelection = pygame.mixer.Sound('Audiofile/Ark_selection.mp3') 
PlayButtonSound = pygame.mixer.Sound('Audiofile/Playbutton.mp3') 
Talksound = pygame.mixer.Sound('Audiofile/DialogueSound.mp3') 


Buttonsound.set_volume(1)

#Image Loader
backgroundd = pygame.image.load('PythonImage/background.jpeg')
backgroundd2 = pygame.image.load('PythonImage/background2.jpeg')
Logo = pygame.image.load('PythonImage/LogoMenu.png')
ark1 = pygame.image.load('PythonImage/Ark1.png')

#SettingsImage
Backbuttonsettings = Button('PythonImage/button_back.png',(50, 500))
MusicOn = Button('PythonImage/button_music-on.png', (120,20))
MusicOff = Button('PythonImage/button_music-off.png', (320,20))
SoundOn = Button('PythonImage/button_sound-on.png', (120,100))
SoundOff = Button('PythonImage/button_sound-off.png', (320,100))

#Ark1

ActPicture = pygame.image.load('PythonImage/Act11.png')
arkAct1 = Button('PythonImage/button_Ark1_1.png', (30,100))
arkAct2 = Button('PythonImage/button_Ark1_2.png', (30,165))
arkAct3 = Button('PythonImage/button_Ark1_3.png', (30,230))
arkAct4 = Button('PythonImage/button_Ark1_4.png', (30,295))
arkAct5 = Button('PythonImage/button_Ark1_5.png', (30,365))

#Menu Chooser
Act1Chooser = Button('PythonImage/button_ark.png', (190,130))
ProgressText = pygame.image.load('PythonImage/PROGRESS.gif')
Act2Chooser = Button('PythonImage/button_ark2.png', (170,400))
Act3Chooser = Button('PythonImage/button_ark3.png', (800,130))
Act4Chooser = Button('PythonImage/button_ark4.png', (800,400))
MembersButton = Button('PythonImage/button_members.png', (40,450))
Whiteprops = pygame.image.load('PythonImage/whitedesign.jpg')
ArkPlay = Button('PythonImage/button_playark.png', (450,70))
titlee = pygame.image.load('PythonImage/Title.png')
titlee2 = pygame.image.load('PythonImage/ActText.png')
button_play = Button('PythonImage/button_play.png', (20,210))
button_exit = Button('PythonImage/button_exit.png', (20,330))
button_settings = Button('PythonImage/button_settings.png', (20,270))
MembersList = pygame.image.load('PythonImage/MemberlistImage.png')  # Replace with your image file
MemberList_rect = MembersList.get_rect()

test_font = pygame.font.Font(None, 30)
text_gameflow = test_font.render('Gameflow: ', False, 'Green')

Timer = pygame.time.Clock()

#Checks settings by file 
if game_data['Musics'] == 1:
    Ark1music.set_volume(0)

if game_data['Musics'] == 0:
    Ark1music.set_volume(1)

if game_data['Sound'] == 0:
    Buttonsound.set_volume(1)
    ActSelection.set_volume(1)
    ArkSelection.set_volume(1)
    PlayButtonSound.set_volume(1)
    Talksound.set_volume(1)
            
if game_data['Sound'] == 1:
    Buttonsound.set_volume(0)
    ActSelection.set_volume(0)
    ArkSelection.set_volume(0)
    PlayButtonSound.set_volume(0)
    Talksound.set_volume(0)

print('Tesllo')

text_font = pygame.font.SysFont(None, 60, bold = True)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Multiple Scene

class Intro:
    def __init__(self):

        WIDTH, HEIGHT = 1080, 585
        BACKGROUND_COLOR = (30, 30, 30)  #Darkgray
        TEXT_COLOR = (255, 255, 255)      #White
        FONT_SIZE = 64
        INTRO_DURATION = 3000  #3seconds
        start_time = pygame.time.get_ticks()
        self.time_left = 10 
        self.start_time = pygame.time.get_ticks()
        font = pygame.font.Font(None, FONT_SIZE)
        
        while True:
            pygame.init()
            mouse = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game()
                    pygame.quit()
                    exit()
            
            screen.fill(BACKGROUND_COLOR)
            text_surface = font.render("MADE BY VISUAL STUDIO :3", True, TEXT_COLOR)

            text_surface2 = font.render("GROUP 2", True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2.1))
            text_rect2 = text_surface.get_rect(center=(WIDTH // 1.4, HEIGHT // 1.7))

            # Blit the text to the screen
            screen.blit(text_surface, text_rect)

            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000
            self.time_left = max(10 - int(elapsed_time), 0)
            if self.time_left <= 0:

                break

            screen.blit(text_surface2, text_rect2)

            
            pygame.display.flip()

            
            if pygame.time.get_ticks() - start_time > INTRO_DURATION:
                 Swoosh.play()
                 Transition()

                 break
        

            pygame.display.update()


class Settingss:
    def __init__(self):
        loop = True
        Transition2()
        loopedTime = True
        while True:
            pygame.init()
            mouse = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game()
                    pygame.quit()
                    exit()



            screen.fill((0, 0, 0))

            if loopedTime: #StopLag
                loopedTime = False
                time.sleep(1)


            if MusicOff.is_pressed():
                if game_data['Musics'] == 0:
                    game_data['Musics'] = 1
                    print("Music Off")
                    Ark1music.set_volume(0)

            if MusicOn.is_pressed():
                if game_data['Musics'] == 1:
                    game_data['Musics'] = 0
                    print("Music On")
                    Ark1music.set_volume(1)

            if SoundOn.is_pressed():
                if game_data['Sound'] == 1:
                    game_data['Sound'] = 0
                    print("Sound On")
                    Buttonsound.set_volume(1)
                    ActSelection.set_volume(1)
                    ArkSelection.set_volume(1)
                    PlayButtonSound.set_volume(1)
                    Talksound.set_volume(1)
            
            if SoundOff.is_pressed():
                if game_data['Sound'] == 0:
                    game_data['Sound'] = 1
                    print("Sound Off")
                    Buttonsound.set_volume(0)
                    ActSelection.set_volume(0)
                    ArkSelection.set_volume(0)
                    PlayButtonSound.set_volume(0)
                    Talksound.set_volume(0)

            MusicOff.draw(screen)
            MusicOn.draw(screen)
            SoundOn.draw(screen)
            SoundOff.draw(screen)


            Backbuttonsettings.draw(screen)

            #kdjadhaadkljijjlkhjyuplaopdpp

            if game_data['Musics'] == 0:
                draw_text("Musics: On", text_font, (0, 255, 0), 10,300)
            elif game_data['Musics'] == 1:
                draw_text("Music: Off", text_font, (255, 0, 0), 10,300)

            if game_data['Sound'] == 0:
                draw_text("Sound: On", text_font, (0, 255, 0), 10,350)
            elif game_data['Sound'] == 1:
                draw_text("Sound: Off", text_font, (255, 0, 0), 10,350)

            if Backbuttonsettings.is_pressed():
                if loop == True:
                    loop = False
                    print(game_data['Sound'])
                    print(game_data['Musics'])
                    save_game()
                    Buttonsound.play()
                    Transition2()
                    MainMenu()
                    break
                    #screen.fill((255,255,255))#white
                    #game = PlayScene()
                    

            pygame.display.update()
            Timer.tick(60)

class MainMenu:
    def __init__(self):
        loop = True
        transitioning = False
        slide_position = HEIGHT
        loopedTime = True
        hovering = False
        #screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #font = pygame.font.Font(None, 36)
        while True:

            pygame.init()
            mouse = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game()
                    pygame.quit()
                    exit()

            screen.blit(backgroundd, (0,0))
            if loopedTime: #StopLag
                loopedTime = False
                time.sleep(1)
            screen.blit(Logo, (850,350))
            screen.blit(ProgressText, (200,150))
            #screen.blit(titlee, (0,0))

            button_play.draw(screen)
            button_exit.draw(screen)
            button_settings.draw(screen)
            MembersButton.draw(screen)

            if transitioning: #Blackscreen
                pygame.draw.rect(screen, (0, 0, 0), (0, slide_position - HEIGHT + 10, WIDTH, HEIGHT))

            slide_position -= 8

            transitioning = True
            mouse_pos = pygame.mouse.get_pos()
            hovering = pygame.Rect(40,450,150,50).collidepoint(mouse_pos)
            if hovering:
                MemberList_rect.topleft = (500, 80)  # Set position where you want the image to appear
                screen.blit(MembersList, MemberList_rect)


            if button_play.is_pressed():
                if loop == True:
                    loop = False
                    PlayButtonSound.play()
                    print("Play button pressed")
                    print(game_data['level'])
                    #screen.fill((255,255,255))#white
                    #game = PlayScene()
                    break
            if button_exit.is_pressed():
                print("Exit button pressed")
                Buttonsound.play()
                pygame.quit()
                exit()
            if button_settings.is_pressed():
                Buttonsound.play()
                print("Settings button pressed")
                Settingss()
                break

            pygame.display.update()
            Timer.tick(60)

class PlayScene:
    
    def __init__(self):
        Act = 0
        transitioning = False
        slide_position = HEIGHT
        loopedTime = True
        while True:
            if game_data['level'] == 1:
                #Tutorial.Tutor()
                main()
                screen.fill((255,255,255))#white
                screen.blit(text_gameflow, (0,0))
                screen.blit(backgroundd2, (0,0))
                screen.blit(Whiteprops, (0,0))
                #screen.blit(titlee2, (25,0))
                Act1Chooser.draw(screen)
                Act2Chooser.draw(screen)
                Act3Chooser.draw(screen)
                Act4Chooser.draw(screen)
                Act3Chooser.draw(screen)
                break
                

            
            pygame.init()
            mouse = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game()
                    pygame.quit()
                    exit()
            
            screen.fill((255,255,255))#white
            if loopedTime: #StopLag
                loopedTime = False
                time.sleep(1)
            screen.blit(text_gameflow, (0,0))
            screen.blit(backgroundd2, (0,0))
            screen.blit(Whiteprops, (0,0))
            #screen.blit(titlee2, (25,0))
            Act1Chooser.draw(screen)
            Act2Chooser.draw(screen)
            Act3Chooser.draw(screen)
            Act4Chooser.draw(screen)
            Act3Chooser.draw(screen)
            #ArkPlay.draw(screen)
            Timer.tick(60)

            if transitioning: #Blackscreen
                pygame.draw.rect(screen, (0, 0, 0), (0, slide_position - HEIGHT + 10, WIDTH, HEIGHT))

            slide_position -= 8

            transitioning = True

            if Act1Chooser.is_pressed():
                if Act == 1:
                    ArkSelection.play()
                    Act = 1
                    print("Ark ", Act," Choosed")
                    break
                else:
                    Act = 1
                    Buttonsound.play()
            if Act2Chooser.is_pressed():
                if Act == 2:
                    ArkSelection.play()
                    Act = 2
                    print("Ark ", Act, " Still locked, Pick another Ark.")
                    pass
                else:
                    Act = 2
                    Buttonsound.play()
            if Act3Chooser.is_pressed():
                if Act == 3:
                    ArkSelection.play()
                    Act = 3
                    print("Ark ", Act, " Still locked, Pick another Ark.")
                    pass
                else:
                    Buttonsound.play()
                    Act = 3
            if Act4Chooser.is_pressed():
                if Act == 4:
                    ArkSelection.play()
                    Act = 4
                    print("Ark ", Act, " Still locked, Pick another Ark.")
                    pass
                else:
                    Buttonsound.play()
                    Act = 4

            if Act == 1: #Act4
                draw_text("Ark 1 - Axion; Cruel Reminices", text_font, (51, 0, 0), 30,10)
                pass
            elif Act == 2: #Act1
                draw_text("Ark 2 - Rhys: Acceptance", text_font, (0, 153, 0), 30,10)
                pass
            elif Act == 3: #Act2
                draw_text("Ark 3 - Reunited: Siblings", text_font, (0, 0, 204), 30,10)
                pass
            elif Act == 4: #Act3
                draw_text("Ark 4 - Reincarnation; Decision", text_font, (153, 153, 0), 30,10)
                pass

            pygame.display.update() 


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

class Transition2:
    def __init__(self):
        TurnTransion = True
        fade_Counter = 0
        self.time_left = 3  # seconds
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
                    
                    pygame.draw.rect(screen, BLACK, (0, 0, fade_Counter, 585))

            
            #Timer 5 seconds
            pygame.display.update() 
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000
            self.time_left = max(3 - int(elapsed_time), 0)
            if self.time_left <= 0:
                break
        
        

class Ark1:
    def __init__(self):
        transitioning = False
        slide_position = HEIGHT
        Act = 0
        Ark1music.play(-1) #Loop Music
        while True:

            pygame.init()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game()
                    pygame.quit()
                    exit()

            screen.blit(ark1, (0,0))
            screen.blit(ActPicture, (300,100))
            arkAct1.draw(screen)
            arkAct2.draw(screen)
            arkAct3.draw(screen)
            arkAct4.draw(screen)
            arkAct5.draw(screen)

            if transitioning: #Blackscreen
                pygame.draw.rect(screen, (0, 0, 0), (0, slide_position - HEIGHT + 10, WIDTH, HEIGHT))

            slide_position -= 8

            transitioning = True

            if arkAct1.is_pressed():
                if Act == 1:
                    ActSelection.play()
                    Ark1music.stop()
                    Transition()
                    dialoguee()
                    break
                else:
                    Buttonsound.play()
                    Act = 1
            if arkAct2.is_pressed():
                if Act == 2:
                    ActSelection.play()
                    print("NOT DONE YET(COMEBACK SOON)")
                    pass
                else:
                    Buttonsound.play()
                    Act = 2
            if arkAct3.is_pressed():
                if Act == 3:
                    ActSelection.play()
                    print("NOT DONE YET(COMEBACK SOON)")
                    pass
                else:
                    Buttonsound.play()
                    Act = 3
            if arkAct4.is_pressed():
                if Act == 4:
                    ActSelection.play()
                    print("NOT DONE YET(COMEBACK SOON)")
                    pass
                else:
                    Buttonsound.play()
                    Act = 4
            if arkAct5.is_pressed():
                if Act == 5:
                    ActSelection.play()
                    print("NOT DONE YET(COMEBACK SOON)")
                    pass
                else:
                    Buttonsound.play()
                    Act = 5

            if Act == 1:
                draw_text("Orphanage House", text_font, (193, 193, 0), 300,350)
            if Act == 2:
                draw_text("Hallway", text_font, (193, 193, 0), 300,350)
            if Act == 3:
                draw_text("Playground", text_font, (193, 193, 0), 300,350)
            if Act == 4:
                draw_text("Children's Room", text_font, (193, 193, 0), 300,350)
            if Act == 5:
                draw_text("Adoption Room", text_font, (193, 193, 0), 300,350)


            draw_text("TESTING DEMO", text_font, (102, 255, 102), 500,500)
            pygame.display.update() 


#MainRun System
if __name__ == '__main__':
    game =  Intro()
    def Retry():

        game = MainMenu()

        Transition2()

        game = PlayScene()

        if game_data['level'] == 1:
            game_data['level'] = 2
            save_game()
            print("Tutorial Complete!")
            Retry()

        if Actt == 1:
            Transition()
            Ark1()
        elif Actt == 2:
            pass
        elif Actt == 3:
            pass
        elif Actt == 4:
            pass

        mainn()

    Retry()
