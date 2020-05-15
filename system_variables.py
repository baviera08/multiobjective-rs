sysvar = {}
sysvar['bd'] = 'testProject'
sysvar['bd_address'] = 'localhost'
sysvar['proyecto'] = 'testProject'

'''
Se definen el tipo de división de datos a utilizar
* calibracion: Se usan los test de validación para calibrar el modelo.
* test: se utiliza solamente un train set y un test set.
* produccion: se realizan las predicciones entrenando sobre todos los datos.
* evaluation: se realiza un k-fold 
'''

sysvar['estado_proyecto'] = 'evaluation'

'''
Datos clasificación, esto define los tipo de datos a utilizar ya sean de 
articulos normales o clasificaciones.

1. articulo
2. clasificacion
'''

sysvar['datos'] = 'clasificacion'

'''
Se definen el tipo de división de datos a utilizar
#conTS: Conjuntos de validation y test con timestamp
#sinTS: Conjuntos de validation y test sin timestamp
'''
sysvar['conjunto_validacion'] = 'sinTS'

'''
reducir la cantidad de usuarios del sistema, de modo 
a agendar a solo los usuarios que compraron más de n productos
'''
sysvar['nro_compras_minimo_usuario'] = 4

sysvar['tesis'] = True

sysvar['folder'] = 10

configuracion = {
    "colaborativo_usuario": None,
    "colaborativo_item_als": True,
    "colaborativo_item_cosine": True,
    "colaborativo_item_bm25": True,
    "evento": None,
    "empresa": None,
    "experto": None,
    "frecuencia": None,
    "tradicional": None,
    "multiobjetivo": None,
}

sysvar['distancia'] = {
    'coseno': True,
    'euclidiana': True,
    'jaccard': True,
}

sysvar['obtener_distancia_bd'] = False
sysvar['guardar_distancia'] = True


################################################################################
################################## #MOP #######################################
################################################################################

class CMultiobjetivo:
    # Cantidad de elementos en cada lista formada
    ind_init_size = 6
    # # Cantidad maxima de items
    # max_item = 50
    # Cantidad maxima de peso, si se tiene
    max_weight = 6
    # Nro total de items diferentes
    max_item = 10
    min_exac = 0.35

    '''
    La politica de desición puede ser:
     *NINGUNO: las solucion 
     *ORIGEN: la solución que está más cerca del origen del plano.
     ## Alguno de los recomendadores no tradicionales ##
     *EXPERTO: la solución que está más cerca del la lista del experto.
     *EMPRESA:la solución que está más cerca del la lista del empresa.
     *EVENTO:la solución que está más cerca del la lista del evento.
     *FRECUENCIA:
     *CLIENTE:
     *PESO
     *LEXICOGRAFICO
     *TODOS
    '''
    politica_decision = 'TODOS'

    # El nro de generaciones de población
    NGEN = 500  # 200
    # nro de la población inicial
    MU = 400
    LAMBDA = 100
    # crossover operation on input sets 0.7
    CXPB = 0.6
    # Mutation that pops or add an element
    MUTPB = 0.3


########## Variables optimización multiobjetivo ###############
sysvar['multiob'] = {}
sysvar['multiob']['opcion1'] = CMultiobjetivo()

modelo = {
    "item_item": True
}

