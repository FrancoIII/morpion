######################
#   Franco and al.   #
#     interface      #
#  graphique pour le #
#       morpion      #
######################


from tkinter import *
from tkinter.messagebox import *
import IA_morpion_class as mp


def Rond(x1, y1):
#fonction qui permet le dessin du disque
    Canevas.create_oval(x1 - 24, y1 - 24, x1 + 24, y1 + 24,fill="black")


def Croix(x1, y1):
#fonction qui permet le dessin de la croix
       Canevas.create_line(x1 - 24, y1 - 24, x1 + 24, y1 + 24,width=4)
       Canevas.create_line(x1 + 24, y1 - 24, x1 - 24, y1 + 24,width=4)


#variables qui permettent de vérifier la validité ou non des entrées de l'utilisateur
entree_1 = True
entree_2 = True
#choix des dimensions du damier
p =(input("Avec combien de colones voulez-vous jouer?"))
n =(input("Avec combien de lignes voulez-vous jouer"))
try : #vérifie que les nombre de lignes et de colones sont de bon format
    p =int(p)
except:
    print("Les nombres de lignes et de colones doivent être des entiers, veuillez relancer le jeux")
    entree_1 = False
try :
    n =int(n)
except :
    print("Les nombres de lignes et de colones doivent être des entiers, veuillez relancer le jeux")
    entree_2 =False
while entree_1 == False or entree_2 == False :
    p = (input("Avec combien de lignes voulez-vous jouer?"))
    n = (input("Avec combien d'allumettes sur chaque ligne?"))
    try:  # vérifie que les nombre de lignes et de colones sont de bon format
        p = int(n)
        entree_1 = True
    except:
        print("Les nombres de lignes et de colones doivent être des entiers, veuillez relancer le jeux")
        entree_1 = False
    try:
        n = int(n)
        entree_2 = True
    except:
        print("Les nonbres de lignes et de colones doivent être des entiers, veuillez relancer le jeux")
        entree_2 = False


IA_mp = mp.IA_morpion(n, p)


#définition de a: variable globale qui permet de savoir quel joueur joue
rep = input("Voulez-vous commencer?")
#vérfie la validité de l'entrée de l'utilisateur
conforme = True
if rep != "oui" and rep != "o" and rep != "yes" and rep != "y" and rep != "non" and rep != "n" and rep != "no" and rep != "n":
    conforme = False
while conforme == False:
    rep = input("Voulez-vous commencer?")
    if rep == "oui" or rep == "o" or rep == "yes" or rep == "y" or rep == "non" or rep == "n" or rep == "no" or rep == "n":
        conforme = True
# cas où c'est l'adversaire qui commence
if rep == "oui" or rep == "o" or rep == "yes" or rep == "y":  # cas où c'est l'adversaire qui commence
    a = 0
# cas où c'est l'ordinateur qui commence
else :
    a =1

#variable qui permet de stocker les cases déjà occuppées

C = []

Mafenetre = Tk()
Mafenetre.title("Morpion")
# Création d'un widget Canevas
Largeur = p*50
Hauteur = n*50
Canevas = Canvas(Mafenetre, width=Largeur, height=Hauteur, bg="white")

#création des lignes et des colones
for i in range (n+1) :
    Canevas.create_line(0, 50 + 50*i, 50*p, 50 + 50*i, fill="black", width=4)

for j in range (p+1):

    Canevas.create_line(50 + j*50, 50*n, 50*p,-100000000, fill="black", width=4)


#initialisation dans le cas où c'est l'ordinateur qui commence
if a ==1:
    if len(C) == 0:
        coup_ordi = IA_mp.lc2ind(n // 2, p // 2)
        coup_ordi = IA_mp.CoupJouer()
        IA_mp.Cases[coup_ordi] = 1
        IA_mp.UpdateScore(coup_ordi)
        (l_ordi, c_ordi) = IA_mp.ind2lc(coup_ordi)
        Rond(c_ordi * 50 + 25, l_ordi * 50 + 25)
#ajout du coup dans la variable C
        C += [[(coup_ordi * 50), (l_ordi * 50)]]

        if IA_mp.Victoire():
            showinfo(title='Défaite', message='Vous avez perdu')
            Mafenetre.destroy()
        a = 0


def pointeur(event):
#fonction qui permet qui construit la boucle de jeu (activée par clic)
    global a, C, IA_mp

#définit X et Y comme les coordonnées du clic
    X = event.x
    Y = event.y

#cas où c'est à l'utilisateur de jouer
    if a == 0:
#vérifie que la case où l'on a cliqué n'est pas déja occupée, c'est à dire n'est pas dans C
        for i in C :
            if X > i[0] and Y > i[1] and X < (i[0] + 50) and Y < (i[1] + 50):
                showinfo(title='Non', message='Vous ne pouvez pas jouer ici')
                a = 1
        if a == 0 :
#dessine la croix dans la case qui correspond au clic
            Croix(X-X%50+25,Y-Y%50+25)
#ajout dans les variables du morpion
            IA_mp.Cases[IA_mp.lc2ind(Y//50, X//50)] = -1
            IA_mp.UpdateScore(IA_mp.lc2ind(Y//50, X//50))
#vérifie si l'utilisateur a gagné
            if IA_mp.Victoire():
                showinfo(title='Victoire', message='Vous avez gagné')
                Mafenetre.destroy()
#changement de joueur
            a = 1
#ajout de la case à la liste des cases occupées (on stocke les coordonnées du coin à haut à gauche de la case)
            C += [[(X-X%50),(Y-Y%50)]]
#permet de rejouer si l'on a cliqué sur une case déja occupée
        else :
            a =0

#cas où c'est à l'ordinateur de jouer
    if a == 1:

#appel au morpion
        coup_ordi = IA_mp.CoupJouer()
        IA_mp.Cases[coup_ordi] = 1
        IA_mp.UpdateScore(coup_ordi)
        (l_ordi, c_ordi) = IA_mp.ind2lc(coup_ordi)
#dessine le disque dans la case correspondante au jeu du morpion
        Rond(c_ordi * 50 + 25, l_ordi * 50 + 25)
#ajout de la case à la variable C
        C += [[(coup_ordi * 50), (l_ordi * 50)]]
#vérifie si l'ordinateur a gagné
        if IA_mp.Victoire():
            showinfo(title='Défaite', message='Vous avez perdu')
            Mafenetre.destroy()
        a =0


#activation du clic et lancement de la fonction pointeur
Canevas.bind("<Button-1>", pointeur)
Canevas.pack(padx=10, pady=10)


# Création d'un widget Button (bouton Quitter)
Button(Mafenetre, text="Quitter", command=Mafenetre.destroy).pack(side=LEFT, padx=5, pady=5)

Mafenetre.mainloop()
