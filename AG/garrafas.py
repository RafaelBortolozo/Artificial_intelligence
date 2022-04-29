from random import Random
from time import time
from math import cos
from math import pi
from inspyred import ec
from inspyred.ec import terminators
import numpy as np
import os 
 
 
# Generate Population
def generate_(random, args):
    size = args.get('num_inputs', 2)
    return [random.randint(0, 800) for i in range(size)]
 
 
# Evaluate Fitness
def evaluate_(candidates, args):
    fitness = []
    for cs in candidates:
        fit = perform_fitness(cs[0], cs[1])
        fitness.append(fit)
    return fitness
 
 
# Perform Fitness, calculate the fitness of each candidate
def perform_fitness(L, S):
    L = np.round(L)
    S = np.round(S)
 
    fit = float((5*L + 4.5*S) / 7375)
    h1 = np.maximum(0, float(((6*L+5*S)/100)-60)) / 15
    h2 = np.maximum(0, float(((10*L+20*S)-15000))) / 3750
    h3 = np.maximum(0, float(L-800)) / 200
    h4 = np.maximum(0, float(S-750)) / 187.5
 
    fit = fit - (h1 + h2 + h3 + h4)
    return fit
 
# Avaliação final do melhor indivíduo(objetivo)
 
 
def solution_evaluation(L, S):
    #L = cs[0]
    #S = cs[1]
 
    L = np.round(L)
    S = np.round(S)
 
    print
    print("..RESUDO DA PRODUÇÃO DE GARRAFAS..")
    print("Lucro total:", float(5*L+4.5*S))
    print("Tempo de utilização semanal", float(10*L+20*S))
    print("Garrafas de leite:", L)
    print("Garrafas de suco:", S)
 
 
def main():
    rand = Random()
    rand.seed(int(time()))
 
    ea = ec.GA(rand)  # Instancia o algoritmo genético
    ea.selector = ec.selectors.tournament_selection  # Meteodo de seleção por torneio
    ea.variator = [ec.variators.uniform_crossover,
                   ec.variators.gaussian_mutation]  # Metodo cruzamento uniforme
    ea.replacer = ec.replacers.steady_state_replacement  # Metodo de substituição
 
    # Função que determina o critério  de parada
    # Critério de parada por geração
    ea.terminator = terminators.generation_termination
 
    # Função para gerar estatistica da evolução
    ea.observer = [ec.observers.stats_observer,
                   ec.observers.file_observer]  # Estatistica
 
    final_pop = ea.evolve(generator=generate_,
                          evaluator=evaluate_,
                          pop_size=1000,
                          maximize=True,
                          bounder=ec.Bounder(0, 800),
                          max_generations=10000,
                          num_inputs=2,
                          crossover_rate=0.25,
                          mutation_rate=0.25,
                          num_elites=1,
                          num_selected=2,
                          tournament_size=2,
                          statistcs_fize=open("statistics.csv", "w"),
                          individuals_file=open("individuals.csv", "w")
                          )
 
    final_pop.sort(reverse=True)
    #print(final_pop[0])
 
    perform_fitness(final_pop[0].candidate[0], final_pop[1].candidate[1])
    solution_evaluation(final_pop[0].candidate[0], final_pop[1].candidate[1])
 
 
main()