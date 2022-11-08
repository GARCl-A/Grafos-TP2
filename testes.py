# Imports
from grafos import Grafo
import time
import random

 
#Grafo a ser analisado: 
grafo_atual = 'grafo_W_1_1' 

grafo = Grafo(tipo_grafo="lista", peso=True, txt=f'{grafo_atual}.txt').grafo

###QUESTAO 1

print('DistânciaHeap10 :\n')
print(f'20: {grafo.distanciaHeap(10, 20)}')
print(f'30: {grafo.distanciaHeap(10, 30)}')
print(f'40: {grafo.distanciaHeap(10, 40)}')
print(f'50: {grafo.distanciaHeap(10, 50)}')
print(f'60: {grafo.distanciaHeap(10, 60)}')

print('DistânciaVetor10 :\n')
print(f'20: {grafo.distanciaVetor(10, 20)}')
print(f'30: {grafo.distanciaVetor(10, 30)}')
print(f'40: {grafo.distanciaVetor(10, 40)}')
print(f'50: {grafo.distanciaVetor(10, 50)}')
print(f'60: {grafo.distanciaVetor(10, 60)}')


#QUESTAO 2
arquivo = open(f'tempo{grafo_atual}.txt','w')
arquivo.writelines('passo,vertice,Heap,Vetor\n')
tempo_heap = 0
tempo_vetor = 0
for i in range(100):
    vertice = random.randint(1,grafo._vertices)
  
    inicio_heap = time.time()
    grafo.DijkstraHeap(vertice)
    fim_heap = time.time()

    inicio_vetor = time.time()
    grafo.DijkstraVetor(vertice)
    fim_vetor = time.time()

    tempo_heap += fim_heap - inicio_heap
    tempo_vetor += fim_vetor - inicio_vetor

    arquivo.writelines(
        f'{i},{vertice},{fim_heap - inicio_heap},{fim_vetor - inicio_vetor}\n'
        )
    print({i})


print(f'Tempo médio de Heap = {tempo_heap/100} segundos')
print(f'Tempo médio de Vetor = {tempo_vetor/100} segundos')
arquivo.close()

###QUESTAO 3
print(grafo.prim(10, 'prim3.txt'))

#QUESTAO 4
##print('Dijkstra-Turing :\n')
##print(f'{grafo.distanciaHeap(2722, 11365)}')
##print('Dijkstra-Kruskal :\n')
##print(f'{grafo.distanciaHeap(2722, 471365)}')
##print('Dijkstra-Kleinberg :\n')
##print(f'{grafo.distanciaHeap(2722, 5709)}')
##print('Dijkstra-Tardos :\n')
##print(f'{grafo.distanciaHeap(2722, 11386)}')
##print('Dijkstra-Ratton :\n')
##print(f'{grafo.distanciaHeap(2722, 343930)}')

#QUESTAO 5
##print('Dijkstra-Turing :\n')
##print(f'{grafo.caminho_minimo(2722, 11365)}')
##print('Dijkstra-Kruskal :\n')
##print(f'{grafo.caminho_minimo(2722, 471365)}')
##print('Dijkstra-Kleinberg :\n')
##print(f'{grafo.caminho_minimo(2722, 5709)}')
##print('Dijkstra-Tardos :\n')
##print(f'{grafo.caminho_minimo(2722, 11386)}')
##print('Dijkstra-Ratton :\n')
##print(f'{grafo.caminho_minimo(2722, 343930)}')
