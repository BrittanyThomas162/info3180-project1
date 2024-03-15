from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, DataRequired , Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class NewPropertyForm(FlaskForm):

    title = StringField('Property Title', validators=[InputRequired()])
    numBed = StringField('No. of Bedrooms', validators=[InputRequired()])
    numBath = StringField('No. of Bathrooms', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])

    prop_type = SelectField("Property Type", choices=[("House", "House"), ("Apartment", "Apartment")])
    description = TextAreaField("Description",validators=[DataRequired(),InputRequired(),Length(max=1000)])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg','png'], 'Images only!')])

