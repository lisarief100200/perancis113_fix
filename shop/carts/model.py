from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerCheckout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(50), unique=False, nullable=False)
    nama = db.Column(db.String(50), unique=False, nullable=False)
    alamat = db.Column(db.String(50), unique=False)
    kontak = db.Column(db.String(50), unique=False)
    status = db.Column(db.String(20), default='Complete', nullable=False)
    pembayaran = db.Column(db.String(50), unique=False)
    order_cust = db.Column(JsonEcodedDict)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    bukti = db.Column(db.String(150), nullable=False, default='cutomer_bukti.jpg')

    def __repr__(self):
        return'<CheckoutCustomer %r>' % self.nama

db.create_all()