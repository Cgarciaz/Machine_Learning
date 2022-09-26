import pandas as pd
import numpy as np

# Index(['MAL_ID', 'Genres', 'Type', 'Episodes', 'Studios', 'Rating',
#        'Start_year', 'Start_season', 'Score', 'range_episodes'],
#       dtype='object')

# Index(['MAL_ID', 'Type', 'Episodes', 'Rating', 'Start_year', 'Start_season',
#        'Score', 'range_episodes', 'anime_id', 'Action',
#        ...
#        'feel.', 'helo.inc', 'iDRAGONS Creative Studio', 'ixtl', 'l-a-unch・BOX',
#        'monofilmo', 'pH Studio', 'production doA', 'teamKG', 'ufotable'],
#       dtype='object', length=689)

class PreProcess():

  def transform(df):
    
    df.reset_index(drop=True, inplace=True) # Reset index

    df['anime_id'] = df.index

    cleaning = df["Genres"].str.split(", ",12, expand=True)
    cleaning.columns = ['Genre_0', 'Genre_1','Genre_2', 'Genre_3','Genre_4', 'Genre_5','Genre_6', 'Genre_7','Genre_8', 'Genre_9', 'Genre_10', 'Genre_11', 'Genre_12']
    df1 = pd.concat([df['anime_id'], cleaning], axis=1)
    
    train_unpivoted = df1.melt(id_vars=['anime_id'], var_name='Type_Genre', value_name='Genre')
    train_unpivoted=train_unpivoted.assign(Value=1)
    #Eliminar columnas que no se usarán para el análisis
    train_unpivoted.drop(['Type_Genre'] , axis = 1 , inplace = True)
    
    train_pivoted = train_unpivoted.pivot_table(index=['anime_id'],columns=['Genre'],aggfunc='count',fill_value=0)
    train_pivoted.columns = train_pivoted.columns.droplevel(0) #remove amount
    train_pivoted = train_pivoted.reset_index().rename_axis(None, axis=1)

    train_2 = pd.merge(df, train_pivoted, on='anime_id', how='outer')
    #Eliminar columnas que no se usarán para el análisis
    train_2.drop(['Genres'] , axis = 1 , inplace = True)

    # Studios----------------------------------------------------------------------
    cleaning = df["Studios"].str.split(", ",6, expand=True)
    cleaning.columns = ['Studio_0', 'Studio_1','Studio_2', 'Studio_3','Studio_4', 'Studio_5','Studio_6']
    train_1 = pd.concat([df['anime_id'], cleaning], axis=1)

    train_unpivoted = train_1.melt(id_vars=['anime_id'], var_name='Type_Studios', value_name='Studio')
    train_unpivoted=train_unpivoted.assign(Value=1)
    # Eliminar columnas que no se usarán para el análisis
    train_unpivoted.drop(['Type_Studios'] , axis = 1 , inplace = True)

    train_pivoted = train_unpivoted.pivot_table(index=['anime_id'],columns=['Studio'],aggfunc='count',fill_value=0)
    train_pivoted.columns = train_pivoted.columns.droplevel(0) #remove amount
    train_pivoted = train_pivoted.reset_index().rename_axis(None, axis=1)

    train_3 = pd.merge(train_2, train_pivoted, on='anime_id', how='outer')
    # Eliminar columnas que no se usarán para el análisis
    train_3.drop(['Studios'] , axis = 1 , inplace = True)

    print("transform process was successful")

    return train_3

  def drop_column(df):

    #Eliminar columnas que sobran
    df.drop(['Start_year','MAL_ID'] , axis = 1 , inplace = True)

    print("drop_column process was successful")

    return df