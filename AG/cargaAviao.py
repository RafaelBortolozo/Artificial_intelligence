from audioop import reverse
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
        fit = perform_fitness(cs[0], cs[1], cs[2], cs[3], cs[4], cs[5], cs[6], cs[7], cs[8], cs[9], cs[10], cs[11])
        fitness.append(fit) # montagem do array com as notas das soluções
    return fitness
 
# Calculo do fitness da solução informada
def perform_fitness(cd1, cc1, ct1, cd2, cc2, ct2, cd3, cc3, ct3, cd4, cc4, ct4):
    cd1 = np.round(cd1)
    cc1 = np.round(cc1)
    ct1 = np.round(ct1)
    cd2 = np.round(cd2)
    cc2 = np.round(cc2)
    ct2 = np.round(ct2)
    cd3 = np.round(cd3)
    cc3 = np.round(cc3)
    ct3 = np.round(ct3)
    cd4 = np.round(cd4)
    cc4 = np.round(cc4)
    ct4 = np.round(ct4)

    totalCargas = cd1+cc1+ct1+cd2+cc2+ct2+cd3+cc3+ct3+cd4+cc4+ct4
    
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
    somaCarga1 = (cd1 + cc1 + ct1)
    somaCarga2 = (cd2 + cc2 + ct2)
    somaCarga3 = (cd3 + cc3 + ct3)
    somaCarga4 = (cd4 + cc4 + ct4)

    # TOTAL DE PESO EM CADA COMPARTIMENTO DO AVIAO
    somaDianteira = (cd1 + cd2 + cd3 + cd4)
    somaCentral = (cc1 + cc2 + cc3 + cc4)
    somaTraseira = (ct1 + ct2 + ct3 + ct4)

    # 18*310 + 15*380 + 23*350 + 12 * 285 = 22750
    # 22750: Estimativa de valor superior
    fit = float((somaCarga1*vpc1 + somaCarga2*vpc2 + somaCarga3*vpc3 + somaCarga4*vpc4) / 13000)

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
    h8 = np.maximum(0, float(cd1*0.48 + cd2*0.65 + cd3*0.58 + cd4*0.39)-6800) / (6800/qtdH)
    h9 = np.maximum(0, float(cc1*0.48 + cc2*0.65 + cc3*0.58 + cc4*0.39)-8700) / (8700/qtdH)
    h10 = np.maximum(0, float(ct1*0.48 + ct2*0.65 + ct3*0.58 + ct4*0.39)-5300) / (5300/qtdH)

    # PENALIZAÇÕES QUANTO A PROPORÇÃO DE CADA COMPARTIMENTO DO AVIAO
    pesoMax = 34000
    h11 = np.maximum(0, float(((somaDianteira / pesoMax) - (10000/pesoMax)))) / ((10000/pesoMax)/qtdH)
    h12 = np.maximum(0, float(((somaCentral / pesoMax) - (16000/pesoMax)))) / ((16000/pesoMax)/qtdH)
    h13 = np.maximum(0, float(((somaTraseira / pesoMax) - (8000/pesoMax)))) / ((8000/pesoMax)/qtdH)

    fit = fit-(h1+h2+h3+h4+h5+h6+h7+h8+h9+h10+h11+h12+h13)
    return fit
 
# Avaliação final do melhor indivíduo(objetivo)
def solution_evaluation(cd1, cc1, ct1, cd2, cc2, ct2, cd3, cc3, ct3, cd4, cc4, ct4):
    cd1 = np.round(cd1)
    cc1 = np.round(cc1)
    ct1 = np.round(ct1)
    cd2 = np.round(cd2)
    cc2 = np.round(cc2)
    ct2 = np.round(ct2)
    cd3 = np.round(cd3)
    cc3 = np.round(cc3)
    ct3 = np.round(ct3)
    cd4 = np.round(cd4)
    cc4 = np.round(cc4)
    ct4 = np.round(ct4)
 
    print("..RESUMO DA CARGA DE AVIÃO..")
    print("DIANTEIRA -- CENTRAL -- TRASEIRA")
    print("PesoCarga1(t): ", cd1, " - ", cc1, " - ", ct1)
    print("PesoCarga2(t): ", cd2, " - ", cc2, " - ", ct2)
    print("PesoCarga3(t): ", cd3, " - ", cc3, " - ", ct3)
    print("PesoCarga4(t): ", cd4, " - ", cc4, " - ", ct4)
 
 
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
                          max_generations=5000, # maximo de gerações
                          num_inputs=12, # numero de genes no cromossomo (3 compartimentos * 4 cargas)
                          crossover_rate=0.5, # taxa de cruzamento
                          mutation_rate=0.7, # taxa de mutação
                          num_elites=1, # numero de individuos elites a serem selecionadas para a proxima população
                          num_selected=12, # numero de individuos
                          tournament_size=12, # tamanho do torneio
                          statistcs_fize=open("statistics.csv", "w"),
                          individuals_file=open("individuals.csv", "w")
                          )
 
    final_pop.sort(reverse=True) #ordena as soluções, indice zero é o melhor
 
    perform_fitness(final_pop[0].candidate[0], final_pop[0].candidate[1], final_pop[0].candidate[2], final_pop[0].candidate[3], final_pop[0].candidate[4], final_pop[0].candidate[5], final_pop[0].candidate[6], final_pop[0].candidate[7], final_pop[0].candidate[8], final_pop[0].candidate[9], final_pop[0].candidate[10], final_pop[0].candidate[11])
    solution_evaluation(final_pop[0].candidate[0], final_pop[0].candidate[1], final_pop[0].candidate[2], final_pop[0].candidate[3], final_pop[0].candidate[4], final_pop[0].candidate[5], final_pop[0].candidate[6], final_pop[0].candidate[7], final_pop[0].candidate[8], final_pop[0].candidate[9], final_pop[0].candidate[10], final_pop[0].candidate[11])
 
main()