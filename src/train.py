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

# Process data - Encoder
df_temp = PreProcess.transform(df_temp)

# Convertimos o serializamos las clases en formato pickle pkl
import joblib

joblib.dump(df_temp, "model/anime_label_encoder.pkl")
print(" --- Pickle labelEncoder dump executed ---")

# Modelling data
X = df_temp.drop(['Score'], axis=1)
y = df_temp['Score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)

#Linear Regression
lm = LinearRegression()
lm.fit(X_train.values, y_train.values)
pickle.dump(lm,open('model/lasso_model.pkl', 'wb'))

lasso = make_pipeline(RobustScaler(), Lasso(alpha =0.0005, random_state=1))
pickle.dump(lasso,open('model/lasso_model.pkl', 'wb'))

ENet = make_pipeline(RobustScaler(), ElasticNet(alpha=0.0005, l1_ratio=.9, random_state=3))
pickle.dump(ENet,open('model/ENet_model.pkl', 'wb'))

KRR = KernelRidge(alpha=0.6, kernel='polynomial', degree=2, coef0=2.5)
pickle.dump(KRR,open('model/KRR_model.pkl', 'wb'))

GBoost = GradientBoostingRegressor(n_estimators=3000, learning_rate=0.05,
                                   max_depth=4, max_features='sqrt',
                                   min_samples_leaf=15, min_samples_split=10, 
                                   loss='huber', random_state =5)
pickle.dump(GBoost,open('model/GBoost_model.pkl', 'wb'))

Tree = DecisionTreeRegressor()
Tree.fit(X_train.values, y_train.values)
pickle.dump(Tree,open('model/Tree_model.pkl', 'wb'))

SVR_model = SVR()
SVR_model.fit(X_train.values, y_train.values)
pickle.dump(SVR_model,open('model/SVR_model.pkl', 'wb'))

rf_model = RandomForestRegressor()
rf_model.fit(X_train.values, y_train.values)
pickle.dump(rf_model,open('model/my_model.pkl', 'wb'))

exit()