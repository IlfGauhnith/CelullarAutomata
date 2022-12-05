from random import randint
import matplotlib.pyplot as plt

grid_size = 25
grid = [[]]
generation = 0


def init_grid():
    global grid
    grid = [[randint(0, 1) for _ in range(grid_size)] for _ in range(grid_size)]


def apply_automata_rules():
    global grid, grid_size

    for i in range(grid_size):
        for j in range(grid_size):
            if j == 0 or j == grid_size - 1:
                grid[i][j] = sum(grid[i]) % 2  # Para a primeira e última posição do grid, aplica 0 se a soma de todos os elementos do grid for par e 1 se for ímpar.
            else:
                grid[i][j] = grid[i][j + 1]


init_grid()
apply_automata_rules()
for generation in range(1, 50):
    apply_automata_rules()

    plt.matshow(grid)
    plt.colorbar()
    plt.title("generation " + str(generation))
    plt.pause(1)
    plt.close()
