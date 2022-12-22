import pygame
import math
import numpy as np
import random
from time import sleep
from constants import *


def seed_generator_semirandom(grid_size):
    """
    Generate a random grid but with 1 requirements satisfied:
    the number of X and O on the same line must be equal
    """
    seed = np.array([0, 0, 0, 1, 1, 1] * grid_size).reshape(grid_size, grid_size)
    while check_seed(seed, grid_size) == False:
        for i in seed:
            np.random.shuffle(i)

    return seed


def check_seed(grid, grid_size=6):
    temp = []
    for ligne in grid:
        if check_ligne(ligne, grid_size) != True:
            return False

    for ligne in grid.T:
        if (
            check_ligne(ligne, grid_size) != True
            or check_ligne_doublons(ligne, grid_size) != True
        ):
            return False

    return True


def check_ligne(ligne, grid_size=6):
    """
    this is only for the generation of the grid, its faster
    """
    doublon = 0
    for i_case in range(grid_size - 1):
        if ligne[i_case] == ligne[i_case + 1] and doublon == 0:
            doublon += 1
            continue
        elif ligne[i_case] == ligne[i_case + 1] and doublon == 1:
            return False
        else:
            doublon = 0

    return True


def check_ligne_doublons(ligne, grid_size):
    """
    this is only for the generation of the grid, its faster
    """
    if (
        np.count_nonzero(ligne == 1, axis=0) > (grid_size // 2)
        or np.count_nonzero(ligne == 0, axis=0) > grid_size // 2
    ):
        return False
    return True


def shaker(grid):
    for ligne_i in range(6):
        temp_i = random.randint(0, 5)
        temp_symbol = grid[ligne_i][temp_i]
        for i in range(6):
            grid[ligne_i][i] = -1
        grid[ligne_i][temp_i] = temp_symbol
    return grid


def check_ligne_userinput(ligne, grid_size=6):
    """
    check the boxes side by side
    """
    doublon = 0
    for i_case in range(grid_size - 1):
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
            return False
        else:
            doublon = 0

    return True

def check_dbl(grid, grid_size=6):
    temp = [0 for i in range(grid_size)]
    temp_grid = grid.tolist()
    for i_ligne in range(grid_size):
        if -1 in temp_grid[i_ligne]:
            continue
        if not (temp_grid[i_ligne] in temp):

            temp[i_ligne] = temp_grid[i_ligne]
        else:
            return temp.index(temp_grid[i_ligne]), i_ligne
    return False


# -------------------------
# GUI
# -------------------------


pygame.init()

ROWS = 6
LINES = 6

win = pygame.display.set_mode((WIDTH, WIDTH))


def reverse_game_array(game_array, grid_size=6):
    """
    permet de transformer les colonnes en lignes dans une matrice
    """
    game_array_r = [[(0, 0, 0, 0) for i in range(grid_size)] for j in range(grid_size)]
    for i in range(grid_size):
        for j in range(grid_size):
            game_array_r[i][j] = game_array[j][i]
    return game_array_r


def stuffed_grid(game_array):
    """
    check if the grid is full
    """
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == -1:
                return False

    return True


def draw_grid():
    """
    draw the grid, lines and columns
    """
    gap = WIDTH // ROWS

    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, BLACK, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, BLACK, (0, x), (WIDTH, x), 3)


def converter(x):
    """
    return the image to display according to the input in the grid
    """
    if x == -1:
        return VIDE_IMAGE
    elif x == 0:
        return O_IMAGE
    elif x == 1:
        return X_IMAGE


def initialize_grid():
    """
    initialize the grid for the first time
    """
    dis_to_cen = WIDTH // ROWS // 2
    forbid = []

    # Initializing the array
    game_array = [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)


            if seed[i][j] in [1, 0]:
                forbid.append((i, j))
                if seed[i][j] == 1:
                    game_array[i][j] = (x, y, seed[i][j], X_init_IMAGE)
                elif seed[i][j] == 0:
                    game_array[i][j] = (x, y, seed[i][j], O_init_IMAGE)
            else:
                game_array[i][j] = (x, y, seed[i][j], converter(seed[i][j]))


    return game_array, forbid


def seed_grid_filler(game_array):
    """
    fill the grid with the seed
    """
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            game_array[i][j][2] = seed[i][j]


def get_symbol_image(char, button):
    """
    Transform the img into the corresponding symbol and vice-versa
    by detecting wich mouse button has been pressed
    """
    LEFT = 1  # left mouse button
    RIGHT = 3  # right mouse button
    if char == -1 and button == LEFT:
        symbol = 1
        img = X_IMAGE
    elif char == -1 and button == RIGHT:
        symbol = 0
        img = O_IMAGE
    elif char == 1 and button == LEFT:
        symbol = -1
        img = VIDE_IMAGE
    elif char == 0 and button == LEFT:
        symbol = -1
        img = VIDE_IMAGE
    elif char == 1 and button == RIGHT:
        symbol = -1
        img = VIDE_IMAGE
    elif char == 0 and button == RIGHT:
        symbol = -1
        img = VIDE_IMAGE
    return img, symbol


def error_event(x, y):
    """
    Make the case at coordonates x,y blink red for 0.1 second
    """
    pygame.mixer.Sound.play(pygame.mixer.Sound(CRASH_SOUND))
    pygame.mixer.music.stop()
    win.blit(ERREUR, (x - ERREUR.get_width() // 2, y - ERREUR.get_height() // 2))
    pygame.display.update()
    sleep(0.1)


def error_event_ligne(ligne_array):
    """
    Make the ligne_array blink red for 0.1 second
    """
    pygame.mixer.Sound.play(pygame.mixer.Sound(CRASH_SOUND))
    pygame.mixer.music.stop()
    for i in range(grid_size):
        x, y, _, _ = ligne_array[i]
        win.blit(ERREUR, (x - ERREUR.get_width() // 2, y - ERREUR.get_height() // 2))
    draw_grid()
    pygame.display.update()


def click(game_array, button):
    """
    do actions according to user input
    """
    global x_turn, o_turn, images, grid_size

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()
    try:
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x, y, char, img = game_array[i][j]

                # Distance between the mouse and the center of the square
                dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

                # If it's inside the square
                if dis < WIDTH // ROWS // 2:
                    img, symbol = get_symbol_image(char, button)

                    if (i, j) in forbid:
                        # Check if the user tries to change the seed
                        error_event(x, y)
                        return

                    # Create a copy of the grid
                    temp = seed.copy()
                    temp[i][j] = symbol

                    # Execute multiple checks to see if the new grid with the user input is valid
                    # Check for three 1 or three 0 by lines
                    if not (check_ligne_userinput(temp[i], grid_size)):

                        # print("Erreur cote a cote ligne")
                        error_event(x, y)
                        return
                    # Check for three 1 or three 0 by columns
                    if not (check_ligne_userinput(temp.T[j], grid_size)):
                        # print("Erreur cote a cote colonne")
                        error_event(x, y)
                        return

                    # Check the number of 0s and 1s by lines
                    if not (check_ligne_doublons(temp[i], grid_size)):
                        # print(f"IMPOSSIBLE trop de {symbol} à la ligne {i}")
                        error_event(x, y)
                        return
                    # Check the number of 0s and 1s by columns
                    if not (check_ligne_doublons(temp.T[j], grid_size)):
                        # print(f"IMPOSSIBLE trop de {symbol} à la colonne {j}")
                        error_event(x, y)
                        return

                    # Check for duplicated lines
                    doublons_l = check_dbl(temp)
                    if doublons_l != False:
                        # print(f"IMPOSSIBLE doublons de colonnes ou lignes")
                        # Make the 2 duplicated lines blink red
                        error_event_ligne(game_array[doublons_l[0]])
                        error_event_ligne(game_array[doublons_l[1]])
                        sleep(0.1)
                        return

                    # Check for duplicated columns
                    doublons_c = check_dbl(temp.T)
                    if doublons_c != False:
                        # print(f"IMPOSSIBLE doublons de colonnes ou lignes")
                        # Make the 2 duplicated columns blink red
                        error_event_ligne(reverse_game_array(game_array)[doublons_c[0]])
                        error_event_ligne(reverse_game_array(game_array)[doublons_c[1]])
                        sleep(0.1)
                        return

                    # If everything is ok with the temporary grid we make
                    # changes to the real one
                    game_array[i][j] = (x, y, symbol, img)
                    seed[i][j] = symbol
                    # To avoid breaking the program by typing too fast
                    sleep(0.05)

    except:
        pass


def render(game_array):
    """
    render the game
    """
    # Fill the background with white
    win.fill(WHITE)
    # Draw the grid
    draw_grid()

    # Drawing 1s and Os and Void by ther images
    for line in game_array:
        for case in line:
            x, y, _, IMAGE = case
            win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()


def main():
    global seed, forbid, grid_size
    pygame.display.set_caption("Binary Suodku")

    grid_size = 6

    seed = shaker(seed_generator_semirandom(6))

    game_array, forbid = initialize_grid()
    render(game_array)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array, event.button)
        if stuffed_grid(game_array):
            render(game_array)
            pygame.mixer.Sound.play(pygame.mixer.Sound(VICTORY_SOUND))
            pygame.mixer.music.stop()
            win.blit(VICTORY, (150, 350))
            pygame.display.update()
            sleep(3)
            render(game_array)
            main()

        render(game_array)


if __name__ == "__main__":
    main()
