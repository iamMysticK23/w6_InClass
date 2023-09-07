from flask import Blueprint, render_template, request, flash, redirect

# internal imports
from rangers_shop.models import Product, Customer, Order, db, product_schema, products_schema
from rangers_shop.forms import ProductForm



# we need to instantiate our Blueprint object
site = Blueprint('site', __name__, template_folder='site_templates')
# site_templates tells blueprint where to load the html files

# create the first route
@site.route('/')
def shop():

    # data = request.json() # if they passed the user_id through the body

    shop = Product.query.all()
    customers = Customer.query.all()
    orders = Order.query.all()

    shop_stats = {
         'products': len(shop),
         'sales': sum([order.order_total for order in orders]), # order totals were total cost of the specific order
         'customers': len(customers)
    }

    return render_template('shop.html', shop=shop, stats=shop_stats) # basically displaying our shop.html page


# create our CREATE route
@site.route('/shop/create', methods= ['GET', 'POST'])
def create():

    createform = ProductForm()

    if request.method == 'POST' and createform.validate_on_submit():

        # try:
            name = createform.name.data
            desc = createform.description.data
            image = createform.image.data
            price = createform.price.data
            quantity = createform.quantity.data

            shop = Product(name, price, quantity, image, desc) # instantiating product object

            db.session.add(shop)
            db.session.commit()

            flash(f" You have successfully created product {name}", category='success')
            return redirect('/')
        
        # except:
        #     flash("We were unable to process your request. Please try again", category='warning')
        #     return redirect('/shop/create')
        
    return render_template('create.html', form=createform)


@site.route('/shop/update/<id>', methods= ['GET', 'POST'])
def update(id):

    updateform = ProductForm()
    product = Product.query.get(id) # WHERE clause WHERE product.prod_id = id

    if request.method == 'POST' and updateform.validate_on_submit():

        try:
            product.name = updateform.name.data
            product.description = updateform.description.data
            product.set_image(updateform.image.data, updateform.name.data) # calling upon the set_image method to set our image
            product.price = updateform.price.data
            product.quantity = updateform.quantity.data

           
            db.session.commit() #commits the changes to our objects

            flash(f" You have successfully updated product {product.name}", category='success')
            return redirect('/')
        
        except:
            flash(" We were unable to process your request. Please try again", category='warning')
            return redirect('/shop/update')
        
    return render_template('update.html', form=updateform, product=product)

@site.route('/shop/delete<id>')
def delete(id):

    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')