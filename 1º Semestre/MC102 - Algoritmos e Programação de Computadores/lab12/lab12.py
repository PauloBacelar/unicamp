class Player:
    def __init__(self, id: int, hand: list['Card']) -> None:
        self._id = id
        self._hand = hand
        self._bluffed = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def hand(self) -> list['Card']:
        return self._hand

    @property
    def bluffed(self) -> bool:
        return self._bluffed

    @hand.setter
    def hand(self, value: list['Card']) -> None:
        self._hand = value

    @bluffed.setter
    def bluffed(self, value: bool) -> None:
        self._bluffed = value

    def __str__(self) -> str:
        if self.hand:
            return f'Mão: {" ".join([c.number + c.suit for c in self.hand])}'
        else:
            return 'Mão:'

    def sort_cards(self, cards=[]) -> list['Card']:
        '''
        Ordena uma lista de cartas.

        Retorna a lista ordenada decrescentemente.

        Parâmetros:
        cards -- lista opcional de cartas a ordenar.
        Caso não seja preenchida, utiliza-se a mão do jogador
        '''

        # Se cards não é especificado, atualizar mão do jogador
        if not cards:
            cards = self.hand

        for i in range(len(cards)):
            for j in range(len(cards) - 1, 0, -1):
                current = cards[j]
                previous = cards[j-1]

                # Trocando cartas adjacentes com números diferentes
                if current.number_strength > previous.number_strength:
                    cards[j], cards[j-1] = previous, current

                # Trocando cartas adjacentes com números iguais
                elif current.number_strength == previous.number_strength:
                    if current.suit_strength > previous.suit_strength:
                        cards[j], cards[j-1] = previous, current

        return cards[::-1]

    def play_cards(self,
                   stack: list['Card'],
                   top_num: int) -> list[list['Card'], int]:
        self.sort_cards()
        '''
        Joga as cartas da mão do jogador no baralho.

        Retorna a lista de cartas jogadas e o número mínimo para fazer jogada.

        Parâmetros:
        stack -- pilha atual.
        top_num -- valor mínimo para realizar jogada
        '''

        # Salvando top_num anterior à rodada em caso de blefe
        old_top_num = top_num

        # Se há carta na pilha, filtrar cartas do jogador
        if len(stack) > 0:
            cards_to_play = []

            # Buscando carta a ser jogada
            while top_num <= 13:
                left = 0
                right = len(self.hand) - 1

                while left <= right:
                    mid = (left + right) // 2

                    # Encontrou carta jogável com menor valor possível
                    if self.hand[mid].number_strength == top_num:
                        cards_to_play.append(self.hand[mid])
                        i = 1

                        # Verificando valores das cartas nas adjacências
                        while True:
                            found = False

                            # Verificando cartas à direita da carta encontrada
                            if (mid + i < len(self.hand) and
                                self.hand[mid + i].number_strength == top_num):
                                cards_to_play.append(self.hand[mid + i])
                                found = True

                            # Verificando cartas à esquerda da carta encontrada
                            if (mid - i >= 0 and
                                self.hand[mid - i].number_strength == top_num):
                                cards_to_play.append(self.hand[mid - i])
                                found = True

                            # Atualizando índice usado na procura das cartas
                            i += 1

                            # Não encontrou mais cartas nas adjacências
                            if not found:
                                break

                        # Finalizou a busca das cartas jogáveis de menor valor
                        break

                    # Se a carta do meio é maior, procurar à direita
                    elif self.hand[mid].number_strength > top_num:
                        left = mid + 1

                    # Se a carta do meio é menor, procurar à esquerda
                    else:
                        right = mid - 1

                # Encontrou as cartas jogáveis
                if cards_to_play != []:
                    cards_to_play = self.sort_cards(cards_to_play)
                    self.bluffed = False
                    break

                # Não encontrou as cartas com top_num. Atualizando seu valor
                else:
                    top_num += 1

            # top_num atingiu valor máximo e não encontrou cartas. Irá blefar
            if not cards_to_play:
                top_num = old_top_num
                self.bluffed = True

        # Se blefou ou pilha está vazia, jogar cartas de menor valor da mão
        if self.bluffed or len(stack) == 0:

            # Se jogador blefou, não atualizar top_num
            if len(stack) == 0:
                top_num = self.hand[-1].number_strength

            # Valor do número/letra das cartas a serem jogadas
            num_to_play = self.hand[-1].number_strength

            # Colocando cartas em cards_to_play
            cards_to_play = []
            for i in range(-1, -len(self.hand) - 1, -1):
                if self.hand[i].number_strength == num_to_play:
                    cards_to_play.append(self.hand[i])
                else:
                    break

        # Imprimindo jogada e retornando valores
        self.print_play(cards_to_play, top_num)
        return [cards_to_play, top_num]

    def print_play(self, played_cards: list['Card'], top_num: int) -> None:
        '''
        Imprime uma jogada.

        Não há retorno.

        Parâmetros:
        played_cards -- lista de cartas jogadas.
        top_num -- valor numérico das cartas jogadas
        '''
        id = self.id
        quantity = len(played_cards)

        num_to_suit = {
            1: 'A',
            11: 'J',
            12: 'Q',
            13: 'K'
        }
        if top_num in num_to_suit.keys():
            number = num_to_suit[top_num]
        else:
            number = top_num

        print(f'[Jogador {id}] {quantity} carta(s) {number}')


class Card:
    def __init__(self, number: int, suit):
        self._number = number
        self._suit = suit
        self._suit_strength = self.get_suit_strength()
        self._number_strength = self.get_number_strength()

    @property
    def number(self) -> str:
        return self._number

    @property
    def suit(self) -> str:
        return self._suit

    @property
    def number_strength(self) -> int:
        return self._number_strength

    @property
    def suit_strength(self) -> int:
        return self._suit_strength

    def __str__(self):
        return f'{self.number}{self.suit}'

    def get_suit_strength(self) -> int:
        '''
        Calcula a força de um naipe.

        Retorna o valor numérico da força.
        '''
        suits_strength = {
            'O': 0,
            'E': 1,
            'C': 2,
            'P': 3
        }
        return suits_strength[self.suit]

    def get_number_strength(self) -> int:
        '''
        Calcula a força de um número/letra.

        Retorna o valor numérico da força.
        '''
        try:
            return int(self.number)
        except ValueError:
            numbers_strength = {
                'A': 1,
                'J': 11,
                'Q': 12,
                'K': 13
            }
            return numbers_strength[self.number]


def print_players(players: list['Player']) -> None:
    '''
    Imprime a lista de jogadores e suas mãos.

    Não há retorno.

    Parâmetros:
    players -- lista de jogadores
    '''
    for player in players:
        print(f'Jogador {player.id}')
        player.sort_cards()
        print(player)


def print_stack(stack: list['Card']) -> None:
    '''
    Imprime a pilha da rodada.

    Não a retorno.

    Parâmetros:
    stack -- pilha a ser impressa
    '''
    print('Pilha:', end='')

    if len(stack) > 0:
        print('', ' '.join([c.number + c.suit for c in stack]))
    else:
        print('')


def main() -> None:
    # Inicializando variáveis do jogo
    players_quant = int(input())
    players = []
    stack = []

    # Criando jogores e mãos
    for i in range(players_quant):
        hand = []
        cards = input().split(', ')

        for card in cards:
            hand.append(Card(card[:-1], card[-1]))
        players.append(Player(i + 1, hand))

    # Criando variáveis da rodada
    challenge_frequency = int(input())
    round = 0
    previous_player = None
    top_num = 1

    # Imprimindo jogadores e pilha antes de iniciar o jogo
    print_players(players)
    print_stack(stack)

    # Inicializando o jogo
    while True:
        # Atualizando ID da rodada
        round += 1

        # Esvaziando lista de cartas jogadas pelo jogador
        played_cards = []

        # Pegando jogador responsável pela jogada
        active_player = players[(round - 1) % len(players)]

        # Jogador duvidou
        if (round - 1) % challenge_frequency == 0 and round != 1:
            print(f'Jogador {active_player.id} duvidou.')

            # Jogador anterior blefou
            if previous_player.bluffed:
                for card in stack:
                    previous_player.hand.append(card)

            # Jogador anterior NÃO blefou
            else:
                for card in stack:
                    active_player.hand.append(card)

            # Imprimindo mão dos jogadores e pilha vazia
            stack = []
            print_players(players)
            print_stack(stack)

            # Verificando se algum jogador venceu após o desafio
            winner = None
            for player in players:
                if player.hand == []:
                    winner = player.id
                    break
            if winner:
                print(f'Jogador {winner} é o vencedor!')
                break

        # Colocando carta na pilha
        [played_cards, top_num] = active_player.play_cards(stack, top_num)
        for card in played_cards:
            stack.append(card)
            active_player.hand.remove(card)

        # Imprimindo pilha da jogada
        print_stack(stack)

        # Jogador ativo não tem cartas e não haverá desafio na próxima rodada
        if active_player.hand == [] and round % challenge_frequency != 0:
            print(f'Jogador {active_player.id} é o vencedor!')
            break

        # Último jogador não tem cartas e inexistiu ou ganhou desafio
        elif previous_player and previous_player.hand == []:
            print(f'Jogador {previous_player.id} é o vencedor!')
            break

        # Não houve vencedor. Salvando atual jogador para a próxima jogada
        else:
            previous_player = active_player


if __name__ == '__main__':
    main()
