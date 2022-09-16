#!flask/bin/python
from app import create_app
from config import DEBUG_MODE

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8100, debug=DEBUG_MODE)