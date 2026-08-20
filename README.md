# 📦 AutoChest-Minescript

**MineSorter** est un ensemble de scripts Python pour [Minescript](https://minescript.net/) permettant d'automatiser entièrement le rangement de vos coffres dans Minecraft en créant des îlots de stockage intelligents.

---

## 🛠️ Installation

1. Assurez-vous d'avoir installez le mod **Minescript** sur votre instance de Minecraft.
2. Téléchargez ce dépôt et placez l'ensemble des fichiers du dossier **minescript** dans le dossier **exec** des scrips du mod :
   * Le chemin depuis votre instance devrait être : */.minecraft/minescript/system/exec*
3. Lancez votre jeu Minecraft.

> Mes tests ont eu lieu sur la version 26.2 (fabric)

---

## 🏝️ Création de la Salle des Coffres (SdC)

Premièrement, rendez-vous en jeu. À vous de concevoir votre salle des coffres comme bon vous semble, du moment **qu'elle valide ces quelques critères** :

* Les différents coffres sont rangés par **îlot** (cf. image ci-dessous). Un îlot est un ensemble de **40 doubles coffres** (20 vers l'Est, et 20 autres vers l'Ouest). Chacun des deux côtés de l'îlot possède **4 rangées de 5 coffres**, d'où le repérage des coffres par le triplet (*îlot*, *ligne*, *colonne*).

> Si un coffre est vers l'Est (resp. vers l'Ouest), il aura pour valeur de ligne **1** (resp. **5**) s'il est placé sur la rangée du haut, et **4** (resp. **8**) sur la rangée du bas.

* Les centres des différents îlots doivent être distants de **30 blocs au maximum** les uns des autres.
* **Tous** les îlots doivent se trouver sur la **même coordonnée Y** (la SdC doit, plus généralement, se situer exclusivement à une unique altitude).

### Schéma d'un Îlot de Stockage

⚠️ **Note :** L'image ci-dessous est un schéma explicatif de la façon dont le script perçoit votre construction. À vous de choisir la base de l'îlot, le bloc central, etc. Veillez à orienter les deux côtés avec les coffres à l'**Est** et à l'**Ouest**, et veillez à ce que l'îlot ne soit pas encombré.

<img src="exemple_îlot.png" alt="Schéma conceptuel des îlots de stockage AutoChest" width="800">

**Explications** :

* **Point de Référence Central (Centre de l'îlot) :** C'est le bloc (ici, un bloc d'or) qui sert d'ancrage pour définir l'îlot entier via la commande `/set {numéro de l'îlot}`.
* **Piles de Stockage (Double Coffres) :** Les coffres sont regroupés par piles. Chacun d'entre eux est assigné à un identifiant (*îlot*, *ligne*, *colonne*).
