from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy Signin

# Product Data
products = [
    {"id": "shoes", "name": "Shoes", "description": "Comfortable running shoes", "price": 25, "image": "shoes-image.jpg", "category": "Shoes"},
    {"id": "shoes-1", "name": "Shoes 1", "description": "Stylish sports shoes", "price": 30, "image": "shoes1-image.jpg", "category": "Shoes"},
    {"id": "shoes-2", "name": "Shoes 2", "description": "Trendy casual shoes", "price": 35, "image": "shoes2-image.jpg", "category": "Shoes"},
    {"id": "shoes-3", "name": "Shoes 3", "description": "Elegant leather shoes", "price": 40, "image": "shoes3-image.jpg", "category": "Shoes"},
    {"id": "shoes-4", "name": "Shoes 4", "description": "Fashionable sneakers", "price": 28, "image": "shoes4-image.jpg", "category": "Shoes"},
    {"id": "shoes-5", "name": "Shoes 5", "description": "Comfort fit loafers", "price": 32, "image": "shoes5-image.jpg", "category": "Shoes"},
    {"id": "shoes-6", "name": "Shoes 6", "description": "Durable boots", "price": 45, "image": "shoes6-image.jpg", "category": "Shoes"},
    {"id": "shoes-7", "name": "Shoes 7", "description": "Casual slip-ons", "price": 22, "image": "shoes7-image.jpg", "category": "Shoes"},
    {"id": "shoes-8", "name": "Shoes 8", "description": "Modern trainers", "price": 38, "image": "shoes8-image.jpg", "category": "Shoes"},
    {"id": "fabric-1", "name": "Fabric 1", "description": "Premium cotton fabric", "price": 10, "image": "fabric1-image.jpg", "category": "Fabrics"},
    {"id": "fabric-2", "name": "Fabric 2", "description": "Soft silk fabric", "price": 15, "image": "fabric2-image.jpg", "category": "Fabrics"},
    {"id": "fabric-3", "name": "Fabric 3", "description": "Colorful Ankara fabric", "price": 12, "image": "fabric3-image.jpg", "category": "Fabrics"},
    {"id": "fabric-4", "name": "Fabric 4", "description": "Elegant lace fabric", "price": 18, "image": "fabric4-image.jpg", "category": "Fabrics"},
    {"id": "fabric-5", "name": "Fabric 5", "description": "Lightweight chiffon fabric", "price": 11, "image": "fabric5-image.jpg", "category": "Fabrics"},
    {"id": "fabric-6", "name": "Fabric 6", "description": "Patterned brocade fabric", "price": 20, "image": "fabric6-image.jpg", "category": "Fabrics"},
    {"id": "fabric-7", "name": "Fabric 7", "description": "Embroidered net fabric", "price": 17, "image": "fabric7-image.jpg", "category": "Fabrics"},
    {"id": "fabric-8", "name": "Fabric 8", "description": "Rich velvet fabric", "price": 22, "image": "fabric8-image.jpg", "category": "Fabrics"},
    {"id": "fabric-9", "name": "Fabric 9", "description": "Durable denim fabric", "price": 14, "image": "fabric9-image.jpg", "category": "Fabrics"},
    {"id": "fabric-10", "name": "Fabric 10", "description": "Stretch lycra fabric", "price": 13, "image": "fabric10-image.jpg", "category": "Fabrics"},
    {"id": "fabric-11", "name": "Fabric 11", "description": "Soft polyester fabric", "price": 9, "image": "fabric11-image.jpg", "category": "Fabrics"},
    {"id": "fabric-12", "name": "Fabric 12", "description": "Printed silk fabric", "price": 16, "image": "fabric12-image.jpg", "category": "Fabrics"},
    {"id": "fabric-13", "name": "Fabric 13", "description": "Plain cotton fabric", "price": 8, "image": "fabric13-image.jpg", "category": "Fabrics"},
    {"id": "fabric-14", "name": "Fabric 14", "description": "Linen fabric for dresses", "price": 19, "image": "fabric14-image.jpg", "category": "Fabrics"},
    {"id": "fabric-15", "name": "Fabric 15", "description": "Checked wool fabric", "price": 21, "image": "fabric15-image.jpg", "category": "Fabrics"},
    {"id": "fabric-16", "name": "Fabric 16", "description": "Shiny taffeta fabric", "price": 18, "image": "fabric16-image.jpg", "category": "Fabrics"},
    {"id": "fabric-17", "name": "Fabric 17", "description": "Textured damask fabric", "price": 24, "image": "fabric17-image.jpg", "category": "Fabrics"},
    {"id": "fabric-18", "name": "Fabric 18", "description": "Color-blocked fabric", "price": 16, "image": "fabric18-image.jpg", "category": "Fabrics"},
    {"id": "fabric-19", "name": "Fabric 19", "description": "Glow-in-the-dark fabric", "price": 26, "image": "fabric19-image.jpg", "category": "Fabrics"},
    {"id": "fabric-20", "name": "Fabric 20", "description": "Designer print fabric", "price": 30, "image": "fabric20-image.jpg", "category": "Fabrics"},
]

# Home Route
@app.route('/')
def home():
    shoes = [p for p in products if p['category'].lower() == 'shoes']
    fabrics = [p for p in products if p['category'].lower() == 'fabrics']
    return render_template('home.html', shoes=shoes, fabrics=fabrics)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            subtotal = product['price'] * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    card_name = request.form.get('card_name')
    card_number = request.form.get('card_number')
    expiry_date = request.form.get('expiry_date')
    cvv = request.form.get('cvv')

    if not (card_name and card_number and expiry_date and cvv):
        flash('Please fill in all payment fields.', 'danger')
        return redirect(url_for('checkout'))

    # Here you would integrate real payment logic. For now, simulate success:
    flash('Payment successful! Thank you for your purchase.', 'success')

    # Clear cart after successful payment
    session.pop('cart', None)

    return redirect(url_for('home'))

# Search
@app.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()
    if not query:
        flash("Enter a search term.", "warning")
        return redirect(url_for('home'))

    results = [p for p in products if query in p['name'].lower() or query in p['category'].lower()]
    return render_template('search_results.html', results=results, query=query)

# Help
@app.route('/help')
def help_page():
    return render_template('help.html')

# Category Page
@app.route('/category/<category>')
def category_page(category):
    matched = [p for p in products if p['category'].lower() == category.lower()]
    if not matched:
        flash("No products found in this category.", "info")
    return render_template('category.html', products=matched, category=category)

# Jinja: Inject cart count globally
@app.context_processor
def inject_cart_count():
    cart = session.get('cart', {})
    return {'cart_count': sum(cart.values())}

@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            cart_items.append({
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'quantity': quantity
            })
            total_price += product['price'] * quantity

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

users = {
    "test@example.com": {
        "password": "password123"
    }
}

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = email
            flash('Successfully signed in.', 'success')
            return redirect(url_for('account'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('signin'))

    return render_template('signin.html')
@app.route('/signout')
def signout():
    session.pop('user', None)  # Adjust if your session key is different
    return redirect(url_for('signin'))  # or redirect to 'home'

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)





