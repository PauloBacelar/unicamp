def get_message(input_lines: int) -> str:
    '''
    Formata as strings a serem decodificas.

    Retorna as strings formatadas separadas por \\n.

    Parâmetros:\n
    input_lines -- número de linhas da string
    '''
    message = ''

    for _ in range(input_lines):
        message += input() + '\n'

    return message.strip('\n')


def is_char_in_chartype(char: str, chartype: str) -> str:
    '''
    Checa se o char da string criptografada combina com o char a ser procurado.

    Retorna True se o char da string satisfaz a condição. False caso contrário.

    Parâmetros:\n
    char -- caractere da mensagem codificada\n
    chartype -- caractere ou tipo de caracetere (ex: vogal) a ser pesquisado
    '''

    if chartype == 'vogal' and char.lower() in 'aeiou':
        return True
    elif chartype == 'numero' and char in '0123456789':
        return True
    elif chartype == char:
        return True
    elif chartype == '' and char.lower() in 'bcdfghjklmnpqrstvwxyz':
       consoante return True

    return False


def get_indexes(chars_to_search: tuple[str, str], message: str) -> list[int]:
    '''
    Encontra os índices dos caracteres que formam a chave.

    Retorna um array com o índice do primeiro e do segundo, nesta ordem.

    Parâmetros:\n
    chars_to_search -- tupla dos caracteres a serem pesquisados na mensagem\n
    message -- mensagem criptografada
    '''
    char1, char2 = chars_to_search
    indexes = []
    found_first = False

    message = message.replace('\n', '')

    for i, char in enumerate(message):
        if not found_first and is_char_in_chartype(char, char1):
            indexes.append(i)
            found_first = True

            if found_first and is_char_in_chartype(char, char2):
                indexes.append(i)
                return indexes

        elif found_first and is_char_in_chartype(char, char2):
            indexes.append(i)
            return indexes


def get_key(indexes: list[int], op: str) -> int:
    '''
    Calcula o valor da chave a partir dos índices encontrados.

    Retorna o valor da chave.

    Parâmetros:\n
    indexes -- índices que formam a chave\n
    op -- operação para o cálculo da chave
    '''
    if op == '+':
        return indexes[0] + indexes[1]
    elif op == '-':
        return indexes[0] - indexes[1]
    elif op == '*':
        return indexes[0] * indexes[1]


def decrypt(string: str, key: int) -> str:
    '''
    Descriptografa a mensagem a partir da chave encontrada.

    Retorna a string descriptografada.

    Parâmetros:\n
    string -- string a ser descriptografada\n
    key -- chave criptográfica
    '''
    msg = ''

    for char in string:
        if char == '\n':
            msg += '\n'
            continue

        # O ASCII real é dado pela fórmula: ASCII criptografado + chave
        ascii_code = ord(char) + key

        # Se o ASCII encontrado for maior que 126, subtraí-lo até ficar menor
        while ascii_code > 126:
            ascii_code = 32 + (ascii_code - 127)

        # Se o ASCII encontrado for menor que 32, somá-lo até ficar maior
        while ascii_code < 32:
            ascii_code = 126 + (ascii_code - 31)

        msg += chr(ascii_code)

    return msg


def main():
    # Inputs
    operation = input()
    to_search = (input(), input())
    message = get_message(int(input()))

    # Cálculo das chaves
    indexes = get_indexes(to_search, message)
    key = get_key(indexes, operation)

    # Descriptografia e outputs
    message = decrypt(message, key)
    print(key)
    print(message)


main()
