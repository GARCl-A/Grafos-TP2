from grafos import GrafoLista as Grafo

teste = Grafo('teste.txt')
print(teste.DijkstraVetor(5))
print(teste.distancia(5,4,1,0))
print(teste.caminho_minimo(5,4,1,0))
print(teste.arvore_geradora(5,1,0,'arvore.txt'))