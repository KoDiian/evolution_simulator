import pygame
import random

class Bacterie:
    def __init__(self, x, y, energy, genes, cellsize):
        self.x = x
        self.y = y
        self.energy = energy
        self.genes = genes
        self.cellsize = cellsize
        self.color = (255, 0, 0)  # Couleur de la bactérie

    def move(self, nx, ny, direction_change_energy):
        self.x = nx
        self.y = ny
        self.energy -= direction_change_energy

    def eat(self, energy_per_food):
        self.energy += energy_per_food

    def die(self):
        self.energy = 0

    def reproduce(self):
        child_energy = self.energy / 2
        child_genes = self.mutate_genes(self.genes)
        return Bacterie(self.x, self.y, child_energy, child_genes, self.cellsize)

    def mutate_genes(self, genes):
        new_genes = genes[:]
        n = random.randint(0, len(new_genes) - 1)
        new_genes[n] += (random.random() - 0.5)
        if new_genes[n] < 0:
            new_genes[n] = 0
        total = sum(new_genes)
        new_genes = [gene / total for gene in new_genes]
        return new_genes

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x * self.cellsize - 2 * self.cellsize,
                                               self.y * self.cellsize - 2 * self.cellsize,
                                               self.cellsize, self.cellsize))
