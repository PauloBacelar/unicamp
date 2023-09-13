def preencher_vetor(
        vetores: list[list[int]],
        operacao: str) -> list[list[int]]:
    '''
    Iguala dois vetores em tamanho, preenchendo o menor com valores neutros.

    Retorna uma lista com os dois vetores tendo o mesmo tamanho.

    Parâmetros:\n
    vetores -- array com os dois vetores a serem comparados/preenchidos\n
    operacao -- string que indica a operação a ser realizada entre os vetores
    '''

    # Definindo maior e menor vetor
    if len(vetores[1]) > len(vetores[0]):  # vetor2 é maior
        maior = vetores[1]
        menor = vetores[0]
    elif len(vetores[0]) > len(vetores[1]):  # vetor1 é maior
        maior = vetores[0]
        menor = vetores[1]
    else:  # Vetores com o mesmo tamanho
        return vetores

    # Igualando os vetores em tamanho
    for _ in range(len(menor), len(maior)):
        if operacao in ['adição', 'subtração']:
            menor.append(0)

        elif operacao == 'multiplicação':
            menor.append(1)

        elif operacao == 'divisão':
            if menor == vetores[0]:  # Menor é denominador, elemento neutro é 0
                menor.append(0)
            else:  # Menor é numerador, elemento neutro é 1
                menor.append(1)

    # Garantindo que ordem de retorno seja [vetor1, vetor2]
    if menor == vetores[0]:
        return [menor, maior]
    else:
        return [maior, menor]


def soma_vetores(vetor1: list[int], vetor2: list[int]) -> list[int]:
    '''
    Soma dois vetores, elemento por elemento.

    Retorna o vetor resultado da soma.

    Parâmetros:\n
    vetor1 -- primeiro vetor da operação\n
    vetor2 -- segundo vetor da operação
    '''

    # Preenchendo vetor menor e criando vetor resultado
    vetor1, vetor2 = preencher_vetor([vetor1, vetor2], 'adição')
    vetor_res = []

    # Somando elementos do vetor1 e vetor2 de mesmo índice
    for i in range(len(vetor1)):
        vetor_res.append(vetor1[i] + vetor2[i])

    return vetor_res


def subtrai_vetores(vetor1: list[int], vetor2: list[int]) -> list[int]:
    '''
    Subtrai dois vetores, elemento por elemento.

    Retorna o vetor resultado da subtração.

    Parâmetros:\n
    vetor1 -- vetor a ser subtraído\n
    vetor2 -- vetor a subtrair
    '''

    # Preenchendo vetor menor e criando vetor resultado
    vetor1, vetor2 = preencher_vetor([vetor1, vetor2], 'subtração')
    vetor_res = []

    # Subtraindo elementos do vetor1 por elementos do vetor2 de mesmo índice
    for i in range(len(vetor1)):
        vetor_res.append(vetor1[i] - vetor2[i])

    return vetor_res


def multiplica_vetores(vetor1: list[int], vetor2: list[int]) -> list[int]:
    '''
    Multiplica dois vetores, elemento por elemento.

    Retorna o vetor resultado da multiplicação.

    Parâmetros:\n
    vetor1 -- primeiro vetor da operação\n
    vetor2 -- segundo vetor da operação
    '''

    # Preenchendo vetor menor e criando vetor resultado
    vetor1, vetor2 = preencher_vetor([vetor1, vetor2], 'multiplicação')
    vetor_res = []

    # Multiplicando elementos do vetor1 e vetor2 de mesmo índice
    for i in range(len(vetor1)):
        vetor_res.append(vetor1[i] * vetor2[i])

    return vetor_res


def divide_vetores(vetor1: list[int], vetor2: list[int]) -> list[int]:
    '''
    Divide dois vetores, elemento por elemento.

    Retorna o vetor resultado da divisão.

    Parâmetros:\n
    vetor1 -- vetor a ser dividido\n
    vetor2 -- vetor a dividir
    '''

    # Preenchendo vetor menor e criando vetor resultado
    vetor1, vetor2 = preencher_vetor([vetor1, vetor2], 'divisão')
    vetor_res = []

    # Dividindo elementos do vetor1 por elementos do vetor2 de mesmo índice
    for i in range(len(vetor1)):
        vetor_res.append(vetor1[i] // vetor2[i])

    return vetor_res


def multiplicacao_escalar(vetor1: list[int], escalar: int) -> list[int]:
    '''
    Multiplica todos os elementos do vetor por um número escalar.

    Retorna o vetor resultado da multiplicação.

    Parâmetros:\n
    vetor1 -- vetor a ser multiplicado\n
    escalar -- valor a multiplicar o vetor
    '''

    # Multiplicando escalar por cada número em vetor1
    return [escalar * num for num in vetor1]


def n_duplicacao(vetor1: list[int], n: int) -> list[int]:
    '''
    Repete os elementos de um vetor n vezes.

    Retorna o novo vetor com elementos repetidos.

    Parâmetros:\n
    vetor1 -- vetor a ser repetido\n
    n -- quantidade de repetições
    '''
    novo_vetor = []

    # Adicionando números do vetor1 n vezes em novo_vetor
    for _ in range(n):
        for num in vetor1:
            novo_vetor.append(num)

    return novo_vetor


def soma_elementos(vetor: list[int]) -> int:
    '''
    Soma todos os elementos de um vetor.

    Retorna o valor da soma.

    Parâmetros:\n
    vetor -- vetor em que será calculada a soma
    '''
    soma = 0

    # Adicionando cada elemento de vetor à variável soma
    for num in vetor:
        soma += num

    return soma


def produto_interno(vetor1: list[int], vetor2: list[int]) -> int:
    '''
    Multiplica dois vetores de mesmo tamanho e soma os elementos do resultante.

    Retorna o valor da soma.

    Parâmetros:\n
    vetor1 -- primeiro vetor da operação\n
    vetor2 -- segundo vetor da operação
    '''
    return soma_elementos(multiplica_vetores(vetor1, vetor2))


def multiplica_todos(vetor1: list[int], vetor2: list[int]) -> list[int]:
    '''
    Multiplica cada elemento de um vetor por todos os elementos do outro.

    Retorna um vetor com o resultado de cada conjunto de multiplicações.

    Parâmetros:\n
    vetor1 -- vetor em que cada elemento será multiplicador\n
    vetor2 -- vetor em que todos os elementos serão multiplicados em cada ciclo
    '''
    novo_vetor = []

    for n1 in vetor1:
        soma = 0

        # Somando o produto de n1 por cada elemento de n2 na variável soma
        for n2 in vetor2:
            soma += n1 * n2

        # Adicionando soma em novo_vetor e indo para o próximo número de vetor1
        novo_vetor.append(soma)

    return novo_vetor


def correlacao_cruzada(vetor: list[int], mascara: list[int]) -> list[int]:
    '''
    Percorre uma máscara calculando o produto interno em outr vetor.

    Retorna um vetor com o resultado de cada conjunto de multiplicações.

    Parâmetros:\n
    mascara -- vetor menor que percorrerá o vetor maior\n
    vetor -- vetor maior que será percorrido pela máscara
    '''

    novo_vetor = []

    # Fórmula do nº de elementos é (n - k + 1)
    # Em que n e k são os tamanhos do vetor e da máscara, respectivamente
    for i in range(len(vetor) - len(mascara) + 1):
        soma = 0

        # O índice do elemento do vetor a ser multiplicado pela máscara é i + j
        # Em que j vai de 0 a k - 1
        for j in range(len(mascara)):
            soma += vetor[i + j] * mascara[j]

        # Adicionando o resultado da soma a novo_vetor e indo para o próximo i
        novo_vetor.append(soma)

    return novo_vetor


def main() -> None:
    # Recebendo input do vetor inicial
    vetor1 = [int(n) for n in input().split(',')]

    while True:
        # Recebendo ação a ser realizada com o vetor1
        tarefa = input()

        # Usuário decide sair do programa
        if tarefa == 'fim':
            break

        # Funções cujos parâmetros são (vetor1, inteiro)
        elif tarefa in ['multiplicacao_escalar', 'n_duplicacao']:
            num = int(input())
            vetor1 = globals()[tarefa](vetor1, num)
            print(vetor1)

        # Funções cujo parâmetro é (vetor1) e retornam inteiros
        elif tarefa in ['soma_elementos']:
            vetor1 = [globals()[tarefa](vetor1)]
            print(vetor1)

        # Funções cujos parâmetros são (vetor1, vetor2)
        else:
            # Recebendo segundo vetor da operações
            vetor2 = [int(n) for n in input().split(',')]

            # Funções que retornam inteiros
            if tarefa in ['produto_interno']:
                vetor1 = [globals()[tarefa](vetor1, vetor2)]

            # Funções que retornam vetores
            else:
                vetor1 = globals()[tarefa](vetor1, vetor2)

            # Imprimindo vetor e indo para o próxima tarefa
            print(vetor1)


if __name__ == '__main__':
    main()
