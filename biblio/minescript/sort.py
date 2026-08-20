"""
Créé par OrangeGrenadine
20/08/2026

                 - - -Ce script est à utiliser en jeu - - -

C'est le script qui se charge de ranger automatiquement
la salle des coffres.
"""


#Bibliothèques utilisées :
import minescript as m
import json
import time
import os

from Biblio_Rscript.json import load_json, save_json
from Biblio_Rscript.misc import sort_inventory, look_at_chest, is_chest
from Biblio_Rscript.R_Minescript import get_non_hotbar_inventory, exit_container
from Biblio_Rscript.goTo import goto, center_on_block
# Cette bibliothèque provient de SmartBoty (on la retrouve dans Biblio)
from Biblio.lib_inv import quickmove


# ----------------------------------------------
# Les constantes :

# Délai entre deux actions
délai = 0.1

# Chemin vers le fichier de sauvegarde de la Salle des Coffres
SDC_PATH = "SdC.json"

# Langue utilisée pour les messages : "fr" pour français, "en" pour anglais
LANGUAGE = "en"

# Dictionnaire des messages, selon la langue choisie ci-dessus.
MESSAGES = {
    "fr": {
        "echec": "Echec de l'auto-rangement",
        "aucune_sdc": "Aucune Salle des Coffres trouvée",
        "succes": "Auto-rangement : fait !",
    },
    "en": {
        "echec": "Auto-storage failed",
        "aucune_sdc": "No Storage Room found",
        "succes": "Auto-storage: done !",
    },
}

# Raccourci vers le dictionnaire de messages de la langue choisie
messages = MESSAGES[LANGUAGE]


# ----------------------------------------------

# Fonction principale
def main():
    # On vérifie que le .json SdC existe
    if not os.path.isfile(SDC_PATH):
        return messages["aucune_sdc"]

    sdc_data = load_json(SDC_PATH) # On charge la SdC

    # On récupère les items de l'inventaire (non_hotbar)
    inventaire_non_hotbar = get_non_hotbar_inventory()

    """On ne garde que les items présent dans la SdC puis on les tries selon
    leur emplacement"""
    inventaire_non_hotbar = sort_inventory(inventaire_non_hotbar, sdc_data)

    """On peut commencer la boucle de rangement
    On vérifie à chaque fois que les fonctions renvoies 1
    ie : exécution sans problème"""


    for groupe_items in inventaire_non_hotbar:
        
        # On localise le coffre (c'est le premier item de la liste)
        item_localisation = sdc_data[groupe_items[0][0]]

        # 1ère étape : On va à l'îlot
        position_joueur = m.player_position()
        if goto(sdc_data[str(item_localisation[0])][0], sdc_data[str(item_localisation[0])][1]) != 1:
            return messages["echec"]
        if m.player_position() != position_joueur:  # On cherche à se placer au centre du bloc
            center_on_block()  # On centre le joueur

        # 2ieme étape : On ouvre le coffre correspondant à l'item
        look_at_chest([item_localisation[1], item_localisation[2]])
        time.sleep(délai)
        m.player_press_use(True)

        # On vérifie que le coffre est ouvert
        compteur_tentatives, recherche = 0, True
        while recherche:
            if is_chest:
                recherche = False
                m.player_press_use(False)
            else:
                if compteur_tentatives > 100:
                    return messages["echec"]
            compteur_tentatives += 1
        m.player_press_use(False)

        # On fait une pause, puis on range les items
        time.sleep(délai * 10)
        for item in groupe_items:
            time.sleep(délai * 2)
            quickmove(item[1] + 45)  # +45 car double coffre
        time.sleep(délai)
        exit_container()

        # On vérifie que le coffre est fermé
        temps_ecoule, recherche = 0.0, True
        while recherche:
            debut_iteration = time.time()
            if not is_chest():
                recherche = False
            else:
                if temps_ecoule > (délai * 20):
                    return messages["echec"]
            temps_ecoule += (time.time() - debut_iteration)

    return messages["succes"]


if __name__ == "__main__":
    m.echo(main())