import pygame
import math
import numpy as np
import random
from time import sleep






def seed_generator_semirandom(taille):
    seed=np.array([0,0,0,1,1,1]*taille).reshape(taille,taille)
    while check_seed(seed,taille)==False:
        for i in seed:
            np.random.shuffle(i) # a changer a
            
    return seed

def unique_matix(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

def check_seed(grille, taille=6):
    temp=[]
    for ligne in grille:
        if check_ligne(ligne, taille) != True :
            return False

    for ligne in grille.T:
        if check_ligne(ligne, taille) != True or check_ligne_doublons(ligne,taille)!=True:
            return False

    return True

def check_ligne(ligne, taille=6):
    """
    verifie les cases cotes a cotes
    """
    doublon = 0
    for i_case in range(taille - 1):
        if (
            ligne[i_case] == ligne[i_case + 1]
            and doublon == 0
        ):
            doublon += 1
            continue
        elif (
            ligne[i_case] == ligne[i_case + 1]
            and doublon == 1
        ):
            # print(f"doublon ligne {ligne}")
            return False
        else:
            doublon = 0

    return True

def check_ligne_doublons(ligne, taille):
    """
    Check si il nya pas de doublons sur la ligne
    """
    # if not('_' in ligne):
    if np.count_nonzero(ligne==1,axis=0) > (taille // 2) or np.count_nonzero(ligne==0,axis=0) > taille // 2:
        return False
    return True

def shaker(grille):
    for ligne_i in range(6):
        temp_i=random.randint(0,5)#on sauvegarde un element au hasard
        temp_symbol=grille[ligne_i][temp_i]
        for i in range(6):
            grille[ligne_i][i]=-1
        grille[ligne_i][temp_i]=temp_symbol
    return grille



def check_ligne_userinput(ligne, taille=6):
    """
    verifie les cases cotes a cotes
    """
    doublon = 0
    for i_case in range(taille - 1):
        if ligne[i_case] == -1:
            continue

        elif (
            ligne[i_case + 1] != -1
            and ligne[i_case] == ligne[i_case + 1]
            and doublon == 0
        ):
            doublon += 1
            continue
        elif (
            ligne[i_case + 1] != -1
            and ligne[i_case] == ligne[i_case + 1]
            and doublon == 1
        ):
            # print(f"doublon ligne {ligne}")
            return False
        else:
            doublon = 0

    return True

def check_dbl(grille, taille=6):
    temp = []
    for ligne in grille:
        if '_' in ligne:
            continue
        if not (ligne in temp):
            temp.append(ligne)
        else:
            print("doublon de lignes")
            return False

    temp = []
    for ligne in reverse_grille(grille, taille):
        if '_' in ligne:
            continue
        if not (ligne in temp):
            temp.append(ligne)
        else:
            print("doublon de colonnes")
            return False

    return True

#-------------------------
#AFFICHAGE
#-------------------------



pygame.init()
WIDTH = 900
ROWS = 6
LINES = 6
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

crash_sound = pygame.mixer.Sound("cute-uwu.mp3")

images = []


X_IMAGE = pygame.transform.scale(pygame.image.load("x.png"), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load("o.png"), (80, 80))
X_init_IMAGE = pygame.transform.scale(pygame.image.load("1_init.png"), (80, 80))
O_init_IMAGE = pygame.transform.scale(pygame.image.load("0_init.png"), (80, 80))
VIDE_IMAGE = pygame.transform.scale(pygame.image.load("vide.png"), (80, 80))
ERREUR = pygame.transform.scale(pygame.image.load("ERREUR.png"), (100, 100))

win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Sudoku Binaire")





def stuffed_grid(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == -1:
                return False

    return True


def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, BLACK, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, BLACK, (0, x), (WIDTH, x), 3)
        
def converter(x):
    if x==-1:
        return VIDE_IMAGE
    elif x==0:
        return O_IMAGE
    elif x==1:
        return X_IMAGE
        


def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2
    forbid=[]
    
    # Initializing the array
    game_array = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None]]
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            # game_array[i][j][2]=seed[i][j]
            if seed[i][j] in [1,0]:
                forbid.append((i,j))
                if seed[i][j]==1:
                    game_array[i][j] = (x, y, seed[i][j], X_init_IMAGE)
                elif seed[i][j]==0:
                    game_array[i][j] = (x, y, seed[i][j], O_init_IMAGE)
            else:
                game_array[i][j] = (x, y, seed[i][j], converter(seed[i][j]))

                #a changer ici pour check ceux deja presents
            
    return game_array,forbid

def seed_grid_filler(game_array):
    
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            game_array[i][j][2]=seed[i][j]
            
            
            
        

def error_event(x,y):
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    win.blit(ERREUR, (x - ERREUR.get_width() // 2, y - ERREUR.get_height() // 2))
    pygame.display.update()
    sleep(0.1)

def error_event_ligne(x,y):
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    temp_x=x
    temp_y=y
    for i in range(taille):
        win.blit(ERREUR, (temp_x - ERREUR.get_width() // 2, temp_y - ERREUR.get_height() // 2))
        temp_x+=150
        temp_y+=150
    pygame.display.update()
    sleep(0.1)
    #A FINIR

def click(game_array,button):
    global x_turn, o_turn, images, taille

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()
    LEFT=1
    RIGHT=3
    
    print(button)
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char,_= game_array[i][j]

            # Distance entre la souris et le centre du carré
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2:  
                if char==-1 and button==LEFT:
                    symbol = 1
                    img= X_IMAGE
                elif char==-1 and button==RIGHT:
                    symbol = 0
                    img= O_IMAGE                 
                elif char==1 and button==LEFT:
                    symbol = -1
                    img= VIDE_IMAGE
                elif char==0 and button==LEFT:
                    symbol = 1
                    img= VIDE_IMAGE
                elif char==1 and button==RIGHT:
                    symbol = 0
                    img= O_IMAGE
                elif char==0 and button==RIGHT:
                    symbol = -1
                    img= VIDE_IMAGE
                    
                
                if (i,j) in forbid:
                    error_event()
                    break
                
                temp = seed.copy()
                temp[i][j] = symbol

                if not(check_ligne_userinput(temp[i], taille)):
                    print("Erreur cote a cote ligne")
                    error_event(x,y)
                    return
                if not (check_ligne_userinput(temp.T[j], taille)):
                    print("Erreur cote a cote colonne")
                    error_event(x,y)
                    return
                
                if not (check_ligne_doublons(temp[i], taille)):
                    print(f"IMPOSSIBLE trop de {symbol} à la ligne {i}")
                    error_event(x,y)
                    return
                if not (check_ligne_doublons(temp.T[j], taille)):
                    print(f"IMPOSSIBLE trop de {symbol} à la colonne {j}")
                    error_event(x,y)
                    return
                
                if check_dbl(temp)
                    print(f"IMPOSSIBLE doublons de colonnes ou lignes")
                    error_event_ligne(x,y)
                    return
            
            
        
                
                
                #A LA FIN SI TOUT EST BON
                game_array[i][j] = (x, y, symbol, img)#problm ici
                seed[i][j] = symbol
                        
    print(seed)
                    
                    
def render(game_array):
    win.fill(WHITE)
    draw_grid()
    #global images

    # Drawing X's and O's
    for ligne in game_array:
        for case in ligne:
            x,y,_,IMAGE=case
            win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()
    
def main():
    global x_turn, o_turn, images, draw, seed, forbid,taille
    
    taille=6
    images = []
    draw = False

    run = True

    seed=shaker(seed_generator_semirandom(6))

    game_array,forbid = initialize_grid()
    render(game_array)
    

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array,event.button)
        if stuffed_grid(game_array):
            main()
            #pygame.quit()
            # a changer avec une condition check win

        render(game_array)


if __name__ == '__main__':
   main()

