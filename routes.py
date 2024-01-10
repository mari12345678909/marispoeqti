
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from forms import AddProductForm, RegisterForm, LoginForm
from extension import app, db, bcrypt
from models import Product, User


@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/view_product/<int:product_id>")
def view_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")
    return render_template("product.html", product=product)


@app.route("/add_product", methods=["GET","POST"])
@login_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        file = form.img.data
        filename = file.filename
        file.save(path.join(app.root_path, "static", filename))


        new_product = Product(name=form.name.data, price=form.price.data, img=filename)
        db.session.add(new_product)
        db.session.commit()



    return render_template ("add_product.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if current_user.role != 'admin':
        return render_template("404.html")

    product = Product.query.get(product_id)
    form = AddProductForm(name=product.name, price=product.price, img=product.img)

    if form.validate_on_submit():
        file = form.img.data
        filename = file.filename
        file.save((path.join(app.root_path, 'static', filename)))

        product.name = form.name.data
        product.price = form.price.data
        product.img = filename

        db.session.commit()

        return redirect("/")

    return render_template("add_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    if current_user.role != 'admin':
        return render_template("404.html")

    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html', form=form)


@app.route("/about")
@login_required
def about_us():
    return render_template('about_us.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
