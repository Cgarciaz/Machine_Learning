import pandas as pd
import numpy as np

class Cleaning():

  def transform(df_season, df):
    
    # Creación de campo para obtener el año de emision del anime
    df['Start_year'] = df['Aired'].dropna(axis = 0).apply(lambda x : x.split('to')[0]).apply(
                          lambda x : x.split(',')).apply(
                          lambda x : x[1] if len(x) > 1 else x[0] ).apply(
                          lambda x : x.replace(' ', ''))

    # Creación de campo para obtener el mes de emision del anime
    df['Start_Month'] = df['Aired'].dropna(axis = 0).apply(lambda x : x.split('to')[0]).apply(
                          lambda x : x.split(',')).apply(
                          lambda x : x[0] ).apply(
                              lambda x : x.split(' ')[0])
    
    # Creación de campo que contenga la temporada cuando se emitió el anime
    df['Season'] = df['Premiered'].dropna(axis = 0).apply(lambda x : x.split(' ')[0])

    df = df.assign(New_score=lambda x:((x['Score-10']*10 + x['Score-9']*9 + x['Score-8']*8
                                        + x['Score-7']*7 + x['Score-6']*6 + x['Score-5']*5 + x['Score-4']*4 + x['Score-3']*3 + x['Score-2']*2
                                        + x['Score-1'])/(x['Score-10'] + x['Score-9'] + x['Score-8']+ x['Score-7'] + x['Score-6'] + x['Score-5']
                                        + x['Score-4'] + x['Score-3'] + x['Score-2']+ x['Score-1'])))

    df1 = pd.merge(
    left=df,right=df_season, how='left', left_on='Start_Month', right_on='Month_emision'
    )

    df1['Start_season'] = np.where(df1['Season_x'].isna(),
                                        df1['Season_y'],df1['Season_x'])

    df1['New_score2'] = np.where(df1['Score'].isna(),
                                    df1['New_score'],df1['Score'])
  
    # df1.rename(columns={'New_score2':'Score'}, inplace=True)

    print("transform process was successful")

    return df1

  def drop(df):
    
    df.drop(['Name' , 'English name' , 'Japanese name','Watching', 'On-Hold', 'Dropped', 'Ranked', 'Popularity',
              'Licensors','Plan to Watch','Producers','Source','Completed','Favorites','Duration','Members',
              'Premiered','Aired', 'Start_Month','Season_x','Month_emision','Season_y', 'Score-10', 'Score-9', 
              'Score-8', 'Score-7', 'Score-6','Score-5', 'Score-4', 'Score-3', 'Score-2', 'Score-1','Score',
              'New_score'] , axis = 1 , inplace = True)
    df.drop_duplicates(inplace=True) # Drop duplicates
    df = df.dropna(axis = 0).copy()

    df.reset_index(drop=True, inplace=True) # Reset index

    print("drop process was successful")

    return df

  def transform2(df):

    # Renombrar columnas
    df.rename(columns={'New_score2':'Score'}, inplace=True)

    # Creación de rango de episodios
    df_range = pd.DataFrame()
    max_episode = int(df['Episodes'].max()) + 12
    for index in range(len(df)):
      for i in range(1, max_episode, 12):
        val2 = i + 12
        if df.Episodes.loc[index] >= i and df.Episodes.loc[index] < val2:
          nueva_fila = {"MAL_ID": int(df.MAL_ID.loc[index]),"range_episodes":'[' + str(i) + ' - ' + str(val2) + ']'} # creamos un diccionario
          df_range = df_range.append(nueva_fila, ignore_index=True)
    df = pd.merge(df, df_range, on = "MAL_ID", how='outer')

    df['Score'] = df['Score'].astype('float')
    df = df[['Start_season','Type','Episodes','Rating','Score']]

    print("transform2 process was successful")

    return df