# Othello 
An working Othello game with __numpy__ !
Ce fichier n'est pas un executable, pour jouer il faut l'ouvrir dans un __IDE python 3__
Il faut suivre les indications donnés dans le shell, pour jouer il faut rentrer les coordonés sous la forme __yx (11)__ pour le coin en haut a gauche.
ENJOY !

## Graphism
Pour le moment, le programme ne comporte pas de graphisme mis a part le shell. Les graphismes seront réalisé avec le programme __pyplot__ afin de garder une unité dans le code car __pyplot__ et __numpy__ sont complémentaire.

## Disclaimer
Le jeu n'est qu'a 50% de sont devellopement. Voici donc la liste des fonctionnalités qui arriveront d'ici peu :
- Une interface graphique en pyplot
- Une IA afin d'implementer different modes de jeu
- un fichier en executable avec un menu 
- Une réorganistation du code pour une meilleur compréhension

# Explication du code

### definition de la matrice
la matrice va etre le squellete de notre plateau de jeu, elle va aussi nous servir pour placer les pions.  

Ici nous definnisons notre matrice que l'on nomme Mplateau et nous placons les pions de départ, nous avons 1 pour le pions blanc et 2 pour le noir, i est notre ligne et j notre collone. la variable p est égal a 1 ou 2 en fonction du joueur qui joue.  
```
Mplateau=np.zeros((8,8),int)  
Mplateau[3,3]=1  
Mplateau[4,4]=1   
Mplateau[4,3]=2   
Mplateau[3,4]=2
```   

La fonction nv_plateaux remet la matrice a son état d'origine.  
```
def nv_plateau(Mplateau):   
    Mplateau=np.zeros((8,8),int)  
    Mplateau[3,3]=1   
    Mplateau[4,4]=1  
    Mplateau[4,3]=2   
    Mplateau[3,4]=2  
    return Mplateau
```  


La fonction surplateau nous permet de savoir si les coordonnés saisie se situe bien sur notre plateau.  
```
def surplateau(i, j):  
    return i >= 0 and i <= 7 and j >= 0 and j <=7
```  
    
Cette fonction primaire nous permet d'afficher la matrice dans le shell et sera remplacée a terme par l'interface graphique.  
```
def dessine_plateau(Mplateau):
    print(Mplateau) 
    return Mplateau  
```  
### Modélisation de la capture

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


