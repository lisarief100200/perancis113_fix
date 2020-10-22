from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt, login_manager
from flask_login import login_required, current_user, logout_user, login_user
from .forms import RegistrationForm, LoginForm, InvoiceUpdate
from .models import User
from shop.products.models import Addproduct, Category
from shop.carts.model import CustomerCheckout
from shop.customers.model import Register, CustomerInvoice
import os

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Silahkan login terlebih dahulu', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title="Admin Page", products=products)

@app.route('/categories')
def categories():
    if 'email' not in session:
        flash(f'Silahkan login terlebih dahulu', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc())
    return render_template("admin/category.html", title="Category page", categories=categories)

@app.route('/listcheckout')
def list_checkout():
    if 'email' not in session:
        flash(f'Silahkan login terlebih dahulu', 'danger')
        return redirect(url_for('login'))
    cust_checkout = CustomerCheckout.query.all()
    cust_invoice = CustomerInvoice.query.all()
    return render_template("admin/listcheckout.html", title="List Checkout page", cust_checkout=cust_checkout, cust_invoice=cust_invoice)

@app.route('/listinvoice')
def list_invoice():
    if 'email' not in session:
        flash(f'Silahkan login terlebih dahulu', 'danger')
        return redirect(url_for('login'))
    cust_invoice = CustomerInvoice.query.all()
    return render_template("admin/listinvoice.html", title="Ubah Status Pesanan", cust_invoice=cust_invoice)

@app.route('/listakun')
def list_akun():
    if 'email' not in session:
        flash(f'Silahkan login terlebih dahulu', 'danger')
        return redirect(url_for('login'))
    cust_acc = Register.query.all()
    return render_template("admin/listakun.html", title="List Account Page", cust_acc=cust_acc)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data}. Terimakasih sudah melakukan register', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registeration page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            paas = bcrypt.check_password_hash(user.password, form.password.data)
            print(paas)
            session['email'] = form.email.data
            flash('Login berhasil', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Password salah, coba lagi!', 'danger')
    return render_template('admin/login.html', form=form, title="Login page")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/deletecheckout/<int:id>', methods=["POST"])
def deletecheckout(id):
    checkout = CustomerCheckout.query.get_or_404(id)
    checkout_invoice = CustomerInvoice.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + checkout.bukti))
        except Exception as e:
            print(e)

        db.session.delete(checkout)
        db.session.delete(checkout_invoice)
        db.session.commit()
        flash(f'Checkout sudah dihapus', 'success')
        return redirect(url_for('list_checkout'))
    flash(f'Checkout tidak bisa dihapus', 'danger')
    return redirect(url_for("admin"))

@app.route('/updatecheckout/<int:id>', methods=["GET", "POST"])
def updatecheckout(id): 
    checkout = CustomerInvoice.query.get_or_404(id)
    form = InvoiceUpdate(request.form)
    if request.method == "POST":
        checkout.status = form.status.data
        checkout.resi = form.resi.data
        checkout.orders = form.orders.data
        db.session.commit()
        flash(f'Pembayaran sudah di update', 'success')
        return redirect(url_for('admin'))

    form.status.data = checkout.status
    form.resi.data = checkout.resi
    form.orders.data = checkout.orders

    return render_template("admin/updatecheckout.html", form=form, checkout=checkout)