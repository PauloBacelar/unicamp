class Character:
    def __init__(self,
                 max_health: int,
                 health: int,
                 arrows: dict[str: int],
                 enemies_quant: int):
        self._max_health = max_health
        self._health = health
        self._arrows = arrows
        self._enemies_quant = enemies_quant
        self._defeated_enemies = 0

    @property
    def max_health(self) -> int:
        return self._max_health

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        self._health = value

    @property
    def defeated_enemies(self) -> int:
        return self._defeated_enemies

    @defeated_enemies.setter
    def defeated_enemies(self, value: int) -> None:
        self._defeated_enemies = value

    @property
    def arrows(self) -> dict[str: int]:
        return self._arrows

    @arrows.setter
    def arrows(self, value: dict[str: int]) -> None:
        self._arrows = value

    @property
    def enemies_quant(self) -> int:
        return self._enemies_quant

    def take_damage(self, machines: list['Machine']) -> None:
        '''
        Diminui a vida do personagem.

        Parâmetros:
        machines -- array com as máquinas do combate
        '''
        for machine in machines:
            if not machine.is_dead:
                self.health -= machine.attack_points

        if self.health < 0:
            self.health = 0

    def has_arrows(self) -> bool:
        '''
        Verifica se personagem possui flechas.

        Retorna True se possui flechas. False caso contrário.
        '''
        return sum(self.arrows.values()) > 0

    def update_arrows(self, arrow: dict[str: int]) -> None:
        '''
        Atualiza o dicionário de flechas.

        Parâmetros:
        arrow -- tipo de flecha utilizada
        '''
        self.arrows[arrow] -= 1

    def heal(self) -> None:
        '''
        Cura o personagem.
        '''
        self.health = min([self.health + self.max_health//2, self.max_health])


class Machine:
    def __init__(self,
                 id: int,
                 health: int,
                 attack_points: int,
                 parts: list[object]):
        self._id = id
        self._health = health
        self._attack_points = attack_points
        self._parts = parts
        self._is_dead = False

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = value

    @property
    def is_dead(self):
        return self._is_dead

    @is_dead.setter
    def is_dead(self, value: int):
        self._is_dead = value

    @property
    def parts(self):
        return self._parts

    @property
    def attack_points(self):
        return self._attack_points

    @property
    def id(self):
        return self._id

    def calc_damage(self,
                    target_part: str,
                    arrow: str,
                    coordinates: tuple[int]):
        '''
        Calcula o dano a ser tomado pela máquina.

        Retorna um inteiro com o valor do dano calculado.

        Parâmetros:
        target_part -- nome da parte atingida
        arrow -- tipo de flecha utilizada
        coordinates -- coordenadas da flecha
        '''

        # Loop para atingir a parte que foi atingida
        for part in self.parts:
            if part.name == target_part:
                # Distância Manhattan
                dist_x = abs(part.coordinates[0] - coordinates[0])
                dist_y = abs(part.coordinates[1] - coordinates[1])
                distance = dist_x + dist_y

                # Se dano é negativo, assume o valor zero
                damage = max(0, part.max_damage - distance)

                # Se flecha não for fraqueza, dano é metade
                if part.weakness not in [arrow, 'todas']:
                    damage //= 2

                return damage

    def take_damage(self,
                    target_part: str,
                    arrow: str,
                    coordinates: tuple[int]):
        '''
        Diminui a vida da máquina.

        Parâmetros:
        target_part -- nome da parte atingida
        arrow -- tipo de flecha utilizada
        coordinates -- coordenadas da flecha
        '''
        self.health -= self.calc_damage(target_part, arrow, coordinates)
        if self.health < 0:
            self.health = 0

        self.is_dead = self.health <= 0


class Part:
    def __init__(self,
                 id: int,
                 name: str,
                 weakness: str,
                 max_damage: int,
                 coordinates: tuple[int]):
        self._id = id
        self._name = name
        self._weakness = weakness
        self._max_damage = max_damage
        self._coordinates = coordinates
        self._critical_hits = 0

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def max_damage(self):
        return self._max_damage

    @property
    def weakness(self):
        return self._weakness

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def critical_hits(self):
        return self._critical_hits

    @critical_hits.setter
    def critical_hits(self, value):
        self._critical_hits = value


def is_finished(aloy: Character):
    '''
    Verifica se o jogo terminou.

    Retorna True se terminou. False caso contrário.

    Parâmetros:
    aloy -- instância do personagem
    '''
    if aloy.health <= 0:
        return True
    elif aloy.defeated_enemies == aloy.enemies_quant:
        return True
    elif sum(aloy.arrows.values()) == 0:
        return True

    return False


def get_char_info() -> list[int, int, dict[str: int], int]:
    '''
    Recebe os inputs do usuário para preencher as informações do personagem.

    Retorna uma lista com vida, vida máxima, flechas e quantidade de inimigos.
    '''

    # Recebendo vida (e vida máxima) e flechas
    health = int(input())
    arrows_data = input().split(' ')

    # Organizando flechas
    arrows = {}
    for i in range(0, len(arrows_data), 2):
        arrows[arrows_data[i]] = int(arrows_data[i + 1])

    # Recebendo quantidade de inimigos
    total_enemies = int(input())

    return [health, health, arrows, total_enemies]


def get_machine_info() -> list[int]:
    '''
    Recebe os inputs do usuário para preencher as informações da máquina.

    Retorna uma lista de inteiros com vida, ataque e quantidade de partes.
    '''
    machine_info = [int(n) for n in input().split(' ')]
    return machine_info


def get_part_info() -> list[str, str, int, tuple[int]]:
    '''
    Recebe os inputs do usuário para preencher as informações da parte.

    Retorna uma lista com nome, fraqueza, dano máximo e coordenadas da parte.
    '''
    # Recebendo input
    part_info = input().split(', ')

    # Separando o input
    name, weakness, max_damage = part_info[:3]
    coordinates = tuple([int(part_info[3]), int(part_info[4])])

    return [name, weakness, int(max_damage), coordinates]


def all_dead(machines):
    '''
    Verifica se todas as máquinas foram derrotadas.

    Retorna True caso tenham sido mortas. False caso contrário.
    '''
    return all([machine.is_dead for machine in machines])


def get_combat_info() -> list[int, str, str, tuple[int]]:
    '''
    Recebe os inputs do usuário para preencher as informações do combate.

    Retorna uma lista com ID + nome do alvo, tipo + coordenadas da flecha.
    '''
    # Recebendo input
    combat_info = input().split(', ')

    # Separando input
    target_machine = int(combat_info[0])
    target_part, arrow_type = combat_info[1:3]
    coordinates = tuple([int(combat_info[3]), int(combat_info[4])])

    return [target_machine, target_part, arrow_type, coordinates]


def print_combat_report(used_arrows: dict[str: int],
                        total_arrows: dict[str: int],
                        machines: list[Machine]):
    '''
    Imprime o relatório de combate (flechas utilizados e críticos acertados).
    '''
    print('Flechas utilizadas:')
    for arrow in used_arrows:
        if used_arrows[arrow][0] > 0:
            used = used_arrows[arrow][0]
            total = total_arrows[arrow]

            print(f'- {arrow}: {used}/{total}')

    # Controle da impressão de 'criticos acertos:'
    first_of_all = True
    for machine in machines:
        # Controle da impressão de 'máquina X'
        first = True

        for part in machine.parts:
            if part.critical_hits > 0:
                if first_of_all:
                    print('Críticos acertados:')
                    first_of_all = False

                if first:
                    print(f'Máquina {machine.id}:')
                    first = False

                print(f'- {part.coordinates}: {part.critical_hits}x')


def main():
    aloy = Character(*get_char_info())
    arrow_stock = aloy.arrows
    combat_id = 0

    # Loop do combate
    while True:
        enemies_quant_combat = int(input())

        # Informações das máquinas
        machines = []
        defeated_machines = []

        # Informações das flechas e críticos
        used_arrows = {k: [0, aloy.arrows[k]] for k in aloy.arrows}
        aloy.arrows = arrow_stock.copy()

        # Variável de controle do fim do loop
        finished = False

        for i in range(enemies_quant_combat):
            # Recebendo inputs da máquinas
            health, attack, parts_quant = get_machine_info()
            parts = []

            # Recebendo inputs da parte
            for j in range(parts_quant):
                parts.append(Part(j, *get_part_info()))

            # Crinado máquina e inserindo na lista machines
            machines.append(Machine(i, health, attack, parts))

        # Controle de quando Aloy irá receber dano
        hits_count = 0

        # Iniciando novo combate
        print(f'Combate {combat_id}, vida = {aloy.health}')
        while True:

            # Recebendo informaçẽos do combate
            target_machine, target_part, arrow, coord = get_combat_info()

            # Atualizando dados da máquina e de Aloy
            machines[target_machine].take_damage(target_part, arrow, coord)
            aloy.update_arrows(arrow)
            used_arrows[arrow][0] += 1

            # Atualizando máquinas derrotadas
            for machine in machines:
                if machine.health <= 0 and machine.id not in defeated_machines:
                    print(f'Máquina {machine.id} derrotada')
                    aloy.defeated_enemies += 1
                    defeated_machines.append(machine.id)

            # Verificando houve acerto crítico
            for part in machines[target_machine].parts:
                if (part.name == target_part and part.coordinates == coord):
                    part.critical_hits = part.critical_hits + 1

            # Aloy leva dano a cada três ataques realizados
            hits_count += 1
            if hits_count % 3 == 0:
                aloy.take_damage(machines)

            # Condições de fim do combate
            # Aloy morreu
            if aloy.health == 0:
                print(f'Vida após o combate = {aloy.health}')
                print('Aloy foi derrotada em combate e não retornará a tribo.')
                finished = True
                break

            # Todas as máquinas do combate foram derrotadas
            elif all_dead(machines):
                print(f'Vida após o combate = {aloy.health}')
                print_combat_report(used_arrows, arrow_stock, machines)

                # Todas as máquinas do jogo foram derrotadas
                if aloy.defeated_enemies == aloy.enemies_quant:
                    print('Aloy provou seu valor e voltou para sua tribo.')
                    finished = True
                break

            # Arroy ficou sem flechas
            elif not aloy.has_arrows():
                print(f'Vida após o combate = {aloy.health}')
                print('Aloy ficou sem flechas e recomeçará sua missão mais preparada.')
                finished = True
                break

        # Curando Aloy
        aloy.heal()

        # Alguma condição de fim do combate foi atendida. Encerrar o loop
        if finished:
            break

        # Atualizando número do combate
        combat_id += 1


if __name__ == '__main__':
    main()
