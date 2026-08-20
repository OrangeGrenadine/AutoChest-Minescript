"""
Créé par OrangeGrenadine
20/08/2026

                 - - -Ce script n'est pas à utiliser en jeu - - -

Ce sont des fonctions non-usuelles de Minescript
"""

# - - - Bibliotèques utilisées - - - 
import minescript as m
import java
import time

Minecraft = java.JavaClass("net.minecraft.client.Minecraft")

def get_non_hotbar_inventory():
	"""Permet d'obtenir sous la forme d'une liste
	les éléments de l'inventaire (non-hotbar) du joueur
	sous forme : [item.name -> str, item.slot -> int]
	"""
	
	inventory = []
	for i in m.player_inventory():
		if i.slot >= 9 and i.slot <= 35:
			inventory.append( [i.item, i.slot] )
	return(inventory)

def exit_container():
	"""
	Permet de quitter une fenêtre en jeu.
	"""
	Minecraft.getInstance().player.closeContainer()
