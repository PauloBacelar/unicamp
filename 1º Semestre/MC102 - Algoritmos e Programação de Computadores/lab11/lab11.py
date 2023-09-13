class Link:
    def __init__(self, health: int, pos: list[int, int], damage: int) -> None:
        self._health = health
        self._damage = damage
        self._pos = pos
        self._old_pos = pos
        self._is_cursed = True

    @property
    def is_cursed(self) -> bool:
        return self._is_cursed

    @is_cursed.setter
    def is_cursed(self, value: int) -> None:
        self._is_cursed = value

    @property
    def pos(self) -> list[int, int]:
        return self._pos

    @pos.setter
    def pos(self, value: list[int, int]) -> None:
        self._pos = value

    @property
    def old_pos(self) -> list[int, int]:
        return self._old_pos

    @old_pos.setter
    def old_pos(self, value: list[int, int]) -> None:
        self._old_pos = value

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        if value < 0:
            self._health = 0
        else:
            self._health = value

    @property
    def damage(self) -> int:
        return self._damage

    @damage.setter
    def damage(self, value: int) -> None:
        self._damage = value

    def move(self, map: list[list[str]]) -> None:
        '''
        Move o personagem pelo mapa.

        Não há retorno, apenas atualiza os atributos pos e old_pos.

        Parâmetros:
        map -- mapa a ser atualizado
        '''
        # Recebedo posições adjacentes à do personagem
        up, right, down, left = get_adjacents(self.pos)

        # Se está amaldiçoado, ir para baixo enquanto ser valido
        if self.is_cursed and pos_is_valid(map, down):
            pos_to_move = down
            self.old_pos = self.pos
            self.pos = pos_to_move
            return
        else:  # Caso contrário, não está amaldiçoado
            self.is_cursed = False

        # Se está em linha par
        if self.pos[0] % 2 == 0:
            # Ir para a esquerda se for válido
            if pos_is_valid(map, left):
                pos_to_move = left
            # Caso contrário, ir para cima
            else:
                pos_to_move = up

        # Se está em linha ímpar
        else:
            # Ir para a direita se for válido
            if pos_is_valid(map, right):
                pos_to_move = right
            # Caso contrário, ir para cima
            else:
                pos_to_move = up

        # Atualizando atributos do personagem
        self.old_pos = self.pos
        self.pos = pos_to_move

    def collect(self, object: 'Object'):
        '''
        Coleta algum objeto.

        Não há retorno, apenas atualiza o atributo health ou damage.

        Parâmetros:
        object -- objeto a ser coletado
        '''
        if object.type == 'v':
            self.health += object.status
        else:
            self.damage += object.status

            # Dano mínimo do personagem é 1
            if self.damage < 1:
                self.damage = 1

    def attack(self, monster):
        '''
        Ataca um monstro.

        Retorna o dano e atualiza o atributo health do monstro.

        Parâmetros:
        monster -- monstro alvo
        '''
        if monster.health - self.damage < 0:
            damage = monster.health
            monster.health = 0
        else:
            damage = self.damage
            monster.health -= self.damage

        return damage


class Monster:
    def __init__(self,
                 id: int,
                 health: int,
                 damage: int,
                 type: str,
                 pos: list[int, int]) -> None:
        self._id = id
        self._health = health
        self._damage = damage
        self._type = type
        self._pos = pos
        self._old_pos = self.pos
        self._can_move = True

    @property
    def id(self) -> int:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def pos(self) -> list[int, int]:
        return self._pos

    @pos.setter
    def pos(self, value: list[int, int]) -> None:
        self._pos = value

    @property
    def old_pos(self) -> list[int, int]:
        return self._old_pos

    @old_pos.setter
    def old_pos(self, value: list[int, int]) -> None:
        self._old_pos = value

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        if value <= 0:
            self._health = 0
        else:
            self._health = value

    @property
    def damage(self) -> int:
        return self._damage

    @property
    def can_move(self) -> bool:
        return self._can_move

    @can_move.setter
    def can_move(self, value: bool) -> None:
        self._can_move = value

    def move(self, map: list[list[str]]) -> None:
        '''
        Move o monstro pelo mapa.

        Não há retorno, apenas atualiza os atributos pos e old_pos.

        Parâmetros:
        map -- mapa a ser atualizado
        '''
        # Recebendo as posições adjacentes
        up, right, down, left = get_adjacents(self.pos)

        # Posição de destino
        pos_to_move = self.pos

        if self.type == 'U' and pos_is_valid(map, up):
            pos_to_move = up
        elif self.type == 'R' and pos_is_valid(map, right):
            pos_to_move = right
        elif self.type == 'D' and pos_is_valid(map, down):
            pos_to_move = down
        elif self.type == 'L' and pos_is_valid(map, left):
            pos_to_move = left
        else:  # Nenhuma posição é válida. Monstro chegou na extremidade
            self.can_move = False

        # Atualizando atributos do monstro
        self.old_pos = self.pos
        self.pos = pos_to_move

    def attack(self, target: 'Link') -> int:
        '''
        Ataca o personagem.

        Retorna o dano e atualiza o atributo health do personagem.

        Parâmetros:
        target -- objeto do personagem
        '''
        if target.health - self.damage < 0:
            damage = target.health
            target.health = 0
        else:
            damage = self.damage
            target.health -= self.damage

        return damage

    def die(self, map: list[list[str]], monsters: list['Monster']):
        '''
        Remove o monstro da lista de monstros e tira o monstro do mapa.

        Retorna o mapa e a lista de monstros atualizados.

        Parâmetros:
        map -- mapa a ser atualizado
        monsters -- lista de monstros a ser atualizada
        '''
        monsters.remove(self)
        update_map(map, self.type, False, self.pos)

        return map, monsters


class Object:
    def __init__(self, name: str, type: str, pos: list[int, int], status: int):
        self._name = name
        self._type = type
        self._pos = pos
        self._status = status

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def pos(self) -> list[int, int]:
        return self._pos

    @property
    def status(self) -> int:
        return self._status

    def get_collected(self,
                      map: list[list[str]],
                      objects: list['Object']) -> (
                      list[list[str]] and list['Object']
                      ):
        '''
        É removido da lista de objetos e do mapa.

        Retorna o mapa e a lista de objetos atualizados.

        Parâmetros:
        map -- mapa a ser atualizado
        objects -- lista de objetos a ser atualizada
        '''
        map = update_map(map, self.type, False, self.pos)
        objects.remove(self)

        return map, objects


def get_map() -> list[list[str]]:
    '''
    Cria o mapa.

    Retorna o mapa criado
    '''
    map = []
    lines, columns = [int(n) for n in input().split(' ')]

    for i in range(lines):
        map.append([])

        for j in range(columns):
            map[i].append('.')

    return map


def get_monsters_info() -> list['Monster']:
    '''
    Recebe e cria os monstros a partir dos inputs do usuário.

    Retorna a lista de monstros.
    '''
    quant = int(input())
    monsters = []

    for i in range(quant):
        info = input().split(' ')

        health, damage = [int(n) for n in info[:2]]
        type = info[2]
        pos = [int(axis) for axis in info[3].split(',')]

        monster = Monster(i, health, damage, type, pos)
        monsters.append(monster)

    return monsters


def get_objects_info() -> list['Object']:
    '''
    Recebe e cria os objetos a partir dos inputs do usuário.

    Retorna a lista de objetos.
    '''
    quant = int(input())
    objects = []

    for _ in range(quant):
        info = input().split(' ')

        name, type = info[:2]
        pos = [int(axis) for axis in info[2].split(',')]
        status = int(info[3])

        object = Object(name, type, pos, status)
        objects.append(object)

    return objects


def get_adjacents(pos: list[int, int]) -> list[list[int]]:
    '''
    Calcula as posições adjacentes de determinada posição.

    Retorna a lista de posições na ordem cima -> direita -> baixo -> esquerda.

    Parâmetros:
    pos -- posição de referência
    '''
    return [
        [pos[0] - 1, pos[1]],
        [pos[0], pos[1] + 1],
        [pos[0] + 1, pos[1]],
        [pos[0], pos[1] - 1]
    ]


def pos_is_valid(map: list[list[str]], pos: list[int]) -> bool:
    '''
    Verifica se determinada posição é válida.

    Retorna True caso seja. False caso contrário.

    Parâmetros:
    map -- mapa da dungeon
    pos -- posição de referência
    '''
    # Linha e coluna são maiores ou iguals a zero
    # E menores do que as delimitações do mapa
    return (len(map) > pos[0] >= 0) and (len(map[0]) > pos[1] >= 0)


def print_map(map: list[list[str]], monsters: list['Monster']) -> None:
    '''
    Imprime o mapa.

    Não há retorno.

    Parâmetros:
    map -- mapa a ser impresso
    monsters -- lista de monstros
    '''
    for i, line in enumerate(map):
        for j, pos_text in enumerate(line):
            # Condições em ordem de prioridade da impressão
            if len(pos_text) == 1:
                print(f'{pos_text}', end='')

            elif 'P' in pos_text:
                print('P', end='')

            elif 'X' in pos_text:
                print('X', end='')

            elif '*' in pos_text:
                print('*', end='')

            # Não há personagem nem fim
            else:
                monsters_in_pos = []

                # Adicionando o monstro em monsters_in_pos
                for monster in monsters:
                    if all([monster.pos == [i, j],
                           monster.type in pos_text,
                           monster not in monsters_in_pos]):
                        monsters_in_pos.append(monster)

                # Se há monstro na pos, imprimir o de maior id (última entrada)
                if monsters_in_pos:
                    ids = [m.id for m in monsters_in_pos]
                    highest_id = max(ids)

                    # Pegando monstro de maior id
                    monster_to_print = next(m for m in monsters if m.id == highest_id)

                    print(monster_to_print.type, end='')

                # Caso contrário (apenas objetos), imprimir o último da posição
                else:
                    print(pos_text[-1], end='')

            # Imprimindo espaço entre posições
            if j < len(line) - 1:
                print('', end=' ')

        # Imprimindo quebra de linha entre linhas
        print('')

    # Imprimindo quebra de linha entre mapas
    print('')


def insert_on_map(map: list[list[str]],
                  char: str,
                  pos: list[int, int]) -> list[list[str]]:
    '''
    Insere um caractere no mapa.

    Retorna o mapa atualizado.

    Parâmetros:
    map -- mapa a ser atualizado
    char -- caractere a ser inserido
    pos -- posição de inserção
    '''

    # Se posição está vazia, passa a ser char
    if map[pos[0]][pos[1]] == '.':
        map[pos[0]][pos[1]] = char

    # Caso contrário, soma-se char à posição
    else:
        map[pos[0]][pos[1]] += char

    return map


def update_map(map: list[list[str]],
               char: str,
               pos: list[int, int],
               old_pos: list[int, int],
               can_move=True) -> list[list[str]]:
    '''
    Atualiza o mapa.

    Retorna o mapa atualizado.

    Parâmetros:
    map -- mapa a ser atualizado
    char -- caractere cuja posição será alterada
    pos -- posição de destino do caractere
    old_pos -- posição de origem do caractere
    can_move -- bool se um monstro atingiu uma parede ou não
    '''
    if can_move:
        # Posição de origem contém apenas o caractere. Ficará vazia
        if map[old_pos[0]][old_pos[1]] == char:
            map[old_pos[0]][old_pos[1]] = '.'

        # Caso contrário, remove o char mais à direita
        else:
            aux = map[old_pos[0]][old_pos[1]]
            map[old_pos[0]][old_pos[1]] = ''.join(aux.rsplit(char, 1))

        # Verificando se não se trata de um monstro abatido ou objeto coletado
        if pos:
            if map[pos[0]][pos[1]] == '.':
                map[pos[0]][pos[1]] = char
            else:
                map[pos[0]][pos[1]] += char

    return map


def main() -> None:
    # Recebendo vida e dano do Link
    health, damage = [int(n) for n in input().split(' ')]

    # Criando mapa
    map = get_map()

    # Recebendo posição do link e posição final
    pos = [int(axis) for axis in input().split(',')]
    end = [int(axis) for axis in input().split(',')]

    # Criando objeto do Link
    link = Link(health, pos, damage)

    # Inserindo ponto final e posição do link no mapa
    map = insert_on_map(map, '*', [end[0], end[1]])
    map = insert_on_map(map, 'P', [pos[0], pos[1]])

    # Criando lista de monstros e objetos
    monsters = get_monsters_info()
    objects = get_objects_info()

    # Inserindo objetos no mapa
    for obj in objects:
        map = insert_on_map(map, obj.type, obj.pos)

    # Inserindo monstros no mapa
    for monster in monsters:
        map = insert_on_map(map, monster.type, monster.pos)

    # Imprimindo mapa inicial
    print_map(map, monsters)

    # Variável de controle para o fim do jogo/combate
    finished = False

    # Loop do jogo
    while True:
        # Movendo link e atualizando mapa
        link.move(map)
        map = update_map(map, 'P', link.pos, link.old_pos)

        # Se link se moveu para uma posição com o ponto final, acabar o jogo
        if '*' in map[link.pos[0]][link.pos[1]]:
            print_map(map, monsters)
            print('Chegou ao fim!')
            finished = True
            break

        # Coletando objetos
        objects_to_exclude = []
        for object in objects:
            if object.pos == link.pos:
                link.collect(object)
                print(f'[{object.type}]Personagem adquiriu o objeto '
                      f'{object.name} com status de {object.status}')
                objects_to_exclude.append(object)

        # Removendo objetos do mapa e de objects
        for object in objects_to_exclude:
            map, objects = object.get_collected(map, objects)

        # Movimentando monstros e atualizando mapa
        for monster in monsters:
            monster.move(map)
            type, pos, old_pos = monster.type, monster.pos, monster.old_pos
            map = update_map(map, type, pos, old_pos, monster.can_move)

            # Se pos do Link é a mesma do monstro e o jogo não acabou, atacar
            if pos == link.pos and not finished:
                damage = link.attack(monster)
                print(f'O Personagem deu {damage} de dano ao '
                      f'monstro na posicao ({link.pos[0]}, {link.pos[1]})')

                # Se o monstro não morreu, atacar Link
                if monster.health > 0:
                    damage = monster.attack(link)
                    print(f'O Monstro deu {damage} de dano ao '
                          f'Personagem. Vida restante = {link.health}')

                    # Se Link morreu com o ataque, atualizar variável de fim
                    if link.health == 0:
                        finished = True

                # Se o monstro morreu com o ataque, retirar do mapa e da lista
                else:
                    map, monsters = monster.die(map, monsters)

        # Se Link morreu em combate, atualizar caractere no mapa
        if link.health == 0:
            for i in range(len(map)):
                for j in range(len(map[i])):
                    if 'P' in map[i][j]:
                        map[i][j] = map[i][j].replace('P', 'X')
                        break

            print_map(map, monsters)
            break
        else:
            print_map(map, monsters)


if __name__ == '__main__':
    main()
