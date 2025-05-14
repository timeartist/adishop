from adishop.services.base import BaseService, parse_args, run_service

class InventoryService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventory = {}  # Format: {item_id: quantity}

    def add_item(self, item_id, quantity):
        """Add or update an item quantity in the inventory."""
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def remove_item(self, item_id, quantity=None):
        """Remove a specific quantity of an item, or remove entirely if quantity is None."""
        if item_id in self.inventory:
            if quantity is None or quantity >= self.inventory[item_id]:
                del self.inventory[item_id]
            else:
                self.inventory[item_id] -= quantity

    def get_items(self):
        """Retrieve all item quantities from the inventory."""
        return self.inventory

    def handle_get(self, _):
        """Handle HTTP GET argss."""
        return {"status": "success", "data": self.get_items()}

    def handle_post(self, args):
        """Handle HTTP POST argss."""
        item_id = args.get("sku")
        quantity = args.get("quantity", 1)
        
        if not item_id:
            return {"status": "error", "message": "sku is required"}
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return {"status": "error", "message": "Quantity must be positive"}
        except (ValueError, TypeError):
            return {"status": "error", "message": "Quantity must be a valid integer"}
            
        self.add_item(item_id, quantity)
        return {"status": "success", "message": "Item quantity updated successfully"}

    def handle_delete(self, args):
        """Handle HTTP DELETE argss."""
        item_id = args.get("sku")
        quantity = args.get("quantity")
        
        if not item_id:
            return {"status": "error", "message": "sku is required"}
        
        if quantity is not None:
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    return {"status": "error", "message": "Quantity must be positive"}
            except (ValueError, TypeError):
                return {"status": "error", "message": "Quantity must be a valid integer"}
        
        self.remove_item(item_id, quantity)
        return {"status": "success", "message": "Item quantity updated successfully"}
    
def main():
    """Main function to run the product service"""
    args = parse_args()
    return run_service(InventoryService, args)
