import pandas as pd

def read_raw_data(filename, ftype='csv', sep=";", usecols=[0, 1, 3],
                  names=['user', 'item', 'rating']):
    if ftype == 'csv':
        data = pd.read_csv(filename, sep=sep, usecols=usecols, names=names)
    if ftype == 'excel':
        data = pd.read_excel(filename)  # This may take a couple minutes

    data.info()
    return data



def read_data(filename, label_archivo=['user', 'item', 'rating'], posicion=[
    0, 1, 3]):
    """ Reads in the last.fm dataset, and returns a tuple of a pandas dataframe
    and a sparse matrix of artist/user/playcount """
    # read in triples of user/artist/playcount from the input dataset
    data = pd.read_table(filename,
                         usecols=posicion,
                         names=label_archivo,
                         sep=";")
    return data


def read_data_ori(filename):
    """ Reads in the last.fm dataset, and returns a tuple of a pandas dataframe
    and a sparse matrix of artist/user/playcount """
    # read in triples of user/artist/playcount from the input dataset
    data = pd.read_table(filename,
                         usecols=[0, 1, 3],
                         names=['user', 'item', 'rating'],
                         sep=";")

    # map each item and user to a unique numeric value
    data['user'] = data['user'].astype("category")
    data['item'] = data['item'].astype("category")

    # create a sparse matrix of all the users/rating
    matrix = coo_matrix((data['rating'].astype(np.float32),
                         (data['item'].cat.codes.copy(),
                          data['user'].cat.codes.copy())))

    matrix.data = np.ones(len(matrix.data))

    return data, matrix


# , rating, info_dataset, dict_usuarios, lista_usuarios, dict_items,lista_items

def read_data_detalles(filename):
    """ Reads in the last.fm dataset, and returns a tuple of a pd dataframe
    and a sparse matrix of artist/user/playcount """
    # read in triples of user/artist/playcount from the input dataset
    data = pd.read_table(filename,
                         usecols=[1, 2],
                         names=['item', 'descripcion'],
                         sep=";")

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

