import numpy as np
import random

class Graph:
    def __init__(self, size, obstacle_ratio, start, end):
        self.size = size
        self.obstacle_ratio = obstacle_ratio
        self.start = start
        self.end = end
        self.graph, self.obstacles = self.generate_grid_graph()
        
    def get_graph(self):
        return self.graph
    
    def get_obstacles(self):
        return self.obstacles

    def generate_grid_graph(self):
        graph = {}
        obstacles = set()
        while len(obstacles) < int(self.size * self.size * self.obstacle_ratio):
            obs = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if obs != self.start and obs != self.end:
                obstacles.add(obs)
        
        for i in range(self.size):
            for j in range(self.size):
                node = (i, j)
                if node in obstacles:
                    continue
                edges = {}
                if i > 0 and (i-1, j) not in obstacles:
                    edges[(i-1, j)] = 1
                if i < self.size - 1 and (i+1, j) not in obstacles:
                    edges[(i+1, j)] = 1
                if j > 0 and (i, j-1) not in obstacles:
                    edges[(i, j-1)] = 1
                if j < self.size - 1 and (i, j+1) not in obstacles:
                    edges[(i, j+1)] = 1
                graph[node] = edges
        return graph, obstacles
