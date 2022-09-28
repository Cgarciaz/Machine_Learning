# Fichero test.py
import joblib

# Realizar unas predicciones de prueba
classifier_loaded = joblib.load("model/my_model.pkl")
encoder_loaded = joblib.load("model/anime_label_encoder.pkl")
print(" --- Pickle classifier y label encoder load executed ---")

# Prediction test con vectores aleatorios
X_manual_test = [[3,5,12,3]] # real: 6.96 - predict: 7.07
print("X_manual_test", X_manual_test)

prediction_raw = classifier_loaded.predict(X_manual_test)
print("Prediction_raw", prediction_raw)

prediction_real = encoder_loaded.inverse_transform(
                            classifier_loaded.predict(X_manual_test))
print("Real prediction", prediction_real)