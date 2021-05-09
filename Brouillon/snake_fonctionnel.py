import tkinter as tk
import random
import os

################CONSTANTES################################################################
WIDTH = 800
HEIGHT = 600
taille_case = 40
dirX = -1
dirY = 0
score = 0
fonte = ("Kristen ITC","24")
fonteListe = ("Kristen ITC","16")
couleurFond = "darkgrey"
couleurBoutonSelect = "green"
couleurBoutonDefaut = "SystemButtonFace"
delaiLent = 200
delaiMoyen = 150
delaiRapide = 100
###########VARIABLES########################################################################
pommes = []
murs = []
global delai
global idSerpent 
idSerpent = []
delai = 100
###########FONCTIONS###########################################################################       
def importerNiveaux():
    """Permet d'importer les différents niveaux(en format ".txt") dans le menu"""
    listeFichier = os.listdir()
    niveaux = []
    for fichier in listeFichier:
        if fichier[0:6] == "niveau":
            niveaux.append(fichier)
    for n in niveaux:
        listeNiveaux.insert(tk.END,n)
    if len(niveaux):
        listeNiveaux.select_set(0)
    listeNiveaux.config(height=len(niveaux))
    return listeNiveaux

def lent():
    """Pour de sélectionner dans le menu principale la vitesse (lente) du serpent et donc le niveau de difficulté"""
    global delai
    btLent.config(bg=couleurBoutonSelect)
    btMoyen.config(bg=couleurBoutonDefaut)
    btRapide.config(bg=couleurBoutonDefaut)
    delai = delaiLent

def moyen():
    """Pour de sélectionner dans le menu principale la vitesse (moyenne) du serpent et donc le niveau de difficulté"""
    global delai
    btLent.config(bg=couleurBoutonDefaut)
    btMoyen.config(bg=couleurBoutonSelect)
    btRapide.config(bg=couleurBoutonDefaut)
    delai = delaiMoyen

def rapide():
    """Pour de sélectionner dans le menu principale la vitesse (rapide) du serpent et donc le niveau de difficulté"""
    global delai
    btLent.config(bg=couleurBoutonDefaut)
    btMoyen.config(bg=couleurBoutonDefaut)
    btRapide.config(bg=couleurBoutonSelect)
    delai = delaiRapide

def jouer():
    """Lance la partie dans une nouvelle fenêtre et suprimme la fenêtre "menu". """
    nomFichier = listeNiveaux.get(listeNiveaux.curselection())
    panMenu.destroy()
    decors(nomFichier)
    deplacement_serpent_auto()
    panJeu.pack()

def decors(nomFichier):
    """Génération du décor correspondant au niveau pré-sélectionné dans le menu principal"""
    global murs, pomme, serpent, idSerpent
    serpent = []
    x, y = 0, 0
    niveau = open(nomFichier)
    for ligne in niveau:
        for i in range(len(ligne)):
            case = ligne[i]
            if case == "X":
                temp = env_jeu.create_rectangle(x, y, x+40, y+40, fill='black')
                murs.append(temp)
            elif case == "P":
                pomme = env_jeu.create_oval(x, y, x+40, y+40, fill='red')
            elif case == "T":
                idSerpent.append(env_jeu.create_rectangle(x, y, x+40, y+40, fill='green'))
            elif case == "Q":
                idSerpent.append(env_jeu.create_rectangle(x, y, x+40, y+40, fill='green'))
            x += 40
        x = 0
        y += 40
    serpent = [env_jeu.coords(idSerpent[0]), env_jeu.coords(idSerpent[-1])]
    niveau.close()

def deplacement_serpent_auto():
    """Déplace de manière continue le serpent sur le canevas"""
    global murs, pomme, dirX, dirY, serpent, prochaines_coords, coords_murs, delai
    coords_murs = []
    prochaines_coords = [(serpent[0][0] + dirX * taille_case), (serpent[0][1] + dirY * taille_case), 
    (serpent[0][2] + dirX * taille_case), (serpent[0][3] + dirY * taille_case)] 
    for i in murs:
        coords_murs.append(env_jeu.coords(i))
        
    serpent.insert(0, prochaines_coords) 
    serpent.remove(serpent[-1])

    for i in range(len(serpent)):
        env_jeu.coords(idSerpent[i], serpent[i])

    manger_pomme()
    percuter()
    snake.after(delai, deplacement_serpent_auto)

def deplacement_serpent_up():
    """Modifie la direction du serpent vers le haut sur le canevas"""
    global dirX, dirY
    dirX, dirY = 0, -1 

def deplacement_serpent_down():
    """Modifie la direction du serpent vers la bas sur le canevas"""
    global dirX, dirY
    dirX, dirY = 0, 1
    
def deplacement_serpent_right():
    """Modifie la direction du serpent vers la droite sur le canevas"""
    global dirX, dirY
    dirX, dirY = 1, 0 
    
def deplacement_serpent_left():
    """Modifie la direction du serpent sur le canevas"""
    global dirX, dirY
    dirX, dirY = -1, 0

def manger_pomme():
    """Ajout d'une nouvelle pomme et des actions qui en découlent, selon les règles données dans les consignes"""
    global pomme, score, serpent, murs, prochaines_coords, dirX, dirY, idSerpent
    if env_jeu.coords(pomme) == serpent[0]:
        x_rd = random.randint(1,18)
        y_rd = random.randint(1,13)
        x_centre = (x_rd*taille_case + x_rd*taille_case + taille_case)//2 
        y_centre = (y_rd*taille_case + y_rd*taille_case + taille_case)//2
        while (idSerpent[0] or idSerpent[-1]) in env_jeu.find_overlapping(x_centre, y_centre,x_centre, y_centre) : 
            for i in murs :
                if i in env_jeu.find_overlapping(x_centre, y_centre,x_centre, y_centre) :
                    x_rd = random.randint(1,18)
                    y_rd = random.randint(1,13)
                    x_centre = (x_rd*taille_case + x_rd*taille_case + taille_case)//2 
                    y_centre = (y_rd*taille_case + y_rd*taille_case + taille_case)//2
        env_jeu.coords(pomme, x_rd*taille_case, y_rd*taille_case, x_rd*taille_case + taille_case, y_rd*taille_case + taille_case)
        serpent.append(serpent[-1])
        idSerpent.append(env_jeu.create_rectangle(serpent[-1], fill="green"))
        #score += 1
        #utiliser cette variable score pour pouvoir Sauvegarder (Rania)

def percuter():
    """Prend en compte la percussion de la tête avec un autre item du canvas, puis termine la partie ou non selon les règles données dans les consignes."""
    global serpent
    x_tete, y_tete, x1_tete, y1_tete = serpent[0]
    x_centre = (x_tete + x1_tete)//2 
    y_centre = (y_tete + y1_tete)//2
    for mur in murs :
        if mur in env_jeu.find_overlapping(x_centre, y_centre, x_centre, y_centre) : 
            perduhahatnul()

    for i in range(1, len(idSerpent)):
        if idSerpent[i] in env_jeu.find_overlapping(x_centre, y_centre, x_centre, y_centre)  :
            perduhahatnul()

def perduhahatnul():
    """Termine la partie et affiche un nouveau menu pour choisir si l'on veut: rejouer, revenir au menu ou bien sauvegarder son score."""
    env_jeu.delete("all")
    env_jeu.config(bg="black")
    env_jeu.create_text(WIDTH//2, HEIGHT//3, text="PERDU", fill="red", font=('system', '45'))
    env_jeu.create_text(WIDTH//2, HEIGHT//2.25, text="Votre score : "+str(score), fill="white", font=('Lucida Console', '15'))
    replay=tk.Button(text="Rejouer", fg="white", bg="black", relief="raised", font=("Lucida Console","20") )
    replay.place(x= WIDTH//2.4,y=HEIGHT//1.7)
    backto=tk.Button(text="Revenir au menu", fg="white", bg="black", relief="raised", font=("Lucida Console","20") )
    backto.place(x= WIDTH//2.9,y=HEIGHT//1.48)
    sauvegardescore=tk.Button(text="Sauvegarder votre score", fg="white", bg="black", relief="raised", font=("Lucida Console","20") )
    sauvegardescore.place(x= WIDTH//3.9,y=HEIGHT//2)
    #rendre les boutons fonctionnels

################################################################################################################          
snake = tk.Tk()
snake.configure(bg=couleurFond)
snake.title("Snake")
snake.geometry(str(WIDTH)+"x"+str(HEIGHT))

panMenu = tk.Frame(snake,bg=couleurFond)
panScore = tk.Frame(snake)
panJeu = tk.Frame(snake)

labelVitesse = tk.Label(panMenu,text="Vitesse",font=fonte,bg=couleurFond)
btLent = tk.Button(panMenu,text="Lent",font=fonte,command=lent)
btMoyen = tk.Button(panMenu,text="Moyen",font=fonte,bg=couleurBoutonSelect,command=moyen)
btRapide = tk.Button(panMenu,text="Rapide",font=fonte,command=rapide)
btJouer = tk.Button(panMenu,text="Jouer",font=fonte,command=jouer)
btScore = tk.Button(panMenu,text="Tableau des scores",font=fonte)
panListe = tk.Frame(panMenu)
labelNiveau = tk.Label(panMenu,text="Niveau",font=fonte,bg=couleurFond)
barreDefilement = tk.Scrollbar(panListe)
listeNiveaux = tk.Listbox(panListe,font=fonte,selectbackground=couleurBoutonSelect,yscrollcommand=barreDefilement.set)

listeNiveaux.pack(side=tk.LEFT, fill=tk.BOTH)
barreDefilement.pack(side=tk.RIGHT, fill=tk.BOTH)
barreDefilement.config(command = listeNiveaux.yview)

labelVitesse.grid(row=0,columnspan=3)
btLent.grid(row=1,column=0)
btMoyen.grid(row=1,column=1)
btRapide.grid(row=1,column=2)
labelNiveau.grid(row=2,columnspan=3)
panListe.grid(row=3,columnspan=3)
btJouer.grid(row=4,columnspan=3)
btScore.grid(row=5,columnspan=3)

panMenu.pack()

env_jeu = tk.Canvas(panJeu, width=WIDTH, heigh=HEIGHT, bg=couleurFond)
env_jeu.pack()

############PROGRAMME#######################################################################################

importerNiveaux()

snake.bind('<Up>', lambda e:deplacement_serpent_up())
snake.bind('<Down>', lambda e:deplacement_serpent_down())
snake.bind('<Right>', lambda e:deplacement_serpent_right())
snake.bind('<Left>', lambda e:deplacement_serpent_left())

snake.mainloop()
