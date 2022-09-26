import pandas as pd
import numpy as np

class Cleaning():

  def drop(df):
    
    df.drop(['Name' , 'English name' , 'Japanese name','Watching', 'On-Hold', 'Dropped', 'Ranked', 'Popularity',
              'Licensors','Plan to Watch','Producers','Source','Completed','Favorites','Duration','Members'] , axis = 1 , inplace = True)
    df.drop_duplicates(inplace=True) # Drop duplicates
    df.reset_index(drop=True, inplace=True) # Reset index

    print("drop process was successful")

    return df

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

    return df