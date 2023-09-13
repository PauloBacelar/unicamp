# Transformando lista de strings em int
def sanitize_nums(nums_str):
    return [int(num) for num in nums_str.split()]


# Definindo até onde vai a metade da lista de jogadores
def get_half(num_players):
    if num_players % 2 == 0:
        return num_players // 2
    else:
        return (num_players // 2) + 1


# Calculando gaps (Ls-Li) a serem multiplicados/somados pelo número recebido pelo jogador
def get_gaps(limits):
    gaps = []
    
    for i in range(0, len(limits) - 1, 2):
        gaps.append(limits[i+1] - limits[i])
        
    return gaps
    

# Calculando a pontuação dos jogadores
def get_points(nums, gaps, num_players):
    half = get_half(num_players)
    points = []
    
    for i in range(len(nums)):
        if i + 1 <= half:
            points.append(nums[i] * gaps[i])
        else:
            points.append(nums[i] + gaps[i])
    
    return points


# Verificando se houve empate
def is_draw(points):
    return points.count(max(points)) > 1
    

# Mostrando resultado
def show_result(points):
    if is_draw(points):
        print('Rodada de cerveja para todos os jogadores!')
    else:
        winner = points.index(max(points)) + 1
        winner_points = points[winner - 1]
        print(f'O jogador número {winner} vai receber o melhor bolo da cidade pois venceu com {winner_points} ponto(s)!')


# Recebendo inputs
num_players = int(input())
nums = sanitize_nums(input())
limits = sanitize_nums(input())

# Recebendo gaps
gaps = get_gaps(limits)

# Recebendo pontuações
points = get_points(nums, gaps, num_players)

# Resultado
show_result(points)
