import math
import random


def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    conflicts = set()
    for analyzed_column in range(0, 8):     # Para cada posicao do array de tamanho 8.
        analyzed_column_value = individual[analyzed_column]    # Obtem o valor armazenado na posicao que esta sendo analizada.
        for i in range(0, 8):
            if analyzed_column != i:  # Ignora a analise da coluna atual.
                if individual[i] == analyzed_column_value:  # Caso esses valores sejam iguais, temos duas rainhas na mesma linha.
                    if i < analyzed_column:
                        conflicts.add((i, analyzed_column))
                    else:
                        conflicts.add((analyzed_column, i))
                elif i < analyzed_column:  # Está a esquerda da coluna sendo analisada.
                    if individual[i] == analyzed_column_value - analyzed_column + i:  # Está na diagonal 'esquerda baixo' da coluna sendo analisada.
                        conflicts.add((i, analyzed_column))
                else:  # Está a direita da coluna sendo analisada.
                    if individual[i] == analyzed_column_value - (i - analyzed_column):  # Está na diagonal 'direita baixo' da coluna sendo analisada.
                        conflicts.add((analyzed_column, i))
    return conflicts.__len__()


def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    winner = []
    if participants.__len__() > 0:
        best_score = math.inf
        # Percorre a lista de individuos e avalia cada um deles. Caso o individuo sob analise seja
        # Melhor que o melhor individuo encontrado até entao, substitui o melhor atual
        # Pelo novo melhor encontrado.
        for individual in participants:
            individual_score = evaluate(individual)
            if individual_score < best_score:
                winner = individual
                best_score = individual_score
    return winner


def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    crossover1 = []
    crossover2 = []
    for i in range(0, index):
        crossover1.append(parent1[i])
        crossover2.append(parent2[i])
    for i in range(index, 8):
        crossover1.append(parent2[i])
        crossover2.append(parent1[i])
    return [crossover1, crossover2]


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    if random.random() < m:
        mutated_individual = individual.copy()     # Instancia a lista que armazenará o individuo mutado.
        selected_position = random.randint(0, 7)   # Seleciona a posição onde ocorrerá a mutação.
        mutation_value = random.randint(1, 8)      # Gera o valor que será colocado na posição da mutação.
        mutated_individual[selected_position] = mutation_value  # 'Realiza' a mutação.
        return mutated_individual
    return individual


def generate_population(number_individuals):
    # Funcao auxiliar, utilizada para gerar os individuos da populacao inicial para execucao do algoritmo.
    count = 0
    population = []
    while count < number_individuals:
        new_individual = []
        for i in range(0, 8):
            new_individual.append(random.randint(1, 8))
        # Comparação feita para garantir que não teremos dois individuos iguais na população inicial.
        if new_individual not in population:
            population.append(new_individual)
            count += 1
    return population


def get_best_individual(population):
    # Função tournament retorna o melhor individuo dentro dos participantes.
    # Ao usarmos a população inteira como participantes, obtemos o melhor
    # Individuo da população.
    return tournament(population)


def get_tournament_participants(population, k):
    # Funcao para selecionar k individuos da populacao para participarem do tournament.
    participants = []
    while participants.__len__() < k:
        selected_participant = population[random.randint(0, (population.__len__())-1)]
        if selected_participant not in participants:
            participants.append(selected_participant)
    return participants


def get_max_num_conflicts(population):
    # Obtem o numero maximo de conflitos dentro de uma geracao.
    max_conflicts = -1
    for individual in population:
        individual_conflicts = evaluate(individual)
        if individual_conflicts > max_conflicts:
            max_conflicts = individual_conflicts
    return max_conflicts


def get_min_num_conflicts(population):
    # Obtem o numero minimo de conflitos dentro de uma geracao.
    return evaluate(get_best_individual(population))


def get_avg_num_conflicts(population):
    # Obtem o valor medio de conflitos dentro de uma geracao.
    total_conflicts = 0
    for individual in population:
        total_conflicts += evaluate(individual)
    avg_conflicts = total_conflicts / population.__len__()
    return avg_conflicts


def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:bool - se vai haver elitismo
    :return:list - melhor individuo encontrado
    """
    generation_count = 0    # Contador de gerações.
    population = generate_population(n)     # Gera os individuos iniciais da população.

    results_file = open('results.txt', 'w')
    results_file.write('Max conflitos populacao inicial: ' + str(get_max_num_conflicts(population)) + '\n')
    results_file.write('Min conflitos populacao inicial: ' + str(get_min_num_conflicts(population)) + '\n')
    results_file.write('Media conflitos populacao inicial: ' + str(get_avg_num_conflicts(population)) + '\n\n')

    while generation_count < g:
        new_generation = []
        if e is True:
            # Caso esteja sendo usado elitismo, inicializa a nova população com o melhor individuo
            # Da população anterior.
            new_generation.append(get_best_individual(population))
        # Enquanto a nova geração não está completamente preenchida.
        while new_generation.__len__() < n:
            # Obtem os dois proximos pais.
            parent1 = tournament(get_tournament_participants(population, k))
            parent2 = tournament(get_tournament_participants(population, k))
            # Realiza o crossover entre os pais.
            crossover_result = crossover(parent1, parent2, random.randint(1, 7))
            # Finalmente, executa o mutate nos dois individuos resultantes do crossover, para assim obter
            # Os dois novos individuos da proxima geracao.
            child1 = mutate(crossover_result[0], m)
            child2 = mutate(crossover_result[1], m)
            # Adiciona ambos novos individos na nova geracao.
            new_generation.append(child1)
            new_generation.append(child2)
        # Quando a nova geração foi obtida, a população sobre a qual o algoritmo irá executar na proxima
        # Iteracao passa a ser essa nova geracao.
        population = new_generation
        generation_count += 1

        results_file.write('Max conflitos geracao ' + str(generation_count) + ': ' + str(get_max_num_conflicts(population)) + '\n')
        results_file.write('Min conflitos geracao ' + str(generation_count) + ': ' + str(get_min_num_conflicts(population)) + '\n')
        results_file.write('Media conflitos geracao ' + str(generation_count) + ': ' + str(get_avg_num_conflicts(population)) + '\n\n')

    # Obtém o melhor individuo da geracao final obtida, para retornar como resultado da funcao.
    best_individual = get_best_individual(population)

    results_file.write('Avaliacao do melhor individuo encontrado: ' + str(evaluate(best_individual)) + '\n')
    results_file.write('Melhor individuo encontrado: ' + str(best_individual))
    results_file.close()

    return best_individual  # retorna o melhor individuo encontrado.


run_ga(20, 50, 8, 0.7, True)
