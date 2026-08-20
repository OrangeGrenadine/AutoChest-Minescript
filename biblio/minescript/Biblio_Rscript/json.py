"""
Créé par OrangeGrenadine
20/08/2026

                 - - -Ce script n'est pas à utiliser en jeu - - -

C'est ici qu'on entrepose les fonctions liées à la bibliotèque
json.
"""

# - - - Bibliotèques utilisées - - - 
import json


def load_json(path): # -> dic
	"""Charge en tant que dictionnaire une SdC (format .json)

	Ici path -> str : correspond au nom de chemin du fichier à charger
	"""
	with open(path, 'r') as f:
		data = json.load(f)
	return(data)

def save_json(dic, path): # -> None
	"""Enregistre un dictionnaire (format .json)

	Ici path -> str : correspond au nom de chemin du fichier à sauvegarder
		dic -> dict : correspond à la SdC
	"""

	with open(path, 'w') as f:
		json.dump(dic, f, indent=4)

def create_SdC():
	sdc = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": [], "manquant": []}

	save_json(sdc, "SdC.json")