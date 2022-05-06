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
    return [random.randint(0, 23000) for i in range(size)]
 
# Avalia a solução com a função fitness
def evaluate_(candidates, args):
    fitness = []
    for cs in candidates: # iterar array de soluções
        fitness.append(perform_fitness(cs)) # montagem do array com as notas das soluções
    return fitness
 
# Calculo do fitness da solução informada
def perform_fitness(cs):
    for i, weight in enumerate(cs):
        cs[i] = np.round(cs[i])
    
    #         | Dianteiro | Central | Traseiro |
    # Carga 1 |   cs[0]   |  cs[4]  |  cs[8]   |
    # Carga 2 |   cs[1]   |  cs[5]  |  cs[9]   |
    # Carga 3 |   cs[2]   |  cs[6]  |  cs[10]  |
    # Carga 4 |   cs[3]   |  cs[7]  |  cs[11]  |

    fit = float((5*L + 4.5*S) / 7375)
    h1 = np.maximum(0, float(((6*L+5*S)/100)-60)) / 15
    h2 = np.maximum(0, float(((10*L+20*S)-15000))) / 3750
    h3 = np.maximum(0, float(L-800)) / 200
    h4 = np.maximum(0, float(S-750)) / 187.5
 
    fit = fit - (h1 + h2 + h3 + h4)
    return fit
 
# Avaliação final do melhor indivíduo(objetivo)
def solution_evaluation(L, S):
    L = np.round(L)
    S = np.round(S)
 
    print
    print("..RESUDO DA CARGA DE AVIÃO..")
    print("Lucro total:", float(5*L+4.5*S))
    print("Tempo de utilização semanal", float(10*L+20*S))
    print("Garrafas de leite:", L)
    print("Garrafas de suco:", S)
 
 
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
 
    perform_fitness(final_pop[0].candidate[0], final_pop[0].candidate[1])
    solution_evaluation(final_pop[0].candidate[0], final_pop[0].candidate[1])
 
main()