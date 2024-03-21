import pygame
from food import Food
from bacterie import Bacterie
import random

pygame.init()

# Constantes
tilesize = 5  # Taille d'une tuile
map = 32  # Multiplicateur de la taille du monde
size = (20, 20)  # Taille du monde
fps = 30  # fps du jeu

# Couleurs
color = {
    "background_color": "#000000",
}

BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 48)

running = True
screen = pygame.display.set_mode((size[0] * map, size[1] * map))
clock = pygame.time.Clock()
dt = 0

nourriture = Food()

nbr_max_x = ((size[0] * map) / tilesize)
nbr_max_y = ((size[1] * map) / tilesize)
x = [int(i * tilesize) for i in range(int(nbr_max_x))]
y = [int(i * tilesize) for i in range(int(nbr_max_y))]

food_in_map = []

# Liste pour stocker les bactéries
bacteries = []

# Initialisation de quelques bactéries au début du programme
for _ in range(5):
    x_coord = random.randint(0, size[0] * map // tilesize - 1)
    y_coord = random.randint(0, size[1] * map // tilesize - 1)
    energy = random.randint(500, 1000)
    genes = [random.random() for _ in range(8)]
    total_genes = sum(genes)
    genes = [gene / total_genes for gene in genes]
    bacteries.append(Bacterie(x_coord, y_coord, energy, genes, tilesize))



screen.fill(color["background_color"])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    screen.fill(color["background_color"])
    
    
    nourriture.draw(screen, tilesize, nbr_max_x, nbr_max_y, x, y, food_in_map)

    # Déplacez et dessinez chaque bactérie
    for bacterie in bacteries:
        bacterie.draw(screen)
        nx = bacterie.x + random.choice([-1, 0, 1])
        ny = bacterie.y + random.choice([-1, 0, 1])
        if bacterie.energy <= 0:
            bacteries.remove(bacterie)
        if 0 <= nx < nbr_max_x and 0 <= ny < nbr_max_y:
            bacterie.move(nx, ny, 1)
            if (nx, ny) in food_in_map:
                bacterie.eat(50)
                food_in_map.remove((nx, ny))
            if bacterie.energy > 700:
                new_bacterie = bacterie.reproduce()
                bacteries.append(new_bacterie)



    pygame.display.flip()
    dt = clock.tick(fps)
pygame.quit()
