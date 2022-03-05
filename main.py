import tkinter as tk
import pandas
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)



myDataset = pandas.read_csv("data.csv", sep=";", encoding="ANSI")
myDataframe = pandas.DataFrame(myDataset)

liste_dates = myDataframe["date"]
liste_mois = []
liste_annee =[]
liste_anneemois= []
for date in liste_dates:
    mois = str(date[3:5])
    liste_mois.append(mois)
    annee = str(date[6:10])
    liste_annee.append(annee)
    liste_anneemois.append(annee+mois)

myDataframe["mois"] = liste_mois
myDataframe["annee"] = liste_annee
myDataframe["anneemois"] =liste_anneemois


root = tk.Tk()

# config the root window
root.geometry('1000x700')
root.resizable(False, False)
root.title('Statistiques avalanches')


frame1 = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame1.pack(fill="x")
#Frame1 contient les critères de sélection des données

#######################################################
#
# Effacer les graphiques contenus dans le canvas
#
#######################################################
def clear_plot():
    global output
    if output:
        for child in canvas.winfo_children():
            child.destroy()
        # or just use canvas.winfo_children()[0].destroy()

    output = None



def changed():
    global radio_type_valeur
    global cb_decedes
    global cb_blesses
    global cb_indemnes
    global selected_departement
    global selected_annee
    global selected_mois
    global selected_commune
    global selected_massif
    global selected_activite
    global selected_loco
    global myDataframe

    global root
    global canvas
    global output
    global fig

    val_blesses = cb_blesses.get()
    val_indemnes = cb_indemnes.get()
    val_decedes = cb_decedes.get()
    val_type_valeur = radio_type_valeur.get()
    val_departement = selected_departement.get()
    val_annee = selected_annee.get()
    val_mois = selected_mois.get()
    val_commune = selected_commune.get()
    val_massif = selected_massif.get()
    val_activite = selected_activite.get()
    val_loco = selected_loco.get()

    ########################################
    #
    # Filtrer les données
    #
    ########################################
    condition_generale = [True for i in range(len(myDataframe["departement"]))]

    if val_departement != "tous":
        liste_condition_departement = myDataframe["departement"] == val_departement
        condition_generale = condition_generale & liste_condition_departement

    if val_annee != "tous":
        liste_condition_annee = myDataframe["annee"] == val_annee
        condition_generale = condition_generale & liste_condition_annee

    if val_mois != "tous":
        liste_condition_mois = myDataframe["mois"] == val_mois
        condition_generale = condition_generale & liste_condition_mois

    if val_commune != "tous":
        liste_condition_commune = myDataframe["commune"] == val_commune
        condition_generale = condition_generale & liste_condition_commune

    if val_massif != "tous":
        liste_condition_massif = myDataframe["massif"] == val_massif
        condition_generale = condition_generale & liste_condition_massif

    if val_activite != "tous":
        liste_condition_activite = myDataframe["activite"] == val_activite
        condition_generale = condition_generale & liste_condition_activite

    if val_loco != "tous":
        liste_condition_loco = myDataframe["locomotion"] == val_loco
        condition_generale = condition_generale & liste_condition_loco

    newDataframe = myDataframe[condition_generale]

    ########################################
    #
    # Afficher un camembert
    #
    ########################################
    if val_annee != "tous" and val_mois != "tous":
        dataframe = newDataframe.sum()

        clear_plot()

        x = []
        y = []

        fig = Figure(figsize=(12, 5), dpi=100)
        plot1 = fig.add_subplot(111)

        if val_decedes == 1:
            x.append("décédés")
            y.append(int(dataframe["decedes"]))

        if val_blesses == 1:
            x.append("blessées")
            y.append(int(dataframe["blessees"]))

        if val_indemnes == 1:
            x.append("indemnes")
            y.append(int(dataframe["indemnes"]))

        plot1.pie(y, labels=x, autopct='%1.2f%%')

        output = FigureCanvasTkAgg(fig, master=canvas)
        output.draw()
        output.get_tk_widget().pack()

    else:
        dataframe = newDataframe.groupby(['anneemois'], as_index=False).sum()
        dataframe.sort_values("anneemois", axis=0, ascending=True, inplace=True)

        clear_plot()

        if val_type_valeur==1:
            ########################################
            #
            # Afficher une courbe
            #
            ########################################
            x = dataframe["anneemois"]

            fig = Figure(figsize=(12, 5), dpi=100)
            plot1 = fig.add_subplot(111)
            plot1.set_xlabel('date')
            plot1.set_ylabel('nb de personnes')

            if val_decedes == 1:
                y1 = dataframe["decedes"]
                plot1.plot(x, y1, "r")

            if val_blesses == 1:
                y2 = dataframe["blessees"]
                plot1.plot(x, y2, "#00FFFF")

            if val_indemnes == 1:
                y3 = dataframe["indemnes"]
                plot1.plot(x, y3, "g")

            output = FigureCanvasTkAgg(fig, master = canvas)
            output.draw()
            output.get_tk_widget().pack()

        else:
            ########################################
            #
            # Afficher un histogramme
            #
            ########################################
            x1 = []
            x2 = []
            x3 = []

            index = 0.0
            for i in range(len(dataframe["anneemois"])):
                x1.append(index)
                x2.append(index + 0.25)
                x3.append(index + 0.5)
                index = index + 1.0

            fig = Figure(figsize=(12, 5), dpi=100)
            plot1 = fig.add_subplot(111)
            plot1.set_xlabel('date')
            plot1.set_ylabel('nb de personnes')

            if val_decedes == 1:
                y1 = dataframe["decedes"]
                plot1.bar(x1, y1, color="r", width=0.25)

            if val_blesses == 1:
                y2 = dataframe["blessees"]
                plot1.bar(x2, y2, color="#00FFFF", width=0.25)

            if val_indemnes == 1:
                y3 = dataframe["indemnes"]
                plot1.bar(x3, y3, color="g", width=0.25)

            output = FigureCanvasTkAgg(fig, master=canvas)
            output.draw()
            output.get_tk_widget().pack()


#######################################################################
#
# Construire l'interface
#
#######################################################################

#########################################################################
############################## Département ##############################
#########################################################################

label_departement = ttk.Label(frame1,text="Choisir un département")
label_departement.pack(fill=tk.X, padx=5, pady=0)

selected_departement = tk.StringVar()
selected_departement.set("tous")

departement_cb = ttk.Combobox(frame1, textvariable=selected_departement)

departement_cb['values'] = ["tous"] + sorted(myDataframe["departement"].unique())
departement_cb['state'] = 'readonly'

departement_cb.pack(fill=tk.X, padx=5, pady=0)


def departement_changed(event):
    changed()

departement_cb.bind('<<ComboboxSelected>>', departement_changed)


#########################################################################
############################## Année ##############################
#########################################################################
label_annee = ttk.Label(frame1,text="Choisir une année")
label_annee.pack(fill=tk.X, padx=5, pady=0)

selected_annee = tk.StringVar()
selected_annee.set("tous")

annee_cb = ttk.Combobox(frame1, textvariable=selected_annee)

annee_cb['values'] = ["tous"] + sorted(myDataframe["annee"].unique())
annee_cb['state'] = 'readonly'

annee_cb.pack(fill=tk.X, padx=5, pady=0)


def annee_changed(event):
    changed()

annee_cb.bind('<<ComboboxSelected>>', annee_changed)

#########################################################################
############################## Mois ##############################
#########################################################################
label_mois = ttk.Label(frame1,text="Choisir un mois")
label_mois.pack(fill=tk.X, padx=5, pady=0)

# selected_mois contient la valeur sélectionnée
selected_mois = tk.StringVar()
selected_mois.set("tous")

# Création de la combobox et rattachement à frame1
mois_cb = ttk.Combobox(frame1, textvariable=selected_mois)

# Liste des valeurs possibles
mois_cb['values'] = ["tous"] + sorted(myDataframe["mois"].unique())
mois_cb['state'] = 'readonly'

# place la combobox dans sa mère
mois_cb.pack(fill=tk.X, padx=5, pady=0)


# Fonction appelée lorsque la valeur sélectionnée change
def mois_changed(event):
    changed()

# Lier la fonction à l’événement de changement de valeur de la combobo
mois_cb.bind('<<ComboboxSelected>>', mois_changed)


#########################################################################
############################## Commune ##############################
#########################################################################

label_commune = ttk.Label(frame1,text="Choisir une commune")
label_commune.pack(fill=tk.X, padx=5, pady=0)

selected_commune = tk.StringVar()
selected_commune.set("tous")

commune_cb = ttk.Combobox(frame1, textvariable=selected_commune)

commune_cb['values'] = ["tous"] + sorted(myDataframe["commune"].unique())
commune_cb['state'] = 'readonly'

commune_cb.pack(fill=tk.X, padx=5, pady=0)


def commune_changed(event):
    changed()

commune_cb.bind('<<ComboboxSelected>>', commune_changed)

#########################################################################
############################## Massif ##############################
#########################################################################
label_massif = ttk.Label(frame1,text="Choisir un massif")
label_massif.pack(fill=tk.X, padx=5, pady=0)

selected_massif = tk.StringVar()
selected_massif.set("tous")

massif_cb = ttk.Combobox(frame1, textvariable=selected_massif)

massif_cb['values'] = ["tous"] + sorted(myDataframe["massif"].unique())
massif_cb['state'] = 'readonly'

massif_cb.pack(fill=tk.X, padx=5, pady=0)


def massif_changed(event):
    changed()

massif_cb.bind('<<ComboboxSelected>>', massif_changed)


#########################################################################
############################## Activité ##############################
#########################################################################
label_activite = ttk.Label(frame1,text="Choisir une activité")
label_activite.pack(fill=tk.X, padx=5, pady=0)

selected_activite = tk.StringVar()
selected_activite.set("tous")

activite_cb = ttk.Combobox(frame1, textvariable=selected_activite)

activite_cb['values'] = ["tous"] + sorted(myDataframe["activite"].unique())
activite_cb['state'] = 'readonly'

activite_cb.pack(fill=tk.X, padx=5, pady=0)


def activite_changed(event):
    changed()

activite_cb.bind('<<ComboboxSelected>>', activite_changed)

#########################################################################
############################## Locomotion ##############################
#########################################################################
label_loco = ttk.Label(frame1,text="Choisir un moyen de locomotion")
label_loco.pack(fill=tk.X, padx=5, pady=0)

selected_loco = tk.StringVar()
selected_loco.set("tous")

loco_cb = ttk.Combobox(frame1, textvariable=selected_loco)

loco_cb['values'] = ["tous"] + sorted(myDataframe["locomotion"].unique())
loco_cb['state'] = 'readonly'

loco_cb.pack(fill=tk.X, padx=5, pady=0)


def loco_changed(event):
    changed()

loco_cb.bind('<<ComboboxSelected>>', loco_changed)


#########################################################################
#   Frame2 contient le choix du type de graphique courbe ou histogramme
#########################################################################
frame2 = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame2.pack(fill="x")

#########################################################################
############################## Courbe / Histoire ########################
#########################################################################
def type_valeur_changed():
    changed()


# radio_type_valeur contient la valeur du groupe
radio_type_valeur = tk.IntVar()

# initialise la valeur du groupe
radio_type_valeur.set(1)

# Créer le 1er radioButton qui correspond à la valeur 1
# le radiobutton a pour mère la frame2
# text associé à la valeur du radiobutton
# variable est la variable qui contient la valeur du groupe. Le fait que plusieurs radiobuttons aient la même variable crée le groupe.
# value est la valeur que prendra variable lorsque le radiobutton sera sélectionné
# command est la fonction qui sera appelée lorsque le groupe changera de valeur
bouton_courbe = tk.Radiobutton(frame2, text="Courbes", variable=radio_type_valeur, value=1,command=type_valeur_changed)
# Afficher le radiobutton
bouton_courbe.pack(side=tk.LEFT,padx=5)

# Créer le 2ème radiobutton qui correspond à la valeur 2
bouton_histo = tk.Radiobutton(frame2, text="Histogrammes", variable=radio_type_valeur, value=2,command=type_valeur_changed)
# Afficher le radiobutton
bouton_histo.pack(side=tk.LEFT,padx=5)


#########################################################################
#   Frame3 Décédés / Blessés / Indemnes
#########################################################################

frame3 = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame3.pack(fill="x")

####################################################################################
############################## Décédés / Blessés / Indemnes ########################
####################################################################################
# cb_decedes contient la valeur de la checkbox
cb_decedes = tk.IntVar()

# initialise la valeur
cb_decedes.set(1)

# Créer le checkbutton
# frame3 est la mère à laquelle elle est rattachée
# text est le texte affiché avant le checkbutton
# variable est la variable qui sera mise à jour lorsque l’utilisateur coche et décoche la checkbox
# onvalue est la valeur que prendra variable lorsque la checkbox est cochée
# offvalue est la valeur que prendra variable lorsque la checkbox est décochée
# command est la fonction qui sera appelé lorsque l’utilisateur clique sur la checkbox
# selectcolor est la couleur de la checkbox
bouton_decedes = tk.Checkbutton(frame3, text="Décédés", variable=cb_decedes, onvalue=1, offvalue=0, command=changed,selectcolor="#FF0000")

# Afficher la checkbox
bouton_decedes.pack(side=tk.LEFT)

###############################################################################

cb_blesses = tk.IntVar()
cb_blesses.set(1)
bouton_blesses = tk.Checkbutton(frame3, text="Blessés", variable=cb_blesses, onvalue=1, offvalue=0, command=changed,selectcolor="#00FFFF")
bouton_blesses.pack(side=tk.LEFT)

###############################################################################

cb_indemnes = tk.IntVar()
cb_indemnes.set(1)
bouton_indemnes = tk.Checkbutton(frame3, text="Indemnes", variable=cb_indemnes, onvalue=1, offvalue=0, command=changed,selectcolor="#00FF00")
bouton_indemnes.pack(side=tk.LEFT)


####################################################################################
####################### Canvas pour dessiner les graphiques ########################
####################################################################################
canvas = tk.Canvas(root)
canvas.pack()

#Pour afficher le graphique
output = None
fig = None

changed()

root.mainloop()