from flask import Flask, session, url_for, render_template, redirect
import joblib

from season import AnimeFeature

# Cargamos los modelos guardados en saved_models
rf_loaded = joblib.load("saved_models/my_model.pkl")
encoder_loaded = joblib.load("saved_models/anime_label_encoder.pkl")

# Creamos la función de predicción
def make_prediction(model, encoder, sample_json):
    Start_season = sample_json['Start_season']
    Type = sample_json['Type']
    Episodes = sample_json['Episodes']
    Rating = sample_json['Rating']
    
    # Creamos un vector de input
    feature = [[Start_season, Type, Episodes, Rating]]

    # Predicción
    prediction_raw = model.predict(feature)

    # Convertimos los índices en labels de las clases
    prediction_real = encoder.inverse_transform(prediction_raw)

    return prediction_real[0]

# creamos la app de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/', methods=['GET','POST'])
def index():
    form = AnimeFeature()

    if form.validate_on_submit():
        session['Start_season'] = form.Start_season.data
        session['Type'] = form.Type.data
        session['Episodes'] = form.Episodes.data
        session['Rating'] = form.Rating.data

        return redirect(url_for('prediction'))
    return render_template("home.html", form=form)

@app.route('/prediction', methods=['POST','GET'])
def prediction():
    content = {'Start_season': float(session['Start_season']), 'Type': float(session['Type']),
               'Episodes': float(session['Episodes']), 'Rating': float(session['Rating'])}

    results = make_prediction(rf_loaded, encoder_loaded, content)

    return render_template('prediction.html', results=results)

# Ejecutamos la aplicación app.run()
if __name__ == '__main__':
    # LOCAL
    # app.run(host='0.0.0.0', port=8080)

    # REMOTO
    app.run()