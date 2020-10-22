from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError, SelectField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from .model import Register

class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    province = StringField('Province: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    zipcode = StringField('Zip code: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg'], 'Image only please')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")

class CustomerLoginForm(FlaskForm):
    email = StringField("Email: ", [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password: ", [validators.DataRequired()])

class CustomerCheckoutForm(FlaskForm):
    nama = StringField('Nama Penerima: ')
    alamat = StringField('Alamat Lengkap Penerima: ', [validators.DataRequired()])
    kontak = StringField('Nomor Telepon: ', [validators.DataRequired()])
    customer_email = StringField('Email: ', [validators.DataRequired()])
    pembayaran = SelectField(u'Pilih Metode', choices=[('mandiri', 'Transfer Bank Mandiri'), ('dana', 'DANA'), ('ovo', "OVO"),("gopay", "GOPAY")])
    bukti = FileField('Bukti Pembayaran', validators=[FileAllowed(['jpg','png','jpeg'], 'Image only please')])