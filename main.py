import pygame
from food import Food
import random

pygame.init()

# Constantes
tilesize = 5 # Taille d'une tuile
map = 32 # Multiplicateur de la taille du monde
size = (20,20) # Taille du monde
fps = 30 # fps du jeu

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

screen.fill(color["background_color"])


nourriture = Food()

nbr_max_x = ((size[0] * map) / tilesize)
nbr_max_y = ((size[1] * map) / tilesize)
x = []
y = []
for i in range(int(nbr_max_x)):
    x.append(int(i*tilesize))
for i in range(int(nbr_max_y)):
    y.append(int(i*tilesize))

food_in_map = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False




    nourriture.draw(screen, tilesize, nbr_max_x, nbr_max_y, x, y, food_in_map)
    

    


    
    pygame.display.flip()
    dt = clock.tick(fps)
print(food_in_map)
pygame.quit()