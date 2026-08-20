"""
Créé par OrangeGrenadine
20/08/2026

                 - - -Ce script n'est pas à utiliser en jeu - - -

Ces fonctions ne sont utilisées (et utiles) que pour le fonctionnement
du script 'sort.py'.
"""

# - - - Bibliotèques utilisées - - - 
import minescript as m

def sort_inventory_ancien(player_inventory, chestroom):
    """Permet de trier/filtrer les items dans l'inventarie selon 
	leur placement dans la SdC (renvoie que ces items)

	Ici: player_inventory: list [item:str, slot:int] -> Correspond à l'inventaire du joueur obtenue à l'aide 
	d'une fonction comme 'get_non_hotbar_inventory' dans R_Minescript.py (de la Biblio)

	chestroom: json -> Correspond à la SdC
	"""

    # 1. On récupère les items uniques présent dans la SdC
    unique_items = set(item[0] for item in player_inventory if item[0] in chestroom)

    # 2. On regroupe les items par emplacement (îlot, ligne, colonne)
    unique_locations = {}
    for item in unique_items:
        # Convertit la liste [îlot, ligne, colonne] en tuple pour pouvoir l'utiliser comme clé
        location = tuple(chestroom[item])
        if location not in unique_locations:
            unique_locations[location] = item

    # 3. On trie les items selon leur emplacement (îlot -> ligne -> colonne)
    sorted_items = [
        item for location, item in sorted(unique_locations.items(), key=lambda x: x[0])
    ]

    return sorted_items

def sort_inventory(player_inventory, chestroom):
    """Permet de trier/filtrer les items dans l'inventarie selon 
	leur placement dans la SdC (renvoie que ces items)

	Ici: player_inventory: list [item:str, slot:int] -> Correspond à l'inventaire du joueur obtenue à l'aide 
	d'une fonction comme 'get_non_hotbar_inventory' dans R_Minescript.py (de la Biblio)

	chestroom: json -> Correspond à la SdC
	"""

    # 1. On regroupe les items (avec leur slot) par emplacement (îlot, ligne, colonne)
    unique_locations = {}
    for item_name, slot in player_inventory:
        if item_name not in chestroom:
            continue

        # Convertit la liste [îlot, ligne, colonne] en tuple pour pouvoir l'utiliser comme clé
        location = tuple(chestroom[item_name])
        if location not in unique_locations:
            unique_locations[location] = []
        unique_locations[location].append([item_name, slot])

    # 2. On trie les emplacements (îlot -> ligne -> colonne), en gardant la liste d'items (+ slot) de chacun
    sorted_items = [
        items for location, items in sorted(unique_locations.items(), key=lambda x: x[0])
    ]
    
    return sorted_items

def look_at_chest(localisation):
	"""Permet d'orienter le joueur vers l'un des coffres d'un îlot.

	Pour rappel, un îlot est composé de 40 coffres, 20 orientés vers l'est et 
	le reste vers l'ouest. Une des deux façade d'un îlot est composée de 4 rangés
	de 5 coffres. D'où leur position sous la forme ici d'une liste [ligne, colonne]

	Si le numéro de ligne dépasse 4, on considère qu'on est fasse à l'ouest.


	Ici: localisation: list [ligne:int, colonne:int] -> Correspond à la localisation d'un coffre dans
	la SdC
	"""


	#Si le coffre se trouve vers l'est
	if localisation[0] < 5:

		#Yaw et Pitch de l'orientation est
		orientation = [[[-116.60984, -23.700014], [-105.899796, -25.800009], [-90.14978, -26.700006], [-75.14974, -25.800009], [-61.9, -24.000013]], [[-118.39978, -11.100011], [-105.8998, -12.000009], [-90.449776, -12.300008], [-75.149734, -12.300008], [-61.949738, -11.2500105]], [[-119.09978, 2.6999917], [-105.14974, 2.6999917], [-90.299706, 2.8499918], [-75.29968, 2.6999917], [-61.2, 3.1]], [[-118.19964, 15.899987], [-105.2996, 15.899988], [-90.14955, 17.399984], [-75.14949, 16.949986], [-61.34944, 16.049988]]]

		#On charge la rotation nécéssaire
		rotation = orientation[localisation[0]-1][localisation[1]-1]

	#Si le coffre se trouve vers l'ouest
	else:
		
		#Yaw et Pitch de l'orientation ouest
		orientation = [[[62.1006, -22.799988], [75.00059, -25.199982], [90.60065, -26.249979], [105.30069, -24.599983], [118.50074, -23.249987]], [[62.1007, -10.349986], [75.6007, -11.099984], [90.30072, -11.549983], [105.45072, -11.099985], [118.20079, -10.649986]], [[62.40076, 3.000014], [76.20077, 3.3000143], [90.60079, 3.1500142], [105.4508, 3.3000143], [118.80082, 2.850014]], [[61.950775, 15.300012], [75.60078, 17.250008], [90.600784, 18.900003], [105.7508, 18.000006], [117.60082, 16.20001]]]

		#On charge la rotation nécéssaire
		rotation = orientation[localisation[0]-5][localisation[1]-1]


	#On actualise l'orientation du joueur
	m.player_set_orientation(rotation[0], rotation[1])
	return(1)


def is_chest():
	"""Renvoie si la fenètre actuelle est ouverte sur un coffre de la SdC
	"""
	return(m.screen_name() == "Large Chest")

