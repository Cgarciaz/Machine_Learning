from sklearn.preprocessing import LabelEncoder

class PreProcess():

  def transform(df):

    df = df[['Start_season','Type','Episodes','Rating','Score']]

    # Para convertir las categóricas en binarias debemos pasarla primero a booleanas
    # evaluando si son del tipo object o category
    categorical_feature = (df.dtypes == "category") | (df.dtypes == object)
    categorical_cols = df.columns[categorical_feature].tolist()

    for c in categorical_cols:
        lbl = LabelEncoder() 
        lbl.fit(list(df[c].values)) 
        df[c] = lbl.transform(list(df[c].values))

    print("transform process was successful")

    return df