#!/bin/bash

PYTHON_SCRIPT="main.py"

# echo "Running visualization..."
# python3 $PYTHON_SCRIPT --mode visualize --size 30 --obstacle_ratio 0.25

# echo "Running benchmark..."
# python3 $PYTHON_SCRIPT --mode benchmark --benchmark_start 10 --benchmark_end 50 --benchmark_step 10 --benchmark_runs 3 --obstacle_ratio 0.15

echo "Running both visualization and benchmark..."
python3 $PYTHON_SCRIPT --mode both --size 40 --obstacle_ratio 0.2 --benchmark_start 10 --benchmark_end 1000 --benchmark_step 20 --benchmark_runs 5

echo "All operations completed."
