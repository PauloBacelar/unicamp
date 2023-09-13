def get_movies(number_of_movies: int) -> dict:
    '''
    Recebe o nome dos filmes e os acopla no dicionário de categorias.

    Retorna o dicionário atualizado e um array com o nome dos filmes.

    Parâmetros:\n
    number_of_movies -- número de filmes a serem digitados
    '''
    movies = []

    for _ in range(number_of_movies):
        movie = input()
        movies.append(movie)

        for category in categories:
            categories[category][movie] = []

    return [categories, movies]


def get_reviews(number_of_reviews: int) -> dict:
    '''
    Recebe as avaliações.

    Retorna um array com o conjunto das avaliações.

    Parâmetros:\n
    number_of_revies -- quantidade de avaliações
    '''

    reviews = []

    for _ in range(number_of_reviews):
        reviews.append(input())

    return reviews


def get_rates(reviews: list[str]) -> dict:
    '''
    Adiciona as notas ao dicionário categorias.

    Retorna o dicionário categorias atualizado.

    Parâmetros:\n
    reviews -- lista de avaliações
    '''
    for review in reviews:
        review = review.split(', ')
        category, movie, rate = review[1], review[2], review[3]
        categories[category][movie].append(int(rate))

    return categories


def calculate_scores(categories: dict) -> dict:
    '''
    Calcula as pontuações de cada filme em cada categoria.

    Retorna o dicionário de categorias atualizado.

    Parâmetros:\n
    categories -- dicionário de categorias
    '''
    for category in list(categories):
        for movie in list(categories[category]):

            # Soma das avaliações e número de avaliações
            sum_rate = sum(categories[category][movie])
            rates_num = len(categories[category][movie])

            # Calculando se houve nota dada ao filme. Se não, deletando do dict
            if rates_num > 0:
                categories[category][movie] = [sum_rate / rates_num, rates_num]
            else:
                categories[category].pop(movie)

    return categories


def get_winners(categories: dict) -> dict:
    '''
    Calcula os vencedores a partir do dicionário de pontuações.

    Retorna um novo dicionário com o vencedor de cada categoria.

    Parâmetros:\n
    categories -- dicionário de pontuações
    '''

    # Criando dicionário de vencedores, que será retornado pela função
    winners = {}

    for category in categories:
        # Maior pontuação da categoria
        highest_rate = 0

        # Quantos votos recebeu o filme com maior pontuação (desempate)
        len_highest_rate = 0

        # Nome do filme vencedor
        winner = ''

        for movie in categories[category]:
            # Filme tem nota maior que a variável highest_rate
            if categories[category][movie][0] > highest_rate:

                # Atualizando variáveis do vencedor
                highest_rate = categories[category][movie][0]
                len_highest_rate = categories[category][movie][1]
                winner = sorted(categories[category].items(),
                                key=lambda x: x[1])[-1]

            # Filme tem a mesma nota da variável highest_rate
            elif categories[category][movie][0] == highest_rate:

                # Comparando a quantidade de votos
                if categories[category][movie][1] > len_highest_rate:

                    # Atualizando variáveis do vencedor
                    highest_rate = categories[category][movie][0]
                    len_highest_rate = categories[category][movie][1]
                    winner = sorted(categories[category].items(),
                                    key=lambda x: x[1])[-1]

        # Alocando vencedor da categoria no dicionário winners
        winners[category] = winner

    return winners


def special_categories(winners: dict, reviews: dict, movies: list) -> dict:
    '''
    Calcula os vencedores das categorias especiais.

    Retorna um dicionário com os vencedores.

    Parâmetros:\n
    winners -- vencedores das categorias simples\n
    reviews -- lista de avaliações\n
    movies -- lista de filmes
    '''

    def get_worst() -> str:
        '''
        Verifica o vencedor da categoria 'pior filme do ano'.

        Retorna o nome do filme vencedor.
        '''

        # Dicionário filmes e suas pontuações
        worst_movies = {}

        # Calculando pontuação princnipal de cada filme
        for category in winners:
            movie_name = winners[category][0]

            # Incrementando pontuação caso o filme esteja no dict
            if movie_name in worst_movies.keys():
                worst_movies[movie_name] += 1

            # Adicionando filme ao dict caso ele não esteja lá
            else:
                worst_movies[movie_name] = 1

        # Lista de filmes empatados
        drawed = []

        # Adicionando filmes com pontuação máxima em drawed
        for movie in worst_movies:
            if worst_movies[movie] == max(worst_movies.values()):
                drawed.append(movie)

        # Apenas um filme com pontuação máxima (não há empate)
        if len(drawed) == 1:
            # Ordenando dict worst_movies por pontuação (crescente)
            worst_movies = sorted(worst_movies.items(), key=lambda x: x[1])

            # Pior filme é o último do dict
            worst_movie = worst_movies[-1][0]

        # Mais de um filme com pontuação máxima (há empate)
        else:
            # Recebendo as pontuações de todas as categorias para desempate
            all_rates = get_rates(reviews)

            # Sobrescrevendo dict worst_movies
            worst_movies = {}

            # Calculando pontuação de desempate
            for category in all_rates:
                for movie in all_rates[category]:
                    # Filme não está empatado na pontuação máxima
                    if movie not in drawed:
                        continue

                    # Notas começam a partir do terceiro elemento do array
                    # 1º elemento é a média, o 2º é o nº de notas
                    rates = all_rates[category][movie][2:]

                    # Calculando média
                    average = sum(rates) / len(rates)

                    # Adicionando filme em worst_movies, caso não esteja
                    if movie not in worst_movies.keys():
                        worst_movies[movie] = average

                    # Incrementando nota de desempate ao filme
                    else:
                        worst_movies[movie] += average

            # Ordenando dict worst_movies por nota e pegando último elemento
            worst_movie = sorted(worst_movies.items(),
                                 key=lambda x: x[1])[-1][0]
      
        # Retornando vencedor da categoria
        return worst_movie

    def get_best() -> list[str]:
        '''
        Verifica o vencedor da categoria 'não merecia estar aqui'.

        Retorna uma string com o nome dos vencedores
        '''

        # Criando lista de vencedores
        best_movies = []

        # Criando conjunto de filmes que foram avaliados
        reviewed_movies = set(review.split(', ')[2] for review in reviews)

        # Adicionando filmes em best_movies
        for movie in movies:
            # Filme não foi avaliado, é vencedor da categoria
            if movie not in reviewed_movies:
                best_movies.append(movie)

        # Retornando vencedores em uma string
        return ', '.join(best_movies)

    # Retornando vencedores de cada categoria
    return {
        'pior filme do ano': get_worst(),
        'não merecia estar aqui': get_best()
    }


def print_result(winners: dict, special_winners: dict) -> None:
    '''
    Imprime os resultados das categorias simples e especiais.

    Não há retorno.

    Parâmetros:\n
    winners -- vencedores das categorias simples\n
    speical_winners -- vencedores das categorias especiais
    '''
    print('#### abacaxi de ouro ####')

    print('\ncategorias simples')
    for category, winner in winners.items():
        print(f'categoria: {category}')
        print(f'- {winner[0]}')

    print('\ncategorias especiais')
    for category, winner in special_winners.items():
        print(f'prêmio {category}')

        if winner in ['', []]:
            print('- sem ganhadores')
        else:
            print(f'- {winner}')


def main():
    # Recebendo filmes
    number_of_movies = int(input())
    categories, movies = get_movies(number_of_movies)

    # Recebendo avaliações e notas
    reviews = get_reviews(int(input()))
    categories = get_rates(reviews)
    categories = calculate_scores(categories)

    # Recebendo vencedores
    winners = get_winners(categories)
    special_winners = special_categories(winners, reviews, movies)

    # Imprimindo resultado
    print_result(winners, special_winners)


# Variável global de dicionário categorias
categories = {
    'filme que causou mais bocejos': {},
    'filme que foi mais pausado': {},
    'filme que mais revirou olhos': {},
    'filme que não gerou discussão nas redes sociais': {},
    'enredo mais sem noção': {}
}

if __name__ == '__main__':
    main()
