from tkinter import *
#from tkinter.messagebox import *
import coeur
import sys

active_player = "BLANC"
next_step = "START"
pos_start = None
pos_end = None
point_joueur_noir = 0
point_joueur_blanc = 0


def draw_checkerboard():
    #Cette fonction dessine le damier

    # Paramètres en entrée
    # --------------------
    # Pas de paramètre en entrée

    # Paramètres en sortie
    # --------------------
    # Pas de paramètre en sortie

    global active_player
    global next_step
    global pos_start
    global pos_end
    global canvas
    global img_damier_jeu_blanc
    global img_damier_jeu_dame_blanche
    global img_damier_jeu_dame_noire
    global img_damier_jeu_noir
    global img_damier_jeu_vide
    global img_damier_non_jeu
    global text_message



    for ligne in range(10):
        y1 = ligne*40

        if ligne<=3:
            img = img_damier_jeu_noir
        else:
            if ligne>=6:
                img = img_damier_jeu_blanc
            else:
                img = img_damier_jeu_vide

        for colonne in range(10):
            x1 = colonne*40

            if (ligne + colonne) %2==0:
                canvas.create_image(x1,y1,anchor=NW,image=img)
            else:
                canvas.create_image(x1,y1,anchor=NW,image=img_damier_non_jeu)

    # canvas.create_image(3*40, 1*40, anchor=NW, image=img_damier_jeu_dame_noire)


def new_game():

    # Cette fonction lance un nouveau jeu.

    # Paramètres en entrée
    # --------------------
    # Pas de paramètre en entrée

    # Paramètres en sortie
    # --------------------
    # Pas de paramètre en sortie

    global active_player
    global next_step
    global pos_start
    global pos_end
    global canvas
    global img_damier_jeu_blanc
    global img_damier_jeu_dame_blanche
    global img_damier_jeu_dame_noire
    global img_damier_jeu_noir
    global img_damier_jeu_vide
    global img_damier_non_jeu
    global text_message
    global point_joueur_blanc
    global point_joueur_noir

    point_joueur_blanc = 0
    point_joueur_noir = 0

    text_point1.set("Points joueur Noir : " + str(point_joueur_noir))
    text_point2.set("Points joueur Blanc : " + str(point_joueur_blanc))

    active_player = "BLANC"
    next_step = "START"
    pos_start = None
    pos_end = None


    draw_checkerboard()
    coeur.new_game()


def action_quitter():
    # Cette fonction arrête l'application

    # Paramètres en entrée
    # --------------------
    # Pas de paramètre en entrée

    # Paramètres en sortie
    # --------------------
    # Pas de paramètre en sortie
    sys.exit()

def click(event):
    # Cette fonction gère les clicks sur le damier (sur le canvas).

    # Paramètres en entrée
    # --------------------
    # Pas de paramètre en entrée

    # Paramètres en sortie
    # --------------------
    # Pas de paramètre en sortie

    global active_player
    global next_step
    global pos_start
    global pos_end
    global canvas
    global img_damier_jeu_blanc
    global img_damier_jeu_dame_blanche
    global img_damier_jeu_dame_noire
    global img_damier_jeu_noir
    global img_damier_jeu_vide
    global img_damier_non_jeu
    global text_message
    global point_joueur_blanc
    global point_joueur_noir

    # coordonnées en pixel du clic
    x = event.x
    y = event.y

    # coordonnées en colonne, ligne dans le damier du clic
    x_case = int(x / 40)
    y_case = int(y / 40)

    # Si click pour choisir la case de départ
    if next_step=="START":
        check_law_start = coeur.check_law_start(x_case,y_case,active_player)
        pos_start = (x_case,y_case)
        if check_law_start["return"] == True:
           if active_player == "BLANC":
               canvas.create_image(x_case*40, y_case*40, anchor=NW, image=img_damier_jeu_blanc_select)
               text_message.set(check_law_start["message"])
               next_step = "END"
           else:
               canvas.create_image(x_case*40, y_case*40, anchor=NW, image=img_damier_jeu_noir_select)
               text_message.set(check_law_start["message"])
               next_step = "END"
        else:
            text_message.set(check_law_start["message"])

    else:
        pos_end = (x_case, y_case)
        check_law_end = coeur.check_law_end(pos_start,pos_end,active_player)
        if check_law_end["return"] == "New_Blanc":
            canvas.create_image(x_case*40, y_case*40, anchor=NW, image=img_damier_jeu_blanc_select)
            canvas.create_image(pos_start[0]*40, pos_start[1]*40, anchor=NW, image=img_damier_jeu_blanc)
            pos_start = (x_case, y_case)
            next_step = "END"
        if check_law_end["return"] == "New_Noir":
            canvas.create_image(x_case*40, y_case*40, anchor=NW, image=img_damier_jeu_noir_select)
            canvas.create_image(pos_start[0]*40, pos_start[1]*40, anchor=NW, image=img_damier_jeu_noir)
            pos_start = (x_case, y_case)
            next_step = "END"
        if check_law_end["return"] == True:
            if active_player == "BLANC":
                if check_law_end["pos_eaten_pawn"]!= None :
                    canvas.create_image(pos_start[0]* 40, pos_start[1]* 40, anchor=NW, image=img_damier_jeu_vide)
                    canvas.create_image(check_law_end["pos_eaten_pawn"][0]* 40,check_law_end["pos_eaten_pawn"][1]* 40, anchor=NW, image=img_damier_jeu_vide)
                    canvas.create_image(x_case* 40, y_case* 40, anchor=NW, image=img_damier_jeu_blanc)
                    text_message.set(check_law_end["message"])
                    point_joueur_blanc = point_joueur_blanc + 1
                    text_point2.set("Points joueur Blanc : " + str(point_joueur_blanc))
                    next_step = "START"
                    active_player = "NOIR"
                    win(point_joueur_noir, point_joueur_blanc)
                else:
                    canvas.create_image(pos_start[0] * 40, pos_start[1] * 40, anchor=NW, image=img_damier_jeu_vide)
                    canvas.create_image(x_case * 40, y_case * 40, anchor=NW, image=img_damier_jeu_blanc)
                    text_message.set(check_law_end["message"])
                    next_step = "START"
                    active_player = "NOIR"
            else:
                if check_law_end["pos_eaten_pawn"]!= None :
                    canvas.create_image(pos_start[0]* 40, pos_start[1]* 40, anchor=NW, image=img_damier_jeu_vide)
                    canvas.create_image(check_law_end["pos_eaten_pawn"][0]* 40,check_law_end["pos_eaten_pawn"][1]* 40, anchor=NW, image=img_damier_jeu_vide)
                    canvas.create_image(x_case* 40, y_case* 40, anchor=NW, image=img_damier_jeu_noir)
                    text_message.set(check_law_end["message"])
                    point_joueur_noir = point_joueur_noir + 1
                    text_point1.set("Points joueur Noir : " + str(point_joueur_noir))
                    next_step = "START"
                    active_player = "BLANC"
                    win(point_joueur_noir, point_joueur_blanc)
                else:
                    canvas.create_image(pos_start[0] * 40, pos_start[1] * 40, anchor=NW, image=img_damier_jeu_vide)
                    canvas.create_image(x_case * 40, y_case * 40, anchor=NW, image=img_damier_jeu_noir)
                    text_message.set(check_law_end["message"])
                    next_step = "START"
                    active_player = "BLANC"
        else:
            text_message.set(check_law_end["message"])

def win(point_joueur_noir, point_joueur_blanc):
    if point_joueur_noir == 20:
        text_message.set("Le Joueur noir a gagné !")
    if point_joueur_blanc == 20:
        text_message.set("Le Joueur blanc a gagné !")


    ###############################################
    #                                             #
    #        LANCEMENT DE L'APPLICATION           #
    #                                             #
    ###############################################

# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel

# Création de la fenetre
fenetre = Tk()
fenetre.geometry("400x500")
fenetre.title("Checkers")
fenetre.configure(background="white")

# Création du menu
menubar = Menu(fenetre)
menu_action = Menu(menubar,tearoff=0)
menu_action.add_command(label="Nouvelle partie",command=new_game)
menu_action.add_separator()
menu_action.add_command(label="Quitter",command=action_quitter)
menubar.add_cascade(label="Action",menu=menu_action)
fenetre.configure(menu=menubar)

# Création du damier
canvas = Canvas(fenetre,width=400,height=400,background="white")
canvas.bind("<Button-1>",click)
#dessiner_echiquier()
canvas.pack(side=TOP)

# Création du message joueur
text_message = StringVar()
text_message.set("")
label = Label(fenetre,textvariable=text_message,bg="white")
label.pack(side=BOTTOM)

# Création des points du joueur 1
text_point1 = StringVar()
text_point1.set("Points joueur Noir : " + str(point_joueur_noir))
label_point1 = Label(fenetre,textvariable=text_point1,bg="white")
label_point1.place(x=10,y=420)

# Création des points du joueur 2
text_point2 = StringVar()
text_point2.set("Point joueur Blanc : " + str(point_joueur_blanc))
label_point2 = Label(fenetre,textvariable=text_point2,bg="white")
label_point2.place(x=250,y=420)

# Création des images
img_damier_jeu_dame_blanche = PhotoImage(file="img_damier_jeu_dame_blanche.gif")
img_damier_jeu_dame_noire = PhotoImage(file="img_damier_jeu_dame_noire.gif")

img_damier_jeu_dame_blanche_select = PhotoImage(file="img_damier_jeu_dame_blanche_select.gif")
img_damier_jeu_dame_noire_select = PhotoImage(file="img_damier_jeu_dame_noire_select.gif")

img_damier_jeu_blanc = PhotoImage(file="img_damier_jeu_blanc.gif")
img_damier_jeu_noir = PhotoImage(file="img_damier_jeu_noir.gif")

img_damier_jeu_blanc_select = PhotoImage(file="img_damier_jeu_blanc_select.gif")
img_damier_jeu_noir_select = PhotoImage(file="img_damier_jeu_noir_select.gif")

img_damier_jeu_vide = PhotoImage(file="img_damier_jeu_vide.gif")
img_damier_non_jeu = PhotoImage(file="img_damier_non_jeu.gif")

# Boucle de la fenetre
fenetre.mainloop()
