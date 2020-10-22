from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField, TextAreaField

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class LoginForm(Form):
    email = StringField('Email:', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password:', [validators.DataRequired()])

class InvoiceUpdate(Form):
    status = SelectField(u'Pilih Metode', choices=[('Menunggu Konfirmasi', 'Menunggu Konfirmasi'), ('Pembayaran Dikonfirmasi', 'Pembayaran Dikonfirmasi'), ('Dikirim', "Dikirim"),("Selesai", "Selesai")])
    resi = TextAreaField('No. Resi', [validators.DataRequired()] )
    orders = TextAreaField('Pesanan', [validators.DataRequired()] )