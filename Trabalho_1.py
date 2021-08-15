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