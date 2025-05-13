import asyncio
import argparse

from temporalio.client import Client
from temporalio.worker import Worker

from adishop.temporal.activities.inventory import modify_inventory
from adishop.temporal.workflows.update_cart import  UpdateCartWorkflow

async def run_worker(temporal_address):
    """Run a Temporal worker that hosts workflow and activity implementations."""
    # Create client connected to Temporal server
    client = await Client.connect(temporal_address)
    
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
    parser = argparse.ArgumentParser(description="Run Temporal worker")
    parser.add_argument("--docker", action="store_true", help="Run in Docker mode - overrides host arg to host.docker.internal")
    parser.add_argument("--host", default="localhost", help="Temporal server host (default: localhost)")
    parser.add_argument("--port", default="7233", help="Temporal server port (default: 7233)")
    
    args = parser.parse_args()
    
    if args.docker:
        args.host = "host.docker.internal"

    temporal_address = f"{args.host}:{args.port}"
    asyncio.run(run_worker(temporal_address))

if __name__ == "__main__":
    main()