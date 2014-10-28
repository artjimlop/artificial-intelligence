__author__ = 'Arturo Jiménez López'
__author__ = 'Antonio León Carrillo'

import random
import itertools


# Esta clase se encarga de extraer los datos del fichero arff y de generar la población inicial.
class Reader:

    #Variables relacionadas con la carga del archivo arff
    file = None
    file_string = None
    split_file = None

    #Variables relacionadas con la búsqueda de los datos del archivo
    relation_position = None
    attributes_positions = []
    data_position = None

    #Variables relacionadas con el contenido del arff
    relation_name = None
    attributes = []
    data = []

    #Variables relacionadas con la generación de la población
    structure = []
    rule_structure = []
    initial_population = []

    #Reglas del conjunto de entrenamiento traducidas:
    arff_population = []

    #Valores positivo y negativo de la relación
    relation_class = []

    # Número de bits para representar una regla
    rule_bits = 0

    #Este boolean se pone a true cuando el atributo class esta en primera posición en lugar de en la última
    first_position = False

    #Este método carga el archivo arff y lo divide en líneas para que sea más cómodo su manejo
    def open_file(self, file_name):
        #Se abre el fichero con nombre file_name en modo lectura
        self.file = open(file_name, 'r')
        self.file_string = self.file.read()
        #Dividimos el string leído es una lista de líneas. Es decir, dividimos cuando encontramos un salto de línea
        self.split_file = self.file_string.split('\n')

    #Buscamos las posiciones en las que se encuentran los datos a leer en el arff para simplificar la lectura.
    #Lo que hacemos es buscar donde esta el nombre de la relación, los diferentes atributos que se usarán en ella y
    #a partir de donde están los datos de la relación.
    def get_positions(self):
        counter = 0
        for line in self.split_file:
            counter += 1
            if line.find('@relation') == 0:
                self.relation_position = counter
            if line.find('@attribute') == 0:
                self.attributes_positions.append(counter)
            if line.find('@data') == 0:
                self.data_position = counter

    #Con este método se carga el contenido del archivo arff.
    #Se ha decidido que los atributos con valor '?' de los arff se traduzcan como atributos con todos sus valores
    #iguales a cero. Es decir, '00', por ejemplo.
    def relation_loader(self):
        #Utilizamos el atributo de posición obtenido en get_positions para extraer el nombre de la relación
        line_relation = self.split_file[self.relation_position - 1]
        self.relation_name = line_relation[len('@relation '):]

        #Utilizamos los atributos de posiciones obtenidos en get_positions relacionados con los atributos para obtener
        #sus diferentes valores:
        #Para cada línea que tiene un atributo
        for position in self.attributes_positions:
            #Lista que englobara el nombre del atributo y sus posibles valores
            attribute_list = []
            #Posibles valores de cada atributo
            attribute_posibilities = []

            #Nos situamos en la línea
            line_attribute = self.split_file[position - 1]
            # Buscamos la posición de los caracteres "{" y "}" porque delimitan
            # los valores que pueden tomar los atributos
            first_limit = line_attribute.find('{')
            second_limit = line_attribute.find('}')
            if first_limit != -1:
                #Sacamos el nombre del atributo
                attribute_name = line_attribute[len('@attribute '):first_limit - 1]
                attribute_list.append(attribute_name)
                #Ahora buscamos sus posibles valores
                attribute_values = line_attribute[first_limit+1:second_limit]
                #Separamos el string de atributos
                attributes = attribute_values.split(",")
                #Como algunos quedan tal que " valor_del_atributo", quitamos el carácter espacio " "
                for attribute in attributes:
                    if attribute.find(" ") == 0:
                        attribute = attribute[1:]
                    #Añadimos a la lista de posibles valores del atributo
                    attribute_posibilities.append(attribute)
            else:
                first_limit = line_attribute.find('[')
                second_limit = line_attribute.find(']')
                #Sacamos el nombre del atributo
                attribute_name = line_attribute[len('@attribute '):first_limit - 1]
                attribute_list.append(attribute_name)
                #Ahora buscamos sus posibles valores
                attribute_values = line_attribute[first_limit+1:second_limit]
                #Separamos el string de atributos
                attributes = attribute_values.split(",")
                for number in range(int(attributes[0]), int(attributes[1])+1):
                    attribute_posibilities.append(number)

            #Añadimos a la lista que engloba el nombre del atributo y sus posibles valores
            attribute_list.append(attribute_posibilities)
            #Añadimos a la variable de la clase
            self.attributes.append(attribute_list)
        #Ahora utilizando el contador para los datos extraemos los mismos
        for line in self.split_file[self.data_position:]:
            #Cada cromosoma es una lista formada por genes
            chromosome = []
            #Dividimos la línea actual en diferentes elementos cada vez que nos encontramos una ","
            split_line = line.split(",")
            #Cada uno de estos elementos es un gen. Añado el gen al cromosoma. Miro antes que la línea no sea un
            #Comentario ni una línea vacía.
            if split_line[0] != "%" and split_line[0] != "":
                for gen in split_line:
                    chromosome.append(gen)
                #Este cromosoma se añade a la variable contenida en la clase.
                self.data.append(chromosome)

    #Este método indica el número de bits necesarios para codificar cada atributo
    def structure(self):
        structure_list = []
        for pair in self.attributes:
            attribute = pair[1]
            structure_list.append(attribute)
        self.rule_structure = structure_list
        #Recorremos estructura y vemos el número de elementos que puede tener en cada posición
        #Lo hacemos porque si en una posición puedes tener sunny,rain u overcast lo traduces con 3 números binarios
        lenghts = []
        for posibility in structure_list:
            length = len(posibility)
            lenghts.append(length)
        self.structure = lenghts
        return lenghts

    #Con este método se crea una población aleatoriamente:
    def generar_poblacion(self, k, n):
        lista_poblacion = []
        cromosoma = ""
        lista_final = []
        total_individuos = k*n
        #Creamos k*n reglas
        #K reglas por cromosoma
        #N número cromosomas.
        for something in range(0, total_individuos):
            lista = ""
            #Nos fijamos en la estructura que tienen las reglas del documento obviando el atributo 'Class':
            for number in range(0, len(self.structure)-1):
                attribute = self.structure[number]
                rule = ""
                #Codificamos la regla
                for index in range(0, attribute):
                    bit = random.randint(0, 1)
                    rule += str(bit)
                lista += rule
            lista_poblacion.append(lista)
        #recorremos la lista agrupando los elementos como máximo de k en k
        cont_elem = 0
        test = k-1
        if test <= 1:
            rules_by_chromosome = k
        else:
            rules_by_chromosome = random.randint(k-1, k)
        number_of_chromosomes = n
        for element in lista_poblacion:
            cromosoma += element
            cont_elem += 1
            #si el contador == k, reseteamos
            if cont_elem == rules_by_chromosome and number_of_chromosomes >= 1:
                lista_final.append(cromosoma)
                number_of_chromosomes -= 1
                cromosoma = ""
                cont_elem = 0
        self.initial_population = lista_final
        return lista_final

    #Este método traduce la población del conjunto de entrenamiento a bits
    def translate_population(self):
        rules = []
        for rule in self.data:
            rule_temp = []
            for cont in range(0, len(rule)):
                attribute = rule[cont]
                number = ""
                #Atendemos a la estructura que debe tener cada regla para traducirla
                for att in self.rule_structure[cont]:
                    if isinstance(att, int) and attribute != "?":
                        attribute = int(attribute)
                    if attribute == att:
                        number += "1"
                    else:
                        number += "0"
                rule_temp.append(number)
            rules.append(rule_temp)
        #Las reglas traducidas las almacenamos en una variable
        self.arff_population = rules
        return rules

    #Obtenemos los valores positivo y negativo de la relación
    def possitive_and_negative(self):
        att_class = self.rule_structure[len(self.rule_structure)-1]
        counter = 0
        bits_needed = len(att_class)
        for number in range(0, len(att_class)):
            self.relation_class.append(str(number))

    #Este método sirve para calcular el tamaño en bits de una regla
    def rule_lenght(self):
        rule_len = 0
        for number in range(0, len(self.structure)-1):
            rule_len += self.structure[number]
        self.rule_bits = rule_len

    #Con este método comprobamos si el atributo class se encuentra en primera posición en lugar de en la última
    def checker(self):
        copy = None
        if self.relation_name != "solar-flare":
            if 'OVERALL_DIAGNOSIS' in self.attributes[0] or 'class' in self.attributes[0] or 'Class' in self.attributes[0]:
                copy = self.attributes[0]
                del self.attributes[0]
                self.attributes.append(copy)
                self.first_position = True

    # Modificamos la posición del atributo class, modificando por tanto la posición de los atributos en la regla
    # y el atributo structure. Esto se hace sólo en los casos en que el atributo class está al inicio del fichero arff.
    def check_arff_population(self):
        if self.first_position is True:
            for rule in self.arff_population:
                copy = rule[0]
                del rule[0]
                rule.append(copy)
            structure_list = []
            #Actualizo las estructuras

            for pair in self.attributes:
                attribute = pair[1]
                structure_list.append(attribute)
            self.rule_structure = structure_list
            lenghts = []

            for posibility in structure_list:
                length = len(posibility)
                lenghts.append(length)
            self.structure = lenghts

    # Traducimos el atributo class a '0' ó '1', modificando por tanto el atributo structure
    def check_classes(self):
        for rule in self.arff_population:
            result = rule[len(rule)-1]
            if result == "10":
                del rule[-1]
                rule.append("0")
            if result == "01":
                del rule[-1]
                rule.append("1")
        del self.structure[-1]
        self.structure.append(1)

    #Estas operaciones en este orden sirven para inicializar lo necesario de la clase Reader
    def reader_initializer(self, document_to_read, k, n):
        self.open_file(document_to_read)
        self.get_positions()
        self.relation_loader()
        self.structure()
        #Checkeamos la posición de class
        self.checker()
        self.translate_population()
        #Checkeamos la poblacion traducida
        self.check_arff_population()
        self.check_classes()
        #self.translate_population()
        self.generar_poblacion(k, n)
        self.possitive_and_negative()
        self.rule_lenght()


#Aquí comienza el problema genético,el código anterior es referente a la lectura y manipulación del fichero arff.
class ProblemaGenetico(object):

    #p1 = Población existente en cada momento
    p1 = None
    #t = Iteración actual
    t = 0
    number_of_iterations = 0
    #Variable que representa a la clase Reader
    reader_class = Reader()
    #Mejor individuo de una determinada iteración
    better_individual = None

    k = 0

    #Constructor de la clase.
    def __init__(self, arff_file, k, n, t):
        self.reader_class.reader_initializer(arff_file, k, n)
        self.t = 0
        self.number_of_iterations = t
        self.p1 = self.reader_class.initial_population
        self.k = k
        self.control_algorithm()

    # Con este método pretendemos dividir los strings obtenidos para agruparlos en
    # atributos y a continuación ir guardándolos
    # en listas.Por último formamos los cromosomas a partir de las reglas
    # que forman los atributos anteriormente mencionados.
    def parser_string_to_lists(self, population):
        #Estructura de una regla
        structure = self.reader_class.structure
        # Población en la que sólo habrá atributos
        new_population = []
        # Para cada cromosoma en la población
        for chromosome in population:
            #Counter nos marcará por qué atributo de la estructura de una regla estamos
            counter = 0
            #Almacenamos el atributo en una variable
            attribute = ""
            #Número de bits necesarios para codificar el atributo con el que estamos operando
            number_of_bits = structure[counter]
            #Recorremos los bits que conforman el cromosoma
            for pointer in range(0, len(chromosome)):
                # Si número de bits necesarios sigue siendo mayor que uno, entonces se añade
                # el bit al atributo y decrementamos los bits necesarios
                if number_of_bits > 1:
                    attribute += chromosome[pointer]
                    number_of_bits -= 1
                # En caso contrario, añadimos el bit al atributo y
                # reseteamos las variables necesarias para hacer la operación
                elif number_of_bits <= 1:
                    attribute += chromosome[pointer]
                    new_population.append(attribute)
                    attribute = ""
                    if counter == len(structure)-2:
                        counter = 0
                    else:
                        counter += 1
                    number_of_bits = structure[counter]
        #Ahora queda agrupar estos atributos en reglas
        #Número de atributos necesarios para conformar una regla
        attributes_by_rule = len(structure) - 1
        #Población que se va a devolver
        parsed_population = []
        attribute_pointer = 1
        rule = []
        for attribute in new_population:
            if attribute_pointer == attributes_by_rule:
                rule.append(attribute)
                parsed_population.append(rule)
                attribute_pointer = 1
                rule = []
            else:
                rule.append(attribute)
                attribute_pointer += 1
        #Finalmente agrupamos las reglas en cromosomas
        final_population = []
        chromosome = []
        rules_counter = 0
        #Reglas que conforman un cromosoma
        bits_necessary = 0
        for number in range(0, len(self.reader_class.structure)-1):
            bits_necessary += self.reader_class.structure[number]
        k = int(len(population[0])/bits_necessary)
        crom_count = 0
        for rule in parsed_population:
            if rules_counter < k-1:
                chromosome.append(rule)
                rules_counter += 1
            else:
                chromosome.append(rule)
                final_population.append(chromosome)
                chromosome = []
                rules_counter = 0
                crom_count += 1
                if crom_count < len(population):
                    k = int(len(population[crom_count])/bits_necessary)
        return final_population

    #Con este método calculamos el valor de la función a optimizar
    #El porcentaje correcto de la fitness (#fitness(individuo) = (porcentaje de reglas cubiertas correctamente)^2)
    # lo hemos expresado en tanto por uno.
    def fitness(self, random_population):
        #Random population = población actual
        population = self.reader_class.arff_population
        relation_class = self.reader_class.relation_class
        random_population = self.parser_string_to_lists(random_population)
        #Anotamos las calificaciones obtenidas por cada cromosoma de la población:
        calificaciones_cromosomas = []
        #Reglas cubiertas por cada regla de cada cromosoma
        covered_rules = []

        #Para cada cromosoma en la población del algoritmo
        for chromosome in random_population:
            #Para cada regla en el cromosoma
            chromosome_covered_rules = []
            #Lista de reglas negativas excluidas por cada gen
            negative_rules_excluded = []
            for chromosome_rule in chromosome:
                #Para cada gen anotamos las reglas que cubre correctamente:
                reglas_cubiertas = 0
                #Se hace un mapa tipo [regla_del_cromosoma,Lista_de_reglas_cubiertas]
                covered_rules_map = []
                covered_rules_map.append(chromosome_rule)
                covered_rules_list = []
                #Comparo la regla de la población con la del cromosoma:
                #Para cada regla en la población inical
                for rule in population:
                    atributos_comparados = 0
                    atributos_cubiertos = 0
                    ones_counter = 0
                    #Recorro los atributos
                    # Flag se utiliza para saber si un atributo es nulo ('00', por ejemplo).
                    # Si lo es, esa regla no cubre a ninguna
                    flag = 0
                    for number in range(0, len(chromosome_rule)):
                        #Extraigo el atributo a comparar
                        attribute = rule[number]
                        #La comparación se hace bit a bit, obviando los atributos que pueden adoptar cualquier valor
                        #(como los "111")

                        #Si tiene al menos un 0 hago la comparación, si no, sé que está cubierto
                        if "0" in chromosome_rule[number]:
                            #Si el atributo es nulo, se le 'castiga'
                            if not "1" in chromosome_rule[number]:
                                #En el caso de que el atributo correspondiente en el conjunto de entrenamiento no esté
                                #solamente compuesto de ceros, se castiga.
                                if "1" in attribute:
                                    atributos_comparados += 1
                                    flag = 1
                                #En el caso contrario, el atributo está correctamente cubierto.
                                else:
                                    atributos_comparados += 1
                                    atributos_cubiertos += 1
                            else:
                                atributos_comparados += 1
                                for bit_pointer in range(0, len(attribute)):
                                    bit = attribute[bit_pointer]
                                    if bit == chromosome_rule[number][bit_pointer]:
                                        #Si el valor de la regla que estamos sacando del conjunto de entrenamiento es
                                        # positivo (e igual por tanto a la regla generada, porque todas son positivas),
                                        # entonces incrementamos el contador
                                        if bit == "1":
                                            atributos_cubiertos += 1
                        else:
                            #En este caso, como se ha dicho antes, está cubierto
                            if "1" in attribute:
                                ones_counter += 1
                                atributos_cubiertos += 1
                                atributos_comparados += 1
                    if ones_counter == atributos_comparados:
                        #Esto quiere decir que la regla son solo unos, esto no sirve para nada así que 'castigamos' esto
                        atributos_cubiertos = 0
                    #Si todos los atributos que se han comparado han coincidido es que la regla esta cubierta
                    if atributos_comparados == atributos_cubiertos and atributos_cubiertos >= 1:
                        #Lo cubre correctamente si además el valor del atributo en la conclusión de
                        # la regla coincide con el valor que el ejemplo toma en ese atributo
                        if rule[len(rule)-1] == relation_class[0] and flag == 0:
                            reglas_cubiertas += 1
                            covered_rules_list.append(rule)
                        #Si la regla cubierta es negativa, la añadimos a la lista de reglas mal cubiertas negativas
                        elif rule[len(rule)-1] != relation_class[0] and flag == 0:
                            negative_rules_excluded.append(rule)
                    #Si los atributos no son iguales pero la conclusión es negativa se considera correctamente cubierta
                    #La regla no puede estar en el cromosoma ya que no estaría correctamente cubierta
                    if atributos_comparados > atributos_cubiertos and atributos_cubiertos > 0:
                        if rule[len(rule)-1] != relation_class[0] and flag == 0 and rule[:len(rule)-1] not in chromosome:
                            reglas_cubiertas += 1
                            covered_rules_list.append(rule)
                #Las calificaciones se ponen en una lista para simplificar la tarea
                covered_rules_map.append(covered_rules_list)
                chromosome_covered_rules.append(covered_rules_map)

            #Aquí eliminamos las reglas 'negativas' cubiertas erroneamente
            for subset in chromosome_covered_rules:
                for rule in subset[1]:
                    if rule in negative_rules_excluded:
                        subset[1].remove(rule)

            #Añadimos el mapa de reglas cubiertas por este cromosoma a la lista de todos los
            # cromosomas para extraer posteriormente la puntuación de cada cromosoma
            covered_rules.append(chromosome_covered_rules)
        #Obtenemos la calificación del mejor individuo:
        better = 0
        worse = 1
        average = 0
        #Necesitamos el número de reglas del conjunto de entrenamiento para hacer el porcentaje
        number_of_rules = len(population)
        #Para cada lista de calificaciones, igualamos la lista cubierta a la posición primera de la regla
        #Luego vemos si la regla cubierta está dentro de dicha lista y por último comprobamos si la regla cubierta
        # no está dentro de la lista de reglas cubiertas, añadiendo en este caso la regla a esta lista.
        chromosome_marks = []
        for chromosome in covered_rules:
            list_of_covered_rules = []
            chromo_list = []
            for rule in chromosome:
                covered_list = rule[1]
                for covered_rule in covered_list:
                    if covered_rule not in list_of_covered_rules:
                        list_of_covered_rules.append(covered_rule)
            #fitness(individuo) = (porcentaje de reglas cubiertas correctamente)^2
            chromo_list.append((len(list_of_covered_rules)/number_of_rules)*(len(list_of_covered_rules)/number_of_rules))
            chromo_list.append(list_of_covered_rules)
            chromosome_marks.append(chromo_list)
        # Con este bloque se pretende hacer una lista tipo [puntuación del cromosoma, cromosoma]
        counter = 0
        individuos_con_calificaciones = []
        for marks_list in chromosome_marks:
            value = marks_list[0]
            individuos_con_calificaciones.append([value, random_population[counter]])
            counter += 1

        #Con el contador tenemos el total de los cromosomas que se han analizado para obtener la media
        contador = 0
        for marks_list in chromosome_marks:
            contador += 1
            #Para cada una de estas calificaciones
            mark = marks_list[0]
            value = mark
            if value > better:
                better = value
            if value < worse:
                worse = value
            average += value
        average /= contador
        return [better, worse, average, individuos_con_calificaciones]

    # Con este método nos quedamos con los mejores individuos de la población.
    # Se ha utilizado la selección mediante élite (ver página 42 del Tema 5)
    # Para reducir el código, en este método obtenemos también los peores elementos.
    def selecciona_mejores(self, population):
        better_population = []
        # Este parámetro variará según queramos quedarnos con más o menos individuos (mejores o peores).
        # La función int() trunca el resultado
        # La presión evolutiva está en 0.6, 0.1
        number_of_better_elements = int(len(population)*0.6)

        number_of_worse_elements = int(len(population)*0.1)

        if number_of_worse_elements < 1:
            number_of_worse_elements = 1
        #Vamos a dividir la población en los individuos mejores y peores.
        #Primero, ordenamos la población de mayor valoración a menor
        sorted_population = sorted(population, reverse=True)

        #Guardamos al mejor individuo en una variable de la clase
        self.better_individual = sorted_population[0]

        #Dividimos la población en mejores y peores
        better_individuals = sorted_population[:number_of_better_elements]
        worse_individuals = sorted_population[number_of_better_elements:]

        #Seleccionamos a los peores individuos aleatoriamente
        worse_individuals_selected = random.sample(worse_individuals, number_of_worse_elements)
        return [better_individuals, worse_individuals_selected]

    #Este método se utiliza para unir individuos
    def merge_individuals(self, good, bad):
        better_population = []
        #Finalmente, los unimos a todos
        for element in good:
            better_population.append(element[1])
        for element in bad:
            better_population.append(element[1])

        #Devolvemos esta población tras un 'shuffle' para mezclar aleatoriamente los elementos
        random.shuffle(better_population)
        return better_population

    #Extrae los elementos tras seleccionar los mejores
    def list_individuals(self, population):
        better_population = []
        for element in population:
            better_population.append(element[1])
        return better_population

    # La idea de este método es simplemente hacer que cada regla de un cromosoma sea un string,
    # luego el cromosoma será una lista de strings
    def parser_list_to_string(self, population):
        new_population = []
        for chromosome in population:
            new_chromosome = []
            for rule in chromosome:
                new_rule = ""
                for attribute in rule:
                    new_rule += attribute
                new_chromosome.append(new_rule)
            new_population.append(new_chromosome)
        return new_population

    #Mediante este método combinamos la información de los padres para obtener nuevos hijos.
    def cruza(self, c1, c2):
        #Se obtienen los números de reglas por cromosoma
        c1_length = len(c1)
        c2_length = len(c2)
        #Se seleccionan las reglas que albergarán a los puntos de corte
        first_cut = random.randint(0, c1_length-1)
        second_cut = random.randint(first_cut, c1_length-1)
        third_cut = random.randint(0, c2_length-1)
        fourth_cut = random.randint(third_cut, c2_length-1)

        #Comprobamos que no haya error
        random_cut_point_1 = 0
        random_cut_point_2 = 0

        if first_cut == second_cut:
            random_cut_point_1 = random.randint(0, len(c1[first_cut])-1)
            random_cut_point_2 = random.randint(random_cut_point_1, len(c1[first_cut]))
        if third_cut == fourth_cut:
            random_cut_point_1 = random.randint(0, len(c1[first_cut])-1)
            random_cut_point_2 = random.randint(random_cut_point_1, len(c1[first_cut]))

        #Calculamos los bits que formarán los trozos para el cruce
        number_of_bits_1 = first_cut*len(c1[first_cut])+random_cut_point_1
        number_of_bits_2 = second_cut*len(c1[second_cut])+random_cut_point_2
        number_of_bits_3 = third_cut*len(c2[third_cut])+random_cut_point_1
        number_of_bits_4 = fourth_cut*len(c2[fourth_cut])+random_cut_point_2

        #Unímos las reglas de los cromosomas para facilitar el cruce
        crom_1 = ""
        crom_2 = ""
        for rule in c1:
            crom_1 += rule
        for rule in c2:
            crom_2 += rule

        #Sacamos los trozos tras las divisiones
        slice_1 = crom_1[:number_of_bits_1]
        slice_2 = crom_1[number_of_bits_1:number_of_bits_2]
        slice_3 = crom_1[number_of_bits_2:]

        slice_4 = crom_2[:number_of_bits_3]
        slice_5 = crom_2[number_of_bits_3:number_of_bits_4]
        slice_6 = crom_2[number_of_bits_4:]

        #Con estos 6 trozos obtenidos, cruzamos y creamos los hijos
        son_1 = slice_1+slice_5+slice_3
        son_2 = slice_4+slice_2+slice_6

        # Cada cromosoma representa máximo k reglas
        rule_length = self.reader_class.rule_bits
        if len(son_1) > self.k*rule_length or len(son_2) > self.k*rule_length:
            return self.cruza(c1, c2)
        return [son_1, son_2]

    # Mutación simplemente voltea bits aleatorios dentro de la población, con una pequeña probabilidad
    def muta(self, population):
        #La probabilidad de mutacion es de 1/1000
        probabilidad_dividendo = 1
        probabilidad_divisor = 1000

        #Dividimos la población en cromosomas que serán una simple lista de bits para simplificar el volteo
        population_list = []
        for chromosome in population:
            chromosome_list = []
            for bit in chromosome:
                chromosome_list.append(bit)

            #Recorremos el cromosoma volteando en función de la probabilidad
            pointer = 0
            chromosome_length = len(chromosome_list)
            for bit in chromosome_list:
                random_number = random.randint(1, probabilidad_divisor)
                if random_number == probabilidad_dividendo:
                    flip_bit_position = random.randint(pointer, chromosome_length-1)
                    flip_bit = chromosome_list[flip_bit_position]
                    old_bit = bit
                    chromosome_list[pointer] = flip_bit
                    chromosome_list[flip_bit_position] = old_bit
                pointer += 1
            population_list.append(chromosome_list)

        #Recorremos nuevamente la población reagrupando en cromosomas
        new_population = []
        for chromosome in population_list:
            string_chromosome = ""
            for bit in chromosome:
                string_chromosome += str(bit)
            new_population.append(string_chromosome)
        return new_population

    #Este método sirve para obtener listas tipo [elemento_tal,siguiente_elemento] y se usa para la operación de cruce
    def list_in_pairs(self, chromos):

        this_element = 0
        next_element = 1
        return_list = []

        while next_element < len(chromos):
            pair = [chromos[this_element], chromos[next_element]]
            this_element = next_element + 1
            next_element += 2
            return_list.append(pair)
        if len(chromos) % 2 != 0:
            return_list.append(chromos[len(chromos)-1])
        return return_list

    #Esta función traduce las reglas de bits a texto legible
    def decodifica(self, population):
        #Necesitamos saber la estructura que tiene la regla así como los atributos originales
        rule_structure_decodifica = self.reader_class.rule_structure
        attributes_decodifica = self.reader_class.attributes
        rules = []
        #Recorremos cada una de las reglas de la población
        for chromosome in population:
            for rule in chromosome:
                attribute_index = 0
                is_the_first_attribute_in_the_string = True
                rule_in_text = "IF "
                non_usable_rule = False
                #Recorremos cada atributo
                for pointer in range(0, len(rule)):
                    attribute = rule[pointer]
                    number_of_ones = attribute.count('1')
                    attribute_length = len(attribute)
                    #Si hay tantos unos como tamaño tiene la regla no hago nada, en caso contrario
                    if number_of_ones < attribute_length:
                        positions = []
                        position = 0
                        #Vemos las posiciones en las que se encuentran los 1
                        for bit in attribute:
                            if bit == '1':
                                positions.append(position)
                            position += 1
                        #Si solo hay un '1', añado el atributo
                        if len(positions) == 1:
                            attribute_name = attributes_decodifica[attribute_index][0]
                            attribute_value = rule_structure_decodifica[attribute_index][positions[0]]
                            if attribute_index > 0 and is_the_first_attribute_in_the_string is False:
                                rule_in_text += " AND "+attribute_name+" = "+str(attribute_value)
                            else:
                                rule_in_text += attribute_name+" = "+attribute_value
                                is_the_first_attribute_in_the_string = False
                        #Si no, hay que añadirlos con la disyunción
                        elif len(positions) > 1:
                            there_is_an_or = False
                            for number in range(0, len(positions)):
                                attribute_name = attributes_decodifica[attribute_index][0]
                                attribute_value = rule_structure_decodifica[attribute_index][positions[number]]
                                if not isinstance(attribute_value, str):
                                    attribute_value = str(attribute_value)
                                if attribute_index > 0 and is_the_first_attribute_in_the_string is False \
                                        and there_is_an_or is False:
                                    rule_in_text += " AND "+attribute_name+" = "+attribute_value
                                else:
                                    rule_in_text += attribute_name+" = "+attribute_value
                                    is_the_first_attribute_in_the_string = False
                                if number < len(positions)-1:
                                    rule_in_text += " OR "
                                    there_is_an_or = True
                        #Si es sólo '0', mostramos que el valor del atributo es '?' (Decisión de implementación)
                        elif len(positions) == 0:
                            attribute_name = attributes_decodifica[attribute_index][0]
                            attribute_value = "?"
                            if attribute_index > 0 and is_the_first_attribute_in_the_string is False:
                                rule_in_text += " AND "+attribute_name+" = "+attribute_value
                            else:
                                rule_in_text += attribute_name+" = "+attribute_value
                                is_the_first_attribute_in_the_string = False
                    attribute_index += 1
                if rule_in_text != "IF " and non_usable_rule is False:
                    rule_in_text += " THEN "+str(attributes_decodifica[len(attributes_decodifica)-1][0])+" = "
                    rule_in_text += str(attributes_decodifica[len(attributes_decodifica)-1][1][0])
                    if rule_in_text not in rules:
                        rules.append(rule_in_text)
        return rules

    # Con este método controlamos el funcionamiento del algoritmo. Gracias a él mostramos
    # lo requerido en las iteraciones, así como el número de ellas.
    def control_algorithm(self):
        self.t = 0
        #La población ya se inicia aleatoriamente en el método  __init__
        fitness_population = self.fitness(self.p1)
        #Esta población nos sirve para encontrar el mejor conjunto de reglas al final del algoritmo
        pop_fitness_final = None
        #fitness de la iteración t
        fitness_t = None
        #Hasta que se llegue a la última iteración
        while self.t < self.number_of_iterations:
            print("ITERACIÓN "+str(self.t))
            if self.t == 0:
                fitness_t = fitness_population
            else:
                fitness_t = self.fitness(self.p1)
            #Seleccionamos las mejores reglas
            p2 = self.selecciona_mejores(fitness_t[3])
            #Aplicamos el operador cruce en pares [cromosoma_cualquiera, siguiente_cromosoma]
            p2 = self.merge_individuals(p2[0], p2[1])
            p2 = self.parser_list_to_string(p2)
            p3 = []
            for pair in self.list_in_pairs(p2):
                if len(pair) == 1:
                    p3.append(pair[0])
                else:
                    # Si el cromosoma se compone de una única regla, evitamos problemas
                    # al cruzar metiéndolo en una lista
                    if isinstance(pair[0], str):
                        pair[0] = [pair[0]]
                    if isinstance(pair[1], str):
                        pair[1] = [pair[1]]
                    p3.append(self.cruza(pair[0], pair[1]))
            #Aplicamos las mutaciones
            p3_chromos = []
            for pairs in p3:
                for chromo in pairs:
                    p3_chromos.append(chromo)
            #Cada cromosoma se muta dentro del método
            p4 = self.muta(p3_chromos)
            #Evaluamos la población
            pop_fitness = self.fitness(p4)
            pop_fitness_final = pop_fitness
            #Ahora es necesario unir los mejores elementos de esta población con la inicial
            # Para la siguiente generación, se toman los mejores de entre los hijos y los individuos originales
            union = []
            for element in fitness_t[3]:
                union.append(element)
            for other_element in pop_fitness_final[3]:
                union.append(other_element)
            poblacion_actual_mejores = self.selecciona_mejores(union)
            poblacion_actual = self.list_individuals(poblacion_actual_mejores[0])
            poblacion_actual = self.parser_list_to_string(poblacion_actual)
            #Población próxima iteración
            pob_t1 = []
            for cromo in poblacion_actual:
                cromosoma = ""
                for rule in cromo:
                    cromosoma += rule
                pob_t1.append(cromosoma)

            #Mostramos los datos siempre que hayamos avanzado un 10%
            percentage = self.number_of_iterations*0.1
            if self.number_of_iterations < 10 or self.t % int(percentage) == 0:
                print("VALORACIÓN MEDIA POBLACIÓN: "+str(pop_fitness[2]))
                print("VALORACIÓN MEJOR INDIVIDUO: "+str(pop_fitness[0]))
                print("VALORACIÓN PEOR INDIVIDUO: "+str(pop_fitness[1]))
            #Para la próxima iteración, la población usada será la obtenida (p5)
            self.p1 = pob_t1
            #Incrementamos el número de la iteración en la que estamos
            self.t += 1
        #Para ver sólo al mejor individuo:
        print("-- VALORACIÓN DE LA ÚLTIMA ITERACIÓN --")
        print("VALORACIÓN MEDIA POBLACIÓN: "+str(pop_fitness_final[2]))
        print("VALORACIÓN MEJOR INDIVIDUO: "+str(pop_fitness_final[0]))
        print("VALORACIÓN PEOR INDIVIDUO: "+str(pop_fitness_final[1]))
        self.selecciona_mejores(pop_fitness_final[3])
        rules_decoded = self.decodifica([self.better_individual[1]])
        print("-- REGLAS EXTRAÍDAS DEL MEJOR INDIVIDUO --")
        for rule_decoded in rules_decoded:
            print(rule_decoded)


#Este método pide los datos necesarios para inicializar el algoritmo
def ask_for_data():
    explanation = "El programa debe tomar como entrada únicamente un " \
                  "fichero en formato arff y los parámetros k, N y T."

    print(explanation)

    arff_file = str(input("Nombre del fichero arff (sin la extensión): "))
    k = int(input("Número maximo de reglas representado en cada cromosoma: "))
    n = int(input("Número de cromosomas que tendrá la población: "))
    t = int(input("Número de iteraciones: "))

    print("Fichero: "+arff_file+ " k: "+str(k)+" N: "+str(n)+" T: "+str(t))

    #Añadimos la terminación
    arff_file += ".arff"

    #Iniciamos la ejecución
    ProblemaGenetico(arff_file,k,n,t)


# Adecuadas para tiempo.arff: ProblemaGenetico('tiempo.arff', 5, 50, 100) vote: 50, 100, 10
#ProblemaGenetico('tic-tac-toe.arff', 50, 100, 50)
ask_for_data()

""" Tema 5 - Página 42
t := 0
Inicia-Población P(t)
Evalúa-Población P(t)
Mientras t < N-Generaciones hacer
    P1 := Selecciona-Mejores P(t)
    P2 := Selecciona-aleatorio (P(t) - P1)
    P3 := Cruza (P1 U P2)
    P4 := Muta P3
    Evalua-Población P4
    P(t+1) := Selecciona-Mejores P4,P(t)
    t:= t+1
Fin-Mientras
Devolver el mejor de P(t)
"""