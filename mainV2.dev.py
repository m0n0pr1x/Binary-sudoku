#Améliorations:
# -Reconstruction des algos avec numpy pour améliorer la vitesse d'execution
# -Implémentation d'une interface graphique
# -Sauvegarder les scores
# -Sauvegarder les grilles

import numpy as np
import random
import cProfile
import timeit





def seed_generator_semirandom(taille):
    while True:
        seed=np.array([0,0,0,1,1,1]*taille).reshape(taille,taille)

        while check_seed(seed,taille)==False:
            for i in seed:
                np.random.shuffle(i) # a changer a
        print(seed)
        continue
            
    return seed

def seed_generator_semirandomV2(taille):
    seed=np.array([[0,0,0,0,1,1,1,1]]*taille)
    while True:
        i=0
        while i < taille:
            np.random.shuffle(seed[i])
            if check_seed(seed,taille)==True:
                return seed
            else:
                i+=1
                
    
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

# sample lists
pattern = ['X','X','X']
mylist = ["X","X","X","O",]

def check_ligneV2(ligne,taille):
    # we want to check all elements of mylist
    # we can stop len(pattern) elements before the end
    pattern=np.array([0,0,0])
    pattern2=np.array([1,1,1])
    for i in range(taille-2):
        # we generate a sublist of mylist, and we compare with list pattern
        #if ligne[i:i+3]==pattern:
            # we print the matches
            #return True
        if np.all(ligne[i:i+3]==pattern) or np.all(ligne[i:i+3]==pattern2):# | ligne[i:i+3]==pattern2):
            return False
    return True


