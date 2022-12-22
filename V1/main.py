import random

RULES = (
    "- the same number of x's and o's in the same row and same column\n"
    "- a maximum of 2 x's or o's next to each other in the same row or column.\n"
    "- columns and rows must be unique\n"
)


def generateur_grille(taille=6):
    """
    generates an empty grid
    """
    grille = [["_" for i in range(taille)] for j in range(taille)]
    return grille




def affichage(grille=generateur_grille(6)):
    i = 0
    for c in [' ',' ','0','1','2','3','4','5']:
        print(c,end=" ")
    print()
    for c in [' ',' ','—','―','—','—','—','—']:
        print(c,end=" ")
    print()
    for ligne in grille:
        for case in [i]+['|']+ligne+['|']:
            print(case,end=" ")
        print()
        i+=1
    for c in [' ',' ','—','―','—','—','—','—']:
        print(c,end=" ")
    print()

def check_seed(grille, taille=6):
    """
    optimized function to check a seed
    - side-by-side line check on grid
    - line check side acote on inverted grid
    - duplicate line check on inverted grid
    - check duplicate lines on inverted grid

    """
    for ligne in grille:
        if check_ligne_cc(ligne, taille) != True:
            return False

    temp = []
    for ligne in reverse_grille(grille, taille):
        if not (ligne in temp):
            temp.append(ligne)
        else:
            return False

        if (
            check_ligne_cc(ligne, taille) == True
            and check_ligne_doublons(ligne, taille) == True
        ):
            continue
        else:
            return False

    return True


def check_grille_doublons(grille, taille=6):
    """
    checks if there are duplicate rows or columns
    """
    temp = []
    for ligne in grille:
        if "_" in ligne:
            continue
        if not (ligne in temp):
            temp.append(ligne)
        else:
            print("duplicate lines")
            return False

    temp = []
    for ligne in reverse_grille(grille, taille):
        if "_" in ligne:
            continue
        if not (ligne in temp):
            temp.append(ligne)
        else:
            print("duplicate columns")
            return False

    return True


def check_ligne_cc(ligne, taille=6):
    """
    check boxes side by side on a line
    """
    doublon = 0
    for i_case in range(taille - 1):
        if ligne[i_case] == "_":
            continue

        elif (
            ligne[i_case + 1] != "_"
            and ligne[i_case] == ligne[i_case + 1]
            and doublon == 0
        ):
            doublon += 1
            continue
        elif (
            ligne[i_case + 1] != "_"
            and ligne[i_case] == ligne[i_case + 1]
            and doublon == 1
        ):
            return False
        else:
            doublon = 0

    return True


def reverse_grille(grille, taille=6):
    """
    converts columns to rows and rows to columns in a matrix
    """
    grille_r = [["_" for i in range(taille)] for j in range(taille)]
    for i in range(taille):
        for j in range(taille):
            grille_r[i][j] = grille[j][i]
    return grille_r


def seed_generator_semirandom(taille=6):
    """
    this function tries to manage the generation but with 2 rules already taken into account
    """
    grille = []
    temp = []
    doublons = []
    i = 0
    while i < taille:
        for j in range(taille // 2):
            temp.append("X")
        for j in range(taille // 2):
            temp.append("O")
        random.shuffle(temp)
        while temp in doublons:
            random.shuffle(temp)
        doublons.append(temp)
        grille.append(temp)
        temp = []
        i += 1
    return grille


def forbid_giver(grille, taille):
    """
    returns the indices already present in the given grid
    """
    forbid_grille = []
    for i_ligne in range(taille):
        for i_case in range(taille):
            if grille[i_ligne][i_case] in ["O", "X"]:
                forbid_grille.append([i_ligne, i_case])
    return forbid_grille


def collectioner(taille=6):
    """
    function that generates an infinite number of grids I found a valid one
    """
    seed = generateur_grille(taille)
    try:
        while True:
            seed = seed_generator_semirandom(taille)
            if check_seed(seed, taille):
                return seed
    except:
        return


def shaker(grille):
    """
    this function will shuffle the grid, to make it playable
    """
    for ligne_i in range(6):
        temp_i = random.randint(0, 5)
        temp_symbol = grille[ligne_i][temp_i]
        for i in range(6):
            grille[ligne_i][i] = "_"
        grille[ligne_i][temp_i] = temp_symbol
    return grille


def check_ligne_doublons(ligne, taille):
    """
    check if there are no duplicates on the line
    """
    # if not('_' in ligne):
    if ligne.count("X") > taille // 2 or ligne.count("O") > taille // 2:
        return False
    return True


def grille_unpacker(grille, taille):
    """
    unpack the grid, will therefore return all the elements of the matrix as a list
    """
    unpacked_list = []
    for i in grille:
        for j in i:
            unpacked_list.append(j)
    return unpacked_list


def main():
    taille = 6
    print(RULES)
    seed = shaker(collectioner(taille))
    forbid_grille = forbid_giver(seed, taille)
    print("type ctrl+c to exit or 42 to display help")

    while "_" in grille_unpacker(seed, taille):
        affichage(seed)
        choix = [0, 0]
        while 42:
            try:
                choix[0] = int(input("Num ligne: "))
                if choix[0] == 42:
                    print(RULES)
                    continue
                choix[1] = int(input("Num col: "))
                if choix[1] == 42:
                    print(RULES)
                    continue
            except KeyboardInterrupt:
                print()
                print("Goodbye !")
                exit()
            except:
                print("wrong format")
                continue
            if choix in forbid_grille:
                print("forbidden to change the seed")
                continue
            if not (choix[0] in range(6)) or not (choix[1] in range(6)):
                print("bad index")
                continue
            break

        while 42:
            try:
                symbol = input("(X,O,_): ")
                if symbol == "42":
                    print(RULES)
                    continue
            except KeyboardInterrupt:
                print()
                print("Goodbye !")
                exit()
            except:
                print("wrong format")
                continue
            if not (symbol in ["X", "_", "O"]):
                print("wrong symbol")
                continue
            break


        temp = [ligne[:] for ligne in seed]
        temp[choix[0]][choix[1]] = symbol

        if not (check_ligne_cc(temp[choix[0]], taille)):
            print(f"IMPOSSIBLE too many {symbol} side by side on line {choix[0]}")
            continue
        if not (check_ligne_cc(reverse_grille(temp, taille)[choix[1]], taille)):
            print(f"IMPOSSIBLE too many {symbol} side by side on line {choix[1]}:")
            # print(*reverse_grille(temp, taille)[choix[1]], sep="\n")
            continue

        if not (check_ligne_doublons(temp[choix[0]], taille)):
            print(f"IMPOSSIBLE too many {symbol} at the line {choix[0]}")
            continue
        if not (check_ligne_doublons(reverse_grille(temp, taille)[choix[1]], taille)):
            print(f"IMPOSSIBLE too many {symbol} at the column {choix[1]}")
            # print(*reverse_grille(temp, taille)[choix[1]], sep="\n")
            continue

        if check_grille_doublons(temp, taille) == False:
            continue

        seed[choix[0]][choix[1]] = symbol
    affichage(seed)
    print("Bravooooo")
    if input("Would you like to continue: ?\n") in ["Yes", "y", "Y", "yes", "YES"]:
        main()
    else:
        print()
        print("Goodbye !")
        exit()


if __name__ == "__main__":
    main()
