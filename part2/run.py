#!/usr/bin/env python3
"""
Main entry point for HBnB application
Run this file to start the Flask server
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    """
    Start the Flask development server
    Access the API at: http://127.0.0.1:5000/
    API Documentation at: http://127.0.0.1:5000/
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
