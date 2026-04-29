import argparse
import pygame 

class Simulation:
    def __init__(): 
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--grid_size", type=int, required=True, help="Grid size of the simulation (int)")
    parser.add_argument("-d","--initial_density", type=int, required=True, help="Percentage of the initial cells that are alive (int)[0-100]")
    def range_density():
        pass
    parser.add_argument("-m","--max_steps", type=int, required=True, help="Grid size of the simulation (int)")
    parser.add_argument("-s","--seed", type=int, required=True, help="Grid size of the simulation (int)")
    parser.add_argument("-v","--save_video", type=int, required=True, help="Grid size of the simulation (int)")