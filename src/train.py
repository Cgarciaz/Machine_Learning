# Get the current working directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) 
# path = os.path.dirname(os.path.abspath(__file__))

# =============================================================================

# Libraries needed to train the model
# import pickle
import pandas as pd

# from sklearn.preprocessing import LabelEncoder
# from sklearn.pipeline import Pipeline
# from sklearn.compose import ColumnTransformer
# from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split, GridSearchCV, RepeatedKFold
# from sklearn.ensemble import RandomForestRegressor

from utils.cleaning import Cleaning
# =============================================================================

# Load data into database
# df = pd.read_csv(path + "src\data\raw\data.csv")
df_temp = pd.read_csv("data/raw/data.csv", sep=',', na_values = ['Unknown'])
df_season = pd.read_csv("data/raw/anime_season.csv")

print(f"Número total de registros ant: {len(df_temp)}")
print(f"Número total de column ant: {len(df_temp.columns)}")
print(f"Número total de column: {df_season.head()}")

# Process data
df_temp = Cleaning.transform(df_season,df_temp)

print(f"Número total de registros: {len(df_temp)}")
print(f"Número total de column: {len(df_temp.columns)}")
print(f"Número total de column: {df_temp.head()}")

# # Process data
# df_temp = Cleaning.drop(df_temp)

# print(f"Número total de registros: {len(df_temp)}")
# print(f"Número total de column: {len(df_temp.columns)}")

exit()