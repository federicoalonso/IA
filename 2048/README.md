## 2048

### Abordaje del problema

Este problema decidimos abordarlo mediante la tecnica MiniMax, para asegurarnos garantizar el mínimo resultado posible. 

Para poder abordar el problema de esta forma, debimos analizar el problema como un problema de competencia entre 2 contrincantes, uno somos nosotros, que deseamos maximizar nuestro puntaje, el otro es el juego mismo, que buscará minimizar nuestro puntaje, hacer la jugada que menos nos favorezca, o sea, colocar un dos o un cuatro en el lugar que más nos incomode.

Por lo anteriormente dicho, nosotros seremos Max, mientras que el juego será Min.

Para poder desarrollar el algoritmo, debemos además verificar un par de cosas extra, entre ellas:

1. Saber cuándo finalizar la búsqueda.
1. Saber cómo evaluar si un estado es mejor que el otro.

Para responder la primer pregunta debemos fijarnos en 3 situaciones.

La primera es si llegamos a la profundidad deseada, a medida que buscamos en profundidad los posibles estados se van ramificando. En el caso del jugador tendremos una rama hijo por cada movimiento posible, lo que nos da como mucho 4, no está aquí el problema, el problema está en las posibilidades del juego, ya que para cada lugar disponible tiene la opción de colocar un 2 o un 4, lo que ramifica ampliamente el problema. Para evitar tanto cómputo utilizaremos además la técnica Alpha Beta Prunning, la cual explicaremos luego.

Con respecto a saber evaluar cada estado, lo haremos con la función heurística, la misma fue evolucionando con el problema para buscar la más óptima, dejaremos un log de las mejores encontradas y un resumen de los resultados de las mismas. El algoritmo irá buscando en profundidad las posibles opciones y se quedará con la que la función heurística maximice la utilidad.

### MiniMax

El funcionamiento de la técnica minimax es sencillo de explicar, se basa en que existen dos contrincantes, uno intenta maximizar las utilidades, mientras que el otro busca minimizarlas, lo que lleva a que tengamos que utilizar dos funcines, una para cada uno de ellos. 

De estas funciones se derivará el movimiento que realizará cada uno de ellos.

En pseudocódigo, la función maxi y mini se desarrolla de la siguiente manera:

```py
def function maxi(board):

    if algorithmHasEnded(board):
        return (None, heuristic_utility(board)) # Si el algoritmo finalizó devolvemos la utility que posee el board en el momento.
    
    (max_board, max_utility) = (None, -INF) # Asignamos un board nulo y una utility de menos infinito

    for child in board.children(): # Para cada uno de los posibles movimientos del jugador se abrirá una rama de estudio
        (_, utility) = mini(children) # Le damos el turno al jugador mini para que use la jugada que más nos perjudique y se siga estudiando en profundidad
        if utility > max_utility: # si esa utilidad encontrada es mejor que la que teníamos, la actualizamos y seguimos.
            (max_board, max_utility) = (children, utility)
    return (max_board, max_utility) # retornamos el board que beneficia al jugador

def function mini(board):
    (min_board, min_utility) = (None, +INF)

    if algorithmHasEnded(board):
      return (None, heuristic_utility(board)) # Si el algoritmo finalizó devolvemos la utility que posee el board en el momento.

    for child in board.children(): # Para cada uno de los posibles lugares donde se puede colocar un 2 o un 4 camos a abrir una rama y seguir estudiando en profundidad
      (_, utility) = maxi(board) # Le damos el turno al jugador maxi para que use la jugada que más le beneficie y se siga estudiando en profundidad
      if utility < min_utility:
        (min_board, min_utility) = (child, utility)

    return (min_board, min_utility) # retornamos el board que perjudica al jugador
```

Como podemos ver, son dos funciones que se llaman entre ellas de manera recursiva hasta que llegue a un fin, si no especificamos el nivel de profundidad deseado, continuarán hasta terminar, abriendo incontables cantidades de ramas, por eso se utiliza un parámetro para establecer la profundidad, dicho parámetro se irá reduciendo a medida que nos penetramos en el estudio, frenando el algoritmo al llegar a la profundidad deseada.

Para mejorar el poder de cómputo, utilizaremos además Alpha Beta Prunning, es una poda utilizada en este tipo de algoritmos para no seguir estudiando casos que no modificarán nuestro resultado, permitiéndonos mejorar la profundidad de estudio del algoritmo. Se llama de esta forma porque agrega dos parámetros extra al algoritmo, Alpha y Beta.

- Alpha es el mejor valor que la función maxi puede garantizar.

- Beta es el mejor valor que la función mini puede garantizar.

El pseudocódigo anterior nos queda de la siguiente forma:

```py
def function maxi(board, alpha, beta):

    if algorithmHasEnded(board):
        return (None, heuristic_utility(board)) 
    
    (max_board, max_utility) = (None, -INF) 

    for child in board.children():
        (_, utility) = mini(children, alpha, beta) 
        if utility > max_utility: 
            (max_board, max_utility) = (children, utility)
        if max_utility >= beta:
            break
        if max_utility > alpha:
            alpha = max_score
    return (max_board, max_utility)

def function mini(board, alpha, beta):
    (min_board, min_utility) = (None, +INF)

    if algorithmHasEnded(board):
      return (None, heuristic_utility(board))

    for child in board.children():
      (_, utility) = maxi(board) 
      if utility < min_utility:
        (min_board, min_utility) = (child, utility)
      if min_utility <= alpha:
        break
      if min_utility < beta:
        beta = min_utility

    return (min_board, min_utility)
```

El algoritmo se llama por primera vez con Alpha -INF y Beta + INF.

En la siguiente figura se muestra el ejemplo que vamos a desarrollar:

![figura1](./assets/abprunning1.PNG)

- En un principio se llama a A con Alpha y Beta con sus valores por defecto, la función maxi seleccionará al mayor entre B y C, comenzaremos con B.
- A B se le aplica la función mini, que seleccionará el mínimo entre D y E, comenzamos con D.
- En D utilizamos la función maxi, y seleccionaremos el máximo entre 3 y 5, comenzará con 3 y se quedará con el máximo entre 3 y -INF, que es 3, como Alpha era -INF, actualizará la misma a 3, para analizar la rama derecha implementará Alpha Beta Prunning.
- D se pregunta si Alpha (3) es mayor a Beta (+INF), lo cual no es verdadero, por lo que sigue analizando la rama derecha.
- D recibe el valor 5, por lo que actualiza Alpha a 5 y retorna 5 a B.
- B estaba utilizando la función mini, por lo que al recibir 5 actualiza a Beta, dejándolo con el mínimo entre 5 y +INF. mini ahora garantiza un valor de 5 o menos. Va a analizar ahora a E para averiguar si da un valor menor a 5.
- E utiliza la función maxi, y hereda los valores de Alpha (-INF) y Beta(5), E seleccionará el mayor resultado posible entre sus hijos.
- E se fija primero en su hijo izquierdo que es 6, y actualiza a Alpha desde -INF a dicho valor. Ahora se fija si le vale la pena buscar en la rama izquierda.
- Como Alpha (6) es mayor que Beta (5), E no precisa fijarse del lado derecho, ya que la función mini garantizó un valor de 5 o menos, E al encontrar un 6 sabe que mini de B no va a seguir por dicha rama, no siendo necesario seguir estudiando.
- B recibe un 6 de D y un 5 de E, por lo que envía un 5 hacia A.
- Por lo que la búsqueda nunca llegó al 9, no siendo computada dicha rama.

![figura1](./assets/abprunning2.PNG)

### Hiperparámetros

En el proyecto tenemos dos hiperparámetros base para comenzar a analizar, la profundidad y la función heurística.

#### La profundidad

Una vez conseguido un algoritmo que funcionaba (lo habíamos implementado con una profundidad de 5), decidimos con la misma función heurística cambiar la profundidad y registrar los valores obtenidos en cuanto a tiempo y cantidad de ganadas.

Obtuvimos la siguiente tabla:

| Profundidad | Ganadas de 10 | Tiempo Promedio | Tiempo Mínimo | Tiempo Máximo |
|-------------|---------|-----------------|---------------|---------------|
| 3 | 4 | 0:00:24 | 0:00:16 | 0:00:29 |
| 4 | 5 | 0:01:41 | 0:01:15 | 0:02:22 |
| 5 | 8 | 0:07:22 | 0:05:46 | 0:11:08 |

Como podemos ver, a medida que aumentamos la profundidad, el tiempo de procesamiento aumenta de forma exponencial y disminuye la efectividad del algoritmo.

Nos quedaremos con una profundidad de 5 que nos brinda una buena efectividad a costo de un tiempo de procesamiento acorde.

#### La función heurística

La función heurística es la que nos establece qué estado es mejor que otro. En un principio comenzamos con una función simple, basada en la suma del puntaje de los lugares, dividido entre la cantidad de espacios ocupados, de esta forma beneficiábamos que hubiera un gran puntaje y la mayor cantidad de espacios libres.

Obtuvimos un resultado rasonable, probamos agregar el smoothness, y se nos complicó en cuanto a la implementación del algoritmo, nos fuimos dando cuenta de errores que teníamos en el código. Una vez solucionados pudimos implementarla de forma correcta, y obtuvimos un peor resultado que la anterior.

Buscamos entonces mezclarlas y variando sus parámetros, entonces conseguimos una función mixta, que fue la que nos brindó la mayor efectividad, y fue con la que hicimos las pruebas de profundidad documentadas anteriormente.

Luego de poseer la función fuimos probando distintas funciones con una profundidad de 4, que nos permitía correrlas en un tiempo razonable como para ir probando.

Obtuvimos los siguientes resultados:

| Variante | Ganadas de 10 |
|----------|---------------|
| Mixta | 7 |
| Favorecer Smooth | 0 |
| Suma**2 / lugares vacíos | 0 | 
| Mixta + Valor por posición | 1 |
| Sólo favorecer posición | 0 |

Como resultado obtuvimos que tanto el smoothnes como la suma de valores en conjunto nos brindan los mejores parámetros de rendimiento.

### Referencias

El código implementado y el análsis teórico fue desarrollado en base a lo dado en clase y a varios artículos encontrados en internet, los más relevantes son los siguientes:

https://towardsdatascience.com/playing-2048-with-minimax-algorithm-1-d214b136bffb
https://towardsdatascience.com/how-to-represent-the-game-state-of-2048-a1518c9775eb
https://towardsdatascience.com/how-to-control-the-game-board-of-2048-ec2793db3fa9

https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/