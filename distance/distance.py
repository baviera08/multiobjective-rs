# -*- coding: utf-8 -*-
from __future__ import division
import logging
import json
import gridfs
from pymongo import MongoClient
from sklearn.preprocessing import normalize
from implicit.nearest_neighbours import (CosineRecommender, ItemItemRecommender,
                                         normalize, bm25_weight)

from variables_sistema import sysvar
from distance.cosine import calculate_distance_matrix
from distance.euclidian import calculate_distance_matrix_euclidian
from distance.jaccard import calculate_distance_matrix_jaccard

# Mongo conexion
client = MongoClient(sysvar['bd_address'], 27017)
database = sysvar['bd']
db = client[database]
fs = gridfs.GridFS(db)


def get_distance_dict_from_db():
    distances_db = json.loads(str(fs.get_last_version(
            filename='distance').read(), 'utf8'))
    distances = distances_db["distance"]
    return distances

def calculate_similarity_matrix(dataset):
    distances = sysvar['distancia']
    matrices = {}

    if distances['coseno']:
        normalize_matrix = bm25_weight(dataset, K1=100, B=0.8)
        matrices['coseno'] = normalize(calculate_distance_matrix(
            normalize_matrix))

    if distances['jaccard']:
        matrices['jaccard'] = normalize(calculate_distance_matrix_jaccard(
            dataset))

    if distances['euclidiana']:
        matrices['euclidiana'] = normalize(calculate_distance_matrix_euclidian(
            dataset))
    return matrices


def get_all_distances_dict(similarity_matrix, info_dataset, items):
    distances = sysvar['distances']
    distance_dict = {}
    for kdiv, valdiv in sorted(distances.items()):
        if valdiv:
            distance_dict[kdiv] = build_distance_dict(similarity_matrix[kdiv],
                                                        info_dataset,
                                                        items,
                                                        kdiv)
    return distance_dict


def build_distance_dict(similarity_matrix, info_dataset, items, nombre):
    '''

    :param similarity_matrix:
    :param info_dataset:
    :param items:
    :param nombre: nombre de la distancia
    :return: distancia entre los items {'x': {'z':0.5, 'y':0.6}}
    '''
    distancia = {}
    for i in range(info_dataset['nitem']):
        item = items[i]
        similarity_item_item = similarity_matrix.T.tocsr()[i]
        # calculate the top related items
        recommendations = similarity_item_item.dot(similarity_matrix)

        best = sorted(
            zip(recommendations.indices, recommendations.data),
            key=lambda x: -x[1])

        distancia_item_item = dict((str(items[x]), str(y)) for x, y in best)
        distancia[str(item)] = distancia_item_item
    logging.debug("Haciendo un dict de las distancias")
    # obtener el nro más grande
    mayor = 0.0
    menor = 999999999999.0
    # distancia por item
    for key, val in distancia.items():
        # Distancia al item key
        # for keydis, valdis in val.items():
        if val.values():
            mayor_local = float(max(val.values()))
            menor_local = float(min(val.values()))
            if mayor_local > mayor:
                mayor = mayor_local

            if menor_local < menor:
                menor = menor_local

    # Normalizar
    if mayor > 1:
        fmayor = float(mayor)
        fmenor = float(menor)
        if (fmayor - fmenor) != 0:
            norm = 1 / (fmayor - fmenor)
            dist_norm = {}
            for key, val in distancia.items():
                dist_norm[key] = {}
                # Distancia al item key
                for keydis, valdis in val.items():
                    normalizado = (float(valdis) - fmenor) * norm
                    if 'coseno' in nombre:
                        similitud = normalizado
                    else:
                        similitud = 1 - normalizado
                    dist_norm[key][keydis] = str(similitud)
        return dist_norm
    else:
        return distancia