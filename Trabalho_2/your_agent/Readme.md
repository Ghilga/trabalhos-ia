# Participantes
Leonardo Augusto, 278998, Turma B

Giusepe Tessari, 282772, Turma B

Maurício Kritli, 232807, Turma A

# Bibliotecas que precisam ser instaladas

Nenhuma biblioteca adicional precisa ser instalada. Todas as bibliotecas utilizadas para implementação do trabalho são padrão no Python.

# Detalhes da Implementação

## Função de Avaliação

A função de avaliação que implementamos para o algoritmo poda alfa-beta leva em conta os seguintes pontos:
- Matriz de pesos para posição: Essa é uma estratégia de avaliação comumente utilizada para o jogo Othelo. Consiste numa matriz contendo pesos para cada posição do tabuleiro, onde posições conhecidamente melhores possuem pesos maiores.
- Vizinhança: É uma estratégia que visa calcular quantas peças estão em volta da possível posição a ser jogada e calcular duas coisas:
    - Contar o total de peças que estão em volta, independente de qual time é (quanto mais peças, melhor a posição).
    - Contar o total de peças que estão em volta, que são do inimigo (quanto mais peças do inimigo, melhor a posição).
- Corners: Essa é a condição máxima em nossa estratégia. Os corners do tabuleiro de Othelo são estratégicamente as melhores posições para se possuir uma peça. Dessa forma, caso exista uma possível jogada em um corner do tabuleiro, essa jogada é automaticamente escolhida.

Assim, caso não haja a possibilidade de uma jogada em algum dos corners, a função de avaliação opera obtendo o valor da matriz de pesos e calculando os dois valores relacionados à vizinhança mencionados acima para cada possível posição a ser jogada, e realiza uma ponderação desses valores utilizando pesos definidos pelo grupo.

## Função de Parada

Para a função de parada decidimos utilizar uma profundidade fixa de 5, a qual testamos manualmente algumas vezes e aparentou ser uma boa profundidade, tanto no resultado da jogada quanto no tempo de execução.

## Possíveis Melhorias

Possíveis melhorias poderiam ser aplicadas na função de parada, pois foi escolhido um valor fixo e sabemos que existem algoritmos mais sofisticados que calculam uma profundidade de parada otimizada. Outra possível melhoria na função de parada seria implementá-la levando em conta o tempo de execução decorrido até então.

Também poderiamos melhorar as funções de avaliação, pois os pesos de cada função foram selecionados a partir dos resultados para os testes executados, sem nenhuma prova formal de que seriam ótimos. Além disso, só testamos o algoritmo contra o agente randômico, tornando mais difícil avaliar o desempenho de cada função.

## Decisões e dificuldades de projeto

Quanto a decisão para a função de parada, optamos por utilizar um valor fixo de profundidade por acreditarmos que seria uma condição razoável e de implementação simples e direta. O valor para profundidade foi escolhido levando em conta a noção que calcular muitas jogadas em avanço pode não trazer melhorias tão significativas, visto que não é possível prever com exatidão qual será o próximo movimento do adversário.

Com relação a função de avaliação, parte dos critérios foram selecionados do "Relatorio othello" referenciado na bibliografia, mais especificamente a matriz de pesos e avaliação dos corners. A matriz de pesos é um critério comumente utilizado e efetivo para o jogo, portanto na ponderação da "qualidade" da jogada utilizamos uma constante maior para esse valor. 
Como mencionado anteriormente, o critério dos corners é uma condição máxima na nossa estratégia de avaliação, portanto se existe uma jogada a ser feita em um corner, essa jogada é selecionada.
Por fim, a condição que avalia a vizinhança foi criada pelo grupo pois acreditamos que quanto maiores o número de peças vizinhas e o número de peças do adversário na vizinhança, melhor é a jogada. Essa noção foi criada pelo grupo a partir de algumas partidas jogadas praticando Othello.

A maior dificuldade que tivemos no projeto foi na implementação da lógica da função de Minimax, mais específicamente nas funções max_value e min_value, pois a lógica dessas funções é bem complicada de se implementar, principalmente a execução da recursão. Também tivemos muitas dificuldades na transferência de parâmetros de uma função para outra, e para isso resolvemos criar uma classe GameState que guardasse alguns parâmetros mais essenciais, que simplificaram muito a implementação.

## Bibliografia

Relatorio othello: https://pt.slideshare.net/helderhp17/relatorio-othello - Acessado pela última vez em 13 de Setembro de 2021.