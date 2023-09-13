def get_map() -> list[list[str]]:
    '''
    Cria o mapa inicial a partir do input do usuário.

    Retorna uma matriz que representa o mapa.
    '''
    lines = int(input())
    map = []

    for _ in range(lines):
        map.append(input().split(' '))

    return map


def get_adjacents(pos: list[int]) -> list[str]:
    '''
    Verifica as posições adjacentes a partir de uma posição dada.

    Retorna uma lista dessas posições.

    Parâmetros:
    pos -- posição de referência
    '''

    # Definindo posições adjacentes
    left = [pos[0], pos[1] - 1]
    up = [pos[0] - 1, pos[1]]
    right = [pos[0], pos[1] + 1]
    down = [pos[0] + 1, pos[1]]

    # Posição de referência está na coluna 0. Não há adjacência à esquerda
    if left[1] < 0:
        left = False

    # Posição de referência está na linha 0. Não há adjacência acima
    if up[0] < 0:
        up = False

    # Posição de referência está na coluna final. Não há adjacência à direita
    if right[1] >= len(map[0]):
        right = False

    # Posição de referência está na linha final. Não há adjacência abaixo
    if down[0] >= len(map):
        down = False

    return [left, up, right, down]


def is_dirty(pos: list[str]) -> bool:
    '''
    Checa se determinada posição está suja ou não.

    Retorna True se estiver. False caso contrário.

    Parâmetros:
    pos -- posição a ser analisada
    '''
    if pos:
        return map[pos[0]][pos[1]] == 'o'

    return False


def move(pos_to_move: list[int]) -> list[dict, list[list[str]]]:
    '''
    Move o robô.

    Retorna o mapa e o dicionário do robô atualizados.

    Parâmetros:
    pos_to_move -- posição destino do robô
    '''

    # Atualizando informações do robô
    old_pos = robot['pos']
    robot['pos'] = pos_to_move
    robot['old_pos'] = old_pos

    # Atualizando mapa
    map[pos_to_move[0]][pos_to_move[1]] = 'r'
    map[old_pos[0]][old_pos[1]] = '.'

    print_map()
    return robot, map


def print_map() -> None:
    '''
    Imprime o mapa.

    Não há retorno
    '''
    print('')
    for line in map:
        print(' '.join(line))


def check_dirt(positions: list[list[str]]) -> list[str] or bool:
    '''
    A partir de uma lista de posições, retorna a primeira que está suja.

    Se não há posições sujas, retorna False.

    Parâmetros:
    positions -- lista de posições
    '''
    for position in positions:
        if position and is_dirty(position):
            return position

    return False


def is_pos_next(pos: list[str]) -> bool:
    '''
    Verifica se determinada posição é a próxima no caminho de scan do robô.

    Retorna True se for. False caso contrário.

    Parâmetros:
    pos -- posição a ser analisada
    '''

    # Robô está em linha ímpar
    if robot['pos'][0] % 2 != 0:

        # Robô está na coluna 0
        if robot['pos'][1] == 0:
            # pos está uma linha abaixo do robô?
            return [robot['pos'][0] + 1, robot['pos'][1]] == pos

        # Robô não está na coluna 0
        else:
            # pos está uma coluna atrás do robô?
            return [robot['pos'][0], robot['pos'][1] - 1] == pos

    # Robô está em linha par
    else:

        # Robô está na coluna final
        if robot['pos'][1] == len(map[0]) - 1:
            # pos está uma linha abaixo do robô?
            return [robot['pos'][0] + 1, robot['pos'][1]] == pos

        # Robô não está na coluna final
        else:
            # pos está uma coluna após o robô?
            return [robot['pos'][0], robot['pos'][1] + 1] == pos


def scan(robot: dict, map: list[list[str]]) -> list[dict, list[list[str]]]:
    '''
    Guia o comportamento do robô durante o modo scan.

    Retorna o dicionário do robô o e mapa atualizados.
    '''

    # Recebendo posições adjacentes ao robô a posição da sujeira
    left, up, right, down = get_adjacents(robot['pos'])
    dirt_pos = check_dirt([left, up, right, down])

    # Posição final do robô no modo finalizar
    final_pos = [len(map) - 1, len(map[0]) - 1]

    # Verificando se robô finalizou
    if robot['mode'] == 'scanning' and robot['pos'] == final_pos:
        robot['finishing'] = True

        # Robô está na posição final e há um número ímpar de linhas
        if len(map) % 2 == 1:
            robot['mode'] = 'finished'

        # Robô está na posição final e há um número par de linhas
        else:
            # Movendo robô da ponta direita para a ponta esquerda
            while robot['pos'][1] != 0:
                left, up, right, down = get_adjacents(robot['pos'])
                robot, map = move(left)

            # Movendo robô da ponta esquerda para a ponta direita (final)
            while robot['pos'][1] != len(map[0]):
                left, up, right, down = get_adjacents(robot['pos'])
                robot, map = move(right)

            robot['mode'] = 'finished'

    # Robô ainda não entrou no processo de finalização
    if not robot['finishing']:
        # Verificando se o robô acabou de descer uma linha
        just_moved_down = robot['pos'][0] == robot['old_pos'][0] + 1

        # Há sujeira adjacente
        if dirt_pos:
            # Movendo para a direita caso a poeira esteja lá
            if robot['pos'][0] % 2 == 0 and dirt_pos == right:
                move(right)

            # Movendo para a esquerda caso a poeira esteja lá
            elif robot['pos'][0] % 2 != 0 and dirt_pos == left:
                move(left)

            # Poeira está acima ou abaixo do robô
            else:
                # Verificando se posição da poeira é a próxima do robô
                if not is_pos_next(dirt_pos):
                    robot['last_scan_pos'].append(robot['pos'])
                robot['mode'] = 'cleaning'

        # Não há sujeira adjacente
        else:
            # Robô está em linha par
            if robot['pos'][0] % 2 == 0:
                # Movendo para baixo caso esteja na ponta direita
                if robot['pos'][1] == len(map[0]) - 1 and not just_moved_down:
                    robot, map = move(down)

                # Movendo para direita caso não esteja na ponta direita
                else:
                    robot, map = move(right)

            # Robô está em linha ímpar
            else:
                # Movendo para baixo caso esteja na ponta esquerda
                if robot['pos'][1] == 0 and not just_moved_down:
                    robot, map = move(down)

                # Movendo para esquerda caso não esteja na ponta esquerda
                else:
                    robot, map = move(left)

    return robot, map


def clear(robot: dict, map: list[list[str]]) -> list[dict, list[list[str]]]:
    '''
    Guia o comportamento do robô durante o modo limpeza.

    Retorna o dicionário do robô o e mapa atualizados.
    '''

    # Recebendo posições adjacentes ao robô a posição da sujeira
    left, up, right, down = get_adjacents(robot['pos'])
    dirt_pos = check_dirt([left, up, right, down])

    # Se há sujeira, mover para a posição dela
    if dirt_pos:
        robot, map = move(dirt_pos)

    # Se não há sujeira, mas limpeza tirou robô do caminho, ir p/ modo retorno
    elif robot['last_scan_pos']:
        robot['mode'] = 'returning'

    # Se não há sujeira e o robô continua no caminho, ir para modo scan
    else:
        robot['mode'] = 'scanning'

    return robot, map


def return_scan(robot: dict,
                map: list[list[str]]) -> list[dict, list[list[str]]]:
    '''
    Guia o comportamento do robô durante o modo limpeza.

    Retorna o dicionário do robô o e mapa atualizados.
    '''
    found_dirt = False  # Encontrou sujeira adjacente ou não
    last_scan_pos = robot['last_scan_pos'][-1]

    # Enquanto não encontrar sujeira adjacente, caminhar até coluna de origem
    while robot['pos'][1] != last_scan_pos[1] and not found_dirt:
        left, up, right, down = get_adjacents(robot['pos'])
        dirt_pos = check_dirt([left, up, right, down])

        # Se há sujeira adjacente durante o retorno, ir para modo limpeza
        if dirt_pos:
            found_dirt = True
            robot['mode'] = 'cleaning'
            break

        # Se não há sujeira adjacente, mover para esquerda/direita
        if robot['pos'][1] > last_scan_pos[1]:
            robot, map = move(left)
        else:
            robot, map = move(right)

    # Enquanto não encontrar sujeira adjacente, caminhar até linha de origem
    while robot['pos'][0] != last_scan_pos[0] and not found_dirt:
        left, up, right, down = get_adjacents(robot['pos'])
        dirt_pos = check_dirt([left, up, right, down])

        # Se há sujeira adjacente durante o retorno, ir para modo limpeza
        if dirt_pos:
            found_dirt = True
            robot['mode'] = 'cleaning'
            break

        # Se não há sujeira adjacente, mover para cima/baixo
        if robot['pos'][0] > last_scan_pos[0]:
            robot, map = move(up)
        else:
            robot, map = move(down)

    # Removendo posição do último scan
    if robot['pos'] == last_scan_pos:
        robot['last_scan_pos'].pop()

        # Caso não existam posições do último scan, retornar ao modo scan
        if len(robot['last_scan_pos']) == 0:
            robot['mode'] = 'scanning'

    return robot, map


def main() -> None:
    global robot, map
    for line in map:
        print(' '.join(line))

    while robot['mode'] != 'finished':
        while robot['mode'] == 'scanning':
            robot, map = scan(robot, map)

        while robot['mode'] == 'cleaning':
            robot, map = clear(robot, map)

        while robot['mode'] == 'returning':
            robot, map = return_scan(robot, map)


# Variáveis globais
map = get_map()
robot = {
    'pos': [0, 0],
    'old_pos': [0, 0],
    'last_scan_pos': [],
    'mode': 'scanning',
    'finishing': False
}


if __name__ == '__main__':
    main()
