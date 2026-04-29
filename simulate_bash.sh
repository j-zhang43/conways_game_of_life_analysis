#!/bin/bash

echo "Starting Simulations ..."

for density in {1..100}; do
    for seed in {1..10}; do
        python cgol_model.py -g 100 -d $density -m 5000 -s $seed
    done
done
