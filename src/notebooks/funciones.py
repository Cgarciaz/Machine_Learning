import pandas as pd

def to_1D(series):
 return pd.Series([x for _list in series for x in _list])


def get_data(col_index_name , col_target_name, dataframe): #col_name es la columna de la que queremos extraer los datos

  datos = []
  cont = 0
  index_column = dataframe.columns.get_loc(col_target_name) #Para saber el indice de la columna
  for list_gen in dataframe[col_index_name]:

    for gen in list_gen:
        
        val = dataframe.iloc[cont , index_column ] #encuentra el valor de la columna
        datos.append(val) #almacenar valores a la lista de datos

    cont += 1
    
  return pd.Series(datos)

# ML
n_folds = 5

def rmsle_cv(model):
    kf = KFold(n_folds, shuffle=True, random_state=42).get_n_splits(X_train.values)
    rmse= np.sqrt(-cross_val_score(model, X_train.values, y_train, scoring="neg_mean_squared_error", cv = kf))
    return(rmse)