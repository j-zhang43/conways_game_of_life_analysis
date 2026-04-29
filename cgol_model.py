import argparse
import numpy as np
import cv2
import random

class Simulation:
    def __init__(self, grid_size, inital_density, max_steps, seed, save_video): 
        self.step = 0
        # fill grid with 0 and randomly fill with 1 based on density
        self.grid = np.zeros((grid_size, grid_size), dtype=int)

        random.seed(seed)
        rand_idxs = random.sample(range(0, grid_size*grid_size), int(grid_size*grid_size*(inital_density/100)))
        for n in rand_idxs:
            self.grid[n//grid_size][n%grid_size] = 1
        
        # history for grid, used to test stagnation
        self.history = {tuple(self.grid.flatten())}

        # simulate and save images if neededa
        cont = True
        self.imgs = []
        if save_video: self.grid_to_imgs()
        while cont and self.step < max_steps:
            if self.step % 50 == 0: print(self.step)
            cont = self.simulation_round()
            if save_video: self.grid_to_imgs()
        
        print(self.step)
        # save video
        if save_video:
            filename = 'output_video.mp4'
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = 10.0
            height, width = self.imgs[0].shape
            frame_size = (width, height)

            out = cv2.VideoWriter(filename, fourcc, fps, frame_size, isColor=False)
            
            for img in self.imgs:
                out.write(img)

            out.release()

    def grid_to_imgs(self):
        cell_size = 1000//len(self.grid)
        img_array = 1 - np.repeat(np.repeat(self.grid, cell_size, axis=0), cell_size, axis=1)
        img_array = (img_array * 255).astype(np.uint8)
        self.imgs.append(img_array)

    def simulation_round(self):
        new_grid = np.zeros((len(self.grid), len(self.grid)), dtype=int)
        dirs = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                count = 0
                # count neighbors for 1
                for dir in dirs:
                    i_new = i + dir[0]
                    j_new = j + dir[1]
                    if 0<= i_new < len(self.grid) and 0<= j_new < len(self.grid) and self.grid[i_new][j_new] == 1: count+=1

                # follow conways game of life rules for next generation
                if self.grid[i][j]:
                    if count < 2: new_grid[i][j] = 0
                    elif count <= 3: new_grid[i][j] = 1
                    else: new_grid[i][j] = 0
                else:
                    if count == 3: new_grid[i][j] = 1
        self.grid = new_grid
        
        if (tuple(self.grid.flatten()) not in self.history):
            self.history.add(tuple(self.grid.flatten()))
        else:
            return False
        
        self.step += 1
        return True

def main():
    def range_density(value):
        ivalue = int(value)
        if not(0 <= ivalue<=100):
            raise argparse.ArgumentTypeError(f"{value} is not between 0-100")
        return ivalue

    def range_positive(value):
        ivalue = int(value)
        if ivalue<0:
            raise argparse.ArgumentTypeError(f"{value} is positive")
        return ivalue

    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--grid_size", type=range_positive, required=True, help="Grid size of the simulation (int > 0)")
    parser.add_argument("-d","--initial_density", type=range_density, required=True, help="Percentage of the initial cells that are alive (int 0-100)")
    parser.add_argument("-m","--max_steps", type=range_positive, required=True, help="Maximum steps before simulation automatically stops (int > 0)")
    parser.add_argument("-s","--seed", type=int, required=True, help="Seed of simulation (int)")
    parser.add_argument("-v","--save_video", action="store_true", help="Save video of simulation if present")
    args = parser.parse_args()

    Simulation(args.grid_size, args.initial_density, args.max_steps, args.seed, args.save_video)

main()
