import os
from TheGame import *

#===========================================# Pygame initialization #===========================================#
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
main_window = pygame.display.set_mode((900, 900))
main_window.blit(pygame.image.load(r'assets\background menu.png'), (0, 0))
pygame.display.set_caption('Space Invaders')


# window icon
windowIcon = pygame.image.load(r'assets\window icon.png')
pygame.display.set_icon(windowIcon)

# clock time
clock = pygame.time.Clock()



#===========================================# Everything button #===========================================#

def Text(text, color,size):
    textSurface = pygame.font.SysFont('comicsansms', size).render(text, True, color)
    return textSurface, textSurface.get_rect()

def Assign_Button_Text(message, txt_color, xcoord, ycoord, width, height, font_size):
    txt_surface, txt_rect = Text(message, txt_color, font_size)
    txt_rect.center = ((xcoord+(width/2)), ycoord+(height/2))
    main_window.blit(txt_surface, txt_rect)

def Hover(window_x, window_y, box_x, box_y, old_color, new_color, cursor, id):
    is_Clicked = pygame.mouse.get_pressed()

    if (window_x + box_x > cursor[0] > window_x and window_y + box_y > cursor[1] > window_y):
        pygame.draw.rect(main_window, (new_color), (window_x, window_y, box_x, box_y))
        pygame.display.update()


        if is_Clicked[0] == 1 and id != None:
            if id == 1:

                def Change_pic(image):
                    pygame.display.update()
                    main_window.blit(pygame.image.load(image), (0,0))

                pygame.mixer.music.stop()

                Change_pic(r'assets\transition\transition1.png')
                Change_pic(r'assets\transition\transition2.png')
                Change_pic(r'assets\transition\transition3.png')
                Change_pic(r'assets\transition\transition4.png')
                Change_pic(r'assets\transition\transition5.png')
                Change_pic(r'assets\transition\transition6.png')
                Change_pic(r'assets\transition\transition7.png')
                Change_pic(r'assets\transition\transition7.png')
                pygame.time.wait(2000)

                main_game()

            if id == 2:
                print('lan party')
            if id == 3:
                pygame.quit()
            else:
                pass
    else:
        pygame.draw.rect(main_window, (old_color), (window_x, window_y, box_x, box_y))


# Background for quit
Exit = pygame.draw.rect(main_window, (86,0,0), (625, 825, 260, 60))
Exit_button = pygame.draw.rect(main_window, (255, 0, 0), (630, 830, 250, 50))

# Background for buttons
Background = pygame.draw.rect(main_window, (19,0,77), (320, 393, 260, 65))

# 1-Player Button
One_Player = pygame.draw.rect(main_window, (0,60,130), (325, 400 ,250 ,50)) # window w\h (450, 200,), box w\h (250,50)


#===========================================# Music #===========================================#

pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.90)
pygame.mixer.music.load(r'assets\music\Undertale Papyrus Theme.mp3') # can be in .mp3 format
pygame.mixer.music.play(0)

#===========================================# Intro #===========================================#

open = True
def intro():
    while open:

        cursor = pygame.mouse.get_pos()

        Hover(325, 400 ,250 ,50, (0,60,130), (0, 92, 156), cursor, id = 1)
        Hover(630, 830, 250, 50, (220, 0, 0), (255, 0, 0), cursor, id = 3)
        Assign_Button_Text('Start Game', (255,255,255), 325, 400, 250, 50, 28)
        Assign_Button_Text('Exit Game', (255, 255, 255), 630, 830, 250, 50, 28)

        pygame.display.update()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if 325 + 250 > cursor[0] > 325 and 400 + 50 > cursor[1] > 400 and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(pygame.mixer.Sound(r'assets\click sound.wav'))

#===========================================# END #===========================================#
intro()





