Projet Sudoku Binaire

-Les règles du jeu sont affichées quand on lance le programme et il est possible d’afficher les règles du jeu grâce à une commande.

-Le jeu se joue sur une grille de 6x6 avec 2 types de pions.

-Au début de chaque partie, 6 cases aléatoires de la grille sont pré-remplies et nonchangeables. Le sudoku doit avoir au moins 1 solution possible.

-L’objectif est de remplir la grille avec les pions, sans qu’il y ait plus de 2 pionsconsécutifs (verticalement ou horizontalement) d’un même motif. Il doit y avoir autant depions de chaque couleur sur chaque ligne et chaque colonne (3 pions X et 3 pions O surchaque ligne et sur chaque colonne). Il ne peut pas y avoir 2 lignes ou 2 colonnes, avecexactement le même motif de couleurs (ex: la ligne XOOXOX ne peut apparaître qu’unefois sur les 6 lignes possibles).

-Pour désigner la case, il faut entrer un chiffre, une lettre ou une combinaison des deux.L’ordinateur ne doit pas accepter d’autres types de réponses :

-Si les cases sont numérotées de 1 à 9, on ne peut pas entrer “A” ou “abcedef”

-Si les 2 pions possibles sont O et X, nous ne pouvons pas entrer autre chose.

-Si l’utilisateur entre un input erroné, l’ordinateur demande de répéter l’input.

-La grille est affichée à chaque modification du joueur.

-Il est possible de remodifier une case à laquelle nous avons déjà assignée une couleur.En revanche, il n’est pas possible de modifier les cases préremplies du départ.

-La partie s'arrête automatiquement lorsque la grille est remplie et que la grille respectetoutes les règles.

-A la fin d’une partie, il est possible de rejouer sans avoir à relancer le programme.

-Il est possible de quitter le programme grâce à une commande.

Règles:
    - autant de 1 que de 0 sur chaque ligne et sur chaque colonne ;
    - pas plus de 2 chiffres identiques côte à côte ;
    - 2 lignes ou 2 colonnes ne peuvent être identiques.

fonction qui génére la grille
- fonction qui genere une ligne
possibilite de generer une grille faisable
puis a la fin d'enlever des valeurs randoms

- fonction qui repetee la fonction precedente 6 fois
fonction qui check si la grille est bonne
une liste qui contient les valeurs interdites 
