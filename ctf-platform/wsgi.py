import os
from app import create_app

# Create Flask app using factory
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run()
