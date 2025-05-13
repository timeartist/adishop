from os import environ

from flask import Flask, render_template
from adishop.api.shopping_cart import shopping_cart_bp

app = Flask(__name__)
app.register_blueprint(shopping_cart_bp)

TEMPORAL_ADDRESS = environ.get('TEMPORAL_ADDRESS', 'localhost:7233')

@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/cart')
def cart():
    return render_template('shopping_cart.jinja', cart_items=[])
def main():
    """Run the Flask server directly"""
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    main()