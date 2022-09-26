from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class Season(FlaskForm):
    Start_season = StringField('Season (0-3)')
    Type = StringField('Type (0-5)')
    Episodes = StringField('Episodes (max 350)')
    Rating = StringField('Rating (0-5)')

    submit = SubmitField("Predict")