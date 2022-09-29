from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AnimeFeature(FlaskForm):
    Start_season = StringField('In What Season Will It Start')
    Type = StringField('What Type Of Distribution')
    Episodes = StringField('How Many Episodes (max 350)')
    Rating = StringField('What Rating')

    submit = SubmitField("Predict")