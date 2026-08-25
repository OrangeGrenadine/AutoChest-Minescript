"""
Créé par OrangeGrenadine
20/08/2026

                 - - -Ce script est à utiliser en jeu - - -

La fonction 'main' ci-dessous prend en entée un emplacement dans la 
Sdc. Si l'item que l'on tient ne s'y trouve pas déjà, on le rajoute/modifie.
"""


#Bibliothèques utilisées :
import minescript as m
import sys
import os
from Biblio_Rscript.json import load_json, save_json, create_SdC


# ----------------------------------------------
# Les constantes :

# C'est le chemin vers le fichier de sauvegarde de la Salle des Coffres
SDC_PATH = "SdC.json"

# Langue utilisée pour les messages : "fr": français, "en": anglais
LANGUAGE = "en"

# Dictionnaire des messages, selon la langue choisie ci-dessus.
MESSAGES = {
    "fr": {
        "ajout": "Ajout de {item} rangé en ({ilot}, {ligne}, {colonne})",
        "modification": "L'item '{item}' est maintenant en ({ilot}, {ligne}, {colonne})",
        "aucune_modification": "Aucune modification pour l'item : '{item}'",
        "nouvelle_sdc": "Nouvelle SdC créée",
        "rien_en_main": "Le joueur ne tient rien",
    },
    "en": {
        "ajout": "Added {item}, stored at ({ilot}, {ligne}, {colonne})",
        "modification": "Item '{item}' is now at ({ilot}, {ligne}, {colonne})",
        "aucune_modification": "No change for item: '{item}'",
        "nouvelle_sdc": "New SdC created",
        "rien_en_main": "The player is holding nothing",
    },
}

# Raccourci vers le dictionnaire de messages de la langue choisie
messages = MESSAGES[LANGUAGE]

# ----------------------------------------------

# Fonction principale
def main(ilot: int, ligne: int, colonne: int):
    item_en_main = m.player_hand_items().main_hand

    # Si le joueur ne tient rien, on ne peut rien ranger
    if item_en_main is None:
        return messages["rien_en_main"]

    """Si le fichier de la Salle des Coffres n'existe pas encore, on le crée
    puis on relance la fonction avec les mêmes coordonnées"""

    if not os.path.isfile(SDC_PATH):
        m.echo(messages["nouvelle_sdc"])
        create_SdC()
        return main(ilot, ligne, colonne)

    sdc_data = load_json(SDC_PATH) #On importe la SdC
    nom_item = item_en_main["item"] #On récupère le nom de l'item en main

    # L'item n'est pas encore enregistré : on l'ajoute
    if nom_item not in sdc_data:
        sdc_data[nom_item] = [ilot, ligne, colonne]
        save_json(sdc_data, SDC_PATH)
        return messages["ajout"].format(item=nom_item, ilot=ilot, ligne=ligne, colonne=colonne)

    # L'item existe déjà, mais à un autre emplacement : on met à jour
    if sdc_data[nom_item] != [ilot, ligne, colonne]:
        sdc_data[nom_item] = [ilot, ligne, colonne]
        save_json(sdc_data, SDC_PATH)
        return messages["modification"].format(item=nom_item, ilot=ilot, ligne=ligne, colonne=colonne)

    # L'item est déjà enregistré au bon emplacement : rien à faire
    return messages["aucune_modification"].format(item=nom_item)


if __name__ == "__main__":
    m.echo(main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))
