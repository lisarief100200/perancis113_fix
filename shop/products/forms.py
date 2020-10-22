from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()] )
    price = DecimalField('Price', [validators.DataRequired()] )
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()] )
    flavor = TextAreaField('Flavor', [validators.DataRequired()] )
    desc = TextAreaField('Description', [validators.DataRequired()] )

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

class SearchForm(FlaskForm):
    search = StringField('Search', [validators.DataRequired()])

    