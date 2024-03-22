import pygame
from food import Food
from bacterie import Bacterie
import random
import matplotlib.pyplot as plt

pygame.init()

# Constantes
tilesize = 5  # Taille d'une tuile
map = 5  # Multiplicateur de la taille du monde
size = (100, 100)  # Taille du monde
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

nbr_bacteries = []
nbr_iteration = []
nbr_iteration_chiffre = 0
nbr_food = []

# Initialisation de quelques bactéries au début du programme
for _ in range(5):
    x_coord_ran = random.randint(0, nbr_max_x-1)
    y_coord_ran = random.randint(0, nbr_max_y-1)
    x_coord = x[x_coord_ran]
    y_coord = y[y_coord_ran]
    energy = 250
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    plt.grid(True)
                    plt.figure("Bacterie")
                    plt.title('Bacterie en fonction du temps')
                    plt.xlabel('Nombre de répition de la boucle while')
                    plt.ylabel('Nombre de bacterie')
                    plt.plot(nbr_iteration, nbr_bacteries, marker='o', linestyle='-')

                    plt.grid(True)
                    plt.figure("Nourriture")
                    plt.title('Nourriture en fonction du temps')
                    plt.ylabel('Nombre de nourriture')
                    plt.plot(nbr_iteration, nbr_food, marker='o', linestyle='-')
                    plt.grid(True)

                    plt.show()
                    


    

    
    for _ in range (5):
        nourriture.draw(screen, tilesize, nbr_max_x, nbr_max_y, x, y, food_in_map)

    # Déplacez et dessinez chaque bactérie
    for bacterie in bacteries:
        nx = bacterie.x + random.choice([-5, 0, 5])
        ny = bacterie.y + random.choice([-5, 0, 5])
        if bacterie.energy <= 0:
            pygame.draw.rect(screen, (0,0,0), (bacterie.x, bacterie.y, tilesize, tilesize))
            bacteries.remove(bacterie)
        else:
            if 0 <= nx < nbr_max_x * 5 and 0 <= ny < nbr_max_y * 5:
                pygame.draw.rect(screen, (0,0,0), (bacterie.x, bacterie.y, tilesize, tilesize))
                
                bacterie.move(nx, ny, 1)
                if (nx, ny) in food_in_map:
                    bacterie.eat(20)
                    food_in_map.remove((nx, ny))
                if bacterie.energy > 300:
                    new_bacterie = bacterie.reproduce()
                    bacterie.energy = bacterie.energy / 2
                    bacteries.append(new_bacterie)
            bacterie.draw(screen)
          
            
    nbr_bacteries.append(len(bacteries))
    nbr_iteration_chiffre +=1
    nbr_iteration.append(nbr_iteration_chiffre)
    nbr_food.append(len(food_in_map))
    
    

  
    print(nbr_iteration_chiffre)

    

    pygame.display.flip()
    dt = clock.tick(fps)



pygame.quit()
