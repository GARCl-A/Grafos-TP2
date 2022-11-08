import numpy as np
import math, heapdict, random, itertools

class Grafo():
    def __init__(self, tipo_grafo, peso, txt):
        if tipo_grafo == "matriz":
            self.grafo = GrafoMatriz(txt)
            if peso == True:
                print("Grafo com matriz apena para grafo sem peso")
                self.grafo = GrafoLista(peso, txt)
        if tipo_grafo =="lista":
            self.grafo = GrafoLista(peso, txt)
            
#Legado do TP1, não possui nenhuma alteração para o TP2              
class GrafoMatriz():
   
    def __init__(self,txt):
        arquivo = open(txt, 'r')
        
        self._vertices = int(arquivo.readline())         #Total de vertices
        self._arestas = 0
        self._matriz = np.zeros([self._vertices, self._vertices], dtype = int)
        #A matriz começa em 0, portanto os vértices serão representados na matriz com a posição "Vértice - 1"
        for linha in arquivo: #Criar Matrizes
            split = linha.split()
            self._matriz[int(linha.split()[0])-1][int(linha.split()[1])-1] = 1
            self._matriz[int(linha.split()[1])-1][int(linha.split()[0])-1] = 1 
            self._arestas += 1 #Total de arestas
        
        arquivo.close()
            
    def vertices(self):
        return self._vertices
    
    def arestas(self):
        return self._arestas
    
    def grau_max(self):
        soma = np.sum(self._matriz, axis= 0)
        grau_max = np.argmax(soma)
        return soma[grau_max]
    
    def grau_min(self):
        soma = np.sum(self._matriz, axis= 0)
        grau_min = np.argmin(soma)
        return soma[grau_min]

    def grau_med(self):
        soma = np.sum(self._matriz, axis= 0)
        soma2 = np.sum(soma, axis= 0)
        grau_med = soma2/self.vertices
        return grau_med
    
    def grau_median(self):
        soma = np.sum(self._matriz, axis= 0)
        grau_median = np.median(soma)
        return int(grau_median)
            
    def busca_largura(self,raiz,nome_arquivo,print):
        vetor_marcacao = np.zeros(self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vetor_graus = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vetor_pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        fila_execucao = []
        vetor_marcacao[raiz-1] = 1
        vetor_pais[raiz-1] = 0
        vetor_graus[raiz-1] = 0
        fila_execucao.append(raiz)
        while fila_execucao != []:
            pai = fila_execucao.pop(0)
            vizinhos = self.retorna_vizinhos(pai)
            for w in vizinhos:
                if vetor_marcacao[w-1] == 0:
                    vetor_marcacao[w-1] = 1
                    vetor_pais[w-1] = pai
                    vetor_graus[w-1] = vetor_graus[pai-1] + 1 
                    fila_execucao.append(w) 

        if print == 1:          
            self.escrever_busca(nome_arquivo, vetor_graus, vetor_pais)
        # -1 = fora da componente conexa; 0 = raiz ; >= 1 = valor do vértice pai
        return [vetor_pais,vetor_graus]
        
    def retorna_vizinhos(self,vertice):
        vizinhos = []
        linha_vertice = self._matriz[vertice - 1]
        indice = 1
        for i in linha_vertice:
            if i == 1:
                vizinhos.append(indice)
            indice += 1
        return vizinhos

    def busca_profundidade(self,raiz,nome_arquivo, print):
        vetor_marcacao = np.zeros(self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        pilha_execucao = [raiz]
        vetor_graus = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vetor_pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vetor_pais[raiz-1] = 0
        vetor_graus[raiz-1] = 0
        while pilha_execucao != []:
            pai = pilha_execucao.pop(-1)
            if vetor_marcacao[pai-1] == 0:
                vetor_marcacao[pai-1] = 1
                vizinhos = self.retorna_vizinhos(pai)
                for w in reversed(vizinhos):
                    pilha_execucao.append(w)
                    if vetor_marcacao[w-1] == 0:
                        vetor_pais[w-1] = pai
                        vetor_graus[w-1] = vetor_graus[pai-1] + 1
        if print == 1:
            self.escrever_busca(nome_arquivo, vetor_graus, vetor_pais)
        
        return vetor_pais # -1 = fora da componente conexa; 0 = raiz ; >= 1 = valor do vértice pai

    def escrever_busca(self, nome_arquivo, vetor_graus, vetor_pais):
        arquivo = open(nome_arquivo, 'w', encoding = "utf-8")
        escrita = ''
        for v in range(self._vertices):
            escrita += f'Vértice: {v+1} - Nivel: {vetor_graus[v]}\n'
        escrita +=  '\nVetor de pais: \n'
        escrita += f' {str(list(range(1,self._vertices + 1))).replace(", ","  ")[1:-1]}\n'
        escrita += str(vetor_pais)[1:-1]
        arquivo.write('Se o Nivel é -1 o vértice fora da componente conexa\n\n'+f'{escrita}')
        arquivo.close()
          
    def distancia(self,partida, chegada):
        vetor_pais = self.busca_largura(partida,'dump.txt',0)[0]

        atual = chegada
        distancia = 0
        while atual != partida:
            atual = vetor_pais[atual - 1]
            if atual == -1:
                return atual
            distancia += 1
        return distancia

    def diametro(self):
        diametro = 0
        lista_pares = itertools.combinations(list(range(self._vertices)), 2)
        for x,y in lista_pares:
            distancia = self.distancia(x,y)
            if distancia > diametro:
                diametro = distancia
        return diametro
    
    def componentes_conexas(self, nome_arquivo):
        componentes_conexas = []
        vetor_pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        
        vetor_pais[0] = 0
        for i in range(1, self._vertices + 1):
            if vetor_pais[i-1] == -1:
                pilha_execucao = [i]
                vetor_marcacao = np.zeros(self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
                while pilha_execucao != []:
                    pai = pilha_execucao.pop(-1)
                    if vetor_marcacao[pai-1] == 0:
                        vetor_marcacao[pai-1] = 1
                        vizinhos = self.retorna_vizinhos(pai)
                        for w in reversed(vizinhos):
                            pilha_execucao.append(w)
                            if vetor_marcacao[w-1] == 0:
                                vetor_pais[w-1] = pai
                componentes_conexas.append(vetor_marcacao)

        self.escrever_componentes(nome_arquivo, componentes_conexas)

    def escrever_componentes(self, nome_arquivo, componentes):
        arquivo = open(nome_arquivo, 'w', encoding = "utf-8")
        arquivo.write(f'Total de componentes conexas:{len(componentes)}\n\n')

        tratadas = []
        for componente in componentes:
            lista_vertices = []
            for i in range(len(componente)):
                if componente[i] == 1:
                    lista_vertices.append(i + 1)
            tratadas.append(lista_vertices)
        
        tratadas = sorted(tratadas, key = lambda x: len(x), reverse= True)
        for i in tratadas:
            arquivo.writelines(f'Tamanho da componente: {len(i)} - Vértices: {i}\n')
        arquivo.close()

class ListaVizinhos:
    #Cada lista dessa classe representa a lista de vizinhos de um vértice
    #Cada lista dessas será um elemento do vetor de vértices da lista de adjacência
    def __init__(self):
        self.head = None
        self.size = 0
    def add(self, vizinho):
        vizinho.proximo = self.head
        self.head = vizinho
        self.size += 1
        
class Vizinho:
    #Cada vizinho dessa classe será um nó da lista de vizinhos
    def __init__(self, vizinho: int, peso: int):
        self.vizinho = vizinho
        self.peso = peso
        self.proximo = None
    def __repr__(self):
        return (str(self.peso))
    
class GrafoLista():
    def __init__(self, peso:bool, txt:str):
        arquivo = open(txt, 'r')
        self._vertices = int(arquivo.readline())         #Total de vertices
        self._arestas = 0
        self._vetor = []
        self._negativo = False
        self._peso = peso
        for vertice in range(self._vertices):    #Inicializando as listas
            self._vetor.append(ListaVizinhos())
        if self._peso == True:
            for linha in arquivo:   #Adicionando vizinhos às listas
                split = linha.split()
            
                vertice1 = int(linha.split()[1])
                vertice2 = int(linha.split()[0])
                peso_aresta = float(linha.split()[2])

                if peso_aresta < 0:
                    self._negativo = True
                
                self._vetor[int(linha.split()[0])-1].add(Vizinho(vertice1, peso_aresta))
                self._vetor[int(linha.split()[1])-1].add(Vizinho(vertice2, peso_aresta))
                self._arestas += 1 #Total de arestas
        else:
            for linha in arquivo:   #Adicionando vizinhos às listas
                split = linha.split()
                self._vetor[int(linha.split()[0])-1].add(Vizinho(int(linha.split()[1]),0))
                self._vetor[int(linha.split()[1])-1].add(Vizinho(int(linha.split()[0]),0))
                self._arestas += 1 #Total de arestas
            
        arquivo.close

    #Legado do TP1
    def vertices(self):
        return self._vertices
    
    #Legado do TP1
    def arestas(self):
        return self._arestas
    
    #Legado do TP1
    def graus(self):
        graus = np.zeros(self._vertices, dtype = int)
        vertice = 0
        for lista in self._vetor:
            graus[vertice] = lista.size
            vertice+=1
        return graus

    #Legado do TP1
    def grau_max(self):
        graus = self.graus()
        return graus.max()
    
    #Legado do TP1
    def grau_min(self):
        graus = self.graus()
        return graus.min()

    #Legado do TP1
    def grau_med(self):
        graus = self.graus()
        return graus.mean()
    
    #Legado do TP1
    def grau_median(self):
        graus = self.graus()
        mediana = np.median(graus, axis=0)
        return int(mediana)

    #Legado do TP1
    def busca_largura(self,raiz,nome_arquivo, print):
        vetor_marcacao = np.zeros(self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vetor_graus = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vetor_pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        fila_execucao = [raiz]
        vetor_marcacao[raiz-1] = 1
        vetor_pais[raiz-1] = 0
        vetor_graus[raiz-1] = 0
        while fila_execucao != []:
            pai = fila_execucao.pop(0)
            lista_vertice = self._vetor[pai - 1]
            proximo_vizinho = lista_vertice.head
            while proximo_vizinho != None:
                w = proximo_vizinho.vizinho
                if vetor_marcacao[w-1] == 0:
                    vetor_marcacao[w-1] = 1
                    vetor_pais[w-1] = pai
                    vetor_graus[w-1] = vetor_graus[pai-1] + 1 
                    fila_execucao.append(w)
                proximo_vizinho = proximo_vizinho.proximo

        if print == 1:            
            self.escrever_busca(nome_arquivo, vetor_graus, vetor_pais)
        # -1 = fora da componente conexa; 0 = raiz ; >= 1 = valor do vértice pai
        return [vetor_pais,vetor_graus] 

    #Legado do TP1    
    def busca_profundidade(self,raiz,nome_arquivo, print):
        vetor_marcacao = np.zeros(self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        pilha_execucao = [raiz]
        vetor_graus = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vetor_pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vetor_pais[raiz-1] = 0
        vetor_graus[raiz-1] = 0
        while pilha_execucao != []:
            pai = pilha_execucao.pop(-1)
            if vetor_marcacao[pai-1] == 0:
                vetor_marcacao[pai-1] = 1
                lista_vertice = self._vetor[pai - 1]
                proximo_vizinho = lista_vertice.head 
                while proximo_vizinho != None:
                    w = proximo_vizinho.vizinho
                    pilha_execucao.append(w)
                    if vetor_marcacao[w-1] == 0:
                        vetor_pais[w-1] = pai
                        vetor_graus[w-1] = vetor_graus[pai-1] + 1
                    proximo_vizinho = proximo_vizinho.proximo

        if print == 1:
            self.escrever_busca(nome_arquivo, vetor_graus, vetor_pais)
        
        return vetor_pais # -1 = fora da componente conexa; 0 = raiz ; >= 1 = valor do vértice pai
    
    #Legado do TP1
    def escrever_busca(self, nome_arquivo, vetor_graus, vetor_pais):
        arquivo = open(nome_arquivo, 'w', encoding = "utf-8")
        escrita = ''
        for v in range(self._vertices):
            escrita += f'Vértice: {v+1} - Nivel: {vetor_graus[v]}\n'
        escrita +=  '\nVetor de pais: \n'
        escrita += f' {str(list(range(1,self._vertices + 1))).replace(", ","  ")[1:-1]}\n'
        escrita += str(vetor_pais)[1:-1]
        arquivo.write('Se o Nivel é -1 o vértice fora da componente conexa\n\n'+f'{escrita}')
        arquivo.close()
           
    #Legado do TP1
    def componentes_conexas(self, nome_arquivo):
        componentes_conexas = []
        vetor_pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        
        vetor_pais[0] = 0
        for i in range(1, self._vertices + 1):
            if vetor_pais[i-1] == -1:
                pilha_execucao = [i]
                vetor_marcacao = np.zeros(self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
                while pilha_execucao != []:
                    pai = pilha_execucao.pop(-1)
                    if vetor_marcacao[pai-1] == 0:
                        vetor_marcacao[pai-1] = 1
                        lista_vertice = self._vetor[pai - 1]
                        proximo_vizinho = lista_vertice.head 
                        while proximo_vizinho != None:
                            w = proximo_vizinho.vizinho
                            pilha_execucao.append(w)
                            if vetor_marcacao[w-1] == 0:
                                vetor_pais[w-1] = pai
                            proximo_vizinho = proximo_vizinho.proximo
                componentes_conexas.append(vetor_marcacao)

        self.escrever_componentes(nome_arquivo, componentes_conexas)

        return componentes_conexas

    #Legado do TP1
    def escrever_componentes(self, nome_arquivo, componentes):
        arquivo = open(nome_arquivo, 'w', encoding = "utf-8")
        arquivo.write(f'Total de componentes conexas:{len(componentes)}\n\n')

        tratadas = []
        for componente in componentes:
            lista_vertices = []
            for i in range(len(componente)):
                if componente[i] == 1:
                    lista_vertices.append(i + 1)
            tratadas.append(lista_vertices)
        
        tratadas = sorted(tratadas, key = lambda x: len(x), reverse= True)
        for i in tratadas:
            arquivo.writelines(f'Tamanho da componente: {len(i)} - Vértices: {i}\n')
        arquivo.close()

    #Legado do TP1   
    def diametro(self) -> float:
        if self._vertices < 1000:
            diametro = 0
            for linha in range(self._vertices):
                vetor_graus = self.busca_largura(linha+1,'dump.txt',0)[1] #Lembrando novamente que o vertice X estará na posição X-1
                maior=np.max(vetor_graus)
                if maior > diametro:
                    diametro = maior
        else: #Aproximação para grafos grandes.
            diametro = 0
            for i in range(1500):
                vertice = random.randint(1, self._vertices)
                print(vertice)
                vetor_graus = self.busca_largura(vertice, 'dump.txt',0)[1] 
                maior=np.max(vetor_graus)
                if maior > diametro:
                    diametro = maior
                
        return diametro
    
    def DijkstraVetor(self, vertice: int):
        matriz = []  #[:][0] -> distancias, [:][1] -> vertice
        for i in range(self.vertices()):
            matriz.append([np.inf, i+1, 0])

        pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vertices = self._vertices
        matriz[vertice-1][0] = 0
        fila = self.cria_fila(matriz)
        while fila != []:
            minimo = self.get_minimo(fila)
            if minimo == None:
                break
            matriz[minimo - 1][2] = 1
            proximo_vizinho = self._vetor[minimo-1].head
            while proximo_vizinho != None:
                vertice_atual = proximo_vizinho.vizinho
                peso_atual = proximo_vizinho.peso
                if matriz[vertice_atual-1][0] > matriz[minimo-1][0] + peso_atual: #Quando há alteração na distância dos vértices
                    matriz[vertice_atual-1][0] = matriz[minimo-1][0] + peso_atual
                    pais[vertice_atual-1] = minimo
                    fila = self.cria_fila(matriz)
                proximo_vizinho = proximo_vizinho.proximo
        
        distancia = self.get_distancias(matriz)
        return (distancia, pais)

    def cria_fila(self,matriz):
        fila = sorted(matriz, key = lambda x: x[0])  
        return fila

    def get_minimo(self,fila):
        for i in fila:
            if i[2] == 0:
                return i[1]

    def get_distancias(self,matriz):
        distancias = []
        for i in matriz:
            distancias.append(i[0])

        return distancias

    def DijkstraHeap(self, vertice: int) -> tuple:
        distancia = np.array([np.inf] * self.vertices()) #array de infinitos.
        pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        vertices = self._vertices
        distancia[vertice-1] = 0
        menor = 0
        heap = heapdict.heapdict()
        heap[vertice] = 0 
        while menor != vertices:
            if len(heap.heap) == 0:
                break
            minimo = heap.popitem()[0] - 1
            if minimo == np.inf:
                break
            menor += 1
            proximo_vizinho = self._vetor[minimo].head
            while proximo_vizinho != None:
                vertice_atual = proximo_vizinho.vizinho
                peso_atual = proximo_vizinho.peso
                if distancia[vertice_atual-1] > distancia[minimo] + peso_atual: #Quando há alteração na distância dos vértices
                    distancia[vertice_atual-1] = distancia[minimo] + peso_atual
                    heap[vertice_atual] = distancia[minimo] + peso_atual #Um vértice só entrará na fila de execução se sua distância por reduzida
                    pais[vertice_atual-1] = minimo + 1
                proximo_vizinho = proximo_vizinho.proximo
        return (distancia, pais)
    
    def caminho_minimo(self,partida:int, chegada:int) -> list:
        if self._peso == False:
            pais = self.busca_largura(partida,'dump.txt', 0)[0]
            if pais[chegada - 1] == -1:
                return 'Não há caminho.' 
            else:
                caminho = [chegada]
                atual = chegada
                print(pais)
                while atual != partida:
                    atual = pais[atual-1]
                    caminho.append(atual)
                caminho.reverse()
                return caminho
    
        elif self._peso == True and self._negativo == False:
            pais = self.DijkstraHeap(partida)[1]
            if pais[chegada - 1] == -1:
                return 'Não há caminho.' 
            else:
                caminho = [chegada]
                atual = chegada
                print(pais)
                while atual != partida:
                    atual = pais[atual-1]
                    caminho.append(atual)
                caminho.reverse()
                return caminho

        elif self._negativo == True:
            caminho = "Grafo apresenta peso negativo." #Dijkstra não é capaz de computar distancias para grafos negativos.

    def prim(self, partida:int, txt_saida:str) -> float:
        pais = np.array([-1] * self._vertices, dtype = int) #Lembrando novamente que o vertice X estará na posição X-1
        pesos = np.array([np.inf] * self.vertices()) #array de infinitos. Isso supõe que não existam pesos infinitos no grafo
        vertices = self._vertices
        pesos[partida-1] = 0
        menor = 0
        heap = heapdict.heapdict()
        heap[partida] = 0 
        while menor != vertices:
            minimo = heap.popitem()[0] - 1
            if minimo == np.inf:
                break
            menor += 1
            proximo_vizinho = self._vetor[minimo].head
            while proximo_vizinho != None:
                vertice_atual = proximo_vizinho.vizinho
                peso_atual = proximo_vizinho.peso
                if pesos[vertice_atual-1] > peso_atual:
                    pesos[vertice_atual-1] = peso_atual
                    heap[vertice_atual] = peso_atual #Um vértice só entrará na fila de execução se sua distância for reduzida
                    pais[vertice_atual-1] = minimo + 1
                proximo_vizinho = proximo_vizinho.proximo
        peso_total = sum(pesos)
        arquivo = open(txt_saida, "w")
        for i in range(1,len(pais)+1):
            if i != partida:
                arquivo.writelines(f'{i} {pais[i-1]} {pesos[i-1]}\n')
        arquivo.close()
        return peso_total

    def distanciaHeap(self,partida:int, chegada:int) -> float:
        if self._peso == False:
            vetor_pais = self.busca_largura(partida,'dump.txt',0)[0]

            atual = chegada
            distancia = 0
            while atual != partida:
                atual = vetor_pais[atual - 1]
                if atual == -1:
                    return atual
                distancia += 1
    
        elif self._peso == True and self._negativo == False:
            #Mudar para heap quando código pronto pois é mais rápido
            distancias = self.DijkstraHeap(partida)[0]
            distancia = distancias[chegada - 1]

        elif self._negativo == True:
            distancia = "Grafo apresenta peso negativo." #Dijkstra não é capaz de computar distancias para grafos negativos.

        return distancia

    def distanciaVetor(self,partida:int, chegada:int) -> float:
        if self._peso == False:
            vetor_pais = self.busca_largura(partida,'dump.txt',0)[0]

            atual = chegada
            distancia = 0
            while atual != partida:
                atual = vetor_pais[atual - 1]
                if atual == -1:
                    return atual
                distancia += 1
    
        elif self._peso == True and self._negativo == False:
            #Mudar para heap quando código pronto pois é mais rápido
            distancias = self.DijkstraVetor(partida)[0]
            distancia = distancias[chegada - 1]

        elif self._negativo == True:
            distancia = "Grafo apresenta peso negativo." #Dijkstra não é capaz de computar distancias para grafos negativos.

        return distancia
 
