from abc import ABC, abstractmethod
from graph import Graph
from typing import List


class Solution(ABC):

    """
    Abstract class serving as a template for solutions
    to Travelling Salesman Problem
    """

    route: List[int]
    distance: int

    def __init__(self) -> None:
        self.route = []
        self.distance = 0

    def __str__(self) -> str:
        return '\n'.join(list(map(str, self.route)))

    @abstractmethod
    def find_route(self, g: Graph) -> None:
        pass
