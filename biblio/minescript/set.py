"""
Créé par OrangeGrenadine
20/08/2026

                 - - -Ce script est à utiliser en jeu - - -

Permet de modifier l'emplacement d'un îlot.
"""


#Bibliothèques utilisées :
import minescript as m
import os
import sys
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
        "modification": "Modification de l'emplacement de l'îlot '{ilot}' en {position}",
        "ilot_inexistant": "L'îlot '{ilot}' n'existe pas dans la SdC",
        "nouvelle_sdc": "Nouvelle SdC créée",
    },
    "en": {
        "modification": "Updated location of island '{ilot}' to {position}",
        "ilot_inexistant": "Island '{ilot}' does not exist in the SdC",
        "nouvelle_sdc": "New SdC created",
    },
}

# Raccourci vers le dictionnaire de messages de la langue choisie
messages = MESSAGES[LANGUAGE]

# ----------------------------------------------

# Fonction principale
def main(ilot: str):
    """Si le fichier de la Salle des Coffres n'existe pas encore, on le crée
    puis on relance la fonction avec le même îlot"""
    if not os.path.isfile(SDC_PATH):
        m.echo(messages["nouvelle_sdc"])
        create_SdC()
        return main(ilot)

    sdc_data = load_json(SDC_PATH) #On importe la SdC

    # L'îlot n'existe pas dans la SdC : on ne peut pas le déplacer
    if ilot not in sdc_data:
        return messages["ilot_inexistant"].format(ilot=ilot)

    """On récupère la position actuelle du joueur et on l'enregistre
    comme nouvel emplacement de l'îlot"""
    x, y, z = m.player_position()
    x, z = int(x), int(z)
    sdc_data[ilot] = [x, z]
    save_json(sdc_data, SDC_PATH)

    return messages["modification"].format(ilot=ilot, position=sdc_data[ilot])


if __name__ == "__main__":
    m.echo(main(str(sys.argv[1])))