from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm, CustomerCheckoutForm
from .model import Register, CustomerInvoice
from shop.carts.model import CustomerCheckout
import secrets, os
import pdfkit

@app.route('/customer/register', methods=["GET", "POST"])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, address=form.address.data, province=form.province.data, city=form.city.data, contact=form.contact.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data}, Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)
    
@app.route('/customer/login', methods=["GET", "POST"])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
def customerLogout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/customer/checkout', methods=["GET", "POST"])
def customer_checkout():
    form = CustomerCheckoutForm(request.form)
    if request.method=="POST" and 'bukti' in request.files:
        nama = form.nama.data
        alamat = form.alamat.data
        kontak = form.kontak.data
        customer_email = form.customer_email.data
        pembayaran = form.pembayaran.data
        bukti = photos.save(request.files.get("bukti"), name=secrets.token_hex(10) + ".")

        cust_checkout = CustomerCheckout(nama=nama, customer_email=customer_email, alamat=alamat, kontak=kontak, bukti=bukti, pembayaran=pembayaran, order_cust=session['Shoppingcart'])
        db.session.add(cust_checkout)
        flash(f'Checkout berhasil', 'success')
        db.session.commit()
        
        return redirect(url_for("terimakasih"))
    return render_template('customer/checkout.html', title='Checkout form page', form=form)

@app.route('/customer/terimakasih')
def terimakasih():
    invoice = secrets.token_hex(5)

    get_invoice = CustomerInvoice(invoice=invoice, orders=session['Shoppingcart'])
    db.session.add(get_invoice)
    db.session.commit()
    session.pop('Shoppingcart')
    return render_template('customer/terimakasih.html', title='Makaroni A6', invoice=invoice)

@app.route('/customer/terimakasih')
def getpdf_terimakasih():
    invoice = secrets.token_hex(5)

    get_invoice = CustomerInvoice(invoice=invoice, orders=session['Shoppingcart'])
    db.session.add(get_invoice)
    db.session.commit()
    session.pop('Shoppingcart')
    return render_template('customer/terimakasih.html', title='Makaroni A6', invoice=invoice)


@app.route('/getorder')
def get_order(): 
    flash('Order kamu sudah dikirim, silahkan isi form berikut untuk melanjutkan pembayaran', 'success')
    return redirect(url_for('customer_checkout'))
