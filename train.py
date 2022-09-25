# Change working directory to the directory of the script
import os 
os.chdir(os.path.dirname(os.path.abspath(__file__))) 

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

from utils.ETL import ETL
from utils.target_preprocess import *

# =============================================================================

# Load data into database
train = pd.read_csv("data/processed/data_train.csv")

# =============================================================================
train.rename(columns={'Unnamed: 0':'anime_id'}, inplace=True)
cleaning = train["Genres"].str.split(", ",12, expand=True)
cleaning.columns = ['Genre_0', 'Genre_1','Genre_2', 'Genre_3','Genre_4', 'Genre_5','Genre_6', 'Genre_7','Genre_8', 'Genre_9', 'Genre_10', 'Genre_11', 'Genre_12']
train_1 = pd.concat([train['anime_id'], cleaning], axis=1)
train_unpivoted = train_1.melt(id_vars=['anime_id'], var_name='Type_Genre', value_name='Genre')
train_unpivoted=train_unpivoted.assign(Value=1)
#Eliminar columnas que no se usarán para el análisis
train_unpivoted.drop(['Type_Genre'] , axis = 1 , inplace = True)
train_pivoted = train_unpivoted.pivot_table(index=['anime_id'],columns=['Genre'],aggfunc='count',fill_value=0)
train_pivoted.columns = train_pivoted.columns.droplevel(0) #remove amount
train_pivoted = train_pivoted.reset_index().rename_axis(None, axis=1)
train_2 = pd.merge(train, train_pivoted, on='anime_id', how='outer')
#Eliminar columnas que no se usarán para el análisis
train_2.drop(['Genres'] , axis = 1 , inplace = True)
cleaning = train["Studios"].str.split(", ",6, expand=True)
cleaning.columns = ['Studio_0', 'Studio_1','Studio_2', 'Studio_3','Studio_4', 'Studio_5','Studio_6']
train_1 = pd.concat([train['anime_id'], cleaning], axis=1)
train_unpivoted = train_1.melt(id_vars=['anime_id'], var_name='Type_Studios', value_name='Studio')
train_unpivoted=train_unpivoted.assign(Value=1)
#Eliminar columnas que no se usarán para el análisis
train_unpivoted.drop(['Type_Studios'] , axis = 1 , inplace = True)
train_pivoted = train_unpivoted.pivot_table(index=['anime_id'],columns=['Studio'],aggfunc='count',fill_value=0)
train_pivoted.columns = train_pivoted.columns.droplevel(0) #remove amount
train_pivoted = train_pivoted.reset_index().rename_axis(None, axis=1)
train_3 = pd.merge(train_2, train_pivoted, on='anime_id', how='outer')
#Eliminar columnas que no se usarán para el análisis
train_3.drop(['Studios'] , axis = 1 , inplace = True)
categorical_feature = (train_3.dtypes == "category") | (train_3.dtypes == object)
categorical_cols = train_3.columns[categorical_feature].tolist()

print(f"Preprocessing data...")

for c in categorical_cols:
    lbl = LabelEncoder() 
    lbl.fit(list(train_3[c].values)) 
    train_3[c] = lbl.transform(list(train_3[c].values))

df = train_3.copy()

# Split data into train and test sets
X = df.drop(columns=['price'])
y = df['price']

X_train, X_test, y_train, y_test, train_index, test_index = train_test_split(
    X, 
    y, 
    df.index,
    test_size=0.2, 
    random_state=42, 
    shuffle=True
)

numeric_cols = X_train.select_dtypes(include=['float64', 'int']).columns.to_list()
cat_cols = X_train.select_dtypes(include=['object', 'category']).columns.to_list()
bool_features = X_train.select_dtypes(include=['bool']).columns

# Preprocessing pipeline for numeric features
numeric_transformer = Pipeline(
                        steps=[
                            ('imputer', SimpleImputer(strategy='mean')),
                            ('scaler', StandardScaler())
                        ]
                      )


# Preprocessing pipeline for categorical features
categorical_transformer = Pipeline(
                            steps=[
                                ('imputer', SimpleImputer(strategy='most_frequent')),
                                ('onehot', OneHotEncoder(handle_unknown='ignore'))
                            ]
                          )

# Preprocessor to run both numeric and categorical transformations
preprocessor = ColumnTransformer(
                    transformers=[
                        ('numeric', numeric_transformer, numeric_cols),
                        ('cat', categorical_transformer, cat_cols)
                    ],
                    remainder='passthrough'
                )

X_train_prep = preprocessor.fit_transform(X_train)
X_test_prep  = preprocessor.transform(X_test)

# Preprocess target variable
y_train_prep, lamda = box_cox_transform(y_train)

# Save preprocessor and lambda value for later use
pickle.dump(preprocessor, open("models/preprocessor.pkl", "wb"))
pickle.dump(lamda, open("models/lamda_value.pkl", "wb"))

print(f"Data preprocessing completed")

# =============================================================================

print(f"Training model...")

# Grid search parameters
param_grid = {
    'n_estimators': range(800, 806),
    'max_depth'   : [None, 16],
    'max_features': ['sqrt', 5]
}

# Create instance of RandomForestRegressor
regressor = RandomForestRegressor(random_state=42)

# Create cross-validation object
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=42)

# Create instance of GridSearchCV
grid_search = GridSearchCV(
    estimator=regressor,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=cv,
    n_jobs=-1,
)

# Fit model to training data
grid_search.fit(X_train_prep, y_train_prep)

print(f"Model training completed")

# =============================================================================
model = grid_search.best_estimator_

# Print best parameters and best score
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_}")

# =============================================================================

# Save model to disk
print(f"Saving model to disk...")
pickle.dump(model, open("models/new_model.pkl", "wb"))

print(f"Model saved successfully, exiting...")
exit()