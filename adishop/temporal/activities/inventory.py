from asyncio import sleep
from temporalio import activity
# from temporalio.exceptions import ApplicationError


@activity.defn
async def modify_inventory(product_id, quantity) -> dict:
    """
    Mocks reserving inventory for a product.
    In a real implementation, this would interact with an inventory service.
    """
    # Mock implementation - always succeeds with a simulated delay
    await sleep(1)
    
    # In a real system, you would check if the requested quantity is available
    # and reserve it in your inventory system
    
    # For demonstration, let's assume we always have enough inventory
    available_quantity = 100  # Mock available quantity
    new_count = available_quantity + quantity
    
    ## TODO: Figure out how to do this correctly
    # if new_count < 0:
    #     raise ApplicationError("InsufficientInventoryError", "Not enough inventory available.")
   
    success = True
    message = f"Successfully reserved {quantity} units of product {product_id}."
    
    return {'success':success, 'available_quantity':new_count, 'message':message}