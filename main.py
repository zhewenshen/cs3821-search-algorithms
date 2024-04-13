import argparse
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from Graph import Graph
from SearchAlgorithm import BFS, DFS, Dijkstra, AStar
from Benchmark import Benchmark

def plot_grid(size, path, start, end, title, obstacles):
    grid = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            if (x, y) in obstacles:
                grid[x, y] = 0  # Obstacles
            else:
                grid[x, y] = 1  # Free space

    if path:
        px, py = zip(*path)
        plt.plot(py, px, 'b-', linewidth=2)

    plt.imshow(grid, cmap='gray', origin='upper')
    plt.plot(start[1], start[0], 'go')
    plt.plot(end[1], end[0], 'ro')
    plt.title(title)
    plt.xticks([])
    plt.yticks([])

def visualize_single_grid(size, obstacle_ratio):
    start = (np.random.randint(size // 2), np.random.randint(size // 2))
    end = (np.random.randint(size // 2) + size // 2, np.random.randint(size // 2) + size // 2)
    graph = Graph(size, obstacle_ratio, start, end)
    algorithms = {'BFS': BFS, 'DFS': DFS, 'Dijkstra': Dijkstra, 'A*': AStar}

    plt.figure(figsize=(12, 12))
    for i, (name, AlgorithmClass) in enumerate(algorithms.items(), 1):
        algorithm = AlgorithmClass(graph)
        path = algorithm.search()
        plt.subplot(2, 2, i)
        plot_grid(size, path, start, end, f'{name} Path', graph.obstacles)
    plt.tight_layout()
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"out/grid_search_{size}_{obstacle_ratio}_{timestamp}.png"
    plt.savefig(filename, dpi=500)
    print(f'Grid search results saved to {filename}')

def main():
    parser = argparse.ArgumentParser(description='Graph Search Visualization and Benchmarking Tool')
    parser.add_argument('--mode', type=str, choices=['visualize', 'benchmark', 'both'], default='both',
                        help='Choose to run visualization, benchmark, or both.')
    parser.add_argument('--size', type=int, default=25, help='Grid size for visualization')
    parser.add_argument('--obstacle_ratio', type=float, default=0.2, help='Obstacle ratio for visualization')
    parser.add_argument('--benchmark_start', type=int, default=10, help='Starting grid size for benchmark')
    parser.add_argument('--benchmark_end', type=int, default=100, help='Ending grid size for benchmark')
    parser.add_argument('--benchmark_step', type=int, default=10, help='Grid size step for benchmark')
    parser.add_argument('--benchmark_runs', type=int, default=1, help='Number of runs for each grid size in benchmark')
    args = parser.parse_args()

    if args.mode in ('visualize', 'both'):
        visualize_single_grid(args.size, args.obstacle_ratio)
    
    if args.mode in ('benchmark', 'both'):
        benchmark = Benchmark({'BFS': BFS, 'DFS': DFS, 'Dijkstra': Dijkstra, 'A*': AStar}, 
                              args.benchmark_start, args.benchmark_end, args.benchmark_step, 
                              args.obstacle_ratio, args.benchmark_runs)
        sizes, time_bench = benchmark.run()
        benchmark.plot_time_benchmarks(sizes, time_bench)

if __name__ == "__main__":
    main()
