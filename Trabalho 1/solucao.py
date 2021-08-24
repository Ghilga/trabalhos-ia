from queue import *
import timeit
import math

ACAO_CIMA = "acima"
ACAO_ABAIXO = "abaixo"
ACAO_ESQUERDA = "esquerda"
ACAO_DIREITA = "direita"
ESTADO_FINAL = "12345678_"

"""
EXERCICIO 1
"""

def sucessor(estado):
    possiveisAcoes = []
    indiceVazio = estado.find('_')
    preencheAcoes(possiveisAcoes, indiceVazio)
    return preencheEstados(possiveisAcoes, estado, indiceVazio)

def preencheEstados(possiveisAcoes, estado, indiceVazio):
    possiveisEstados = []
    for acao in possiveisAcoes:
        if acao == ACAO_CIMA:
            possiveisEstados.append((acao, moveVazio(estado, indiceVazio, indiceVazio - 3)))
        elif acao == ACAO_ABAIXO:
            possiveisEstados.append((acao, moveVazio(estado, indiceVazio, indiceVazio + 3)))
        elif acao == ACAO_ESQUERDA:
            possiveisEstados.append((acao, moveVazio(estado, indiceVazio, indiceVazio - 1)))
        else: #acao == ACAO_DIREITA
            possiveisEstados.append((acao, moveVazio(estado, indiceVazio, indiceVazio + 1)))

    return possiveisEstados

def preencheAcoes(possiveisAcoes, indiceVazio):
    if podeMoverCima(indiceVazio):
        possiveisAcoes.append(ACAO_CIMA)
    if podeMoverBaixo(indiceVazio):
        possiveisAcoes.append(ACAO_ABAIXO)
    if podeMoverEsquerda(indiceVazio):
        possiveisAcoes.append(ACAO_ESQUERDA)
    if podeMoverDireita(indiceVazio):
        possiveisAcoes.append(ACAO_DIREITA)

def moveVazio(estado, indiceVazio, indiceDestino):
    listaEstado = list(estado)
    listaEstado[indiceVazio], listaEstado[indiceDestino] = listaEstado[indiceDestino], listaEstado[indiceVazio]
    return ''.join(listaEstado)

def podeMoverCima(indiceVazio):
    if indiceVazio > 2:  
        return True
    return False

def podeMoverBaixo(indiceVazio):
    if indiceVazio < 6:  
        return True
    return False

def podeMoverEsquerda(indiceVazio):
    if indiceVazio not in [0,3,6]:  
        return True
    return False

def podeMoverDireita(indiceVazio):
    if indiceVazio not in [2,5,8]:
        return True
    return False

"""
EXERCICIO 2
"""
class Nodo():

    def __init__(self, estado, pai, acao, custo):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
    
    def __str__(self):
        return """
        - acao: {}
        - estado: {}
        - pai: {}
        - custo: {}""".format(self.acao, self.estado, self.pai.getEstado(), self.custo)

    def getEstado(self):
        return self.estado
    
    def getPai(self):
        return self.pai

    def getAcao(self):
        return self.acao
    
    def getCusto(self):
        return self.custo
      
"""
EXERCICIO 3
"""
def expande(nodo):
    sucessores = []
    tuplasSucessores = sucessor(nodo.getEstado())
    for acao, estado in tuplasSucessores:
        sucessores.append(Nodo(
                        estado = estado,
                        acao = acao,
                        custo = nodo.getCusto() + 1,
                        pai = nodo))

    return sucessores

"""
EXERCICIO 4
"""
def insereFronteira(nodoAtual, fronteira):
    for nodo in expande(nodoAtual):
        fronteira.put(nodo)

def insereFronteiraHamming(nodoAtual, fronteira):
    for nodo in expande(nodoAtual):
        fronteira.put((distanciaHamming(nodo.getEstado()) + nodo.getCusto(), timeit.default_timer(), nodo))

def insereFronteiraManhattan(nodoAtual, fronteira):
    for nodo in expande(nodoAtual):
        fronteira.put((distanciaManhattan(nodo.getEstado()) + nodo.getCusto(), timeit.default_timer(), nodo))

def naoFoiExplorado(nodo, explorados):
    if explorados.get(nodo.getEstado()) is None:
        return True
    return False

def atualTemCustoMenor(nodoExplorado, nodoAtual):
    return nodoExplorado.getCusto() >= nodoAtual.getCusto()

def retornaCaminho(nodo, caminho):
    nodoAtual = nodo
    while nodoAtual.getPai() is not None:
        caminho.append(nodoAtual)
        nodoAtual = nodoAtual.getPai()

def distanciaHamming(estado):
    distancia = 0
    for i in range(len(estado)):
        if estado[i] != ESTADO_FINAL[i]:
            distancia += 1
    return distancia
        
def distanciaManhattan(estado):
    if estado == ESTADO_FINAL:
        return 0

    distancia = 0
    for indice, peca in enumerate(estado):
        if peca == "_":
            peca = 9
        else:
            peca = int(peca)
        distancia += abs((indice+1)%3 - peca%3) # posicao coluna
        distancia += abs(math.ceil((indice+1)/3) - math.ceil(peca/3)) # posicao linha
    return distancia

def bfs(estado):
    if estado == ESTADO_FINAL:
        return []

    solucaoEncontrada = False
    nodoInicial = Nodo(
        estado = estado,
        acao = None,
        custo = 0,
        pai = None
    )
    explorados = {}
    fronteira = Queue()
    fronteira.put(nodoInicial)
    while not solucaoEncontrada:
        if fronteira.empty():
            return None
        
        nodoAtual = fronteira.get()
        if nodoAtual.getEstado() == ESTADO_FINAL:
            caminho = []
            retornaCaminho(nodoAtual, caminho)
            return list(reversed(caminho))

        if naoFoiExplorado(nodoAtual, explorados):
            explorados[nodoAtual.getEstado()] = nodoAtual
            insereFronteira(nodoAtual, fronteira)

def dfs(estado):
    if estado == ESTADO_FINAL:
        return []

    solucaoEncontrada = False
    nodoInicial = Nodo(
        estado = estado,
        acao = None,
        custo = 0,
        pai = None
    )
    explorados = {}
    fronteira = LifoQueue()
    fronteira.put(nodoInicial)
    while not solucaoEncontrada:
        if fronteira.empty():
            return None
        
        nodoAtual = fronteira.get()
        if nodoAtual.getEstado() == ESTADO_FINAL:
            caminho = []
            retornaCaminho(nodoAtual, caminho)
            return list(reversed(caminho))

        if naoFoiExplorado(nodoAtual, explorados):
            explorados[nodoAtual.getEstado()] = nodoAtual
            insereFronteira(nodoAtual, fronteira)
        elif atualTemCustoMenor(explorados.get(nodoAtual.getEstado()), nodoAtual):
            explorados[nodoAtual.getEstado()] = nodoAtual

def astar_hamming(estado):
    if estado == ESTADO_FINAL:
        return []

    solucaoEncontrada = False
    nodoInicial = Nodo(
        estado = estado,
        acao = None,
        custo = 0,
        pai = None
    )
    explorados = {}
    fronteira = PriorityQueue()
    fronteira.put((0, timeit.default_timer(), nodoInicial))
    while not solucaoEncontrada:
        if fronteira.empty():
            return None
        
        nodoAtual = fronteira.get()[2]
        if nodoAtual.getEstado() == ESTADO_FINAL:
            caminho = []
            retornaCaminho(nodoAtual, caminho)
            return list(reversed(caminho))

        if naoFoiExplorado(nodoAtual, explorados):
            explorados[nodoAtual.getEstado()] = nodoAtual
            insereFronteiraHamming(nodoAtual, fronteira)
    
def astar_manhattan(estado):
    if estado == ESTADO_FINAL:
        return []

    solucaoEncontrada = False
    nodoInicial = Nodo(
        estado = estado,
        acao = None,
        custo = 0,
        pai = None
    )
    explorados = {}
    fronteira = PriorityQueue()
    fronteira.put((0, timeit.default_timer(), nodoInicial))
    while not solucaoEncontrada:
        if fronteira.empty():
            return None
        
        nodoAtual = fronteira.get()[2]
        if nodoAtual.getEstado() == ESTADO_FINAL:
            caminho = []
            retornaCaminho(nodoAtual, caminho)
            return list(reversed(caminho))

        if naoFoiExplorado(nodoAtual, explorados):
            explorados[nodoAtual.getEstado()] = nodoAtual
            insereFronteiraManhattan(nodoAtual, fronteira)


"""
Secao de Testes
"""
#start = timeit.default_timer()
#caminhoBfs = bfs("2_3541687")
#stop = timeit.default_timer()
#print('\n-- BFS --')
#print(f'Nós expandidos: {len(caminhoBfs)}')
#print(f'Tempo: {stop - start:.5f}')  
#print(f'Custo: {caminhoBfs[len(caminhoBfs)-1].getCusto()}')  

#start = timeit.default_timer()
#caminhoDfs = dfs("2_3541687")
#stop = timeit.default_timer()
#print('\n-- DFS --')
#print(f'Nós expandidos: {len(caminhoDfs)}')
#print(f'Tempo: {stop - start:.5f}')  
#print(f'Custo: {caminhoDfs[len(caminhoDfs)-1].getCusto()}')

#start = timeit.default_timer()
#caminhoAstarHamming = astar_hamming("2_3541687")
#stop = timeit.default_timer()
#print('\n-- A* Hamming --')
#print(f'Nós expandidos: {len(caminhoAstarHamming)}')
#print(f'Tempo: {stop - start:.5f}')  
#print(f'Custo: {caminhoAstarHamming[len(caminhoAstarHamming)-1].getCusto()}')

#start = timeit.default_timer()
#caminhoAstarManhattan = astar_manhattan("2_3541687")
#stop = timeit.default_timer()
#print('\n-- A* Manhattan --')
#print(f'Nós expandidos: {len(caminhoAstarManhattan)}')
#print(f'Tempo: {stop - start:.5f}')  
#print(f'Custo: {caminhoAstarManhattan[len(caminhoAstarManhattan)-1].getCusto()}')