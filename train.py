# Get the current working directory
import os 
os.path.dirname(os.path.abspath(__file__))

# =============================================================================

# Libraries needed to train the model
import pickle
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, RepeatedKFold
from sklearn.ensemble import RandomForestRegressor

# from utils.procesador import *
# =============================================================================

# Load data into database
# df = pd.read_csv("data/processed/data_train.csv")
print("Current working directory: {0}".format(ss))
print(f"Model saved successfully, exiting...")
exit()