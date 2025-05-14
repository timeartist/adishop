from adishop.services.base import BaseService, parse_args, run_service

class CartService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.carts = {}

    def add_item(self, user_id, sku):
        """Add an SKU to the user's cart."""
        if user_id not in self.carts:
            self.carts[user_id] = []
        self.carts[user_id].append(sku)

    def remove_item(self, user_id, sku):
        """Remove an SKU from the user's cart."""
        if user_id in self.carts:
            self.carts[user_id] = [
                item for item in self.carts[user_id] if item != sku]

    def get_items(self, user_id):
        """Retrieve items from the user's cart."""
        return self.carts.get(user_id, [])

    def handle_get(self, args):
        """Handle HTTP GET requests."""
        user_id = args.get("user_id")
        if not user_id:
            return {"status": "error", "message": "User ID is required"}
        return {"status": "success", "data": self.get_items(user_id)}

    def handle_post(self, args):
        """Handle HTTP POST requests."""
        user_id = args.get("user_id")
        sku = args.get("sku")
        if not user_id or not sku:
            return {"status": "error", "message": "User ID and SKU are required"}
        self.add_item(user_id, sku)
        return {"status": "success", "message": "Item added successfully"}

    def handle_delete(self, args):
        """Handle HTTP DELETE requests."""
        user_id = args.get("user_id")
        sku = args.get("sku")
        if not user_id or not sku:
            return {"status": "error", "message": "User ID and SKU are required"}
        self.remove_item(user_id, sku)
        return {"status": "success", "message": "Item removed successfully"}
    
def main():
    """Main function to run the cart service"""
    args = parse_args()
    return run_service(CartService, args)