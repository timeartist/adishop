from flask import Flask, render_template
from adishop.services.shopping_cart import shopping_cart_bp

app = Flask(__name__)
app.register_blueprint(shopping_cart_bp)

@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/cart')
def cart():
    return render_template('shopping_cart.jinja', cart_items=[])

if __name__ == '__main__':
    app.run(debug=True)