"""
EXERCICIO 1

Recebe um estado (no estilo '_23541687') 
e retorna uma lista com tuplas com ação e estado atingido, 
por exemplo: [(abaixo,“2435_1687”),  (direita,“23_541687”)]

In: _23541687
Out: [(abaixo,“523_41687”),  (direita,“2_3541687”)]

In: 23541687_
Out: [(cima,“23541_876”),  (esquerda,“2354168_7”)]

In: 2354_1687
Out: [(acima,“2_5431687”),  (direita,“23541_687”),  (abaixo,“2354816_7”),  (esquerda,“235_41687”)]

"""

ACAO_CIMA = "acima"
ACAO_ABAIXO = "abaixo"
ACAO_ESQUERDA = "esquerda"
ACAO_DIREITA = "direita"

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

print(sucessor("2354_1687"))

"""
EXERCICIO 2
"""
class Nodo():

    def __init__(self, estado, pai, acao, custo):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

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
