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
from utils.pre_process import PreProcess
# =============================================================================

# Load data into database
df_temp = pd.read_csv("data/raw/data.csv", sep=',', na_values = ['Unknown'])
df_season = pd.read_csv("data/raw/anime_season.csv")

# Cleaning data
df_temp = Cleaning.transform(df_season,df_temp)
df_temp = Cleaning.drop(df_temp)
df_temp = Cleaning.transform2(df_temp)

# Process data
df_temp = PreProcess.transform(df_temp)
df_temp = PreProcess.drop_column(df_temp)

# print(df_temp.columns)

exit()