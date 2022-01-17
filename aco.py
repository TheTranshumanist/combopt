from graph import Graph
from src.classes import Solution
from typing import List, Dict
from time import perf_counter
import random


class Ant:

    """
    Implementation of agent class
    """

    trail: List[int]
    visited: List[bool]
    trail_length: float

    def __init__(self, g: Graph) -> None:
        start = random.randint(1, g.dimension)
        self.trail = [start]
        self.visited = [False] * (g.dimension + 1)
        self.visited[start] = True
        self.trail_length = 0

    def visit_vertex(self, vertex: int, g: Graph) -> None:
        self.trail_length += g.distances[self.trail[-1]][vertex]
        self.trail.append(vertex)
        self.visited[vertex] = True

    def get_length(self, g: Graph) -> float:
        return self.trail_length + g.distances[self.trail[-1]][self.trail[0]]


class AntSystemSolution(Solution):

    """
    Implementation of the Ant Colony Optimization Algorithm
    for Travelling Salesman Problem
    """

    q0: float = 0.9
    alpha: float = 1
    beta: float = 5
    rho: float = 0.1
    phi: float = 0.1
    iterations: int = 10000
    ant_count: int = 10
    init_pheromone: float = 1e-6

    ants: List[Ant]
    pheromone: Dict[int, Dict[int, float]]
    graph: Graph

    def set_pheromone(self) -> None:
        n = self.graph.dimension
        self.pheromone = {i: {j: self.init_pheromone for j in range(
            1, n + 1) if j != i} for i in range(1, n + 1)}

    def find_route(self, g: Graph) -> None:
        self.distance = float('inf')
        self.graph = g
        self.set_pheromone()
        start = perf_counter()
        for i in range(self.iterations):
            end = perf_counter()
            if end - start > 300:
                break
            self.setup_ants()
            self.move_ants()
            self.update_solution()
            self.update_pheromone_global()
            print(f'{i + 1} iteration | Best trail length -> {self.distance}')

    def setup_ants(self) -> None:
        self.ants = [Ant(self.graph) for _ in range(self.ant_count)]

    def move_ants(self) -> None:
        for ant in self.ants:
            for i in range(self.graph.dimension - 1):
                target = self.select_next(ant)
                ant.visit_vertex(target, self.graph)
                self.update_pheromone_local(ant)

    def select_next(self, ant: Ant) -> int:
        q = random.uniform(0, 1)
        if q > self.q0:
            probabilities = self.calc_probabilities(ant)
            random_value = random.random()
            for vertex, probability in enumerate(probabilities):
                random_value -= probability
                if random_value <= 0:
                    return vertex
        else:
            probabilities = self.calc_argmax(ant)
            vertex = max(range(len(probabilities)),
                         key=lambda i: probabilities[i])
            return vertex

    def calc_probabilities(self, ant: Ant) -> List[float]:
        cur = ant.trail[-1]
        denominator = 0
        for i in range(1, self.graph.dimension + 1):
            if not ant.visited[i]:
                denominator += self.pheromone[cur][i]**self.alpha * \
                    (1 / self.graph.distances[cur][i])**self.beta
        arr = [0] * (self.graph.dimension + 1)
        for i in range(1, self.graph.dimension + 1):
            if not ant.visited[i]:
                p = self.pheromone[cur][i]**self.alpha * \
                    (1 / self.graph.distances[cur][i])**self.beta
                arr[i] = p / denominator
        return arr

    def calc_argmax(self, ant: Ant) -> List[float]:
        cur = ant.trail[-1]
        arr = [0] * (self.graph.dimension + 1)
        for i in range(1, self.graph.dimension + 1):
            if not ant.visited[i]:
                arr[i] = self.pheromone[cur][i] * \
                    (1 / self.graph.distances[cur][i])**self.beta
        return arr

    def update_pheromone_local(self, ant: Ant) -> None:
        i = ant.trail[-2]
        j = ant.trail[-1]
        self.pheromone[i][j] *= (1 - self.phi)
        self.pheromone[i][j] += self.phi * self.init_pheromone
        self.pheromone[j][i] = self.pheromone[i][j]

    def update_pheromone_global(self) -> None:
        for i in range(1, self.graph.dimension + 1):
            for j in range(i + 1, self.graph.dimension + 1):
                if self.pheromone[i][j] * (1 - self.rho) < 1e-32:
                    self.pheromone[i][j] = 1e-32
                else:
                    self.pheromone[i][j] *= (1 - self.rho)
        for index in range(len(self.route) - 1):
            i = self.route[index]
            j = self.route[index + 1]
            self.pheromone[i][j] += self.rho * (1 / self.distance)
            self.pheromone[j][i] = self.pheromone[i][j]

    def update_solution(self):
        for ant in self.ants:
            ant_distance = ant.get_length(self.graph)
            if ant_distance < self.distance:
                self.distance = ant_distance
                self.route = ant.trail.copy()
