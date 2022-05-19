from operator import xor
from random import Random
from time import time
from inspyred import ec
from inspyred.ec import terminators
import numpy as np

from sympy import comp 
 
# Dianteiro: 10t, 6800m³, 680m³/t
# Central: 16t, 8700m³, 543,75m³/t
# traseiro: 8t, 5300m³, 662,5m³/t

def is_valid_proportion(value, total, proportion_min, proportion_max):
    if (value/total >= proportion_min) and (value/total <= proportion_max):
        return True
    return False 

# gerar 12 valores aleatórios, cada compartimento recebe partes das 4 cargas
def generate_(random, args):
    size = args.get('num_inputs', 12)
    pesoDianteiro = 10000
    pesoCentro = 16000
    pesoTraseiro = 8000
    tamDianteiro = 6800
    tamCentro = 8700
    tamTraseiro = 5300
    tamDianteiroKG = tamDianteiro/1000
    tamCentroKG = tamCentro/1000
    tamTraseiroKG = tamTraseiro/1000
   
    cd = np.random.randint(low=10, high=pesoDianteiro, size=4).tolist()
    cc = np.random.randint(low=10, high=pesoCentro, size=4).tolist()
    ct = np.random.randint(low=10, high=pesoTraseiro, size=4).tolist()

    # SE A SOMA DOS PESOS DAS CARGAS FOR MENOR QUE A CAPACIDADE DO COMPARTIMENTO, VAI INCREMENTANDO +1kg EM QUALQUER CARGA
    while sum(cd) < pesoDianteiro:
        i = random.randint(0, 3)
        cd[i] += 1

    while sum(cc) < pesoCentro:
        i = random.randint(0, 3)
        cc[i] += 1
    
    while sum(ct) < pesoTraseiro:
        i = random.randint(0, 3)
        ct[i] += 1
    
    # SE A SOMA DOS PESOS DAS CARGAS FOR MAIOR QUE A CAPACIDADE DO COMPARTIMENTO, VAI DECREMENTANDO -1kg EM QUALQUER CARGA
    while sum(cd) > pesoDianteiro:
        i = random.randint(0, 3)
        if cd[i] != 0:
            cd[i] -= 1

    while sum(cc) > pesoCentro:
        i = random.randint(0, 3)
        if cc[i] != 0:
            cc[i] -= 1
    
    while sum(ct) > pesoTraseiro:
        i = random.randint(0, 3)
        if ct[i] != 0:
            ct[i] -= 1

    # # Inicialmente, cria valores aleatorios limitados à capacidade de cada compartimento
    # cd = np.random.randint(low=0, high=pesoDianteiro, size=4).tolist()
    # cc = np.random.randint(low=0, high=pesoCentro, size=4).tolist()
    # ct = np.random.randint(low=0, high=pesoTraseiro, size=4).tolist()

    # # Verifica os valores, se extrapolar o Peso ou o Espaço dos compartimentos, então gere novos valores.
    # # Então, o algoritmo genético não vai punir soluções por extrapolar algum valor (não vai existir).
    # breakLoop = False
    # while not breakLoop:
    #     breakLoop = True # Se não entrar em nenhuma das condicionais, o loop será quebrado
        
    #     # Compartimento dianteiro
    #     if (sum(cd) > pesoDianteiro) or ((cd[0]*0.48 + cd[1]*0.65 + cd[2]*0.58 + cd[3]*0.39) > tamDianteiro):
    #         cd = np.random.randint(low=0, high=pesoDianteiro, size=4).tolist()
    #         breakLoop = False

    #     # Compartimento Central
    #     if (sum(cc) > pesoCentro) or ((cc[0]*0.48 + cc[1]*0.65 + cc[2]*0.58 + cc[3]*0.39) > tamCentro):
    #         cc = np.random.randint(low=0, high=pesoCentro, size=4).tolist()
    #         breakLoop = False

    #     # Compartimento Traseiro
    #     if (sum(ct) > pesoTraseiro) or ((ct[0]*0.48 + ct[1]*0.65 + ct[2]*0.58 + ct[3]*0.39) > tamTraseiro):
    #         ct = np.random.randint(low=0, high=pesoTraseiro, size=4).tolist()
    #         breakLoop = False

    # [cd1, cc1, ct1, cd2, cc2, ct2, cd3, cc3, ct3, cd4, cc4, ct4]
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

    # VALOR DAS CARGAS POR KG
    vpc1 = 0.31  # R$ 310/t
    vpc2 = 0.38  # R$ 380/t
    vpc3 = 0.35  # R$ 350/t
    vpc4 = 0.285 # R$ 285/t
    
    # TOTAL DA CARGA n DENTRO DO AVIAO
    somaCarga1 = (cd1 + cc1 + ct1)
    somaCarga2 = (cd2 + cc2 + ct2)
    somaCarga3 = (cd3 + cc3 + ct3)
    somaCarga4 = (cd4 + cc4 + ct4)

    # TOTAL DE PESO EM CADA COMPARTIMENTO
    somaPesoDianteira = (cd1 + cd2 + cd3 + cd4)
    somaPesoCentral = (cc1 + cc2 + cc3 + cc4)
    somaPesoTraseira = (ct1 + ct2 + ct3 + ct4)

    # TOTAL DE VOLUME EM CADA COMPARTIMENTO 
    somaVolumeDianteiro = (cd1*0.48 + cd2*0.65 + cd3*0.58 + cd4*0.39)
    somaVolumeCentral = (cc1*0.48 + cc2*0.65 + cc3*0.58 + cc4*0.39)
    somaVolumeTraseiro = (ct1*0.48 + ct2*0.65 + ct3*0.58 + ct4*0.39)

    # LIMITES DO AVIAO
    pesoMax = 34000
    volumeMax = 20800

    # 13000: Estimativa empirica de valor superior
    fit = float((somaCarga1*vpc1 + somaCarga2*vpc2 + somaCarga3*vpc3 + somaCarga4*vpc4) / 13000)

    # PENALIZAÇÕES
    qtdH = 15
    
    # PENALIZAÇÃO QUANTO AO PESO DAS CARGAS
    h1 = np.maximum(0, float(somaCarga1 - 18000)) / (18000/qtdH)
    h2 = np.maximum(0, float(somaCarga2 - 15000)) / (15000/qtdH)
    h3 = np.maximum(0, float(somaCarga3 - 23000)) / (23000/qtdH)
    h4 = np.maximum(0, float(somaCarga4 - 12000)) / (12000/qtdH)

    # PENALIZAÇÃO QUANTO AO PESO DOS COMPARTIMENTOS DO AVIAO
    h5 = np.maximum(0, float(somaPesoDianteira - 10000)) / (10000/qtdH)
    h6 = np.maximum(0, float(somaPesoCentral - 16000)) / (16000/qtdH)
    h7 = np.maximum(0, float(somaPesoTraseira - 8000)) / (8000/qtdH)

    # PENALIZAÇÕES QUANTO AO VOLUME DOS COMPARTIMENTOS DO AVIAO
    h8 = np.maximum(0, float(cd1*0.48 + cd2*0.65 + cd3*0.58 + cd4*0.39)-6800) / (6800/qtdH)
    h9 = np.maximum(0, float(cc1*0.48 + cc2*0.65 + cc3*0.58 + cc4*0.39)-8700) / (8700/qtdH)
    h10 = np.maximum(0, float(ct1*0.48 + ct2*0.65 + ct3*0.58 + ct4*0.39)-5300) / (5300/qtdH)

    # PENALIZAÇÕES QUANTO A PROPORÇÃO DE CADA COMPARTIMENTO DO AVIAO
    h11 = np.maximum(0, float(((somaPesoDianteira / totalCargas) - (10000/pesoMax))) / ((10000/pesoMax)/qtdH))
    h12 = np.maximum(0, float(((somaPesoCentral / totalCargas) - (16000/pesoMax))) / ((16000/pesoMax)/qtdH))
    h13 = np.maximum(0, float(((somaPesoTraseira / totalCargas) - (8000/pesoMax))) / ((8000/pesoMax)/qtdH))

    # PENALIZAÇÕES QUANTO AOS LIMITES DO AVIAO
    h14 = np.maximum(0, float((somaPesoDianteira+somaPesoCentral+somaPesoTraseira) - pesoMax)) / (pesoMax/qtdH)
    h15 = np.maximum(0, float((somaVolumeDianteiro+somaVolumeCentral+somaVolumeTraseiro)) - volumeMax) / (volumeMax/qtdH)

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
    print("PesoCarga1(kg): ", cd1, " - ", cc1, " - ", ct1)
    print("PesoCarga2(kg): ", cd2, " - ", cc2, " - ", ct2)
    print("PesoCarga3(kg): ", cd3, " - ", cc3, " - ", ct3)
    print("PesoCarga4(kg): ", cd4, " - ", cc4, " - ", ct4)
    lucro = ((cd1+cc1+ct1)*0.31 + (cd2+cc2+ct2)*0.38 + (cd3+cc3+ct3)*0.35 + (cd4+cc4+ct4)*0.285)
    print(f"Lucro(R$): {lucro}")

    # TOTAL DE PESO EM CADA COMPARTIMENTO DO AVIAO
    somaDianteira = (cd1 + cd2 + cd3 + cd4)
    somaCentral = (cc1 + cc2 + cc3 + cc4)
    somaTraseira = (ct1 + ct2 + ct3 + ct4)
    total = somaDianteira+somaCentral+somaTraseira
    print("PesoTotal(kg): ", total)

    # VERIFICAÇÃO DOS PESOS
    if somaDianteira > 10000:
        print(f"Peso dianteiro excedido: {somaDianteira}")
    if somaCentral > 16000:
        print(f"Peso central excedido: {somaCentral}")
    if somaTraseira > 8000:
        print(f"Peso traseiro excedido: {somaTraseira}")
    
    # VERIFICAÇÃO DOS METROS CUBICOS
    if (cd1*0.48 + cd2*0.65 + cd3*0.58 + cd4*0.39) > 6800:
        print(f"espaço dianteiro excedido: {cd1*0.48 + cd2*0.65 + cd3*0.58 + cd4*0.39}")
    if (cc1*0.48 + cc2*0.65 + cc3*0.58 + cc4*0.39) > 8700:
        print(f"espaço central excedido: {cc1*0.48 + cc2*0.65 + cc3*0.58 + cc4*0.39}")
    if (ct1*0.48 + ct2*0.65 + ct3*0.58 + ct4*0.39) > 5300:
        print(f"espaço traseiro excedido: {ct1*0.48 + ct2*0.65 + ct3*0.58 + ct4*0.39}")
 
    # VERIFICAÇÃO DE PROPORÇÃO, USEI A MESMA LÓGICA DA TABELA
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
                          pop_size=7500, # tamanho da populacao a cada geração
                          maximize=True, #True: maximização, False: minimização
                          bounder=ec.Bounder(0, 16000), # limites minimos e maximos dos genes (maior capacidade do avião é 16t)
                          max_generations=15000, # maximo de gerações
                          num_inputs=12, # numero de genes no cromossomo (3 compartimentos * 4 cargas)
                          crossover_rate=0.2, # taxa de cruzamento
                          mutation_rate=0.2, # taxa de mutação
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