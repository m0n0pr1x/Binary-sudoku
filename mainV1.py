import random

RULES=\
"- The same number of X and O's on the same line and column\n" \
"- A maximum of 2 X's or O's next to each other on the same line or column\n"\
"- Columns and lines must be unique\n"\

def generateur_grille(taille=6):
    grille = [["_" for i in range(taille)] for j in range(taille)]
    return grille


def affichage(grille=generateur_grille(6)):
    print("-" * 34)
    c=0
    for i in ([[" ","0","1","2","3","4","5"]]+ grille):
        if c==0:
            print(i)
        else:
            print([f"{c-1}"]+i)
        c+=1
    print("-" * 34)


def check_seed(grille, taille=6):
    """
    fonction optimisée pour checker une seed

    - check ligne_cote_acote sur grille
    - check ligne_cote_acote sur grille inversée
    - check ligne_doublons sur grille inversée
    - check lignes dupliquées sur grille inversée

    """
    # temp = []
    for ligne in grille:
        #         if not (ligne in temp):
        #             temp.append(ligne)
        #         else:
        #             return False

        #         if check_ligne(ligne, taille)==True :
        #             continue
        #         else:
        #             return False
        if check_ligne(ligne, taille) != True:
            return False

    temp = []
    for ligne in reverse_grille(grille, taille):
        if not (ligne in temp):
            temp.append(ligne)
        else:
            return False

        if (
            check_ligne(ligne, taille) == True
            and check_ligne_doublons(ligne, taille) == True
        ):
            continue
        else:
            # print(f"erreur ligne {ligne}")
            return False

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


def check_ligne(ligne, taille=6):
    """
    verifie les cases cotes a cotes
    """
    doublon = 0
    compteur = [ligne.count("O"), ligne.count("X")]  # 0 et 1
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
            # print(f"doublon ligne {ligne}")
            return False
        else:
            doublon = 0

    return True


def reverse_grille(grille, taille=6):
    """
    permet de transformer les colonnes en lignes dans une matrice
    """
    grille_r = [["_" for i in range(taille)] for j in range(taille)]
    for i in range(taille):
        for j in range(taille):
            grille_r[i][j] = grille[j][i]
    return grille_r

def seed_generator_semirandom(taille=6):
    """
    Cette fonction essaye de gerer la génération mais avec 2 regles pas de doublons
    et pas de trop de x et trop de O seulement pour les lignes !

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
    here the grille given is already a seed
    A OPTIMISER EN LISTE PAR COMPREHENSION
    """
    forbid_grille = []
    for i_ligne in range(taille):
        for i_case in range(taille):
            if grille[i_ligne][i_case] in ["O", "X"]:
                forbid_grille.append([i_ligne, i_case])
    return forbid_grille




def collectioner(taille=4):
    seed = generateur_grille(taille)
    seed_list = []
    compteur = 0
    try:
        while compteur <= 400:
            seed = seed_generator_semirandom(taille)
            if check_seed(seed, taille):
                # print(affichage(seed))
                return seed
                seed_list.append(seed)
                compteur += 1
    except:
        pass
    return seed_list


def shaker(grille):
    for ligne_i in range(6):
        temp_i=random.randint(0,5)#on sauvegarde un element au hasard
        temp_symbol=grille[ligne_i][temp_i]
        for i in range(6):
            grille[ligne_i][i]='_'
        grille[ligne_i][temp_i]=temp_symbol
    return grille
        


def check_ligne_doublons(ligne, taille):
    """
    Check si il nya pas de doublons sur la ligne
    """
    # if not('_' in ligne):
    if ligne.count("X") > taille // 2 or ligne.count("O") > taille // 2:
        return False
    return True


def grille_unpacker(grille, taille):
    """
    unpack la grille
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
    
    while  (
        "_" in grille_unpacker(seed, taille)
    ):
        # try:
        affichage(seed)
        choix=[0,0]
        while 42:
            try:
                choix[0] = int(input("Num ligne: "))
                choix[1] = int(input("Num colonne: "))
            except KeyboardInterrupt:
                print()
                print("Goodbye !")
                exit()
            except:
                print("Mauvais format")
                continue
            if choix in forbid_grille:
                print("Interdit de changer la seed")
                continue
            if not(choix[0] in range(6)) or not(choix[1] in range(6)):
                print("Mauvais indice")
                continue
            break
            
        while 42:
            try:
                symbol = input("(X,O,_): ")
            except KeyboardInterrupt:
                print()
                print("Goodbye !")
                exit()
            except:
                print("Mauvais format")
                continue
            if not(symbol in ['X','_','O']):
                print("Mauvais symbol")
                continue
            break
                

        # temp = seed.copy()
        temp = [ligne[:] for ligne in seed]
        temp[choix[0]][choix[1]] = symbol

        if not (check_ligne(temp[choix[0]], taille)):
            print(f"IMPOSSIBLE trop de {symbol} cotes à cotes à la ligne {choix[0]}")
            continue
        if not (check_ligne(reverse_grille(temp, taille)[choix[1]], taille)):
            print(f"IMPOSSIBLE trop de {symbol} cotes à cotes à la colonne {choix[1]}:")
            #print(*reverse_grille(temp, taille)[choix[1]], sep="\n")
            continue

        if not (check_ligne_doublons(temp[choix[0]], taille)):
            print(f"IMPOSSIBLE trop de {symbol} à la ligne {choix[0]}")
            continue
        if not (check_ligne_doublons(reverse_grille(temp, taille)[choix[1]], taille)):
            print(f"IMPOSSIBLE trop de {symbol} à la colonne {choix[1]}")
            #print(*reverse_grille(temp, taille)[choix[1]], sep="\n")
            continue
        
        if check_dbl(temp,taille) == False:
            continue

        seed[choix[0]][choix[1]] = symbol
    affichage(seed)
    print("Bravooooo")
    if input("Voulez vous continuez: ?\n") in ["Oui","o","O","oui","OUI"]:
        main()
    else:
        print()
        print("Goodbye !")
        exit()



