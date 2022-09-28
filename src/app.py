from flask import Flask, session, url_for, render_template, redirect
# import joblib

from feature import AnimeFeature

# creamos la app de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/', methods=['GET'])
# @app.route('/', methods=['GET','POST'])
def index():
    
    form = AnimeFeature()
    # if form.validate_on_submit():
    #     session['Start_season'] = form.Start_season.data
    #     session['Type'] = form.Type.data
    #     session['Episodes'] = form.Episodes.data
    #     session['Rating'] = form.Rating.data

    #     return redirect(url_for('prediction'))
    return render_template("home.html", form=form)

    # return 'hola'

# Ejecutamos la aplicación app.run()
if __name__ == '__main__':
    # LOCAL
    # app.run(host='0.0.0.0', port=8080)

    # REMOTO
    app.run()