from flask import Flask, render_template,request, redirect, flash, session, json

app = Flask(__name__)
app.secret_key = 'balagan'


# Load products data from JSON file
def load_products_data():
    try:
        with open('data/products.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save products data to JSON file
def save_products_data(products):
    with open('data/products.json', 'w') as file:
        json.dump(products, file)

# Initialize products
products = load_products_data()
cart=[]



@app.route('/')
def index():
    return render_template('index.html', products=products, cart=cart)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    for item in cart:
        for product in products:
            if product["name"] == item["name"]:
                product["availability"] -= 1
    save_products_data(products)            
    cart.clear()
    return render_template('cart.html')


@app.route('/goToAbout/')
def about_page():
    return render_template('about.html')

@app.route('/goToCart/')
def colored_page():
    return render_template('cart.html', cart=cart)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form.get('product_name')
    product_price = float(request.form.get('product_price'))
    product_availability = int(request.form.get('product_availability'))
    if product_availability >=1:
        cart.append({
                'name': product_name,
                'price': product_price,
                'availability': product_availability
            })
        flash(f'Added {product_name} to the cart successfully!')
    else:  
        flash(f'{product_name} is out of stock.')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
