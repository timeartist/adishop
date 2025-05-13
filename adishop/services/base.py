import re
from argparse import ArgumentParser
from random import randint

from flask import Flask ,jsonify

class BaseService: 
    def __init__(self, host='127.0.0.1', port=5000,
                 debug=True, random_failures=False, random_failure_ratio=.1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        self.random_failures = random_failures
        self.random_failure_ratio = random_failure_ratio
        self._setup_routes()
    
    
    def _should_fail(self):
        """Randomly decide if the service should fail based on the failure ratio"""
        if self.random_failures and randint(1, 100) <= int(self.random_failure_ratio * 100):
            return True
        else:
            return False
    
    def random_fail(self, f):
            def wrapper(*args, **kwargs):
                if self._should_fail():
                    return jsonify({"error": "Random failure occurred!"}), 500
                return f(*args, **kwargs)
            return wrapper
    
    def _setup_routes(self):
        ##TODO: Wrap this in a decorator to do the random failure check, subclasses should overwrite handle function
        """Set up the Flask routes"""
        @self.app.route('/', endpoint='get_endpoint')
        @self.random_fail
        def get():
            return self.handle_get()
        
        @self.app.route('/', methods=['POST'], endpoint='post_endpoint')
        @self.random_fail
        def post():
            return self.handle_post()

        @self.app.route('/', methods=['PUT'], endpoint='put_endpoint')
        @self.random_fail
        def put():
            return self.handle_put()

        @self.app.route('/', methods=['DELETE'], endpoint='delete_endpoint')
        @self.random_fail
        def delete():
            return self.handle_delete()

        @self.app.route('/', methods=['PATCH'], endpoint='patch_endpoint')
        @self.random_fail
        def patch():
            return self.handle_patch()
    
    def run(self):
        """Run the Flask server directly"""
        print(f"Server running at http://{self.host}:{self.port}/")
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def handle_get(self):
        """Handle the request, to be overridden by subclasses"""
        return jsonify({"message": "GET method not implemented"}), 501
    
    def handle_post(self):
        """Handle POST request, to be overridden by subclasses"""
        return jsonify({"message": "POST method not implemented"}), 501

    def handle_put(self):
        """Handle PUT request, to be overridden by subclasses"""
        return jsonify({"message": "PUT method not implemented"}), 501

    def handle_delete(self):
        """Handle DELETE request, to be overridden by subclasses"""
        return jsonify({"message": "DELETE method not implemented"}), 501

    def handle_patch(self):
        """Handle PATCH request, to be overridden by subclasses"""
        return jsonify({"message": "PATCH method not implemented"}), 501

def parse_args():
    # Set up argument parser
    parser = ArgumentParser(description='Run Flask service')
    parser.add_argument('--host', type=str, default='127.0.0.1', 
                        help='Host to run the server on (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, 
                        help='Port to run the server on (default: 5000)')
    parser.add_argument('--debug', action='store_true', 
                        help='Run in debug mode (default: False)')
    parser.add_argument('--random-failures', action='store_true', 
                        help='Enable random failures (default: False)')
    parser.add_argument('--failure-ratio', type=float, default=0.1, 
                        help='Ratio of requests that will fail (0.0-1.0) (default: 0.1)')
    
    args = parser.parse_args()

    # Validate input arguments
    if args.port < 1 or args.port > 65535:
        parser.error("Port must be between 1 and 65535")
        
    if args.failure_ratio < 0.0 or args.failure_ratio > 1.0:
        parser.error("Failure ratio must be between 0.0 and 1.0")

        
    if not args.host.strip():
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', args.host):
            parser.error("Host must be a valid IP address (e.g. 127.0.0.1)")
        parser.error("Host cannot be empty")

    return args

def run_service(ServiceClass:BaseService, args):
    '''
    Generically run the service - this should be something that is usable/importable for other subclassed services
    Args:
        ServiceClass: The class of the service to run
        args: The arguments to pass to the service
    '''
    service = ServiceClass(
        host=args.host,
        port=args.port,
        debug=args.debug,
        random_failures=args.random_failures,
        random_failure_ratio=args.failure_ratio
    )
    service.run()

def main():
    '''
    This exists primarily for poetry to hook into to make command line config cleaner'''
    # Parse command line arguments
    args = parse_args()
    
    # Run the service with the parsed arguments
    run_service(BaseService, args)