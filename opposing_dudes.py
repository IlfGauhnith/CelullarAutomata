import os
import random as random
import shutil

import imageio as imageio
import matplotlib.pyplot as plt
import numpy as np

grid_size = 50
grid = [[]]
generation_max = 100
dudes_coordinates = ([0, grid_size - 1], [grid_size - 1, 0])
amount_of_dudes = 0
dudes_movement_control = []


def clear_directory(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def generate_gif():
    with imageio.get_writer(f'opposing_dudes/{generation_max}generations_{amount_of_dudes}dudes.gif', mode='I') as writer:
        for i in range(generation_max):
            image = imageio.imread('output_pngs/generation' + str(i) + '.png')
            writer.append_data(image)


def generate_dudes():
    global grid
    occupied_coordinates = []

    for _ in range(amount_of_dudes):

        while True:
            coordinates = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))

            if coordinates not in occupied_coordinates:
                break

        occupied_coordinates.append(coordinates)
        grid[coordinates[0]][coordinates[1]] = 1


def init_grid():
    global grid
    grid = np.zeros((grid_size, grid_size), dtype=int)

    generate_dudes()


def generate_new_coordinates(current_x, current_y):
    if current_x == 0:
        x = 1
    elif current_x == grid_size - 1:
        x = - 1
    else:
        x = random.choice([-1, 1])  # up: -1, down: +1

    if current_y == 0:
        y = 1
    elif current_y == grid_size - 1:
        y = - 1
    else:
        y = random.choice([-1, 1])  # left: -1, right: +1

    return random.choice([(current_x, current_y + y), (current_x + x, current_y)])


def collision(pretended_x, pretended_y):
    return grid[pretended_x][pretended_y] == 1


def apply_automata_rules():
    global grid, dudes_movement_control

    for i in range(grid_size):
        for j in range(grid_size):

            if (i, j) in dudes_movement_control:
                continue
            elif grid[i][j] != 0:
                go_to = generate_new_coordinates(i, j)

                if not collision(go_to[0], go_to[1]):
                    grid[go_to[0]][go_to[1]] = grid[i][j]
                    grid[i][j] = 0
                    dudes_movement_control.append((go_to[0], go_to[1]))

    dudes_movement_control = []


for amount_of_dudes in [10, 25, 50, 100]:
    clear_directory('output_pngs')
    init_grid()
    apply_automata_rules()

    for i in range(generation_max):
        apply_automata_rules()
        plt.matshow(grid)
        plt.savefig('output_pngs/generation' + str(i) + '.png')

    generate_gif()
    clear_directory('output_pngs')
