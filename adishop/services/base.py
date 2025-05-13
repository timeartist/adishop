import re
from argparse import ArgumentParser
from random import randint

from flask import Flask

class BaseService: 
    def __init__(self, host='127.0.0.1', port=5000, response_message="Hello, World!", 
                 debug=True, random_failures=False, random_failure_ratio=.1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.response_message = response_message
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
    
    def _setup_routes(self):
        
        ##TODO: Wrap this in a decorator to do the random failure check, subclasses should overwrite handle function
        """Set up the Flask routes"""
        @self.app.route('/')
        def home():
            if self._should_fail():
                return "Random failure occurred!", 500
            else:
                return self.response_message, 200
    
    def set_response_message(self, message):
        """Update the response message at runtime"""
        self.response_message = message
    
    def run(self):
        """Run the Flask server directly"""
        print(f"Server running at http://{self.host}:{self.port}/")
        self.app.run(host=self.host, port=self.port, debug=self.debug)

def main():
    # Set up argument parser
    parser = ArgumentParser(description='Run Flask service')
    parser.add_argument('--message', type=str, default="Hello, World!", 
                        help='Response message (default: "Hello, World!")')
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
        
    if not args.message.strip():
        parser.error("Message cannot be empty")
        
    if not args.host.strip():
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', args.host):
            parser.error("Host must be a valid IP address (e.g. 127.0.0.1)")
        parser.error("Host cannot be empty")

    print(args.random_failures)
    
    # Example usage with command line arguments
    service = BaseService(
        host=args.host,
        port=args.port,
        response_message=args.message,
        debug=args.debug,
        random_failures=args.random_failures,
        random_failure_ratio=args.failure_ratio
    )
    service.run()


if __name__ == "__main__":
    main()
    