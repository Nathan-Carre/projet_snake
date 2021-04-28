import tkinter as tk
import random
import os


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
global delai
delai = 100
delaiLent = 200
delaiMoyen = 150
delaiRapide = 100
pommes = []

        
def importerNiveaux():
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
    global delai
    btLent.config(bg=couleurBoutonSelect)
    btMoyen.config(bg=couleurBoutonDefaut)
    btRapide.config(bg=couleurBoutonDefaut)
    delai = delaiLent


def moyen():
    global delai
    btLent.config(bg=couleurBoutonDefaut)
    btMoyen.config(bg=couleurBoutonSelect)
    btRapide.config(bg=couleurBoutonDefaut)
    delai = delaiMoyen


def rapide():
    global delai
    btLent.config(bg=couleurBoutonDefaut)
    btMoyen.config(bg=couleurBoutonDefaut)
    btRapide.config(bg=couleurBoutonSelect)
    delai = delaiRapide


def jouer():
    nomFichier = listeNiveaux.get(listeNiveaux.curselection())
    panMenu.destroy()
    decors(nomFichier)
    deplacement_serpent_auto()
    panJeu.pack()


def decors(nomFichier):
    global murs, pomme, tete, queue, serpent 
    serpent = []
    x, y = 0, 0
    murs = []
    niveau = open(nomFichier)
    for ligne in niveau:
        for i in range(len(ligne)):
            case = ligne[i]
            if case == "X":
                temp = env_jeu.create_rectangle(x, y, x+40, y+40, fill='black')
                murs.append(temp)
            elif case == "P":
                pomme = env_jeu.create_oval(x, y, x+40, y+40, fill='red')
                pommes.append(pomme)
            elif case == "T":
                tete = env_jeu.create_rectangle(x, y, x+40, y+40, fill='green')
            elif case == "Q":
                queue = env_jeu.create_rectangle(x, y, x+40, y+40, fill='green')
            x += 40
        x = 0
        y += 40
    serpent = [env_jeu.coords(tete), env_jeu.coords(queue)]
    niveau.close()

def deplacement_serpent_auto():
    """Déplace le serpent sur le canevas"""
    global tete, queue, murs, pomme, dirX, dirY, serpent, prochaines_coords, coords_murs, delai
    print(delai)
    coords_murs = []
    prochaines_coords = [serpent[0][0] + dirX * taille_case, serpent[0][1] + dirY * taille_case, 
    serpent[0][2] + dirX * taille_case, serpent[0][3] + dirY * taille_case] 
    for i in murs:
        coords_murs.append(env_jeu.coords(i))

    if prochaines_coords not in coords_murs:
        serpent.insert(0, prochaines_coords) 
        serpent.remove(serpent[-1])
        env_jeu.coords(tete, serpent[0])
        env_jeu.coords(queue, serpent[-1])
        snake.after(delai, deplacement_serpent_auto)
        #snake.after_cancel(snake.after(delai, deplacement_serpent_auto))
    

def deplacement_serpent_up():
    """Déplace le serpent vers le haut sur le canevas"""
    global tete, queue, murs, pomme, dirX, dirY, serpent, prochaines_coords, coords_murs, delai

    dirX, dirY = 0, -1 
    #deplacement_serpent_auto()

    
def deplacement_serpent_down():
    """Déplace le serpent vers la bas sur le canevas"""
    global tete, queue, murs, pomme, dirX, dirY, serpent, prochaines_coords, coords_murs, delai

    dirX, dirY = 0, 1
    #deplacement_serpent_auto()

def deplacement_serpent_right():
    """Déplace le serpent vers la droite sur le canevas"""
    global tete, queue, murs, pomme, dirX, dirY, serpent, prochaines_coords, coords_murs, delai

    dirX, dirY = 1, 0 
    #deplacement_serpent_auto()
    
def deplacement_serpent_left():
    """Déplace le serpent sur le canevas"""
    global tete, queue, murs, pomme, dirX, dirY, serpent, prochaines_coords, coords_murs, delai

    dirX, dirY = -1, 0
    #deplacement_serpent_auto()



def manger_pomme():
    global pomme, score, tete
    if pommes[0] == serpent[0]:
        x_rd = random.randint(0,20)
        y_rd = random.randint(0,15)
        x_centre = (x_rd*taille_case + x_rd*taille_case + taille_case)//2 
        y_centre = (y_rd*taille_case + y_rd*taille_case + taille_case)//2
        while (mur or pomme or tete or queue) in canvas.find_overlapping(x_centre, y_centre) : #à voir si la syntaxe fonctionne    
            x_rd = random.randint(0,20)
            y_rd = random.randint(0,15)
            x_centre = (x_rd*taille_case + x_rd*taille_case + taille_case)//2 
            y_centre = (y_rd*tzille_case + y_rd*taille_case + taille_case)//2
        env_jeu.coords(pomme, x_rd*taille_case, y_rd*taille_case, x_rd*taille_case + taille_case, y_rd*taille_case + taille_case)
        score += 1
        pommes.remove(pommes[-1])

def percuter():
    x_tete, y_tete, x1_tete, y1_tete = env_jeu.coords(tete)
    x_centre = (x_tete + x1_tete)//2 
    y_centre = (y_tete + y1_tete)//2
    if corps or queue in canvas.find_overlapping(x_centre, y_centre) :
        for mur in murs :
            if mur in canvas.find_overlapping(x_centre, y_centre) : #corps à créer svp :D + à voir si la syntaxe fonctionne    
                None #à completer quand la fonction pour démarrer la partie sera créée    
            


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


importerNiveaux()

snake.bind('<Up>', lambda e:deplacement_serpent_up())
snake.bind('<Down>', lambda e:deplacement_serpent_down())
snake.bind('<Right>', lambda e:deplacement_serpent_right())
snake.bind('<Left>', lambda e:deplacement_serpent_left())






snake.mainloop()