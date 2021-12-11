from random import randint


def gen_file(file_name: str, dimension: int) -> None:
    """Generate given number of coordinates and write them into a file"""

    with open(file_name, 'w') as f:
        f.write(f'{dimension}\n')
        for i in range(dimension):
            x = randint(0, 10000)
            y = randint(0, 10000)
            f.write(f'{i + 1} {x} {y}\n')


def main() -> None:
    file_name = './instances/file2.txt'
    dimension = 20
    gen_file(file_name, dimension)


if __name__ == '__main__':
    main()
