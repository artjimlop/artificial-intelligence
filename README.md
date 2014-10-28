artificial-intelligence
=======================

Solution of an Artificial Intelligence problem by using a genetic algorithm based on elite and randomness. Made by @artjimlop and @antleocar.

--- GOOGLE TRANSLATE

Finding the best set of rules to classify a training set
It is a difficult task. In this paper the implementacióon Python calls a genetic algorithm that returns the best set of rules obtained after applying the algorithm. To do this, the student must take the system representacióon and crossover operators and mutation especicados in [1] with the following considerations:
Just consider databases with discrete (or discretized) values.
Not consider attributes with numerical values??.
A chromosome representing a set of rules.
Unlike the basic model seen in class, the chromosomes of a population
may have different length according to the number of rules shown. If a rule is represented by n bits (0 or 1) representing a chromosome rules shall length k * n k.
To simplify the work, we will only consider learning problems where
clasicacion has only two possible values ??(as in Table 1) and use the
hypothesis closed to represent the set of rules the world. Therefore, to
Unlike [1], we will not use one bit to represent clasicacion.

[1] Kenneth A. De Jong, William M. Spears, and Diana F. Gordon. Using genetic algo-
rithms for concept learning.
Machine Learning, 13: 161 {188, 1993}

--- Español

Encontrar el mejor conjunto de reglas que clasifique un conjunto de entrenamiento
es una tarea difícil. En el presente trabajo se pide la implementacióon en Python de un algoritmo genético que devuelva el mejor conjunto de reglas obtenido tras la aplicación del algoritmo. Para ello, el alumno debe tomar el sistema de representacióon y los operadores de cruce y mutacion especicados en [1] con las siguientes consideraciones:
Solo consideraremos bases de datos con valores discretos (o discretizados). 
No consideraremos atributos con valores numericos.
Un cromosoma representara un conjunto de reglas.
A diferencia del modelo basico visto en clase, los cromosomas de una poblacion
pueden tener longitud diferente, segun el numero de reglas representado. Si una regla se representa por n bits (0 o 1) un cromosoma que represente k reglas tendra longitud k*n.
Para simplicar el trabajo, solo consideraremos problemas de aprendizaje donde la clasicacion solo tiene dos posibles valores (como en el Cuadro 1) y usaremos la hipotesis del mundo cerrado para representar el conjunto de reglas. Por tanto, a
diferencia de [1], no usaremos un bit para representar la clasicacion.

[1] Kenneth A. De Jong, William M. Spears, and Diana F. Gordon. Using genetic algo-
rithms for concept learning.
Machine Learning, 13:161{188, 1993}