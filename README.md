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

The `poser_pion` function returns a list defining the color of player 1 and that of player 2. If the first player chooses the color black (2) then the second player will get the color white (1). In addition, the choice of this color will define the color of our first pawn in the matrix via this function.
```
def poser_pion():
    p = 0
    while not (p == '2' or p == '1'):
        print('Entrez 2 pour que les noirs commencent')
        p = input()
    if p == 2:      
        return [2, 1]
    else:           
        return [1, 2]
```  
The `coup_possible` function returns `False` if the move is not possible, ie if the square is not empty (= a 0) or if the pawn is not on the board. To check if a move is possible, this function temporarily places a pawn on the board, where the player wants to play.
```
def coup_possible(Mplateau, p, istart, jstart):
    
    if Mplateau[istart,jstart] != 0 or not surplateau(istart,jstart): 
        return False                           
        
    Mplateau[istart,jstart] = p                
    if p == 1:
        otherP = 2
    else:
        otherP = 1
``` 
Once the move is defined as possible, the program calls the `pion_a_retourner` function. This function has the list of directions. As soon as this function finds a pawn of the opposite color to that of our player, it will go up in its direction, stopping once it leaves the board or when it encounters an empty square which will validate the move and proceed to the capture by changing the color of the pawns until reaching its starting position. In addition, if no pawn has been returned, the move is defined as invalid.
```
    pion_a_retourner = []
    for idirection, jdirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        i, j = istart, jstart
        i += idirection # premier pas dans la direction
        j += jdirection # premier pas dans la direction
        if surplateau(i, j) and Mplateau[i,j] == otherP:   
            i += idirection
            j += jdirection
            if not surplateau(i, j):
                continue
            while Mplateau[i,j] == otherP:
                i += idirection
                j += jdirection
                if not surplateau(i, j):
                    break
            if not surplateau(i, j):
                continue
            if Mplateau[i,j] == p: 
                while True:
                    i -= idirection
                    j -= jdirection
                    if i == istart and j == jstart:
                        break
                    pion_a_retourner.append([i, j])
                    
    Mplateau[istart,jstart] = 0 
    if len(pion_a_retourner) == 0:   
        return False
    return pion_a_retourner
```  
This last function allows to output a list of all the moves possible by a player by using the preceding functions.
```
def donne_coup_possible(Mplateau, p):
    coup_valide = []
    for i in range(8):
        for j in range(8):
            if coup_possible(Mplateau, p, i, j) != False:
                coup_valide.append([i, j])
    return coup_valide
```

### Relative to the stroke

This function allows us to place a pawn on the board by checking thanks to the previous function that the move is valid, this function also returns the pawns when there is a capture.
```
def jouer(Mplateau, p, istart, jstart):
    pion_a_retourner = coup_possible(Mplateau, p, istart, jstart)
    
    if pion_a_retourner == False:
        return False
    
    Mplateau[istart,jstart] = p
    for i, j in pion_a_retourner:
        Mplateau[i,j] = p
    return True
```
The `coup_joueur` function allows the player to choose the move he wants to make and transforms his input number into position [i, j].
```
def coup_joueur(Mplateau, joueurp):# Laissez le joueur taper son coup.# Renvoie le déplacement sous la forme [i, j] 
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split() #permet de prendre les chiffres séparemment
    while True:
        print('entrer le coup')
        move = input().lower()
        
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            i = int(move[0]) - 1
            j = int(move[1]) - 1
            if coup_possible(Mplateau, joueurp, i, j) == False:
                continue
            else: 
                break
        else:
             print("Ce n'est pas un coup possible.")
             
    return [i, j]
```

### Jouer(jeu et definition de qui joue)

This basic function allows you to define who plays first regardless of the color chosen in the shell (dev function)
```
def first_joueur(): #le joueur qui commence.
        return 'joueur2'
```
This function allows you to count the number of black pawns on the board (1 pawn = 1 point).
```
def nscores(Mplateau):
    global nscore
    nscore =0
    for i in range(8):
        for j in range(8):
            if Mplateau[i,j] == 2:
                nscore += 1
    print(nscore)
```
This function allows you to count the number of white pawns on the board (1 pawn = 1 point).
```
def bscores(Mplateau):
    global bscore
    bscore = 0
    for i in range(8):
        for j in range(8):
            if Mplateau[i,j] == 1:
                bscore += 1
    print(bscore)
```
This function is a point counter, it compares the results of the two previous functions: `nscores` and` bscores`.
```
def qui_gagne(bscores, nscores):
    if nscore > bscore:
        print('les noirs ont gagnes!')
    elif nscore < bscore:
        print('les blancs ont gagnes!')
    else:
        print('Egalite!')
```

### script principal pour jouer dans le shell

This part of the code is the main loop, it is this part that allows everything to be coordinated and made so that the players can take their turns, while saying when no more moves are possible.
```
print('Bienvenue sur OTHELLO !')

while True:
    mainBoard = nv_plateau(Mplateau) # Réinitialisez le plateau et le jeu.
    
    joueur1, joueur2 = poser_pion()
    turn = first_joueur()
    print('Le ' + turn + ' commence.')
    
    while True:
        if turn == 'joueur1': 
            dessine_plateau(Mplateau)
            move = coup_joueur(Mplateau, 1)
            jouer(Mplateau, 1, move[0], move[1])
            if donne_coup_possible(Mplateau, 2) == []:
                break
            else:
                turn = 'joueur2'
                        
        else:
            dessine_plateau(Mplateau)
            move = coup_joueur(Mplateau, 2)
            jouer(Mplateau, 2, move[0], move[1])
            if donne_coup_possible(Mplateau, 1) == []:
                break
            else:
                turn = 'joueur1'
```
Once no more moves are possible, the board is displayed with the last pawn placed and the cores are counted in order to define who has won.
```                             
    dessine_plateau(Mplateau) # Afficher le plateau avec le dernier pion posé (final).
    print('la partie est fini !')
    print('score des noirs :')
    nscores(Mplateau)
    print('score des blancs :')
    bscores(Mplateau)
    qui_gagne(bscores, nscores)
    break
```
