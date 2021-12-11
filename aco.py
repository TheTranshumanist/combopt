from graph import Graph
from src.classes import Solution
from typing import List, Dict
import random


class Ant:

    """
    Implementation of agent class
    """

    trail: List[int]
    visited: List[bool]
    trail_length: float
    pheromone_change: Dict[int, Dict[int, float]]

    def __init__(self, g: Graph) -> None:
        start = random.randint(1, g.dimension)
        self.trail = [start]
        self.visited = [False] * (g.dimension + 1)
        self.visited[start] = True
        self.trail_length = 0
        self.pheromone_change = {i: {j: 0 for j in range(
            1, g.dimension + 1) if j != i} for i in range(1, g.dimension + 1)}

    def visit_vertex(self, vertex: int, g: Graph) -> None:
        self.trail_length += g.distances[self.trail[-1]][vertex]
        self.trail.append(vertex)
        self.visited[vertex] = True

    def get_length(self, g: Graph) -> float:
        return self.trail_length + g.distances[self.trail[-1]][self.trail[0]]

    def calc_pheromone_change(self, q: int) -> None:
        for index in range(len(self.trail) - 1):
            i = self.trail[index]
            j = self.trail[index + 1]
            self.pheromone_change[i][j] = q / self.trail_length
            self.pheromone_change[j][i] = q / self.trail_length


class AntSystemSolution(Solution):

    """
    Implementation of the Ant Colony Optimization Algorithm
    for Travelling Salesman Problem
    """

    q: int = 71
    alpha: float = 7.95
    beta: float = 19.54
    rho: float = 0.87
    iterations: int = 10000
    ant_count: int = 200
    init_pheromone: float = 1e-4

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
        for i in range(self.iterations):
            self.setup_ants()
            self.move_ants()
            self.update_pheromone()
            self.update_solution()
            print(f'{i + 1} iteration | Best trail length -> {self.distance}')

    def setup_ants(self) -> None:
        self.ants = [Ant(self.graph) for _ in range(self.ant_count)]

    def move_ants(self) -> None:
        for ant in self.ants:
            for i in range(self.graph.dimension - 1):
                target = self.select_next(ant)
                ant.visit_vertex(target, self.graph)

    def select_next(self, ant: Ant) -> int:
        probabilities = self.calc_probabilities(ant)
        random_value = random.random()
        for vertex, probability in enumerate(probabilities):
            random_value -= probability
            if random_value <= 0:
                return vertex

    def calc_probabilities(self, ant: Ant) -> List[float]:
        cur = ant.trail[-1]
        denominator = 0
        for i in range(1, self.graph.dimension + 1):
            if not ant.visited[i]:
                denominator += self.pheromone[cur][i]**self.alpha * \
                    (1 / self.graph.distances[cur][i])**self.beta
        probabilities = [0] * (self.graph.dimension + 1)
        for i in range(1, self.graph.dimension + 1):
            if not ant.visited[i]:
                p = self.pheromone[cur][i]**self.alpha * \
                    (1 / self.graph.distances[cur][i])**self.beta
                probabilities[i] = p / denominator
        return probabilities

    def update_pheromone(self) -> None:
        for i in range(1, self.graph.dimension + 1):
            for j in range(i + 1, self.graph.dimension + 1):
                contributions = sum([ant.pheromone_change[i][j]
                                     for ant in self.ants])
                if self.pheromone[i][j] * (1 - self.rho) < 1e-32:
                    self.pheromone[i][j] = 1e-32
                else:
                    self.pheromone[i][j] *= (1 - self.rho)
                self.pheromone[i][j] += contributions
                self.pheromone[j][i] = self.pheromone[i][j]

    def update_solution(self):
        for ant in self.ants:
            ant_distance = ant.get_length(self.graph)
            if ant_distance < self.distance:
                self.distance = ant_distance
                self.route = ant.trail.copy()
