from flask import Blueprint, request, jsonify

shopping_cart_bp = Blueprint('shopping_cart', __name__)

# In-memory storage for demonstration
cart_storage = {}

@shopping_cart_bp.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """
    Add an item to the shopping cart.
    
    Expected JSON body:
    {
        "user_id": "user123",
        "product_id": "product456",
        "quantity": 1
    }
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['user_id', 'product_id', 'quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Call the service function to handle the business logic
    result = add_item_to_cart(
        data['user_id'],
        data['product_id'],
        data['quantity']
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 400

def add_item_to_cart(user_id, product_id, quantity):
    """
    Stub function to add an item to a user's shopping cart.
    
    Args:
        user_id (str): The ID of the user
        product_id (str): The ID of the product to add
        quantity (int): The quantity to add
        
    Returns:
        dict: Result of the operation
    """
    # This is a stub - in a real implementation you would:
    # 1. Validate the product exists
    # 2. Check inventory availability
    # 3. Add to or update the cart in your database
    # 4. Return appropriate response
    
    # For now, just simulate storing in memory
    if user_id not in cart_storage:
        cart_storage[user_id] = {}
    
    if product_id in cart_storage[user_id]:
        cart_storage[user_id][product_id] += quantity
    else:
        cart_storage[user_id][product_id] = quantity

    print(f"Added {quantity} of product {product_id} to user {user_id}'s cart")
    
    return {
        "success": True,
        "message": f"Added {quantity} of product {product_id} to cart",
        "cart": cart_storage[user_id]
    }

# Additional endpoint for viewing the cart (optional)
@shopping_cart_bp.route('/api/cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    """Get the contents of a user's shopping cart"""
    if user_id in cart_storage:
        return jsonify({
            "user_id": user_id,
            "items": cart_storage[user_id]
        })
    else:
        return jsonify({"user_id": user_id, "items": {}}), 200