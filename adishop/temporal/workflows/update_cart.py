from datetime import timedelta
from typing import Dict, Any
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError
from adishop.temporal.activities.inventory import modify_inventory



@workflow.defn
class UpdateCartWorkflow:
    """Workflow to update cart and adjust inventory counts."""

    @workflow.run
    async def run(self, args) -> Dict[str, Any]:
        """
        Update inventory count for a given item.
        
        Args:
            item_id: The ID of the item to update
            quantity: The quantity to adjust (negative for removing from inventory)
        
        Returns:
            Dict containing status of the operation
        """
        item_id, quantity = args

        # Define a retry policy for the activity
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=5),
            maximum_attempts=3,
            # non_retryable_error_types=["InvalidItemError", "InsufficientInventoryError"],
        )
        
        ##TODO: figure out how to catch the errors in the workflow
        # try:
        # Call the appropriate activity to update inventory count
        result = await workflow.execute_activity(
            modify_inventory,
            args=[item_id, quantity],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=retry_policy,
        )

        return {
            "success": True,
            "item_id": item_id,
            "quantity_adjusted": quantity,
            "new_count": result.get('available_quantity', 0),
            "message": "Inventory updated successfully"
        }
            
        # except ApplicationError as e:
        #     return {
        #         "success": False,
        #         "item_id": item_id,
        #         "quantity_adjusted": 0,
        #         "error": str(e)
        #     }