# 📦 AutoChest-Minescript

[ [🇫🇷 Français](README.md) | 🇬🇧 English ]

---

**This** is a set of Python scripts for [Minescript](https://minescript.net/) designed to fully automate your Minecraft chest sorting by creating *smart* storage islets.

---

## 🛠️ Installation

1. Make sure you have the **Minescript** mod installed on your Minecraft instance.
2. Download this repository and place all files from the **minescript** folder into the mod's **exec** folder:
   * The relative path from your instance should be: `/.minecraft/minescript/system/exec`
3. Launch your Minecraft game.

> Tests were conducted on version 26.2 (Fabric).

---

## 🏝️ Creating the Storage Room (SdC)

First, join your game. You are free to design your storage room however you like, as long as it meets **these few criteria**:

* Chests are arranged by **islet** (see image below). An islet is a group of **40 double chests** (20 facing East, and 20 facing West). Each side of the islet consists of **4 rows of 5 chests**, hence identifying chests by the triplet (*islet*, *row*, *column*).

> If a chest faces East (resp. West), its row value will be **1** (resp. **5**) if it is located on the top row, and **4** (resp. **8**) on the bottom row.

* The centers of the different islets must be at most **30 blocks apart** from each other.
* **All** islets must be on the **same Y coordinate** (more generally, the storage room must be located exclusively at a single altitude).

### Storage Islet Diagram

⚠️ **Note:** The image below is an explanatory diagram showing how the script perceives your setup. Feel free to choose the base of the islet, the central block, etc. Make sure to face the two sides of chests East and West, and ensure the islet is free of obstacles.

> A schematic is also available to help you design your islets.

<img src="exemple_ilot.png" alt="AutoChest Storage Islet Conceptual Diagram" width="800">

**Explanations**:

* **Central Reference Point (Islet Center):** This is the block (here, a gold block) serving as the anchor point to define the entire islet via the in-game command `\set {islet_number}`.
* **Storage Stacks (Double Chests):** Chests are grouped into stacks. Each chest is assigned an identifier (*islet*, *row*, *column*).

### Setting Up the Storage Room

Now, you need to register your storage room layout with the script.

1. Define your islets by standing on one of the central blocks and running the in-game command **`\set {islet_number}`**.

> A `.json` file named **`SdC.json`** will be generated at the root of your instance as soon as you start defining your islets. This file will store your different items associated with their respective chest triplet defined earlier.

2. Register an item by holding it in your main hand and running the in-game command **`\addTo {islet_number} {row_number} {column_number}`**.

> This is likely the most time-consuming step. However, if you prefer, you can copy the `SdC.json` file from the repository's `biblio` folder into your instance root. That's my own pre-filled storage room template eheh :)

If you are wondering where a specific item is stored, hold it in your hand and run the **`\getInfo`** command in-game.

---

## 🎮 Usage

You can now use the in-game command **`\sort`**, which automatically sorts and deposits items from your inventory (excluding the hotbar).

⚠️ **Warning**: During sorting (`sort`), the script temporarily takes control of your player's movements and actions. Do not use your keyboard or mouse during the process.

### Commands Overview

* `\set {islet_number}`: Defines or resets an islet central point.
* `\addTo {islet_number} {row_number} {column_number}`: Assigns the item in hand to the targeted chest.
* `\sort`: Starts the automatic sorting routine. The player moves towards the corresponding chests and deposits items from their inventory.
* `\getInfo`: Displays information about the item in hand, specifying whether or not it is registered in the storage room.

## 🎬 Demonstration

[![MineSorter Demo](https://i9.ytimg.com/vi/CoqGcpnG2-U/mqdefault.jpg?sqp=CMyDndQG-oaymwEmCMACELQB8quKqQMa8AEB-AHUBoAC4AOKAgwIABABGGUgVShAMA8=&rs=AOn4CLAIliztgFaBAEu90uyoJjZ8VbNTAg)](https://www.youtube.com/watch?v=CoqGcpnG2-U)
