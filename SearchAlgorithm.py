import heapq
import time

class SearchAlgorithm:
    def __init__(self, graph):
        self.graph = graph.graph
        self.start = graph.start
        self.end = graph.end

    def search(self):
        raise NotImplementedError

    def track_path(self, came_from):
        path = []
        step = self.end
        if self.end not in came_from:
            return []
        while step != self.start:
            path.append(step)
            step = came_from[step]
        path.append(self.start)
        path.reverse()
        return path

class BFS(SearchAlgorithm):
    def search(self):
        queue = [(self.start, 0)]
        visited = set()
        came_from = {self.start: None}
        while queue:
            node, distance = queue.pop(0)
            if node == self.end:
                return self.track_path(came_from)
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        came_from[neighbor] = node
                        queue.append((neighbor, distance + 1))
        return []

class DFS(SearchAlgorithm):
    def search(self):
        stack = [(self.start, 0)]
        visited = set()
        came_from = {self.start: None}
        while stack:
            node, distance = stack.pop()
            if node == self.end:
                return self.track_path(came_from)
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        came_from[neighbor] = node
                        stack.append((neighbor, distance + 1))
        return []

class Dijkstra(SearchAlgorithm):
    def search(self):
        distances = {node: float('inf') for node in self.graph}
        distances[self.start] = 0
        pq = [(0, self.start)]
        came_from = {self.start: None}
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            if current_node == self.end:
                return self.track_path(came_from)
            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
                    came_from[neighbor] = current_node
        return []

class AStar(SearchAlgorithm):
    def search(self):
        open_set = [(0, self.start)]
        came_from = {self.start: None}
        g_score = {node: float('inf') for node in self.graph}
        g_score[self.start] = 0
        f_score = {node: float('inf') for node in self.graph}
        f_score[self.start] = self.heuristic(self.start, self.end)

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == self.end:
                return self.track_path(came_from)
            for neighbor in self.graph[current]:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return []

    def heuristic(self, node, end):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])
