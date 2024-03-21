import pygame
import random

class Bacteries:
    def __init__(self):
        self.x_pos_rand = 0
        self.y_pos_rand = 0
        self.x_pos_select = 0
        self.y_pos_select = 0
    
    def draw(self, screen, tilesize, nbr_max_x, nbr_max_y, x, y):
        self.x_pos_rand = random.randint(0, (nbr_max_x - 1))
        self.y_pos_rand = random.randint(0, (nbr_max_y - 1))
        self.x_pos_select = x[self.x_pos_rand]
        self.y_pos_select = y[self.y_pos_rand]
        pygame.draw.rect(screen, (255, 0, 0), (self.x_pos_select, self.y_pos_select, tilesize, tilesize))

