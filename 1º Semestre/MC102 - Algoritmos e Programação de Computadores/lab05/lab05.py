def params_to_int(*args):
  '''
  Recebe múltiplos parâmetros e os retorna como inteiros.

  Parâmetros:\n
  *args -- um conjunto de dois ou mais dados não-inteiros
  '''
  return [int(arg) for arg in args]


def reverter(i, j):
  '''
  Reverte a sequência do DNA dos índices i ao j.

  Retorna a nova sequência com a parte invertida.

  Parâmetros:\n
  i -- índice inicial\n
  j -- índice final
  '''
  i, j = params_to_int(i, j)

  # Colhendo sequência inalterada até i
  new_sequence = sequence[:i]

  # Se o j é maior que o tamanho da sequência, j vai só até o fim da sequência
  if j > len(sequence) - 1:
    j = len(sequence) - 1
  
  # Adicionando ordem inversa de i ao j da sequência à variável new_sequence
  for n in range(j, i-1, -1):
    new_sequence += sequence[n]

  # Colhendo sequência inalterada de j ao fim e retornando a nova sequência
  new_sequence += sequence[j+1:]
  return new_sequence


def transpor(i, j, k):
  '''
  Coloca uma parte A da sequência no local de uma outra parte B, e vice-versa

  Retorna a nova sequência com as partes trocadas.
  
  Parâmetros:\n
  i -- índice inicial (início da parte A)\n
  j -- índice médio (fim da parte A e início da parte B)\n
  k -- índice final (fim da parte B)
  '''
  i, j, k = params_to_int(i, j, k)

  # Colhendo parte inalterada até o índice i
  sequence1 = sequence[:i]

  # Separando as partes A e B a serem trocadas
  first_slice = sequence[i:j+1]
  second_slice = sequence[j+1:k+1]

  # Se a parte B não termina no fim da sequência
  if k+1 < len(sequence):
    sequence2 = sequence[k+1:] # Colher a parte inalterada após o índice k
    return sequence1 + second_slice + first_slice + sequence2

  return sequence1 + second_slice + first_slice


def combinar(g, i):
  '''
  Adiciona genes na sequência original em um índice i.

  Retorna a nova sequência alterada com os novos genes.

  Parâmetros:\n
  g -- sequência a ser adicionada\n
  i -- índice que indica onde adicionar g na sequência
  '''
  i = int(i)  
  return sequence[:i] + g + sequence[i:]
  

def concatenar(g):
  '''
  Adiciona genes no fim da sequência original.

  Retorna a nova sequência alterada com os novos genes.

  Parâmetros:\n
  g -- sequência a ser adicionada
  '''
  return sequence + g


def remover(i, j):
  '''
  Remove uma parte da sequência, do indíce i ao j.

  Retorna a nova sequência alterada com a parte excluída.

  Parâmetros:\n
  i -- índice incial da parte a ser removida\n
  j -- índice final da parte a ser removida
  '''
  i, j = params_to_int(i, j)
  
  return sequence[:i] + sequence[j+1:]


def transpor_e_reverter(i, j, k):
  '''
  Troca duas partes A e B da sequência e as inverte como uma parte só.

  Retorna a nova sequência alterada com as partes A e B transpostas e invertidas.

  Parâmetros: \n
  i -- índice inicial (início da parte A)\n
  j -- índice médio (fim da parte A e início da parte B)\n
  k -- índice final (fim da parte B)
  '''

  # Mudanças em sequence devem afetar todo o programa antes mesmo do return
  global sequence
  sequence = transpor(i, j, k)
  sequence = reverter(i, k)

  return sequence


def buscar(g):
  '''
  Imprime quantas vezes determinada parte aparece na sequência.

  Apenas na direção esquerda-direita.

  Parâmetros: \n
  g -- sequência a ser buscada\n
  '''
  print(sequence.count(g))


def buscar_bidirecional(g):
  '''
  Imprime quantas vezes determinada parte aparece na sequência.

  Contabiliza nas direções esquerda-direita e direita-esquerda.

  Parâmetros: \n
  g -- sequência a ser buscada\n
  '''
  print(sequence.count(g) + sequence[::-1].count(g))


def mostrar():
  '''
  Imprime a sequência.
  '''
  print(sequence)


def sair():
  '''
  Encerra a execução do programa.
  '''
  quit()



def main():
  while True:
    # Recebe os inputs e os coloca em uma lista entre os espaços
    inputs = input().split()

    # Determina a ação a ser realizada, que é sempre a primeira string do input
    task = inputs[0]

    # Se não há parâmetros, apenas executa a função
    if len(inputs) == 1:
      tasks[task]()
    else:
      # Caso contrário, separa os parâmetros em outra lista
      params = inputs[1:]

      # Funções que não alteram a variável sequence e não têm retorno
      if task in ['buscar_bidirecional', 'buscar']:
        tasks[task](*params)
      else:
        # Funções que alteram a variável sequence e têm retorno
        global sequence
        sequence = tasks[task](*params)


# Recebendo a sequência inicial
sequence = input()

# Definindo dicionário de ações
# Cada key aponta para a função correspondente, que pode ser executada como tasks['funcao']()
tasks = {
  'reverter': reverter,
  'transpor': transpor,
  'combinar': combinar,
  'concatenar': concatenar,
  'remover': remover,
  'transpor_e_reverter': transpor_e_reverter,
  'buscar': buscar,
  'buscar_bidirecional': buscar_bidirecional,
  'mostrar': mostrar,
  'sair': sair
}

main()
