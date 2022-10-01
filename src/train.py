# Get the current working directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# =============================================================================

# Libraries needed to train the model
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.linear_model import ElasticNet, Lasso
from sklearn.ensemble import RandomForestRegressor,  GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler

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

# Matriz de features
categorical_feature = (df_temp.dtypes == "category") | (df_temp.dtypes == object)
categorical_cols = df_temp.columns[categorical_feature].tolist()

# Creamos la instancia de LabelEncoder
from sklearn.preprocessing import LabelEncoder

for c in categorical_cols:
    lbl = LabelEncoder() 
    lbl.fit(list(df_temp[c].values)) 
    df_temp[c] = lbl.transform(list(df_temp[c].values))

# Convertimos o serializamos las clases en formato pickle pkl
import joblib

joblib.dump(df_temp, "model/anime_label_encoder.pkl")
print(" --- Pickle labelEncoder dump executed ---")

# Train and Test split
X = df_temp.drop(['Score'], axis=1)
y = df_temp['Score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)

#Linear Regression
model_lr = LinearRegression()
model_lr.fit(X_train,y_train)
pickle.dump(model_lr,open('model/lr_model.pkl', 'wb'))

# Random Forest
model_rf = RandomForestRegressor()
model_rf.fit(X_train, y_train)
pickle.dump(model_rf,open('model/rf_model.pkl', 'wb'))

# Decision Tree
model_dt = DecisionTreeRegressor()
model_dt.fit(X_train, y_train)
pickle.dump(model_rf,open('model/dt_model.pkl', 'wb'))

# Support Vector
model_svr = SVR()
model_svr.fit(X_train, y_train)
pickle.dump(model_rf,open('model/svr_model.pkl', 'wb'))

# Kernel Ridge
model_krr = KernelRidge(alpha=1.0,kernel='polynomial',degree=3)
model_krr.fit(X_train, y_train)
pickle.dump(model_rf,open('model/krr_model.pkl', 'wb'))

# Gradient Boosting
model_gbt = GradientBoostingRegressor()
model_gbt.fit(X_train, y_train)
pickle.dump(model_rf,open('model/my_model.pkl', 'wb'))

exit()