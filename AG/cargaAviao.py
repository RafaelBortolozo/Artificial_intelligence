from random import Random
from time import time
from math import cos
from math import pi
from inspyred import ec
from inspyred.ec import terminators
import numpy as np
import os 
 
# Dianteiro: 10t, 6800m³, 680m³/t
# Central: 16t, 8700m³, 543,75m³/t
# traseiro: 8t, 5300m³, 662,5m³/t

# gerar 12 valores aleatórios, cada compartimento recebe partes das 4 cargas
def generate_(random, args):
    size = args.get('num_inputs', 12)
    return [random.randint(0, 16000) for i in range(size)]
 
# Avalia a solução com a função fitness
def evaluate_(candidates, args):
    fitness = []
    for cs in candidates: # iterar array de soluções
        fit = perform_fitness(cs)
        fitness.append(fit) # montagem do array com as notas das soluções
    return fitness
 
# Calculo do fitness da solução informada
def perform_fitness(cs):
    totalCargas = 0
    for i, weight in enumerate(cs):
        cs[i] = np.round(cs[i])
        totalCargas += cs[i]
    
    #         | Dianteiro | Central | Traseiro |
    # Carga 1 |   cs[0]   |  cs[1]  |  cs[2]   |
    # Carga 2 |   cs[3]   |  cs[4]  |  cs[5]   |
    # Carga 3 |   cs[6]   |  cs[7]  |  cs[8]   |
    # Carga 4 |   cs[9]   |  cs[10] |  cs[11]  |

    # CALCULO DO FIT, MULTIPLICA O PESO(kg) PELO PREÇO, SOMA TUDO E DIVIDE PELO ???? 
    vpc1 = 0.31  # Valor do peso na carga 1 (R$ 310/t)
    vpc2 = 0.38  # Valor do peso na carga 2 (R$ 380/t)
    vpc3 = 0.35  # Valor do peso na carga 3 (R$ 350/t)
    vpc4 = 0.285 # Valor do peso na carga 4 (R$ 285/t)
    
    # TOTAL DA CARGA x DENTRO DO AVIAO
    somaCarga1 = (cs[0] + cs[1] + cs[2])
    somaCarga2 = (cs[3] + cs[4] + cs[5])
    somaCarga3 = (cs[6] + cs[7] + cs[8])
    somaCarga4 = (cs[9] + cs[10] + cs[11])

    # TOTAL DE PESO EM CADA COMPARTIMENTO DO AVIAO
    somaDianteira = (cs[0] + cs[3] + cs[6] + cs[9])
    somaCentral = (cs[1] + cs[4] + cs[7] + cs[10])
    somaTraseira = (cs[2] + cs[5] + cs[8] + cs[11])

    fit = float((somaCarga1*vpc1 + somaCarga2*vpc2 + somaCarga3*vpc3 + somaCarga4*vpc4) / 42000)

    # PENALIZAÇÕES
    qtdH = 13

    # PENALINAZAÇÃO QUANTO AO PESO DAS CARGAS
    h1 = np.maximum(0, float(somaCarga1 - 18000)) / (18000/qtdH)
    h2 = np.maximum(0, float(somaCarga2 - 15000)) / (15000/qtdH)
    h3 = np.maximum(0, float(somaCarga3 - 23000)) / (23000/qtdH)
    h4 = np.maximum(0, float(somaCarga4 - 12000)) / (12000/qtdH)
    
    # PENALIZAÇÃO QUANTO AO PESO DOS COMPARTIMENTOS DO AVIAO
    h5 = np.maximum(0, float(somaDianteira - 10000)) / (10000/qtdH)
    h6 = np.maximum(0, float(somaCentral - 16000)) / (16000/qtdH)
    h7 = np.maximum(0, float(somaTraseira - 8000)) / (8000/qtdH)

    # PENALIZAÇÕES QUANTO AO VOLUME DOS COMPARTIMENTOS DO AVIAO
    h8 = np.maximum(0, float(cs[0]*0.48 + cs[3]*0.65 + cs[6]*0.58 + cs[9]*0.39)-6800) / (6800/qtdH)
    h9 = np.maximum(0, float(cs[1]*0.48 + cs[4]*0.65 + cs[7]*0.58 + cs[10]*0.39)-8700) / (8700/qtdH)
    h10 = np.maximum(0, float(cs[2]*0.48 + cs[5]*0.65 + cs[8]*0.58 + cs[11]*0.39)-5300) / (5300/qtdH)

    # PENALIZAÇÕES QUANTO A PROPORÇÃO DE CADA COMPARTIMENTO DO AVIAO
    h11 = np.maximum(0, float(((somaDianteira / totalCargas) - (10000/34000)))) / ((10000/34000)/qtdH)
    h12 = np.maximum(0, float(((somaCentral / totalCargas) - (16000/34000)))) / ((16000/34000)/qtdH)
    h13 = np.maximum(0, float(((somaTraseira / totalCargas) - (8000/34000)))) / ((8000/34000)/qtdH)

    fit = fit-(h1+h2+h3+h4+h5+h6+h7+h8+h9+h10+h11+h12+h13)
    return fit
 
# Avaliação final do melhor indivíduo(objetivo)
def solution_evaluation(cs):
    for i, value in enumerate(cs):
        cs[i] = np.round(cs[i])
 
    print("..RESUMO DA CARGA DE AVIÃO..")
    print("DIANTEIRA -- CENTRAL -- TRASEIRA")
    print("PesoCarga1(t): ", float(cs[0] * 0.310), " ", float(cs[1] * 0.310), " ", float(cs[2] * 0.310))
    print("PesoCarga2(t): ", float(cs[3] * 0.380), " ", float(cs[4] * 0.380), " ", float(cs[5] * 0.380))
    print("PesoCarga3(t): ", float(cs[6] * 0.350), " ", float(cs[7] * 0.350), " ", float(cs[8] * 0.350))
    print("PesoCarga4(t): ", float(cs[9] * 0.285), " ", float(cs[10] * 0.285), " ", float(cs[11] * 0.285))
 
 
def main():
    # função principal, cada execução é diferente
    rand = Random()
    rand.seed(int(time()))
 
    ea = ec.GA(rand)  # Instancia da classe de algoritmo genético
    ea.selector = ec.selectors.tournament_selection  # metodo de seleção: torneio
    ea.variator = [ec.variators.uniform_crossover,   # metodo de cruzamento uniforme
                   ec.variators.gaussian_mutation]   # metodo de mutacao
    ea.replacer = ec.replacers.steady_state_replacement  # Metodo de substituição
 
    # Função que determina o critério de parada do algoritmo
    # Critério de parada por geração
    ea.terminator = terminators.generation_termination
 
    # Função para gerar estatistica da evolução
    ea.observer = [ec.observers.stats_observer, ec.observers.file_observer]
 
    final_pop = ea.evolve(generator=generate_, # funcao que gera a população aleatoriamente
                          evaluator=evaluate_, # funcao que avalia as solucoes
                          pop_size=1000, # tamanho da populacao a cada geração
                          maximize=True, #True: maximização, False: minimização
                          bounder=ec.Bounder(0, 16000), # limites minimos e maximos dos genes (maior capacidade do avião é 16t)
                          max_generations=500, # maximo de gerações
                          num_inputs=12, # numero de genes no cromossomo (3 compartimentos * 4 cargas)
                          crossover_rate=0.25, # taxa de cruzamento
                          mutation_rate=0.25, # taxa de mutação
                          num_elites=1, # numero de individuos elites a serem selecionadas para a proxima população
                          num_selected=2, # numero de individuos
                          tournament_size=2, # tamanho do torneio
                          statistcs_fize=open("statistics.csv", "w"),
                          individuals_file=open("individuals.csv", "w")
                          )
 
    final_pop.sort(reverse=True) #ordena as soluções, indice zero é o melhor
 
    perform_fitness(final_pop[0].candidate[0], final_pop[1].candidate[1])
    solution_evaluation(final_pop[0].candidate[0], final_pop[1].candidate[1])
 
main()