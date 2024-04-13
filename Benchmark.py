from Graph import Graph
import numpy as np
import time
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm

class Benchmark:
    def __init__(self, algorithms, grid_size_start, grid_size_end, grid_size_step, obstacle_ratio, num_runs):
        self.algorithms = algorithms
        self.grid_size_start = grid_size_start
        self.grid_size_end = grid_size_end
        self.grid_size_step = grid_size_step
        self.obstacle_ratio = obstacle_ratio
        self.num_runs = num_runs

    def run(self):
        time_bench = {name: [] for name in self.algorithms}
        sizes = range(self.grid_size_start, self.grid_size_end + 1, self.grid_size_step)

        # Wrap the outer loop with tqdm for a progress bar
        for size in tqdm(sizes, desc="Benchmarking Grid Sizes"):
            avg_times = {name: 0 for name in time_bench}
            for _ in range(self.num_runs):
                start = (np.random.randint(size // 2), np.random.randint(size // 2))
                end = (np.random.randint(size // 2) + size // 2, np.random.randint(size // 2) + size // 2)
                graph = Graph(size, self.obstacle_ratio, start, end)
                for name, alg_class in self.algorithms.items():
                    algorithm = alg_class(graph)
                    start_time = time.time()
                    algorithm.search()
                    end_time = time.time()
                    avg_times[name] += (end_time - start_time)

            for name in avg_times:
                avg_times[name] /= self.num_runs
                time_bench[name].append(avg_times[name])

        return sizes, time_bench

    def plot_time_benchmarks(self, sizes, time_bench):
        plt.figure(figsize=(12, 6))
        for name, times in time_bench.items():
            coefs = np.polyfit(sizes, times, deg=3)
            smooth_line = np.poly1d(coefs)(sizes)
            plt.plot(sizes, smooth_line, label=name)

        plt.xlabel('Grid Size')
        plt.ylabel('Average Runtime (seconds)')
        plt.title('Average Search Algorithms Runtime Comparison')
        plt.legend()
        plt.grid(True)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"out/benchmark_{self.grid_size_start}-{self.grid_size_end}_{self.obstacle_ratio}_{timestamp}.png"
        plt.savefig(filename, dpi=500)
        plt.close()
        print(f'Benchmark results saved to {filename}')
