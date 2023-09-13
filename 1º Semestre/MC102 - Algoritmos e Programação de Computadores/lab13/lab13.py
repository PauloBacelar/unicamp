def get_adjacents(coord, image):
    adjacents = []

    for i in range(-1, 2):
        if len(image) > coord[0] + i >= 0:
            for j in range(-1, 2):
                if ([i, j] != [0, 0] and
                        len(image[0]) > coord[1] + j >= 0):
                    adjacents.append((coord[0] + i, coord[1] + j))
        else:
            continue

    print(adjacents)
    return adjacents


def bucket(color, tolerance, coord, image):
    print(coord)
    adjacents = get_adjacents(coord, image)
    print('')


def negative(tolerance, coord, image):
    print(coord)
    adjacents = get_adjacents(coord, image)
    print('')


def cmask(tolerance, coord, image):
    print(coord)
    adjacents = get_adjacents(coord, image)
    print('')


def save():
    pass


def read_image():
    with open(f'lab13/images/{input()}', 'r') as file:
        lines = file.readlines()

    max_color = int(lines[3])
    image = []

    for i, line in enumerate(lines[4:]):
        image.append([])

        line = line.split()
        for number in line:
            image[i].append(int(number))

    return max_color, image


def main():
    max_color, image = read_image()

    op_quant = int(input())
    for i in range(op_quant):
        task_input = input().split(' ')

        task = task_input[0]
        params = task_input[1:]

        if task == 'bucket':
            color, tolerance = int(params[1]), int(params[2])
            coord = tuple([int(n) for n in params[:-3:-1]])
        elif task in ['negative', 'cmask']:
            tolerance = int(params[1])
            coord = tuple([int(n) for n in params[:-3:-1]])

        if task == 'bucket':
            bucket(color, tolerance, coord, image)
        elif task == 'negative':
            negative(tolerance, coord, image)
        elif task == 'cmask':
            cmask(tolerance, coord, image)
        else:
            save()
            pass


if __name__ == '__main__':
    main()
