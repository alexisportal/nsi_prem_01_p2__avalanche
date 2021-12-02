checkerboard = []
point_joueur_noir = 0
point_joueur_blanc = 0


def new_game():

    # Cette fonction lance une nouvelle partie.

    # Paramètres en entrée
    # --------------------
    # Pas de paramètre en entrée

    # Paramètres en sortie
    # --------------------
    # Pas de paramètre en sortie
    # checkerboard initialisé
    # Points des joueurs réinitialisés

    global checkerboard
    global point_joueur_noir
    global point_joueur_blanc

    checkerboard = []

    for ligne in range(10):
        if ligne <= 3:
            identity_case = "CASE_PION_NOIR"
        else:
            if ligne >= 6:
                identity_case = "CASE_PION_BLANC"
            else:
                identity_case = "CASE_VIDE"
        data_ligne = []
        for colonne in range(10):
            if (ligne + colonne) % 2 == 0:
                data_ligne.append(identity_case)
            else:
                data_ligne.append("CASE_INTERDITE")

        checkerboard.append(data_ligne)


    point_joueur_noir = 0
    point_joueur_blanc = 0



def check_law_start(x_case, y_case, active_player):

    # Cette fonction vérifie que le joueur a le droit de commencer un déplacement par la case x_case, y_case

    # Paramètres en entrée
    # --------------------
    # - x_case : colonne de la case de départ du déplacement. Valeur de 0 à 9 (10 colonnes)
    # - y_case : ligne de la case de départ du déplacement. Valeur de 0 à 9 (10 lignes)
    # - active_player : joueur qui fait le mouvement. Valeurs possibles=["NOIR", "BLANC"]

    # Paramètres en sortie
    # --------------------
    # check_law_start est le dictionnaire qui contient la réponse de la fonction:
    # - "return" : contient True s'il est possible de commencer le déplacement de la case (x_case,y_case)
    # - "message" : contient le message d'erreur si "retour"==False
    # - "pawn_type" : contient le type du point à déplacer. Valeurs possibles=["PION", "DAME"]

    global checkerboard
    if active_player == "NOIR":
        if checkerboard[y_case][x_case] == "CASE_PION_NOIR":
            return {"return": True, "message": "", "pawn_type": "PION"}
        else:
            if checkerboard[y_case][x_case] == "CASE_DAME_NOIRE":
                return {"return": True, "message": "", "pawn_type": "DAME"}
            else:
                return {"return": False, "message": "Sélection impossible", "pawn_type": ""}

    if active_player == "BLANC":
        if checkerboard[y_case][x_case] == "CASE_PION_BLANC":
            return {"return": True, "message": "", "pawn_type": "PION"}
        else:
            if checkerboard[y_case][x_case] == "CASE_DAME_BLANCHE":
                return {"return": True, "message": "", "pawn_type": "DAME"}
            else:
                return {"return": False, "message": "Sélection impossible", "pawn_type": ""}

def check_law_end(pos_start, pos_end, active_player):

    # Cette fonction vérifie qu'un déplacement de pièces est possible et déplace les pièces dans checkerboard si le déplacement est possible

    # Paramètres en entrée
    # --------------------
    # - pos_start : ce nuplet contient les coordonnées de la case de départ (x=pos_start[0],y=pos_start[1])
    # - pos_end : ce nuplet contient les coordonnées de la case d'arrivée (x=pos_end[0],y=pos_end[1])
    # - active_player : joueur qui fait le mouvement. Valeurs possibles=["NOIR", "BLANC"]

    # Paramètres en sortie
    # --------------------
    # check_law_end est le dictionnaire qui contient la réponse de la fonction:
    # - "return" : contient True si le déplacement est possible et False sinon
    # - "pos_eaten_pawn" : ce nuplet contient les coordonnées du point mangé (x,y)
    # - "pawn_type" : contient le type du point à déplacer. Valeurs possibles=["PION", "DAME"]
    # - "message" : contient le message d'erreur si "retour"==False

    global checkerboard
    global point_joueur_noir
    global point_joueur_blanc
    if checkerboard[pos_start[1]][pos_start[0]] in ["CASE_PION_BLANC", "CASE_PION_NOIR"]:
        pawn_type = "PION"
    else:
        pawn_type = "DAME"
    # Si l’arrivée contient déjà un pion  erreur
    if checkerboard[pos_end[1]][pos_end[0]] in ["CASE_DAME_NOIRE", "CASE_DAME_BLANCHE", "CASE_PION_NOIR", "CASE_PION_BLANC"]:
        if active_player == "BLANC":
            if checkerboard[pos_end[1]][pos_end[0]] in ["CASE_PION_BLANC"]:
                return {"return": "New_Blanc", "pos_eaten_pawn": None, "pawn_type": pawn_type, "message":""}
            else:
                return {"return": False, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message":"Contient deja une pièce"}
        else:
            if checkerboard[pos_end[1]][pos_end[0]] in ["CASE_PION_NOIR"]:
                return {"return": "New_Noir", "pos_eaten_pawn": None, "pawn_type": pawn_type, "message":""}
            else:
                return {"return": False, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message":"Contient deja une pièce"}

    # Si l’arrivée est une case interdite  erreur
    if checkerboard[pos_end[1]][pos_end[0]] == "CASE_INTERDITE":
        return {"return": False, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message":"Case interdite"}
    # Cas d’un pion
    if pawn_type == "PION":
        # Cas d’un pion noir (qui ne peut que descendre mais aller à droite ou à gauche)
        if active_player == "NOIR":
            # Déplacement sans manger
            if pos_end[1]-pos_start[1] == 1 and (pos_end[0]-pos_start[0]==1 or pos_end[0]-pos_start[0]==-1):
                checkerboard[pos_start[1]][pos_start[0]] = "CASE_VIDE"
                checkerboard[pos_end[1]][pos_end[0]] = "CASE_PION_NOIR"
                return {"return": True, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message":""}
            # Déplacement en mangeant
            # on vérifie la case du milieu
            if pos_end[1]-pos_start[1] == 2 and (pos_end[0]-pos_start[0]==2 or pos_end[0]-pos_start[0]==-2):
                x_milieu = int((pos_end[0]+pos_start[0])/2)
                y_milieu = int((pos_end[1]+pos_start[1])/2)
                if checkerboard[y_milieu][x_milieu] == "CASE_PION_BLANC" or checkerboard[y_milieu][x_milieu] == "CASE_DAME_BLANCHE":
                    checkerboard[pos_start[1]][pos_start[0]] = "CASE_VIDE"
                    checkerboard[y_milieu][x_milieu] = "CASE_VIDE"
                    checkerboard[pos_end[1]][pos_end[0]] = "CASE_PION_NOIR"
                    return {"return": True, "pos_eaten_pawn": (x_milieu, y_milieu), "pawn_type": pawn_type, "message": ""}
                else:
                    return {"return": False, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message": "Déplacement impossible"}
            if pos_end[1]-pos_start[1] == -2 and (pos_end[0]-pos_start[0]==2 or pos_end[0]-pos_start[0]==-2):
                x_milieu = int((pos_end[0]+pos_start[0])/2)
                y_milieu = int((pos_end[1]+pos_start[1])/2)
                if checkerboard[y_milieu][x_milieu] == "CASE_PION_BLANC" or checkerboard[y_milieu][x_milieu] == "CASE_DAME_BLANCHE":
                    checkerboard[pos_start[1]][pos_start[0]] = "CASE_VIDE"
                    checkerboard[y_milieu][x_milieu] = "CASE_VIDE"
                    checkerboard[pos_end[1]][pos_end[0]] = "CASE_PION_NOIR"
                    return {"return": True, "pos_eaten_pawn": (x_milieu, y_milieu), "pawn_type": pawn_type, "message": ""}
                else:
                    return {"return": False, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message": "Déplacement impossible"}
        if active_player == "BLANC":
            # Déplacement sans manger
            if pos_end[1]-pos_start[1] == -1 and (pos_end[0]-pos_start[0]==1 or pos_end[0]-pos_start[0]==-1):
                checkerboard[pos_start[1]][pos_start[0]] = "CASE_VIDE"
                checkerboard[pos_end[1]][pos_end[0]] = "CASE_PION_BLANC"
                return {"return": True, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message":""}
            # Déplacement en mangeant
            # on vérifie la case du milieu
            if pos_end[1]-pos_start[1] == -2 and (pos_end[0]-pos_start[0]==2 or pos_end[0]-pos_start[0]==-2):
                x_milieu = int((pos_end[0]+pos_start[0])/2)
                y_milieu = int((pos_end[1]+pos_start[1])/2)
                if checkerboard[y_milieu][x_milieu] == "CASE_PION_NOIR" or checkerboard[y_milieu][x_milieu] == "CASE_DAME_NOIRE":
                    checkerboard[pos_start[1]][pos_start[0]] = "CASE_VIDE"
                    checkerboard[y_milieu][x_milieu] = "CASE_VIDE"
                    checkerboard[pos_end[1]][pos_end[0]] = "CASE_PION_BLANC"
                    return {"return": True, "pos_eaten_pawn": (x_milieu, y_milieu), "pawn_type": pawn_type, "message": ""}
                else:
                    return {"return": False, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message": "Déplacement impossible"}
            if pos_end[1]-pos_start[1] == 2 and (pos_end[0]-pos_start[0]==2 or pos_end[0]-pos_start[0]==-2):
                x_milieu = int((pos_end[0]+pos_start[0])/2)
                y_milieu = int((pos_end[1]+pos_start[1])/2)
                if checkerboard[y_milieu][x_milieu] == "CASE_PION_NOIR" or checkerboard[y_milieu][x_milieu] == "CASE_DAME_NOIRE":
                    checkerboard[pos_start[1]][pos_start[0]] = "CASE_VIDE"
                    checkerboard[y_milieu][x_milieu] = "CASE_VIDE"
                    checkerboard[pos_end[1]][pos_end[0]] = "CASE_PION_BLANC"
                    return {"return": True, "pos_eaten_pawn": (x_milieu, y_milieu), "pawn_type": pawn_type, "message": ""}
                else:
                    return {"return": False, "pos_eaten_pawn": None, "pawn_type": pawn_type, "message": "Déplacement impossible"}
