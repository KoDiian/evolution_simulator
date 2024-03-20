import pygame
import random


class SimulatedEvolution:
    def __init__(self, cfg):
        # Colors
        self.colMicrobe = (0, 0, 255)
        self.colBack = (0, 0, 0)
        self.colFood = (0, 255, 0)
        # Other simulation parameters
        self.food_spawn_per_tick = cfg['food_spawn_per_tick']
        self.energy_per_food = cfg['energy_per_food']
        self.energy_max = cfg['energy_max']
        self.energy_to_reproduce = cfg['energy_to_reproduce']
        self.initial_microbe_num = cfg['initial_microbe_num']
        self.microbe_num = 0
        # Microbe Motion Table. One Entry per Motion Direction
        self.motion_tab = [[-1.0, 1.0], [0.0, 1.0], [1.0, 1.0],
                           [-1.0, 0.0], [1.0, 0.0],
                           [-1.0, -1.0], [0.0, -1.0], [1.0, -1.0]]
        # Ammount of energy subtracted from the microbe depending on the change in movement direction
        # (there is a price for taking hard turns)
        self.steering_cost = [[0], [1], [2], [4], [8], [4], [2], [1]]
        # Copy simulation parameters
        self.cv_width = cfg['cv_width']
        self.cv_height = cfg['cv_height']
        self.cellsize = cfg['cellsize']
        self.cv = pygame.display.set_mode((self.cv_width, self.cv_height))
        pygame.display.set_caption("Simulated Evolution")
        self.cells_x = self.cv_width // self.cellsize
        self.cells_y = self.cv_height // self.cellsize
        self.clock = pygame.time.Clock()
        self.food = [[0 for _ in range(self.cells_x)]
                     for _ in range(self.cells_y)]
        # create initial population
        self.microbes = []
        for _ in range(self.initial_microbe_num):
            self.microbe_create(None)
        # initialize food
        for _ in range(40000):
            self.put_food(random.randint(0, self.cells_x - 1),
                          random.randint(0, self.cells_y - 1))

    def put_food(self, x, y):
        self.food[y][x] = 1

    def remove_food(self, x, y):
        self.food[y][x] = 0

    def tick(self):
        self.cv.fill(self.colBack)
        self.spawn_food_normal()  # Dessiner la nourriture normalement
        for m in self.microbes:
            self.microbe_move(m)
            self.microbe_draw(m)
        pygame.display.flip()
        self.clock.tick(60)

    def spawn_food_normal(self):
        for _ in range(self.food_spawn_per_tick):
            x = random.randint(0, self.cells_x - 1)
            y = random.randint(0, self.cells_y - 1)
            pygame.draw.rect(self.cv, self.colFood, (x * self.cellsize,
                             y * self.cellsize, self.cellsize, self.cellsize))
            self.put_food(x, y)

    def spawn_food_grid(self):
        grid_size = 10
        for x in range(0, self.cells_x, grid_size):
            for y in range(0, self.cells_y, grid_size):
                pygame.draw.rect(self.cv, self.colFood, (x * self.cellsize,
                                 y * self.cellsize, self.cellsize, self.cellsize))
                self.put_food(x, y)

    def spawn_food_center_rect(self):
        rect_size = min(self.cells_x, self.cells_y) // 3
        rect_x = (self.cells_x - rect_size) // 2
        rect_y = (self.cells_y - rect_size) // 2
        pygame.draw.rect(self.cv, self.colFood, (rect_x * self.cellsize,
                         rect_y * self.cellsize, rect_size * self.cellsize, rect_size * self.cellsize))
        for x in range(rect_x, rect_x + rect_size):
            for y in range(rect_y, rect_y + rect_size):
                self.put_food(x, y)

    def microbe_create(self, parent):
        self.microbe_num += 1
        if parent is None:
            m = {
                'x': random.randint(0, self.cells_x - 1),
                'y': random.randint(0, self.cells_y - 1),
                'dir': random.randint(0, 7),
                'energy': self.microbe_num + 100,
                'age': 0,
                'genes': self.create_random_genes(),
            }
        else:
            new_genes = self.mutate_genes(parent['genes'])
            m = {
                'x': parent['x'],
                'y': parent['y'],
                'dir': random.randint(0, 7),
                'energy': parent['energy'] / 2,
                'age': 0,
                'genes': new_genes,
            }
            parent['energy'] = parent['energy'] / 2
        self.microbes.append(m)

    def microbe_die(self, m):
        self.microbe_num -= 1
        if m in self.microbes:
            self.microbes.remove(m)

    def microbe_move(self, m):
        m['age'] += 1
        m['energy'] -= 1
        nx = int(m['x'] + self.motion_tab[m['dir']][0])
        ny = int(m['y'] + self.motion_tab[m['dir']][1])
        if 0 <= nx < self.cells_x and 0 <= ny < self.cells_y:
            if self.food[ny][nx] > 0 and m['energy'] < self.energy_max:
                m['energy'] += self.energy_per_food
                self.remove_food(nx, ny)  # Supprimer la nourriture de la cellule
        new_dir = random.choices(range(len(m['genes'])), weights=m['genes'])[0]
        energy_for_dir_change = (
            new_dir + len(m['genes']) - m['dir']) % len(m['genes'])
        m['dir'] = new_dir
        m['energy'] -= self.steering_cost[energy_for_dir_change][0]
        m['x'] = nx
        m['y'] = ny
        if m['energy'] < 0:
            self.microbe_die(m)
        elif m['energy'] > self.energy_to_reproduce:
            self.microbe_create(m)


    def create_random_genes(self):
        genes = [random.random() for _ in range(8)]
        total = sum(genes)
        genes = [gene / total for gene in genes]
        return genes

    def mutate_genes(self, genes):
        new_genes = genes[:]
        n = random.randint(0, len(new_genes) - 1)
        new_genes[n] += (random.random() - 0.5)
        if new_genes[n] < 0:
            new_genes[n] = 0
        total = sum(new_genes)
        new_genes = [gene / total for gene in new_genes]
        return new_genes

    def microbe_draw(self, m):
        pygame.draw.rect(self.cv, self.colMicrobe, (m['x'] * self.cellsize - 2 * self.cellsize,
                                                    m['y'] * self.cellsize -
                                                    2 * self.cellsize,
                                                    self.cellsize * 4, self.cellsize * 4))


if __name__ == "__main__":
    pygame.init()
    config = {
        'food_spawn_per_tick': 2,
        'energy_per_food': 40,
        'energy_max': 1500,
        'energy_to_reproduce': 1000,
        'initial_microbe_num': 10,
        'cv_width': 800,
        'cv_height': 600,
        'cellsize': 2
    }
    simulation = SimulatedEvolution(config)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    simulation.spawn_food_normal()
                elif event.key == pygame.K_2:
                    simulation.spawn_food_grid()
                elif event.key == pygame.K_3:
                    simulation.spawn_food_center_rect()
        simulation.tick()
    pygame.quit()
