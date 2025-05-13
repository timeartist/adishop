import asyncio
from uuid import uuid4
from adishop.temporal.workflows.update_cart import UpdateCartWorkflow
from temporalio.client import Client

async def run_update_cart(item_id, quantity):
    """
    Simple function to run the update cart workflow directly.
    
    Args:
        item_id: The ID of the item to update
        quantity: The quantity to add (positive) or remove (negative)
        
    Returns:
        The result of the workflow execution
    """
    # Connect to Temporal server
    guid = str(uuid4())
    print(f"Running update cart workflow with ID: {guid}")
    
    client = await Client.connect("localhost:7233")
    
    # Execute the workflow
    result = await client.execute_workflow(
        UpdateCartWorkflow.run,
        [item_id, quantity],
        task_queue="adishop-task-queue",
        id=f"update-cart-{guid}",
    )
    
    print(f"Update cart result: {result}")
    return result

# Example usage
if __name__ == "__main__":
    item_id = "item123"
    quantity = 2  # Change as needed
    asyncio.run(run_update_cart(item_id, quantity))
    quantity = 0
    asyncio.run(run_update_cart(item_id, quantity))
    quantity = -3
    asyncio.run(run_update_cart(item_id, quantity))
    
    ##TODO: we want this to fail, but it's failing in a way that we are not catching - commenting out for now
    quantity = -101
    asyncio.run(run_update_cart(item_id, quantity))