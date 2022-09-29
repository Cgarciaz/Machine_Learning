from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AnimeFeature(FlaskForm):
    Start_season = StringField('Season')
    Type = StringField('Type')
    Episodes = StringField('Episodes (max 350)')
    Rating = StringField('Rating')

    submit = SubmitField("Predict")