from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Addproduct, Category
from .forms import Addproducts, SearchForm
from shop.customers.model import CustomerInvoice
import secrets, os

def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories

@app.route('/allproduct')
def home():
    products = Addproduct.query.filter(Addproduct.stock > 0)#.paginate(page=page, per_page=4)
    return render_template("products/index.html", products=products, categories=categories())

#####testttt
@app.route('/')
def defaultpage():
    return render_template("products/defaultpage.html", categories=categories())

@app.route('/carapesan')
def carapesan():
    return render_template("products/carapesan.html", categories=categories())

@app.route('/tracking', methods=['GET'])
def tracking():
    cust_invoice = request.args.get('search')
    invoice = db.session.query(CustomerInvoice).filter(CustomerInvoice.invoice == cust_invoice)
    return render_template("products/tracking.html", categories=categories(), invoice=invoice)

@app.route('/livechat', methods=['GET'])
def livechat():
    return render_template("products/livechat.html", categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html', product=product, categories=categories())

@app.route('/category/<int:id>')
def get_category(id):
    category = Addproduct.query.filter_by(category_id=id)
    return render_template("products/index.html", category=category, categories=categories())

@app.route('/addcategory', methods=["GET","POST"])
def addcategory():
    if request.method == "POST":
        getcategory = request.form.get("category")
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f"Kategori {getcategory} berhasil dimasukkan", "success")
        db.session.commit()
        return redirect(url_for("addcategory"))
    return render_template('products/addcategory.html')

@app.route('/updatecategory/<int:id>', methods=["GET", "POST"])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Silahkan login terlebih dahulu', 'danger')
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        flash(f'Kategory berhasil diupdate', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatecategory.html', title='Update category page', updatecategory=updatecategory)

@app.route('/deletecategory/<int:id>', methods=["POST"])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'Kategori {category.name} berhasil dihapus', 'success')
        return redirect(url_for('admin'))
    flash(f'Kategori {category.name} tidak bisa dihapus', 'warning')
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'email' not in session:
        flash(f'Silahkan login terlebih dahulu', 'danger')
        return redirect(url_for('login'))
    form = Addproducts(request.form)
    categories = Category.query.all()
    if request.method=="POST" and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        flavor = form.flavor.data
        desc = form.desc.data
        category = request.form.get('category')
        image_1 = photos.save(request.files.get("image_1"), name=secrets.token_hex(10) + ".")
        
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, flavor=flavor, desc=desc, category_id=category, image_1=image_1)
        db.session.add(addpro)
        flash(f'Produk {name} berhasil dimasukkan', 'success')
        db.session.commit()
        return redirect(url_for("admin"))

    return render_template('products/addproduct.html', title='Add product page', form=form, categories=categories)

@app.route('/updateproduct/<int:id>', methods=["GET", "POST"])
def updateproduct(id): 
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.category_id = category
        product.flavor = form.flavor.data
        product.desc = form.desc.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'Produk berhasil diupdate', 'success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.flavor.data = product.flavor
    form.desc.data = product.desc

    return render_template("products/updateproduct.html", form=form, categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f'Produk {product.name} berhasil dihapus', 'success')
        return redirect(url_for('admin'))
    flash(f'Produk tidak bisa dihapus', 'danger')
    return redirect(url_for("admin"))