# -*- coding: utf-8 -*-

# Run a test server.
from app import application
# app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    application.run()