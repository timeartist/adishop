import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from adishop.temporal.activities.inventory import modify_inventory
from adishop.temporal.workflows.update_cart import  UpdateCartWorkflow

async def run_worker():
    """Run a Temporal worker that hosts workflow and activity implementations."""
    # Create client connected to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Create a worker that hosts implementations of workflows and activities
    worker = Worker(
        client,
        task_queue="adishop-task-queue",
        workflows=[UpdateCartWorkflow],
        activities=[modify_inventory],
    )
    
    # Start the worker
    print("Starting worker...")
    await worker.run()

def main():
    """Main entry point."""
    asyncio.run(run_worker())

if __name__ == "__main__":
    main()