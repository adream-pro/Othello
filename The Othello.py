##Importations
import numpy as np
import os
import matplotlib.pyplot as plt
import random
import sys

##plateau

Mplateau=np.zeros((8,8),int)
Mplateau[3,3]=1
Mplateau[4,4]=1 #pion blanc
Mplateau[4,3]=2 
Mplateau[3,4]=2 #pion noir

#p=1 ou 2 en fonction du joueur/ i= numero ligne/ j=numero colone

def nv_plateau(Mplateau): # Efface le tableau sur lequel il est passé, sauf pour la position de départ d'origine.
    Mplateau=np.zeros((8,8),int)
    Mplateau[3,3]=1 # Pièces de départ:
    Mplateau[4,4]=1 #pion blanc
    Mplateau[4,3]=2 
    Mplateau[3,4]=2 #pion noir
    return Mplateau

def surplateau(i, j):  # Renvoie True si les coordonnées se trouvent sur la carte.
    return i >= 0 and i <= 7 and j >= 0 and j <=7
    
def dessine_plateau(Mplateau):
    print(Mplateau)
    return Mplateau
    
##modelisation de la capture
def poser_pion():# Renvoie une liste avec le pion du joueur comme premier élément et le pion du second joueur comme second
    p = 0
    while not (p == '2' or p == '1'):
        print('Entrez 2 pour que les noirs commencent')
        p = input()
    if p == 2:      # le premier élément de la liste est le pion du joueur2, le second est le pion du joueur 1.
        return [2, 1]
    else:           # joueur 1 puis joueur 2 
        return [1, 2]

def coup_possible(Mplateau, p, istart, jstart):
    
    if Mplateau[istart,jstart] != 0 or not surplateau(istart,jstart): # Renvoie False si le mouvement du joueur sur l'espace istart, jstart n'est pas valide.
        return False                            # S'il s'agit d'un coup valide, renvoie une liste d'espaces qui deviendraient ceux du joueur s'il effectuait un mouvement ici.
        
    Mplateau[istart,jstart] = p                 # place temporairement le pion sur le plateau.
    if p == 1:
        otherP = 2
    else:
        otherP = 1
    
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

def donne_coup_possible(Mplateau, p):# Renvoie une liste de [i, j] listes de coups valides pour le joueur donné sur le plateau donné.
    coup_valide = []
    for i in range(8):
        for j in range(8):
            if coup_possible(Mplateau, p, i, j) != False:
                coup_valide.append([i, j])
    return coup_valide
    
##relatif a la pose

def jouer(Mplateau, p, istart, jstart):# Placez le pion sur le plateau à istart, jstart et retournez n'importe quelle pièce de l'adversaire. # Renvoie False s'il s'agit d'un déplacement non valide, True s'il est valide.
    pion_a_retourner = coup_possible(Mplateau, p, istart, jstart)
    
    if pion_a_retourner == False:
        return False
    
    Mplateau[istart,jstart] = p
    for i, j in pion_a_retourner:
        Mplateau[i,j] = p
    return True
    
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

        
##jouer(jeu et definition de qui joue)
        
def first_joueur(): #le joueur qui commence.
        return 'joueur2'
    
def nscores(Mplateau):
    global nscore
    nscore =0
    for i in range(8):
        for j in range(8):
            if Mplateau[i,j] == 2:
                nscore += 1
    print(nscore)

def bscores(Mplateau):
    global bscore
    bscore = 0
    for i in range(8):
        for j in range(8):
            if Mplateau[i,j] == 1:
                bscore += 1
    print(bscore)
    
def qui_gagne(bscores, nscores):
    if nscore > bscore:
        print('les noirs ont gagnes!')
    elif nscore < bscore:
        print('les blancs ont gagnes!')
    else:
        print('Egalite!')
    
    
    
##script principal pour jouer dans le shell

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
                                 
    dessine_plateau(Mplateau) # Afficher le plateau avec le dernier pion posé (final).
    print('la partie est fini !')
    print('score des noirs :')
    nscores(Mplateau)
    print('score des blancs :')
    bscores(Mplateau)
    qui_gagne(bscores, nscores)
    break
    