"""
Créé par OrangeGrenadine
20/08/2026

                 - - -Ce script est à utiliser en jeu - - -

Si un item en main est présent dans la SdC (Salle des Coffres), on 
renvoie simplement son emplacement.
"""

#Bibliothèques utilisées :
import minescript as m
import os
from Biblio_Rscript.json import load_json, save_json, create_SdC

# ----------------------------------------------
# Les constantes :

# Chemin vers le fichier de sauvegarde de la Salle des Coffres
SDC_PATH = "SdC.json"

# Langue utilisée pour les messages : "fr": français, "en": anglais
LANGUAGE = "en"

# Dictionnaire des messages, selon la langue choisie ci-dessus.
MESSAGES = {
    "fr": {
        "info_item": "L'item '{item}' est en ({ilot}, {ligne}, {colonne})",
        "aucune_info": "Aucune information pour l'item : '{item}'",
        "nouvelle_sdc": "Nouvelle SdC créée",
        "rien_en_main": "Le joueur ne tient rien",
    },
    "en": {
        "info_item": "Item '{item}' is at ({ilot}, {ligne}, {colonne})",
        "aucune_info": "No information for item: '{item}'",
        "nouvelle_sdc": "New SdC created",
        "rien_en_main": "The player is holding nothing",
    },
}

# Raccourci vers le dictionnaire de messages de la langue choisie
messages = MESSAGES[LANGUAGE]


# ----------------------------------------------

# Fonction principale
def main():
    item_en_main = m.player_hand_items().main_hand

    # Si le joueur ne tient rien, on ne peut rien chercher
    if item_en_main is None:
        return messages["rien_en_main"]

    """Si le fichier de la Salle des Coffres n'existe pas encore, on le crée
    puis on relance la fonction"""
    if not os.path.isfile(SDC_PATH):
        m.echo(messages["nouvelle_sdc"])
        create_SdC()
        return main()

    sdc_data = load_json(SDC_PATH) #On importe la SdC
    nom_item = item_en_main["item"] #On récupère le nom de l'item en main

    # L'item n'est pas enregistré dans la SdC
    if nom_item not in sdc_data:
        return messages["aucune_info"].format(item=nom_item)

    # L'item est enregistré : on renvoie son emplacement
    ilot, ligne, colonne = sdc_data[nom_item]
    return messages["info_item"].format(item=nom_item, ilot=ilot, ligne=ligne, colonne=colonne)


if __name__ == "__main__":
    m.echo(main())