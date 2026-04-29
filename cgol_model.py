import argparse
import numpy as np
import cv2
import random

class Simulation:
    def __init__(self, grid_size, inital_density, max_steps, seed, save_video): 
        self.step = 0
        
        self.grid = np.zeros((grid_size, grid_size), dtype=np.uint8)

        # create random grid with 1s (alive baseed on densit)
        random.seed(seed)
        rand_idxs = random.sample(range(0, grid_size*grid_size), int(grid_size*grid_size*(inital_density/100)))
        for n in rand_idxs:
            self.grid[n//grid_size][n%grid_size] = 1
        
        self.history = {tuple(self.grid.flatten())}

        self.kernel = np.array([[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1]], dtype=np.float32)

        # simulate and save images if needed
        cont = True
        self.imgs = []
        if save_video: self.grid_to_imgs()
        while cont and self.step < max_steps:
            cont = self.simulation_round()
            if save_video: self.grid_to_imgs()
        
        # save video
        if save_video:
            filename = f"g-{grid_size}d-{inital_density}s-{seed}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = 10.0
            height, width = self.imgs[0].shape
            frame_size = (width, height)

            out = cv2.VideoWriter(filename, fourcc, fps, frame_size, isColor=False)
            
            for img in self.imgs:
                out.write(img)

            out.release()

        final_density = np.count_nonzero(self.grid)/ (grid_size*grid_size)
        reason = None # zeros, stagnated, max
        if not np.any(self.grid):reason = "zeros"
        elif self.step == max_steps: reason = "max"
        else: reason = "stagnated"

        # write to csv
        with open("data.csv", "a") as file:
            file.write(f"{seed},{inital_density},{self.step},{final_density},{reason} \n")

    def grid_to_imgs(self):
        cell_size = max(1, 1000//len(self.grid))
        img_array = 1 - np.repeat(np.repeat(self.grid, cell_size, axis=0), cell_size, axis=1)
        img_array = (img_array * 255).astype(np.uint8)
        self.imgs.append(img_array)

    def simulation_round(self):
        neighbor_count = cv2.filter2D(self.grid, -1, self.kernel, borderType=cv2.BORDER_CONSTANT)
    
        # Create boolean masks to identify alive and dead cells
        alive = (self.grid == 1)
        dead = (self.grid == 0)
        
        next_grid = self.grid.copy()
        
        next_grid[alive & ((neighbor_count < 2) | (neighbor_count > 3))] = 0
        next_grid[dead & (neighbor_count == 3)] = 1

        self.grid = next_grid
        
        # check if already exists
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

if __name__ == "__main__":
    main()