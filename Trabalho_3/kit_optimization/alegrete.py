import numpy as np

def compute_mse(theta_0, theta_1, data):
    """
    Calcula o erro quadratico medio
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    total_elements = data.shape[0]

    mse_Dividend = lambda x,y : ((theta_0 + theta_1*x) - y)**2
    mse_Dividend_Array = mse_Dividend(data[:,0],data[:,1])

    mse = (1.0/total_elements) * sum(mse_Dividend_Array)

    return mse

# degree é o grau do valor do x que multiplica a diferenca entre y obtido e o real
# para theta_0 o degree eh 0 para theta_1 o degree eh 1
def calc_grad(degree, theta_0, theta_1, data):
    total_elements = data.shape[0]

    grad_Dividend = lambda x,y : ((theta_0 + theta_1*x) - y)*(x**degree)
    grad_Dividend_Array = grad_Dividend(data[:,0],data[:,1])

    return (2.0/total_elements) * sum(grad_Dividend_Array)


def step_gradient(theta_0, theta_1, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de theta_0 e theta_1.
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de theta_0 e theta_1, respectivamente
    """
    new_tetha_0 = theta_0 - alpha*calc_grad(0,theta_0, theta_1, data)
    new_tetha_1 = theta_1 - alpha*calc_grad(1,theta_0, theta_1, data)

    return new_tetha_0,new_tetha_1


def fit(data, theta_0, theta_1, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de theta_0 e theta_1.
    Ao final, retorna duas listas, uma com os theta_0 e outra com os theta_1
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os theta_0 e outra com os theta_1 obtidos ao longo da execução
    """
    tetha_0_list = list()
    tetha_1_list = list()

    actual_tetha_0 = theta_0
    actual_tetha_1 = theta_1    

    for i in range(num_iterations):
        actual_tetha_0, actual_tetha_1 = step_gradient(actual_tetha_0,actual_tetha_1,data,alpha)

        tetha_0_list.append(actual_tetha_0)
        tetha_1_list.append(actual_tetha_1)

    return tetha_0_list, tetha_1_list
