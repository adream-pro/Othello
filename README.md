# Othello with Numpy and matrix !
An working Othello game with __numpy__ !
This file is not an executable, to play it must be opened in a __IDE python 3__
You have to follow the instructions given in the shell, to play you have to enter the coordinates in the form __yx (11)__ for the top left corner.
ENJOY!

## Graphics
For the moment, the program does not include any graphics except the shell. The graphics will be made with the __pyplot__ program in order to keep a unit in the code because __pyplot__ and __numpy__ are complementary.

## Disclaimer
The game is only 50% of its development. Here is the list of features that will arrive shortly:
- A pyplot graphical interface
- An AI to implement different game modes
- an executable file with a menu
- A reorganization of the code for a better understanding

# Explanation of the code

### definition of the matrix
the matrix will be the squellete of our game board, it will also be used to place the pawns.  

Here we define our matrix which we call `Mplateau` and we place the starting pawns, we have 1 for the white pawns and 2 for the black, i is our row and j our collone. the variable p is equal to 1 or 2 depending on the player who is playing.
```
Mplateau=np.zeros((8,8),int)  
Mplateau[3,3]=1  
Mplateau[4,4]=1   
Mplateau[4,3]=2   
Mplateau[3,4]=2
```   

The `nv_plateaux` function returns the matrix to its original state.   
```
def nv_plateau(Mplateau):   
    Mplateau=np.zeros((8,8),int)  
    Mplateau[3,3]=1   
    Mplateau[4,4]=1  
    Mplateau[4,3]=2   
    Mplateau[3,4]=2  
    return Mplateau
```  


The `surplateau` function allows us to know if the coordinates entered is well on our board.  
```
def surplateau(i, j):  
    return i >= 0 and i <= 7 and j >= 0 and j <=7
```  
    
This primary function allows us to display the matrix in the shell and will eventually be replaced by the graphical interface.
```
def dessine_plateau(Mplateau):
    print(Mplateau) 
    return Mplateau  
```  
### Capture modeling

```
def poser_pion():# Renvoie une liste avec le pion du joueur comme premier élément et le pion du second joueur comme second
    p = 0
    while not (p == '2' or p == '1'):
        print('Entrez 2 pour que les noirs commencent')
        p = input()
    if p == 2:      # le premier élément de la liste est le pion du joueur2, le second est le pion du joueur 1.
        return [2, 1]
    else:           # joueur 1 puis joueur 2 
        return [1, 2]
```  

```
def coup_possible(Mplateau, p, istart, jstart):
    
    if Mplateau[istart,jstart] != 0 or not surplateau(istart,jstart): # Renvoie False si le mouvement du joueur sur l'espace istart, jstart n'est pas valide.
        return False                            # S'il s'agit d'un coup valide, renvoie une liste d'espaces qui deviendraient ceux du joueur s'il effectuait un mouvement ici.
        
    Mplateau[istart,jstart] = p                 # place temporairement le pion sur le plateau.
    if p == 1:
        otherP = 2
    else:
        otherP = 1
``` 

```
    pion_a_retourner = []
    for idirection, jdirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        i, j = istart, jstart
        i += idirection # premier pas dans la direction
        j += jdirection # premier pas dans la direction
        if surplateau(i, j) and Mplateau[i,j] == otherP:   # Il y a une pièce appartenant à l'autre joueur à côté de notre pièce
            i += idirection
            j += jdirection
            if not surplateau(i, j):
                continue
            while Mplateau[i,j] == otherP:
                i += idirection
                j += jdirection
                if not surplateau(i, j): # sortir de la boucle while, puis continuer dans la boucle for
                    break
            if not surplateau(i, j):
                continue
            if Mplateau[i,j] == p: # Il y a des pièces à retourner. Allez dans le sens inverse jusqu'à ce que nous atteignions la case de départ, en notant toutes les pions le long du chemin.
                while True:
                    i -= idirection
                    j -= jdirection
                    if i == istart and j == jstart:
                        break
                    pion_a_retourner.append([i, j])
                    
    Mplateau[istart,jstart] = 0 # restaure l'espace vide
    if len(pion_a_retourner) == 0:   # Si aucun pion n'a été retournée, ce n'est pas un coup valide.
        return False
    return pion_a_retourner
```  

```
def donne_coup_possible(Mplateau, p):# Renvoie une liste de [i, j] listes de coups valides pour le joueur donné sur le plateau donné.
    coup_valide = []
    for i in range(8):
        for j in range(8):
            if coup_possible(Mplateau, p, i, j) != False:
                coup_valide.append([i, j])
    return coup_valide
```


