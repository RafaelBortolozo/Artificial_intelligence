from random import Random
from time import time
from inspyred import ec
from inspyred.ec import terminators
import numpy as np 

# CONSTANTES DO AVIÃO:
PESO_DIANTEIRO = 10000  # (kg)
PESO_CENTRO = 16000     # (kg)
PESO_TRASEIRO = 8000    # (kg)
VOLUME_DIANTEIRO = 6800 # (m³)
VOLUME_CENTRO = 8700    # (m³)
VOLUME_TRASEIRO = 5300  # (m³)

# CONSTANTES DAS CARGAS:
PESO_CARGA_1 = 18000  # (kg)
PESO_CARGA_2 = 15000  # (kg)
PESO_CARGA_3 = 23000  # (kg)
PESO_CARGA_4 = 12000  # (kg)
VOLUME_CARGA_1 = 0.48 # (m³/kg)
VOLUME_CARGA_2 = 0.65 # (m³/kg)
VOLUME_CARGA_3 = 0.58 # (m³/kg)
VOLUME_CARGA_4 = 0.39 # (m³/kg)
VALOR_CARGA_1 = 0.31  # (R$/kg)
VALOR_CARGA_2 = 0.38  # (R$/kg)
VALOR_CARGA_3 = 0.35  # (R$/kg)
VALOR_CARGA_4 = 0.285 # (R$/kg)

def generate_(random, args):    
    # 4 VALORES SÃO GERADOS PARA CADA COMPARTIMENTO, LIMITADOS PELA CAPACIDADE DO COMPARTIMENTO
    cd = np.random.randint(low=0, high=PESO_DIANTEIRO, size=4).tolist()
    cc = np.random.randint(low=0, high=PESO_CENTRO, size=4).tolist()
    ct = np.random.randint(low=0, high=PESO_TRASEIRO, size=4).tolist()

    # SE A SOMA DOS PESOS DAS CARGAS FOR MENOR QUE A CAPACIDADE DO COMPARTIMENTO, VAI INCREMENTANDO +1kg EM QUALQUER CARGA
    while sum(cd) < PESO_DIANTEIRO:
        i = random.randint(0, 3)
        cd[i] += 1

    while sum(cc) < PESO_CENTRO:
        i = random.randint(0, 3)
        cc[i] += 1
    
    while sum(ct) < PESO_TRASEIRO:
        i = random.randint(0, 3)
        ct[i] += 1
    
    # SE A SOMA DOS PESOS DAS CARGAS FOR MAIOR QUE A CAPACIDADE DO COMPARTIMENTO, VAI DECREMENTANDO -1kg EM QUALQUER CARGA
    while sum(cd) > PESO_DIANTEIRO:
        i = random.randint(0, 3)
        if cd[i] != 0:
            cd[i] -= 1

    while sum(cc) > PESO_CENTRO:
        i = random.randint(0, 3)
        if cc[i] != 0:
            cc[i] -= 1
    
    while sum(ct) > PESO_TRASEIRO:
        i = random.randint(0, 3)
        if ct[i] != 0:
            ct[i] -= 1

    return [cd[0], cc[0], ct[0], cd[1], cc[1], ct[1], cd[2], cc[2], ct[2], cd[3], cc[3], ct[3]]
 
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
    
    # TOTAL DA CARGA n DENTRO DO AVIAO
    somaPesoCarga1 = (cd1 + cc1 + ct1)
    somaPesoCarga2 = (cd2 + cc2 + ct2)
    somaPesoCarga3 = (cd3 + cc3 + ct3)
    somaPesoCarga4 = (cd4 + cc4 + ct4)

    # TOTAL DE PESO EM CADA COMPARTIMENTO
    somaPesoDianteiro = (cd1 + cd2 + cd3 + cd4)
    somaPesoCentro = (cc1 + cc2 + cc3 + cc4)
    somaPesoTraseiro = (ct1 + ct2 + ct3 + ct4)

    # TOTAL DE VOLUME EM CADA COMPARTIMENTO 
    somaVolumeDianteiro = (cd1*VOLUME_CARGA_1 + cd2*VOLUME_CARGA_2 + cd3*VOLUME_CARGA_3 + cd4*VOLUME_CARGA_4)
    somaVolumeCentro    = (cc1*VOLUME_CARGA_1 + cc2*VOLUME_CARGA_2 + cc3*VOLUME_CARGA_3 + cc4*VOLUME_CARGA_4)
    somaVolumeTraseiro  = (ct1*VOLUME_CARGA_1 + ct2*VOLUME_CARGA_2 + ct3*VOLUME_CARGA_3 + ct4*VOLUME_CARGA_4)

    # LIMITES DO AVIAO
    pesoMaxAviao = PESO_DIANTEIRO + PESO_CENTRO + PESO_TRASEIRO
    volumeMaxAviao = VOLUME_DIANTEIRO + VOLUME_CENTRO + VOLUME_TRASEIRO

    # 12000: Estimativa empirica de valor superior
    fit = float((somaPesoCarga1*VALOR_CARGA_1 + somaPesoCarga2*VALOR_CARGA_2 + somaPesoCarga3*VALOR_CARGA_3 + somaPesoCarga4*VALOR_CARGA_4) / 12000)

    # PENALIZAÇÕES
    qtdH = 15
    
    # PENALIZAÇÃO QUANTO AO PESO DAS CARGAS
    h1 = np.maximum(0, float(somaPesoCarga1 - PESO_CARGA_1)) / (PESO_CARGA_1/qtdH)
    h2 = np.maximum(0, float(somaPesoCarga2 - PESO_CARGA_2)) / (PESO_CARGA_2/qtdH)
    h3 = np.maximum(0, float(somaPesoCarga3 - PESO_CARGA_3)) / (PESO_CARGA_3/qtdH)
    h4 = np.maximum(0, float(somaPesoCarga4 - PESO_CARGA_4)) / (PESO_CARGA_4/qtdH)

    # PENALIZAÇÃO QUANTO AO PESO DOS COMPARTIMENTOS DO AVIAO
    h5 = np.maximum(0, float(somaPesoDianteiro - PESO_DIANTEIRO)) / (PESO_DIANTEIRO/qtdH)
    h6 = np.maximum(0, float(somaPesoCentro - PESO_CENTRO)) / (PESO_CENTRO/qtdH)
    h7 = np.maximum(0, float(somaPesoTraseiro - PESO_TRASEIRO)) / (PESO_TRASEIRO/qtdH)

    # PENALIZAÇÕES QUANTO AO VOLUME DOS COMPARTIMENTOS DO AVIAO
    h8 = np.maximum(0, float(cd1*VOLUME_CARGA_1 + cd2*VOLUME_CARGA_2 + cd3*VOLUME_CARGA_3 + cd4*VOLUME_CARGA_4)-VOLUME_DIANTEIRO) / (VOLUME_DIANTEIRO/qtdH)
    h9 = np.maximum(0, float(cc1*VOLUME_CARGA_1 + cc2*VOLUME_CARGA_2 + cc3*VOLUME_CARGA_3 + cc4*VOLUME_CARGA_4)-VOLUME_CENTRO) / (VOLUME_CENTRO/qtdH)
    h10 = np.maximum(0, float(ct1*VOLUME_CARGA_1 + ct2*VOLUME_CARGA_2 + ct3*VOLUME_CARGA_3 + ct4*VOLUME_CARGA_4)-VOLUME_TRASEIRO) / (VOLUME_TRASEIRO/qtdH)

    # PENALIZAÇÕES QUANTO A PROPORÇÃO DE CADA COMPARTIMENTO DO AVIAO
    h11 = np.maximum(0, float(((somaPesoDianteiro / totalCargas) - (PESO_DIANTEIRO/pesoMaxAviao))) / ((PESO_DIANTEIRO/pesoMaxAviao)/qtdH))
    h12 = np.maximum(0, float(((somaPesoCentro / totalCargas) - (PESO_CENTRO/pesoMaxAviao))) / ((PESO_CENTRO/pesoMaxAviao)/qtdH))
    h13 = np.maximum(0, float(((somaPesoTraseiro / totalCargas) - (PESO_TRASEIRO/pesoMaxAviao))) / ((PESO_TRASEIRO/pesoMaxAviao)/qtdH))

    # PENALIZAÇÕES QUANTO AOS LIMITES DO AVIAO
    h14 = np.maximum(0, float((somaPesoDianteiro+somaPesoCentro+somaPesoTraseiro) - pesoMaxAviao)) / (pesoMaxAviao/qtdH)
    h15 = np.maximum(0, float((somaVolumeDianteiro+somaVolumeCentro+somaVolumeTraseiro)) - volumeMaxAviao) / (volumeMaxAviao/qtdH)

    fit = fit-(h1+h2+h3+h4+h5+h6+h7+h8+h9+h10+h11+h12+h13+h14+h15)
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
    print("PESO_CARGA1(kg): ", cd1, " - ", cc1, " - ", ct1)
    print("PESO_CARGA2(kg): ", cd2, " - ", cc2, " - ", ct2)
    print("PESO_CARGA3(kg): ", cd3, " - ", cc3, " - ", ct3)
    print("PESO_CARGA4(kg): ", cd4, " - ", cc4, " - ", ct4)
    lucro = ((cd1+cc1+ct1)*VALOR_CARGA_1 + (cd2+cc2+ct2)*VALOR_CARGA_2 + (cd3+cc3+ct3)*VALOR_CARGA_3 + (cd4+cc4+ct4)*VALOR_CARGA_4)
    print(f"Lucro(R$): {np.round(lucro, 2)}")

    # TOTAL DE PESO EM CADA COMPARTIMENTO DO AVIAO
    somaDianteira = (cd1 + cd2 + cd3 + cd4)
    somaCentral = (cc1 + cc2 + cc3 + cc4)
    somaTraseira = (ct1 + ct2 + ct3 + ct4)
    total = somaDianteira+somaCentral+somaTraseira
    print("PesoTotal(kg): ", total)

    # VERIFICAÇÃO DOS PESOS
    if somaDianteira > PESO_DIANTEIRO:
        print(f"Peso dianteiro excedido: {somaDianteira}")
    if somaCentral > PESO_CENTRO:
        print(f"Peso central excedido: {somaCentral}")
    if somaTraseira > PESO_TRASEIRO:
        print(f"Peso traseiro excedido: {somaTraseira}")
    
    # VERIFICAÇÃO DOS METROS CUBICOS
    if (cd1*VOLUME_CARGA_1 + cd2*VOLUME_CARGA_2 + cd3*VOLUME_CARGA_3 + cd4*VOLUME_CARGA_4) > VOLUME_DIANTEIRO:
        print(f"espaço dianteiro excedido: {cd1*VOLUME_CARGA_1 + cd2*VOLUME_CARGA_2 + cd3*VOLUME_CARGA_3 + cd4*VOLUME_CARGA_4}")
    if (cc1*VOLUME_CARGA_1 + cc2*VOLUME_CARGA_2 + cc3*VOLUME_CARGA_3 + cc4*VOLUME_CARGA_4) > VOLUME_CENTRO:
        print(f"espaço central excedido: {cc1*VOLUME_CARGA_1 + cc2*VOLUME_CARGA_2 + cc3*VOLUME_CARGA_3 + cc4*VOLUME_CARGA_4}")
    if (ct1*VOLUME_CARGA_1 + ct2*VOLUME_CARGA_2 + ct3*VOLUME_CARGA_3 + ct4*VOLUME_CARGA_4) > VOLUME_TRASEIRO:
        print(f"espaço traseiro excedido: {ct1*VOLUME_CARGA_1 + ct2*VOLUME_CARGA_2 + ct3*VOLUME_CARGA_3 + ct4*VOLUME_CARGA_4}")
 
    # VERIFICAÇÃO DE PROPORÇÃO, MESMA LÓGICA DA TABELA
    if (((somaDianteira/total) >= 0.3) or ((somaDianteira/total) <= 0.29)):
        print(f"proporção dianteira incorreta: {np.round((somaDianteira/total),4)}")
    if (((somaCentral/total) >= 0.48) or ((somaCentral/total) <= 0.47)):
        print(f"proporção central incorreta: {np.round((somaCentral/total),4)}")
    if (((somaTraseira/total) >= 0.24) or ((somaTraseira/total) <= 0.23)):
        print(f"proporção traseira incorreta: {np.round((somaTraseira/total),4)}")

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
                          pop_size=5000, # tamanho da populacao a cada geração
                          maximize=True, #True: maximização, False: minimização
                          bounder=ec.Bounder(0, 16000), # limites minimos e maximos dos genes (maior capacidade do avião é 16t)
                          max_generations=10000, # maximo de gerações
                          num_inputs=12, # numero de genes no cromossomo (3 compartimentos * 4 cargas)
                          crossover_rate=0.2, # taxa de cruzamento
                          mutation_rate=0.3, # taxa de mutação
                          num_elites=2, # numero de individuos elites a serem selecionadas para a proxima população
                          num_selected=12, # numero de individuos
                          tournament_size=2, # tamanho do torneio
                          statistcs_fize=open("statistics.csv", "w"),
                          individuals_file=open("individuals.csv", "w")
                          )

 
    final_pop.sort(reverse=True) #ordena as soluções, indice zero é o melhor
 
    perform_fitness(final_pop[0].candidate[0], final_pop[0].candidate[1], final_pop[0].candidate[2], final_pop[0].candidate[3], final_pop[0].candidate[4], final_pop[0].candidate[5], final_pop[0].candidate[6], final_pop[0].candidate[7], final_pop[0].candidate[8], final_pop[0].candidate[9], final_pop[0].candidate[10], final_pop[0].candidate[11])
    solution_evaluation(final_pop[0].candidate[0], final_pop[0].candidate[1], final_pop[0].candidate[2], final_pop[0].candidate[3], final_pop[0].candidate[4], final_pop[0].candidate[5], final_pop[0].candidate[6], final_pop[0].candidate[7], final_pop[0].candidate[8], final_pop[0].candidate[9], final_pop[0].candidate[10], final_pop[0].candidate[11])
 
main()