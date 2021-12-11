from dataclasses import dataclass
from math import sqrt
from typing import Dict, List


@dataclass
class Vertex:

    """Implementation of a graph node"""

    id: int
    x: int
    y: int

    def distance(self, other: 'Vertex') -> float:
        """Calculate Euclidean distance between two vertices"""

        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def __str__(self) -> str:
        """Turn vertex into a printable string. Format: id -> (x, y)"""

        return f'{self.id} -> ({self.x}, {self.y})'


class Graph:

    """Graph representation to be used in Travelling Salesman Problem"""

    dimension: int
    vertex_list: List[Vertex]
    distances: Dict[int, Dict[int, float]]

    def __init__(self, dimension: int, vertex_list: List[Vertex]) -> None:
        self.dimension = dimension
        self.vertex_list = vertex_list
        self.distances = {}
        self.generate_distances()

    def __str__(self) -> str:
        """Turn graph's vertex list into a printable string"""

        return '\n'.join(list(map(str, self.vertex_list)))

    def generate_distances(self) -> None:
        """Create a nested dictionary of distances between every vertex"""

        for i in range(self.dimension):
            origin_id = self.vertex_list[i].id
            if origin_id not in self.distances:
                self.distances[origin_id] = {}
            for j in range(i + 1, self.dimension):
                distance = self.vertex_list[i].distance(self.vertex_list[j])
                target_id = self.vertex_list[j].id
                if target_id not in self.distances:
                    self.distances[target_id] = {}
                self.distances[origin_id][target_id] = distance
                self.distances[target_id][origin_id] = distance


class GraphGenerator:

    """
    Class to generate graph given in the TSP
    instance from an external file
    """

    file_name: str

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    @staticmethod
    def reformat_line(line: str) -> Vertex:
        """Turn string from file's line into a Vertex object"""

        vertex_util = list(map(int, line.split()))
        return Vertex(vertex_util[0], vertex_util[1], vertex_util[2])

    def generate_graph(self) -> Graph:
        """Generate graph from a given vertex list"""

        list_util = self.generate_vertex_list()
        return Graph(len(list_util), list_util)

    def generate_vertex_list(self) -> List[Vertex]:
        """Read the file and generate list of vertices from it"""

        lines = None
        with open(self.file_name, 'r') as f:
            lines = f.readlines()
        if lines:
            return list(map(self.reformat_line, lines[1:]))
