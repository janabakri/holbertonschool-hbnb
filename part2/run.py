#!/usr/bin/env python3
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("HBnB API Server Starting...")
    print("API Documentation: http://127.0.0.1:5000/")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
