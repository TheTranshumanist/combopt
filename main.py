from enum import Enum, auto
from graph import Graph, GraphGenerator
from greedy import GreedySolution
from aco import AntSystemSolution
from src.classes import Solution
from src.decorators import timer
from random import randint


class SolutionType(Enum):
    GREEDY = auto()
    ACO = auto()


class FinderType(Enum):
    OPTIMAL = auto()
    RANDOM = auto()
    DEFAULT = auto()


def calc_solution(solution_type: SolutionType,
                  g: Graph,
                  start: int) -> Solution:
    """Calculate the route using the chosen algorithm"""

    if solution_type == SolutionType.GREEDY:
        s = GreedySolution()
        s.start = start
    elif solution_type == SolutionType.ACO:
        s = AntSystemSolution()
    s.find_route(g)
    return s


@timer
def find_solution(file_name: str,
                  solution_type: SolutionType,
                  finder_type: FinderType,
                  start: int = 1) -> Solution:
    """Find the solution to the TSP"""

    gen = GraphGenerator(file_name)
    g = gen.generate_graph()
    if finder_type == FinderType.OPTIMAL:
        solutions = [calc_solution(solution_type, g, i + 1)
                     for i in range(g.dimension)]
        return min(solutions, key=lambda s: s.distance)
    elif finder_type == FinderType.RANDOM:
        start = randint(1, g.dimension)
        return calc_solution(solution_type, g, start)
    elif finder_type == FinderType.DEFAULT:
        return calc_solution(solution_type, g, start)


def save_result(file_name: str, s: Solution) -> None:
    with open(file_name, 'w') as f:
        f.write(f'Distance: {s.distance:.2f}\nRoute:\n')
        for vertex in s.route:
            f.write(f'{vertex}\n')


def main() -> None:
    src_name = './instances/berlin52.txt'
    dest_name = './results/aco_berlin.txt'
    solution_type = SolutionType.ACO
    finder_type = FinderType.DEFAULT
    start = 1
    s = find_solution(src_name, solution_type, finder_type, start)
    save_result(dest_name, s)


if __name__ == '__main__':
    main()
