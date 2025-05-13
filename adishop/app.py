import asyncio
from os import environ

from flask import Flask, render_template
from temporalio.client import Client

from adishop.api.shopping_cart import shopping_cart_bp
from adishop.temporal.workflows.update_cart import UpdateCartWorkflow

app = Flask(__name__)
app.register_blueprint(shopping_cart_bp)

TEMPORAL_ADDRESS = environ.get('TEMPORAL_ADDRESS', 'localhost:7233')

async def _get_temporal_client():
    """
    Create a Temporal client connected to the Temporal server.
    This function is used to create a client for interacting with Temporal workflows and activities.
    """
    
    return await Client.connect(TEMPORAL_ADDRESS) 

TEMPORAL_CLIENT = asyncio.run(_get_temporal_client())

@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/cart')
async def cart():
    result = await TEMPORAL_CLIENT.execute_workflow(
    UpdateCartWorkflow.run,
    ['item_id', -1],
    task_queue="adishop-task-queue",
    id=f"update-cart-(user-id)",
    )
    return render_template('shopping_cart.jinja', cart_items=[])

def main():
    """Run the Flask server directly"""
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    main()