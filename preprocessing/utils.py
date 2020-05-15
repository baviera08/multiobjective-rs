

def get_dataset_details(dataset, userlist, productlist):
    # Number of possible interactions in the matrix
    matrix_size = dataset.shape[0] * dataset.shape[1]
    # Number of items interacted with
    num_purchases = len(dataset.nonzero()[0])
    sparsity = 100 * (1 - (num_purchases / matrix_size))
    print("Sparcity of the dataset {} clients {} products {} transactions {" \
    "}".format( sparsity, len(userlist), len(productlist), num_purchases))
    information = {}
    information['nuser'] = len(userlist)
    information['nitem'] = len(productlist)
    information['ntransaccion'] = num_purchases
    information['sparcity_of_matrix'] = sparsity

    return information


def get_aditional_data(dataset):
    copy_dataset = dataset
    copy_dataset['user'] = copy_dataset['user'].astype("category")
    copy_dataset['item'] = copy_dataset['item'].astype("category")
    # items = dict(enumerate(dataset['item'].cat.categories))
    # to_generate = sorted(list(items), key=lambda x: -user_count[x])
    info_dataset = {}

    # veces que aparecen
    # Cuenta las veces que un item ha sido comprado por un usuario
    info_dataset['item'] = dataset.groupby('item').size()
    # Cuenta las veces que un usuario ha comprado items
    info_dataset['user'] = dataset.groupby('user').size()

    # obtiene el nro total
    info_dataset['nuser'] = info_dataset['user'].size
    info_dataset['nitem'] = info_dataset['item'].size

    # obtener el nro total unico de las transacciones
    info_dataset['transaccion'] = dataset.groupby(['user', 'item']).size()
    info_dataset['ntransaccion'] = info_dataset['transaccion'].size

    sparcity = float(info_dataset['ntransaccion']) / float(info_dataset[
                                                               'nuser'] *
                                                           info_dataset[
                                                               'nitem'])
    info_dataset['sparcity_of_matrix'] = 1 - sparcity

    info_dataset['item_enumerado'] = dict(enumerate(copy_dataset[
                                                        'user'].cat.categories))

    print('nro usuarios {},nro articulos {}, transaciones {}, sparsity {'
          '}'.format(
        info_dataset['nuser'],
        info_dataset['nitem'],
        info_dataset['ntransaccion'],
        info_dataset['sparcity_of_matrix'])
    )

    # imprimir informacion del dataset
    return info_dataset

def obtener_lista_articulos_tradicional(info_dataset, items):
    lista_articulo = []
    for i in range(info_dataset['nitem']):
        item = items[i]
        lista_articulo.append(item)
    lista = list(set(lista_articulo))

    return lista


def obtener_lista_articulos(rating):
    lista = list(rating.item.unique())

    return lista
