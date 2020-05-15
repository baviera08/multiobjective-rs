# -*- coding: utf-8 -*-
from __future__ import print_function
import pandas as pd
import scipy.sparse as sparse
import numpy as np
from implicit.nearest_neighbours import bm25_weight
from scipy.sparse.linalg import spsolve
from scipy.sparse import coo_matrix, csr_matrix
import argparse
import logging
import time
from distancia.distancia import calculate_distance_matrix, distance_dict

'''
Instead of representing an explicit rating, the purchase quantity can represent 
a “confidence” in terms of how strong the interaction was. Items with a larger 
number of purchases by a customer can carry more weight in our ratings matrix 
of purchases.

Our last step is to create the sparse ratings matrix of users and items
'''

def generate_sparse_matrix_csr(grouped_purchased, item='item',
                               usuario='usuario',
                               rating='rating'):
    # Get our unique customers
    customers = list(np.sort(grouped_purchased[usuario].unique()))
    # Get our unique products that were purchased
    products = list(grouped_purchased[item].unique())
    # All of our purchases
    quantity = list(grouped_purchased[rating])

    rows = grouped_purchased[usuario].astype('category',
                                             categories=customers).cat.codes
    # Get the associated row indices
    cols = grouped_purchased[item].astype('category',
                                          categories=products).cat.codes
    # Get the associated column indices
    purchases_sparse = sparse.csr_matrix((quantity, (rows, cols)),
                                         shape=(len(customers), len(products)))

    return purchases_sparse, customers, products


'''
* Group purchase quantities together by stock code and item ID
* Change any sums that equal zero to one (this can happen if items were 
returned, but we want to indicate that the user actually purchased the item 
instead of assuming no interaction between the user and the item ever took place)

* Only include customers with a positive purchase total to eliminate possible 
errors.
* Set up our sparse ratings matrix.
*OBS so we can save a lot of memory by keeping the matrix sparse and only saving
 the locations and values of items that are not zero.
'''

def preprocess_analysis(data, item='item', rating='rating', user='user'):
    # Convert to int for customer ID
    data[user] = data[user].astype(int)
    # Get rid of unnecessary info
    campos_a_utilizar = [item, rating, user]
    cleaned_retail = data[campos_a_utilizar]
    # Group together
    grouped_cleaned = cleaned_retail.groupby(
        [user, item]).sum().reset_index()
    # Replace a sum of zero purchases with a one to # indicate purchased
    grouped_cleaned[rating].loc[grouped_cleaned[rating] == 0] = 1
    # Only get customers where purchase totals were positive
    query = rating + ' > 0'
    grouped_purchased = grouped_cleaned.query(query)
    grouped_purchased.head()
    return grouped_purchased


def reduccion_usuarios(data, item='item', rating='rating', usuario='usuario'):
    sum_usuario = data.groupby([usuario]).sum()
    df_reducido = sum_usuario.query('rating > 5').reset_index()
    lista_usuario = df_reducido[usuario].tolist()
    # copy_data = data[data.usuario != 0]
    datos_ssparcity = data[data[usuario].isin(lista_usuario)]
    return datos_ssparcity


def item_values(data, item='id', description='descripcion'):
    # Only get unique item/description pairs
    item_lookup = data[[item, description]].drop_duplicates()
    # Encode as strings for future lookup ease
    item_lookup[item] = item_lookup[item].astype(str)
    # item_lookup.head()
    return item_lookup


def clean_data(data, campo):
    campo_cliente = data[campo]
    # Limpiamos los datos null o missing values si es que hay
    cleaned_retail = data.loc[pd.isnull(campo_cliente) == False]
    cleaned_retail.info()

    return cleaned_retail


def get_label_index(dataset, info):
    # Cuenta las veces que un usuario ha comprado items
    cant_usuarios_dataset = info['user']
    # Cuenta las veces que un item ha sido comprado por un usuario
    cant_items_dataset = info['item']
    ##### USUARIO ######
    # Asignar label a las posiciones de la matriz para conocer la correspondencia
    # Guarda los id de los usuarios en una lista
    dict_usuarios = dict(enumerate(dataset['user'].cat.categories))
    # ordena los usuarios y le da forma de una lista ordenada
    lista_usuarios = sorted(list(dict_usuarios),
                            key=lambda x: -cant_usuarios_dataset[x])

    ##### ITEM ######
    '''
    # cat Concatenate strings in the Series/Index with given separator.
    # Setting assigns new values to each category (effectively a rename of each individual category).
    # enumerate It allows us to loop over something and have an automatic counter
    '''
    dict_items = dict(enumerate(dataset['item'].cat.categories))
    lista_items = sorted(list(dict_items), key=lambda x: -cant_items_dataset[x])

    return dict_usuarios, lista_usuarios, dict_items, lista_items


# 1. Partir en train set y test set
# 2. Accesores de tuplas a través de listas.
# 2. A los que tienen solo una puntuación sacarle de la lista entonces la
# matriz no es tan dispersa.
# 3. A esos que se les quita de la matriz hay que guardarlos y recomendarle
# cosas de los recomendadores generales.

# n. Métodos de evaluación validos


def generate_sparse_matrix_coo(data):
    data['user'] = data['user'].astype("category")
    data['item'] = data['item'].astype("category")
    '''
        |      - COO is a fast format for constructing sparse matrices
        |      - Once a matrix has been constructed, convert to CSR or
        |        CSC format for fast arithmetic and matrix vector operations
        |      - By default when converting to CSR or CSC format, duplicate (i,j)
        |        entries will be summed together.  This facilitates efficient
        |        construction of finite element matrices and the like. (see example)
        '''
    matrix = coo_matrix((data['rating'].astype(np.float32),
                         (data['item'].cat.codes.copy(),
                          data['user'].cat.codes.copy())))

    matrix.data = np.ones(len(matrix.data))

    return matrix


def obtain_data_detalles(data):
    # map each item and user to a unique numeric value
    # data['descripcion'] = data['descripcion'].astype("category")
    # data['item'] = data['item'].astype("category")

    data['descripcion'] = data['descripcion'].drop_duplicates()
    data['item'] = data['item'].drop_duplicates()
    # create a sparse matrix of all the users/rating
    # data.to_dict(orient='dict')
    # data_agrupado = data.groupby('item')

    # setea el índice como un único elemento (tipo group by)
    data_diccionario = data.set_index('item')['descripcion'].to_dict()
    # indexado = data.set_index(data['item'])
    return data_diccionario


''''
1. Hacer que ordene todo, y así voy a poder tener la ubicación de los cliente y artículos
2. Con ello cambiar el train

'''
def obtener_datos(input_filename):
    logging.debug("Calculating similar items. This might take a while")

    # read in the input data file
    logging.debug("reading data from %s", input_filename)
    start = time.time()

    df, rating, info_dataset, dict_usuarios, lista_usuarios, dict_items, \
    lista_items = read_data(input_filename)

    rating = bm25_weight(rating, K1=100, B=0.8)
    # obtenemos el id y la descripcion del articulo
    detalle_articulo = read_data_detalles(input_filename)
    logging.debug("read data file in %s", time.time() - start)

    # calcula la matriz de distancia entre items
    items = dict(enumerate(df['item'].cat.categories))
    # calcula la matriz distancia entre los items
    similarity_matrix = calculate_distance_matrix(rating)
    # guarda la distancia en un dict
    distance = distance_dict(similarity_matrix, info_dataset, items)
    # obtiene la lista de artículos en el sistema
    # TODO CAMBIAR ESTE
    lista_articulos = obtener_lista_articulos_tradicional(info_dataset, items)

    return df, rating, info_dataset, detalle_articulo, similarity_matrix, \
           distance, lista_articulos, dict_usuarios, lista_usuarios, dict_items, \
           lista_items
