from crypt import methods
import json
from types import MethodDescriptorType
from flask import Flask, jsonify, request
import joblib
import sklearn

app = Flask(__name__)

@app.route("/")
def home():
    return "la pagina esta funcionando"

@app.route("/predecir", methods = ["POST"])
def predecir():
    json = request.get_json(force=True)
    medidas = json['Medidas']
    clasificador = joblib.load('my_model.pkl')

if __name__ == '__main__':
    app.run()