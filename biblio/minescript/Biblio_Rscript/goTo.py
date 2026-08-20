"""
Créé par OrangeGrenadine
20/08/2026

                 - - -Ce script n'est pas à utiliser en jeu - - -

Nb : Pour m'aider à coder certaines fonctions de ce fichier, une IA (Gemini)
a été utilisée
"""

# - - - Bibliotèques utilisées - - - 
import minescript as m
import time
from collections import deque
import math

"""
Ici:
RADIUS (en blocs) : correspond à la zone scannée autour du joueur.

Ici on cherche à créer une matrice carrée (de taille 2*RADIUS+1 )
qui représente l'espace autour du joueur. On utilise ensuite un 
algorithme de "parcours en largeur" (ou BFS: Breadth-First Search) pour 
trouver le chemin optimale. La matrice est vierge au début, on cherche
le chemin le plus court, puis on vérifie si il y a des obstacles.
Si oui, on actualise la matrice, et on recommence.  

Nb : Vous devriez vous assurer qu'il n'y a aucun trou autour de vous, en 
en effet, le script ne regarde que les obstacles à la hauteur du joueur :)
"""

# ----------------------------------------------
# La constante :
RADIUS = 30

# ----------------------------------------------


GRID_SIZE = RADIUS * 2 + 1


def bfs(matrix, start, end):
    """
    Cette fonction prend une matrice de 0:obstacle ou 1:vide en entrée
    qui correspond à la map. On cherche ensuite le chemin le plus court
    reliant le point 'start' au point 'end'.

    Ici:
    matrix -> Matrice (de liste) de 0 ou 1
    start -> list [int, int] : correspond au point de départ
    end -> list [int, int] : correspond au point d'arrivé
    """

    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([start])
    visited = {start: None}

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = visited[(x, y)]
            path.append(start)
            path.reverse()
            return path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if matrix[nx][ny] == 1 and (nx, ny) not in visited:
                    visited[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
    return None

def is_path(player_pos, path):
    """Pour éviter de scanner les alentours du joueur (pour RADIUS blocs 
    d'alentours, ça correspond déjà à GRID_SIZE x GRID_SIZE blocs, donc 
    GRID_SIZE*GRID_SIZE requêtes pour connaître les blocs autour du joueur), 
    on préfère actualiser la map (premièrement vide) avec des obstacles au 
    fur et à mesure. On fait alors les vérifications d'obstacles uniquement
     sur UN chemin donné par la fonction 'bfs', si obstacle, on le rajoute puis on
     cherche à nouveau le chemin le plus cours à l'aide de 'bfs'

     Ici:
     player_pos -> obtenue à l'aide de m.player_position()
     path -> chemin obtenue à l'aide de 'bfs'
    )
    """
    for i in path:
        if m.getblock(player_pos[0] + (i[0]-RADIUS), player_pos[1], player_pos[2] + (i[1]-RADIUS)) != "minecraft:air":
            return (False, (i[0], i[1]))
    return (True, (-1, -1))

def get_path(a, b, max_distance=RADIUS * 2):
    """Ici, on crée la matrice 'monde' qu'on enverra à 'bfs'.
    On crée le 'monde' sans aucun obstacle, puis 'bfs' se charge de
    vérifier la fidélité du chemin. Ou bien le chemin est le bon, ou bien 
    il y a un obstacle, dans ce cas, on actualise la map.

    -> Ici:
    a, b -> int : correspond au point d'arrivé
    """
    x, y, z = m.player_position()
    x, y, z = math.floor(x), math.floor(y), math.floor(z)

    if (math.fabs(x - a) > max_distance) and (math.fabs(z - b) > max_distance):
        return False

    goal = (int(a - x + RADIUS), int(b - z + RADIUS))
    world = [[1 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

    while True:
        chemin = bfs(world, (RADIUS, RADIUS), goal)
        if chemin is None:
            return []
        verification = is_path((x, y, z), chemin)
        if verification[0]:
            return chemin
        else:
            world[verification[1][0]][verification[1][1]] = 0

def get_instructions(path, facing="south"):
    """
    Si un chemin est trouvé, on cherche à limiter au maximum les instructions
    nécéssaires au joueur pour se rendre d'un point 'a' à un point 'b'.

    ici: path -> chemin optimal obtenu à l'aide de 'bfs'
    """
    if not path or len(path) < 2:
        return []

    start_x, y, start_z = m.player_position()
    start_x, start_z = math.floor(start_x), math.floor(start_z)

    relative_dirs = {
        "south": {(1, 0): "left", (-1, 0): "right", (0, 1): "forward", (0, -1): "back"},
        "north": {(1, 0): "right", (-1, 0): "left", (0, 1): "back", (0, -1): "forward"},
        "east":  {(1, 0): "forward", (-1, 0): "back", (0, 1): "left", (0, -1): "right"},
        "west":  {(1, 0): "back", (-1, 0): "forward", (0, 1): "right", (0, -1): "left"}
    }

    dir_map = relative_dirs.get(facing.lower(), relative_dirs["south"])
    instructions = []

    i = 1
    while i < len(path):
        dx = path[i][0] - path[i-1][0]
        dz = path[i][1] - path[i-1][1]

        direction = dir_map.get((dx, dz))
        if not direction:
            i += 1
            continue

        j = i + 1
        while j < len(path):
            next_dx = path[j][0] - path[j-1][0]
            next_dz = path[j][1] - path[j-1][1]
            if next_dx == dx and next_dz == dz:
                j += 1
            else:
                break

        end_rel_x, end_rel_z = path[j - 1]
        abs_x = start_x + (end_rel_x - RADIUS)
        abs_z = start_z + (end_rel_z - RADIUS)

        instructions.append((direction, (abs_x, abs_z)))
        i = j

    return instructions

def move_step(press_func, target_x, target_z, direction, timeout=8.0, poll=0.02, settle=0.1):
    """C'est se qui permet de se déplacer en ligne droite vers un certains points

    Ici:
    press_func -> Fonction (forward, backward, left ou right)
    """
    press_func(True)
    t0 = time.time()
    reached = False
    try:
        while True:
            x, y, z = m.player_position()
            if (math.floor(x), math.floor(z)) == (target_x, target_z):

                #Ajustement pour éviter d'être bloqué
                if direction == 1:
                    if (z - target_z) > 0.1:
                        reached = True
                elif direction == 2:
                    if (z - target_z) < 0.7:
                        reached = True
                elif direction == 3:
                    if (x - target_x) > 0.2:
                        reached = True
                else:
                    if (x - target_x) < 0.8:
                        reached = True

                if reached:
                    break

            if time.time() - t0 > timeout:
                m.echo(f"bloque en essayant d'atteindre ({target_x}, {target_z})")
                break
            time.sleep(poll)
    finally:
        press_func(False)
        time.sleep(settle)  # laisse l'inertie retomber avant l'etape suivante
    return reached

"""
Les quatres fonctions suivantes sont nécéssaires à la fonction : move_step
Elles correspondent à l'appuie des touches pour se déplacer dans les quatres
directions.
"""
def forward(a, b):
    return move_step(m.player_press_forward, a, b, 1)

def backward(a, b):
    return move_step(m.player_press_backward, a, b, 2)

def left(a, b):
    return move_step(m.player_press_left, a, b, 3)

def right(a, b):
    return move_step(m.player_press_right, a, b, 4)

"""
            --- Fonction principale ---
"""
def goto(a, b):
    """C'est la fonction que l'on appelle en jeu, qui permet de trouver le
    chemin optimal reliant deux points et permet au joueur de s'y déplacer.

    -> Ici:
    a, b -> int : correspond au point d'arrivé
    """
    x, y, z = m.player_position()
    x, y, z = math.floor(x), math.floor(y), math.floor(z)

    if (math.fabs(x - a) > RADIUS) and (math.fabs(z - b) > RADIUS):
        m.echo("la destination est trop éloignée")
        return None

    m.player_set_orientation(0.0, 0.0)

    path = get_path(a, b)
    if not path:
        m.echo("aucun chemin trouvé")
        return None

    instruction = get_instructions(path)

    action = {"forward": forward, "back": backward, "right": right, "left": left}

    for direction, (tx, tz) in instruction:
        func = action.get(direction)
        if func is None:
            continue
        ok = func(tx, tz)
        if not ok:
            # l'etape a timeout: on s'arrete au lieu de continuer a l'aveugle
            # avec un trajet desynchronise
            m.echo("déplacement interrompu, position inattendue")
            return 0

    return 1

def center_on_block(error=0.1, timeout=2.0, poll=0.02, tap=0.05):
    """
    Recentre le joueur au centre du bloc sur lequel il se trouve actuellement.

    Ici:
    error   -> tolérance acceptée (en blocs) entre la position du joueur et le centre du bloc
    timeout -> temps maximum (en secondes) alloué pour le recentrage
    poll    -> intervalle entre chaque vérification de position
    tap     -> durée de chaque "petite pression" de touche pour ajuster la position

    Suppose une orientation sud (comme dans 'goto'), donc on la force ici
    pour garder la même correspondance touche/direction que le reste du code.
    """
    m.player_set_orientation(0.0, 0.0)

    x, y, z = m.player_position()
    target_x = math.floor(x) + 0.5
    target_z = math.floor(z) + 0.5

    t0 = time.time()
    while time.time() - t0 < timeout:
        x, y, z = m.player_position()
        dx = target_x - x
        dz = target_z - z

        if abs(dx) <= error and abs(dz) <= error:
            return True

        if abs(dz) > error:
            press = m.player_press_forward if dz > 0 else m.player_press_backward
            press(True)
            time.sleep(tap)
            press(False)

        if abs(dx) > error:
            press = m.player_press_left if dx > 0 else m.player_press_right
            press(True)
            time.sleep(tap)
            press(False)

        time.sleep(poll)

    m.echo("centrage non atteint dans le temps imparti")
    return False
