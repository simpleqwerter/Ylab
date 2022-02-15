from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField
from wtforms.validators import InputRequired, Email, NumberRange


class SquareForm(FlaskForm):
    side = IntegerField()
    square = IntegerField()
    diagonal = IntegerField()
    r = IntegerField()
    R = IntegerField()
    perimetr = IntegerField()



