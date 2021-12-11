from graph import Graph
from src.classes import Solution


class GreedySolution(Solution):

    """
    Implementation of the Greedy algorithm for
    Travelling Salesman Problem
    """
    start: int

    def find_route(self, g: Graph) -> None:
        """
        Calculate the route from the given starting vertex
        always selecting the closest neighbor
        """

        origin = self.start
        while len(self.route) < g.dimension:
            possible_neighbours = {
                k: v for k, v in g.distances[origin].items()
                if k not in self.route}
            origin = min(possible_neighbours, key=possible_neighbours.get)
            self.route.append(origin)
            self.distance += possible_neighbours[origin]
        self.distance += g.distances[self.route[0]][self.route[-1]]
